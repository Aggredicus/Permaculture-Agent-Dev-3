#!/usr/bin/env python3
"""Address-to-terrain analysis with public USGS 3DEP DEMs or a local DEM.

Unlike Google's proprietary Earth analysis layers, derivatives here are from
independently sourced, locally stored DEMs and can be exported. Not a survey.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from pyproj import CRS, Transformer
from rasterio.enums import Resampling
from rasterio.features import geometry_mask
from rasterio.transform import from_origin
from rasterio.warp import reproject
from shapely.geometry import LineString, Polygon, MultiPolygon, Point, mapping, shape
from shapely.ops import transform as shp_transform
import requests

ELEVATION_SERVICE = 'https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer'
NOMINATIM = 'https://nominatim.openstreetmap.org/search'
VERSION = '1.0.0'


def geocode(address: str, cache: Path, user_agent: str) -> tuple[float, float, str]:
    cache.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(cache.read_text()) if cache.exists() else {}
    key = address.strip().casefold()
    if key in existing:
        saved = existing[key]
        return float(saved['lat']), float(saved['lon']), saved['display_name']
    r = requests.get(NOMINATIM, params={'q': address, 'format': 'jsonv2', 'limit': 1},
                     headers={'User-Agent': user_agent, 'Accept-Language': 'en'}, timeout=35)
    r.raise_for_status()
    results = r.json()
    if not results:
        raise ValueError('Address not found. Try --lat/--lon or confirm the address.')
    record = results[0]
    existing[key] = {k: record[k] for k in ('lat', 'lon', 'display_name')}
    cache.write_text(json.dumps(existing, indent=2))
    return float(record['lat']), float(record['lon']), record['display_name']


def utm_crs(lat: float, lon: float) -> CRS:
    if not (-80 <= lat <= 84):
        raise ValueError('Automatic UTM requires latitude between 80°S and 84°N.')
    zone = int(math.floor((lon + 180) / 6) + 1)
    zone = max(1, min(60, zone))
    return CRS.from_epsg((32600 if lat >= 0 else 32700) + zone)


def parse_geometry_geojson(path: Path):
    data = json.loads(path.read_text())
    if data.get('type') == 'FeatureCollection':
        features = data.get('features', [])
        if len(features) != 1:
            raise ValueError('Boundary must be one Polygon/MultiPolygon feature (one property per run).')
        data = features[0]['geometry']
    elif data.get('type') == 'Feature':
        data = data['geometry']
    geom = shape(data)
    if not isinstance(geom, (Polygon, MultiPolygon)) or geom.is_empty or not geom.is_valid:
        raise ValueError('Boundary must be a valid non-empty Polygon/MultiPolygon GeoJSON.')
    coords = [(g[0], g[1]) for polygon in ([geom] if geom.geom_type == 'Polygon' else geom.geoms) for g in polygon.exterior.coords]
    if any(not (-180 <= x <= 180 and -90 <= y <= 90) for x, y in coords):
        raise ValueError('Boundary GeoJSON coordinates must be WGS84 longitude, latitude (EPSG:4326).')
    return geom


def compute_terrain(z: np.ndarray, resolution_m: float, site: np.ndarray,
                    target: float | None, flat_threshold_deg: float = 0.5) -> dict:
    """Raster rows grow south. Aspect is compass bearing of downslope, 0=N, 90=E."""
    valid = np.isfinite(z) & site
    if valid.sum() < 9:
        raise ValueError('No sufficient valid DEM cells inside the site.')
    # Central differences; derivatives against meter axes.
    dz_south, dz_east = np.gradient(z.astype(np.float64), resolution_m, resolution_m)
    slope = np.degrees(np.arctan(np.hypot(dz_east, dz_south)))
    aspect = (np.degrees(np.arctan2(-dz_east, dz_south)) + 360) % 360
    aspect[slope < flat_threshold_deg] = np.nan
    # Cut (+) and fill (-) are vertical distances from a constant grading plane.
    # Arithmetic mean elevation achieves equal net cut/fill for equal-area raster cells.
    target_m = float(np.mean(z[valid])) if target is None else float(target)
    delta = z.astype(np.float64) - target_m
    pixel_area = resolution_m ** 2
    cut_m3 = float(np.maximum(delta[valid], 0).sum() * pixel_area)
    fill_m3 = float(np.maximum(-delta[valid], 0).sum() * pixel_area)
    for arr in (slope, aspect, delta):
        arr[~valid] = np.nan
    slope_bins = [0, 5, 10, 15, 30, float('inf')]
    slope_stats = {}
    for lo, hi in zip(slope_bins[:-1], slope_bins[1:]):
        label = f'{lo}-{hi} degrees' if math.isfinite(hi) else f'{lo}+ degrees'
        n = np.count_nonzero(valid & (slope >= lo) & (slope < hi))
        slope_stats[label] = round(100.0 * n / valid.sum(), 2)
    south_aspect_pct = (100.0 * np.count_nonzero(valid & (aspect >= 135) &
                       (aspect <= 225)) / np.count_nonzero(valid & np.isfinite(aspect))) if np.count_nonzero(valid & np.isfinite(aspect)) else None
    return dict(valid=valid, slope=slope, aspect=aspect, cutfill=delta, target_m=target_m,
                cut_m3=cut_m3, fill_m3=fill_m3, net_m3=cut_m3-fill_m3,
                slope_bands_pct=slope_stats, south_facing_pct=south_aspect_pct)


def download_dem(out: Path, bbox: tuple[float, float, float, float], epsg: int,
                 width: int, height: int, user_agent: str):
    params = dict(f='image', bbox=','.join(map(str, bbox)), bboxSR=str(epsg),
                  imageSR=str(epsg), size=f'{width},{height}', format='tiff',
                  pixelType='F32', interpolation='RSP_BilinearInterpolation',
                  noDataInterpretation='esriNoDataMatchAny', returnSquarePixels='true')
    r = requests.get(ELEVATION_SERVICE + '/exportImage', params=params,
                     headers={'User-Agent': user_agent}, timeout=180)
    r.raise_for_status()
    if r.content[:4] not in (b'II*\x00', b'MM\x00*', b'II+\x00', b'MM\x00+'):
        raise RuntimeError('USGS service did not return a TIFF: ' + r.text[:450])
    out.write_bytes(r.content)
    return r.url


def get_raster(local_dem: Path | None, dem_path: Path, bbox, transform, crs, h, w, ua):
    if local_dem is None:
        src_url = download_dem(dem_path, bbox, crs.to_epsg(), w, h, ua)
    else:
        src_url = str(local_dem.resolve())
    with rasterio.open(local_dem or dem_path) as src:
        if src.crs is None:
            raise ValueError('Input DEM must have an explicit CRS.')
        if src.count != 1:
            raise ValueError('Input DEM must be a single-band elevation raster.')
        dest = np.full((h, w), np.nan, dtype='float32')
        reproject(source=rasterio.band(src, 1), destination=dest,
                  src_transform=src.transform, src_crs=src.crs,
                  src_nodata=src.nodata, dst_transform=transform, dst_crs=crs,
                  dst_nodata=np.nan, resampling=Resampling.bilinear,
                  init_dest_nodata=True)
    return dest, src_url


def write_raster(path, arr, transform, crs):
    with rasterio.open(path, 'w', driver='GTiff', height=arr.shape[0], width=arr.shape[1],
                       count=1, dtype='float32', crs=crs, transform=transform,
                       nodata=np.nan, compress='deflate') as dst:
        dst.write(arr.astype('float32'), 1)


def vector_contours(dem, transform, poly, interval_m, inverse_transformer, out_geojson):
    finite = dem[np.isfinite(dem)]
    start = math.ceil(float(finite.min()) / interval_m) * interval_m
    stop = math.floor(float(finite.max()) / interval_m) * interval_m
    levels = np.arange(start, stop + interval_m/2, interval_m)
    if len(levels) > 500:
        raise ValueError('Contour interval generates >500 contour levels; increase --contour-m.')
    rows, cols = dem.shape
    x = transform.c + (np.arange(cols) + 0.5) * transform.a
    y = transform.f + (np.arange(rows) + 0.5) * transform.e
    fig, ax = plt.subplots()
    features=[]
    if len(levels) > 0:
        cs = ax.contour(x, y, np.ma.masked_invalid(dem), levels=levels)
        # Old and new Matplotlib use allsegs; each segment is x/y in projected meters.
        for level, segs in zip(cs.levels, cs.allsegs):
            for verts in segs:
                if len(verts)<2: continue
                clipped = LineString(verts).intersection(poly)
                candidates = list(clipped.geoms) if hasattr(clipped,'geoms') else [clipped]
                for line in candidates:
                    if line.geom_type != 'LineString' or line.is_empty or line.length < 1:
                        continue
                    coords=[list(inverse_transformer.transform(float(a),float(b))) for a,b in line.coords]
                    features.append({'type':'Feature', 'properties':{'elevation_m':round(float(level),3)},
                                     'geometry':{'type':'LineString','coordinates':coords}})
    plt.close(fig)
    out_geojson.write_text(json.dumps({'type':'FeatureCollection','features':features},indent=2))
    return features


def kml_from_vectors(path, features, geom_wgs):
    ns = 'http://www.opengis.net/kml/2.2'
    ET.register_namespace('', ns)
    def el(parent, tag, text=None, attrib=None):
        obj=ET.SubElement(parent, '{'+ns+'}'+tag, attrib or {})
        if text is not None: obj.text = str(text)
        return obj
    root=ET.Element('{'+ns+'}kml')
    doc=el(root,'Document')
    el(doc,'name','Terrain Site Analysis — Contours and boundary')
    boundary_style = el(doc, 'Style', attrib={'id': 'siteBoundary'})
    line_style = el(boundary_style, 'LineStyle')
    el(line_style, 'color', 'ff00ffff')
    el(line_style, 'width', '2.5')
    poly_style = el(boundary_style, 'PolyStyle')
    el(poly_style, 'fill', '0')
    el(poly_style, 'outline', '1')
    contour_style = el(doc, 'Style', attrib={'id': 'contours'})
    cs = el(contour_style, 'LineStyle')
    el(cs, 'color', 'ff333333')
    el(cs, 'width', '1.2')
    p=el(doc,'Placemark'); el(p,'name','Site boundary')
    el(p,'styleUrl','#siteBoundary')
    boundary_polys = [geom_wgs] if geom_wgs.geom_type=='Polygon' else list(geom_wgs.geoms)
    multi=el(p,'MultiGeometry')
    for polygon in boundary_polys:
        po=el(multi,'Polygon'); outer=el(po,'outerBoundaryIs'); ring=el(outer,'LinearRing')
        el(ring,'coordinates',' '.join(f'{x:.8f},{y:.8f},0' for x,y in polygon.exterior.coords))
        for hole in polygon.interiors:
            inner=el(po,'innerBoundaryIs'); hring=el(inner,'LinearRing')
            el(hring,'coordinates',' '.join(f'{x:.8f},{y:.8f},0' for x,y in hole.coords))
    for f in features:
        p=el(doc,'Placemark'); el(p,'name',f"{f['properties']['elevation_m']:g} m")
        el(p,'styleUrl','#contours')
        line=el(p,'LineString'); el(line,'tessellate','1')
        el(line,'coordinates',' '.join(f'{x:.8f},{y:.8f},0' for x,y in f['geometry']['coordinates']))
    ET.ElementTree(root).write(path, encoding='utf-8', xml_declaration=True)


def preview(out, z, results, site, transform, geometry):
    rows, cols=z.shape
    extent=[transform.c, transform.c+transform.a*cols,
            transform.f+transform.e*rows, transform.f]
    arrs=[np.where(site,z,np.nan), results['slope'],results['aspect'],results['cutfill']]
    title=['Elevation + contours (m)','Slope (degrees)','Downslope aspect (degrees)','Cut (+) / fill (−) depth (m)']
    cmaps=['terrain','YlOrRd','twilight','RdBu_r']
    fig, axes=plt.subplots(2,2,figsize=(13,11),layout='constrained')
    finite=z[np.isfinite(z)]
    levels=np.linspace(float(finite.min()),float(finite.max()),9)
    shapes=[geometry] if geometry.geom_type=='Polygon' else list(geometry.geoms)
    for i,ax in enumerate(axes.flat):
        a=arrs[i]
        if i==3:
            lim=float(np.nanmax(np.abs(a)))
            lim=max(lim,1e-6)
            im=ax.imshow(a,origin='upper',extent=extent,cmap=cmaps[i],vmin=-lim,vmax=lim)
        else:
            im=ax.imshow(a,origin='upper',extent=extent,cmap=cmaps[i],vmin=(0 if i==1 else None),vmax=(360 if i==2 else None))
        if i==0 and np.ptp(finite)>0:
            xx=transform.c+(np.arange(cols)+0.5)*transform.a
            yy=transform.f+(np.arange(rows)+0.5)*transform.e
            ax.contour(xx, yy, np.ma.masked_where(~site | ~np.isfinite(z), z),
                       levels=levels, colors='black', linewidths=0.6, alpha=0.7)
        for p in shapes:
            x,y=p.exterior.xy
            ax.plot(x,y,c='black',lw=1.7)
        ax.set_title(title[i],fontsize=12,fontweight='bold')
        ax.set_xlabel('Easting (m)');ax.set_ylabel('Northing (m)')
        ax.set_aspect('equal')
        fig.colorbar(im,ax=ax,shrink=0.75)
    fig.suptitle('TERRAIN / SITE ATLAS  •  PRELIMINARY SCREENING',fontsize=17,fontweight='bold')
    fig.savefig(out,dpi=145,facecolor='white')
    plt.close(fig)


def main(argv=None):
    parser=argparse.ArgumentParser(description='Repeatable terrain analysis by address or coordinates (U.S. 3DEP / local DEM).')
    pos=parser.add_mutually_exclusive_group(required=True)
    pos.add_argument('--address', help='Geocoded address (public Nominatim, one lookup)')
    pos.add_argument('--lat', type=float, help='WGS84 latitude, used with --lon')
    parser.add_argument('--lon',type=float,help='WGS84 longitude; used with --lat')
    parser.add_argument('--boundary',type=Path,help='Actual site boundary GeoJSON (WGS84 EPSG:4326).')
    parser.add_argument('--radius-m',type=float,default=120,help='Screening radius without boundary; NOT a property line (default 120 m).')
    parser.add_argument('--resolution-m',type=float,default=2,help='DEM output grid spacing; NOT source accuracy (default 2 m).')
    parser.add_argument('--contour-m',type=float,default=1,help='Contour interval in meters (default 1 m).')
    parser.add_argument('--target-m',type=float,help='Flat grading plane elevation meters; default area-weighted mean elevation.')
    parser.add_argument('--dem',type=Path,help='Offline GeoTIFF DEM, single band, elevations in meters.')
    parser.add_argument('--out',type=Path,default=Path('terrain_site_output'))
    parser.add_argument('--user-agent',default=os.environ.get('TERRAIN_SKILL_USER_AGENT','TerrainSiteAnalysis/1.0 (personal desktop GIS skill)'))
    args=parser.parse_args(argv)
    if args.lat is not None and args.lon is None: parser.error('--lat requires --lon')
    if args.lat is not None and not (-90<=args.lat<=90 and -180<=args.lon<=180): parser.error('Invalid lat/lon')
    if args.radius_m<=0 or args.resolution_m<=0 or args.contour_m<=0: parser.error('radii and intervals must be >0')
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    if args.address:
        lat,lon,location=geocode(args.address,out/'geocode_cache.json',args.user_agent)
    else:
        lat,lon,location=args.lat,args.lon,f'{args.lat:.6f}, {args.lon:.6f}'
    crs=utm_crs(lat,lon)
    to_proj=Transformer.from_crs('EPSG:4326',crs,always_xy=True)
    to_geo=Transformer.from_crs(crs,'EPSG:4326',always_xy=True)
    if args.boundary:
        geo=parse_geometry_geojson(args.boundary)
        boundary_source='supplied WGS84 polygon (user responsible for legal accuracy)'
        poly=shp_transform(to_proj.transform,geo)
        if poly.area<4*args.resolution_m**2:
            raise ValueError('Property polygon too small for selected DEM grid resolution.')
    else:
        x,y=to_proj.transform(lon,lat)
        poly=Point(x,y).buffer(args.radius_m,resolution=64)
        geo=shp_transform(to_geo.transform,poly)
        boundary_source=f'{args.radius_m:g} m geocoded-point screening buffer; NOT parcel boundaries'
    if poly.is_empty or not poly.is_valid: raise ValueError('Site boundary invalid or empty.')
    # Add padding so gradients and contours can be computed around the border.
    pad=max(args.resolution_m*4,8.0)
    minx,miny,maxx,maxy=poly.bounds
    minx-=pad;miny-=pad;maxx+=pad;maxy+=pad
    w=math.ceil((maxx-minx)/args.resolution_m)
    h=math.ceil((maxy-miny)/args.resolution_m)
    if w*h>2_500_000 or max(w,h)>8000:
        raise ValueError(f'Site request {w}×{h} exceeds safety limit; increase --resolution-m or split into tiles.')
    # Adjust projected extent to exact multiples of requested cell size.
    maxx=minx+w*args.resolution_m;miny=maxy-h*args.resolution_m
    bbox=(minx,miny,maxx,maxy)
    trans=from_origin(minx,maxy,args.resolution_m,args.resolution_m)
    dem,dem_source=get_raster(args.dem,out/'dem_source.tif',bbox,trans,crs,h,w,args.user_agent)
    site=geometry_mask([mapping(poly)],out_shape=(h,w),transform=trans,invert=True,all_touched=False)
    coverage=np.count_nonzero(np.isfinite(dem)&site)/max(1,np.count_nonzero(site))
    if coverage<0.98:
        raise ValueError(f'DEM covers only {coverage:.1%} of the site. Use better DEM coverage or a smaller boundary.')
    result=compute_terrain(dem,args.resolution_m,site,args.target_m)
    for name,data in [('elevation_m.tif',np.where(result['valid'],dem,np.nan)),
                      ('slope_deg.tif',result['slope']),('aspect_deg.tif',result['aspect']),
                      ('cutfill_depth_m.tif',result['cutfill'])]:
        write_raster(out/name,data,trans,crs)
    geojson={'type':'FeatureCollection','features':[{'type':'Feature','properties':{'source':boundary_source},'geometry':mapping(geo)}]}
    (out/'site_boundary.geojson').write_text(json.dumps(geojson,indent=2))
    features=vector_contours(np.where(np.isfinite(dem),dem,np.nan),trans,poly,args.contour_m,to_geo,out/'contours.geojson')
    kml_from_vectors(out/'google_earth_contours.kml',features,geo)
    preview(out/'terrain_preview.png',dem,result,site,trans,poly)
    v=dem[result['valid']]
    report={
        'skill_version':VERSION,'generated_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'location_query':location,'center_lat':lat,'center_lon':lon,
        'boundary_source':boundary_source,'boundary_area_m2':round(poly.area,2),
        'estimated_grid_area_m2':round(float(result['valid'].sum()*args.resolution_m**2),2),
        'dem_source':dem_source,'dem_cell_spacing_m':args.resolution_m,
        'dem_coverage_fraction':round(coverage,4), 'elevation_min_m':float(v.min()),
        'elevation_mean_m':float(v.mean()),'elevation_max_m':float(v.max()),
        'slope_min_deg':float(np.nanmin(result['slope'])),'slope_mean_deg':float(np.nanmean(result['slope'])),
        'slope_max_deg':float(np.nanmax(result['slope'])),'slope_bands_percent':result['slope_bands_pct'],
        'south_facing_percent_nonflat':None if result['south_facing_pct'] is None else round(result['south_facing_pct'],2),
        'target_plane_elevation_m':round(result['target_m'],4),
        'cut_volume_m3':round(result['cut_m3'],2),'fill_volume_m3':round(result['fill_m3'],2),
        'net_cut_minus_fill_m3':round(result['net_m3'],2),'contour_interval_m':args.contour_m,
        'contour_segments_exported':len(features),'projected_crs':crs.to_string(),
        'notes':['Conceptual grading to a constant horizontal plane, not a construction bid.',
                 'Output grid spacing does not guarantee the original DEM resolution or vertical accuracy.',
                 'No hydrology, drainage, soil, floodplain, legal parcel, or field survey verification is included.',
                 'Absolute earthwork estimates omit shrink/swell, stripping topsoil, obstructions, vegetation and haul routes.',
                 'Check original DEM vertical datum, accuracy and data timestamp before field use.']}
    (out/'report.json').write_text(json.dumps(report,indent=2))
    south_label = 'not defined' if result['south_facing_pct'] is None else f"{result['south_facing_pct']:.1f}%"
    md = f"""# Terrain / Site Analysis

