#!/usr/bin/env python3
"""Fetch documented Hager Park outline & USGS DEM, then run the reusable terrain skill.

This runner does NOT use synthetic terrain for the real address. Default outline is
OpenStreetMap way 158802227 (park footprint), not a surveyed legal boundary.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import requests
from shapely.geometry import shape
from pyproj import Geod

ROOT = Path(__file__).resolve().parent
SKILL_ROOT = ROOT.parent.parent
CONFIG = json.loads((ROOT / 'site.json').read_text(encoding='utf-8'))
OSM_URL = f"https://api.openstreetmap.org/api/0.6/way/{CONFIG['osm_way_id']}/full"
COUNTY_URL = 'https://gis.miottawa.org/arcgis/rest/services/HostedServices/ParcelsPublic/FeatureServer/0/query'
USER_AGENT = 'TerrainSiteAnalysis/1.0 (Hager Park GIS site assessment; personal noncommercial research)'


def osm_way_to_geojson(xml: str, way_id: int):
    root = ET.fromstring(xml)
    if root.tag != 'osm':
        raise ValueError('OSM API did not return <osm> XML')
    nodes = {}
    for node in root.findall('node'):
        nodes[node.attrib['id']] = (float(node.attrib['lon']), float(node.attrib['lat']))
    for way in root.findall('way'):
        if way.attrib.get('id') != str(way_id):
            continue
        refs = [nd.attrib['ref'] for nd in way.findall('nd')]
        tags = {t.attrib['k']: t.attrib['v'] for t in way.findall('tag')}
        if tags.get('leisure') != 'park' or 'hager' not in tags.get('name', '').lower():
            raise ValueError(f'OSM way identity mismatch: tags={tags}')
        if len(refs) < 4 or refs[0] != refs[-1]:
            raise ValueError('Park way is not a closed polygon')
        missing = [r for r in refs if r not in nodes]
        if missing:
            raise ValueError(f'Missing {len(missing)} OSM nodes')
        feature = {
            'type': 'Feature',
            'properties': {
                'name': tags.get('name'), 'source': OSM_URL,
                'osm_way_id': way_id,
                'boundary_status': 'community-mapped park extent, NOT a surveyed legal parcel'
            },
            'geometry': {'type': 'Polygon', 'coordinates': [[list(nodes[r]) for r in refs]]}
        }
        polygon = shape(feature['geometry'])
        if not polygon.is_valid or polygon.is_empty:
            raise ValueError('OSM park polygon invalid')
        b = polygon.bounds
        if not (-85.87 < b[0] < -85.82 and -85.87 < b[2] < -85.82 and
                42.90 < b[1] < 42.94 and 42.90 < b[3] < 42.94):
            raise ValueError('OSM boundary not located near Hager Park')
        return feature
    raise ValueError(f'OSM way {way_id} missing from API result')


def fetch_osm_boundary(path: Path, offline: bool):
    if path.exists():
        feature = json.loads(path.read_text(encoding='utf-8'))['features'][0]
        return feature, 'cache'
    if offline:
        raise RuntimeError('No cached OSM polygon. Supply --boundary FILE (an actual GeoJSON) or run online once.')
    r = requests.get(OSM_URL, headers={'User-Agent': USER_AGENT}, timeout=65)
    r.raise_for_status()
    feature = osm_way_to_geojson(r.text, CONFIG['osm_way_id'])
    path.write_text(json.dumps({'type': 'FeatureCollection', 'features': [feature]}, indent=2), encoding='utf-8')
    return feature, 'online'


def fetch_county_candidate(out: Path, offline: bool):
    """Reference ONLY: the identified parcel is not assumed to be the whole park."""
    filename = out/'county_candidate_parcel.geojson'
    if filename.exists():
        obj = json.loads(filename.read_text(encoding='utf-8'))
        return len(obj.get('features', [])), 'cache', None
    if offline:
        return 0, 'not requested offline', None
    params = {'where': f"FinalPIN='{CONFIG['candidate_county_parcel_pin']}'",
              'outFields': 'FinalPIN,PropertyAddress,Acreage,OwnerName',
              'returnGeometry': 'true', 'outSR': '4326', 'f': 'geojson'}
    try:
        r = requests.get(COUNTY_URL, params=params, headers={'User-Agent': USER_AGENT}, timeout=65)
        r.raise_for_status()
        obj = r.json()
        features = obj.get('features', [])
        if obj.get('type') != 'FeatureCollection' or len(features) != 1:
            return len(features), 'county query', f'Expected one candidate parcel; got {len(features)}'
        geom = shape(features[0]['geometry'])
        if not geom.is_valid or geom.is_empty:
            return 0, 'county query', 'County candidate geometry invalid'
        filename.write_text(json.dumps(obj, indent=2), encoding='utf-8')
        return 1, 'county query', None
    except Exception as exc:
        return 0, 'county query failed', f'{type(exc).__name__}: {exc}'


def geographic_acres(geometry) -> float:
    geod = Geod(ellps='WGS84')
    area, _ = geod.geometry_area_perimeter(shape(geometry))
    return abs(area) / 4046.8564224


def main(argv=None):
    ap = argparse.ArgumentParser(description='Hager Park real-DEM terrain analysis. Requires internet or cached real DEM and boundary.')
    ap.add_argument('--boundary', type=Path, help='Use your own WGS84 GeoJSON (override OSM park boundary).')
    ap.add_argument('--dem', type=Path, help='Use a real local USGS or surveyed elevation GeoTIFF; elevations in meters.')
    ap.add_argument('--offline', action='store_true', help='Forbid downloads; requires --boundary or prior cached boundary and --dem.')
    ap.add_argument('--resolution-m', type=float, default=3.0, help='Output grid spacing (not native DEM accuracy). Default 3 m.')
    ap.add_argument('--contour-m', type=float, default=1.0, help='Contours every n meters; default 1 m.')
    ap.add_argument('--target-m', type=float, help='Optional concept flat-grade target meters.')
    ap.add_argument('--out', type=Path, default=ROOT/'results'/'hager_park')
    ap.add_argument('--skip-county-check', action='store_true')
    args = ap.parse_args(argv)
    if args.offline and args.dem is None:
        ap.error('Offline mode requires --dem with a real georeferenced DEM; do not use the synthetic test DEM.')
    out = args.out.resolve(); out.mkdir(parents=True, exist_ok=True)
    if args.boundary:
        boundary = args.boundary.resolve()
        if not boundary.exists():
            ap.error('--boundary file does not exist')
        source = f'user-provided GeoJSON: {boundary.name}; legal accuracy unverified'
        geojson = json.loads(boundary.read_text(encoding='utf-8'))
        geom = geojson['features'][0]['geometry'] if geojson.get('type')=='FeatureCollection' else geojson.get('geometry',geojson)
    else:
        boundary = out/'park_boundary_osm.geojson'
        feature, status = fetch_osm_boundary(boundary, args.offline)
        geom = feature['geometry']
        source = f'OpenStreetMap park way {CONFIG["osm_way_id"]} ({status}); approximate recreational park footprint, NOT surveyed legal boundary'
    observed_acres = geographic_acres(geom)
    if not 40 < observed_acres < 250:
        raise ValueError(f'Site boundary area {observed_acres:.1f} acres is inconsistent with the 104-acre park; verify boundary manually.')
    count, county_status, county_error = (0, 'skipped', None) if args.skip_county_check else fetch_county_candidate(out, args.offline)
    cmd = [sys.executable, str(SKILL_ROOT/'scripts'/'terrain_site_analysis.py'),
           '--lat', str(CONFIG['reference_lat']), '--lon', str(CONFIG['reference_lon']),
           '--boundary', str(boundary), '--resolution-m', str(args.resolution_m),
           '--contour-m', str(args.contour_m), '--out', str(out)]
    if args.target_m is not None: cmd += ['--target-m', str(args.target_m)]
    if args.dem: cmd += ['--dem', str(args.dem.resolve())]
    provenance = {
        'prepared_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'address': CONFIG['official_address'], 'park_name': CONFIG['name'],
        'reference_center_lat_lon': [CONFIG['reference_lat'], CONFIG['reference_lon']],
        'boundary_source': source,
        'approx_boundary_acres_geodesic': round(observed_acres, 3),
        'park_area_published_by_county_acres': CONFIG['reported_park_area_acres'],
        'county_candidate_parcel': CONFIG['candidate_county_parcel_pin'],
        'county_candidate_found': bool(count), 'county_lookup': county_status,
        'county_lookup_note': county_error,
        'dem_status': 'user-provided DEM: independently verify it is real and correctly referenced' if args.dem else 'live USGS 3DEP service fetch required',
        'no_synthetic_dem': True,
        'methodology': 'Contours; degree slope; downslope aspect; illustrative level cut/fill for whole boundary',
        'warnings': CONFIG['warnings']
    }
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2), encoding='utf-8')
    (out/'RUN_COMMAND.txt').write_text(' '.join(cmd)+'\n',encoding='utf-8')
    print(f"Hager Park: boundary {observed_acres:.1f} mapped acres ({source})",flush=True)
    print('Preparing terrain analysis; USGS internet access is needed unless --dem is supplied.',flush=True)
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        (out/'RUN_FAILED.txt').write_text(
            'Run incomplete: real USGS DEM download or processing did not finish. '\
            'No measured terrain results were produced. Check network/service or pass --dem REAL_DEM.tif.\n' +
            f'Exit code: {exc.returncode}\n',encoding='utf-8')
        raise
    final_report = out/'report.json'
    report=json.loads(final_report.read_text(encoding='utf-8'))
    report['boundary_source']=source
    report['published_county_park_acres']=CONFIG['reported_park_area_acres']
    report['approx_osm_or_user_boundary_acres']=round(observed_acres,3)
    report['site_provenance_file']='provenance.json'
    final_report.write_text(json.dumps(report,indent=2),encoding='utf-8')
    reportmd = out/'report.md'
    original = reportmd.read_text(encoding='utf-8')
    original = original.replace('**Area definition:** supplied WGS84 polygon (user responsible for legal accuracy)',
                                '**Area definition:** '+source)
    original += '\n\n## Hager Park site-specific caveats\n\n'
    original += '\n'.join('- '+w for w in CONFIG['warnings'])+'\n'
    reportmd.write_text(original, encoding='utf-8')
    print('Completed calculations from DEM input: '+str(final_report))

if __name__=='__main__':
    try: main()
    except Exception as exc:
        print('HAGER PARK ANALYSIS FAILED:', str(exc), file=sys.stderr)
        raise SystemExit(2)