**Location:** {location}  
**Area definition:** {boundary_source}  
**Source DEM:** {dem_source}  
**Output grid:** {args.resolution_m:g} m, {w}×{h}; CRS {crs.to_string()}  
**Valid site coverage:** {coverage:.1%}

## Elevation and slope

- Elevation: {v.min():.2f}–{v.max():.2f} meters; mean {v.mean():.2f} m
- Mean slope: {report['slope_mean_deg']:.2f}°; maximum: {report['slope_max_deg']:.2f}°
- South-facing aspect (135–225° of non-flat cells): {south_label}
- Slope area distribution: {json.dumps(result['slope_bands_pct'])}

## Conceptual cut and fill to a flat plane

- Target elevation: {result['target_m']:.2f} meters
- Cut: {result['cut_m3']:.1f} m³
- Fill: {result['fill_m3']:.1f} m³
- Net cut less fill: {result['net_m3']:.1f} m³

These are screening estimates, not construction-ready volumes. A mass-balanced plane does **not** establish design suitability.

## Files

- `terrain_preview.png` — four-map summary
- `elevation_m.tif`, `slope_deg.tif`, `aspect_deg.tif`, `cutfill_depth_m.tif` — numeric rasters
- `contours.geojson` and `google_earth_contours.kml` — reusable vector contours
- `site_boundary.geojson` — site envelope
- `report.json` — machine-readable provenance/statistics

## Important limits

"""
    md += '\n'.join('- '+note for note in report['notes'])
    md += '\n\n**Attribution:** Elevation from USGS 3DEP if online; geocoding © OpenStreetMap contributors if used.\n'
    (out/'report.md').write_text(md)
    print(json.dumps({'ok':True,'output':str(out),'center':[lat,lon], 'report':str(out/'report.json'), 'preview':str(out/'terrain_preview.png')},indent=2))
    return 0

if __name__=='__main__':
    try: sys.exit(main())
    except Exception as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        sys.exit(2)