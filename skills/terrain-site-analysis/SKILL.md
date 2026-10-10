---
name: terrain-site-analysis
description: Analyze a land parcel or screening area from a street address, coordinates, or polygon with elevation contours, slope, downslope aspect, and conceptual cut/fill using an independent DEM. Export GeoTIFF, GeoJSON, KML, annotated maps, and reproducible provenance for landscape, land acquisition, permaculture, and preliminary civil engineering review.
---

# Terrain Site Analysis

## When to use

Use when asked to "analyze terrain at this address," "show contours/slope/aspect," "estimate cut and fill," "assess south-facing slopes," or "repeat the new Google Earth terrain-analysis workflow." This is the **four-tool terrain-analysis workflow** from the Google Earth tutorial `https://youtu.be/jm92Wx-yv5c`. The skill reproduces the **analytical methods**, **not Google's proprietary maps or exact algorithms**. Google Earth's own analysis layers cannot currently be exported as raw data.

## Contract

**Required:** a full street address OR `lat` and `lon`. To compute actual parcel statistics, a georeferenced site boundary is additionally required in WGS84 GeoJSON. Without it, use a explicitly labeled **circular screening buffer**, never call it a property boundary. For locations outside USGS 3DEP service coverage, require a local GeoTIFF DEM with elevations in meters.

**Optional:** `boundary`, `dem`, `radius_m`, `resolution_m`, `contour_m`, `target_m`, `out`.

**Outputs:** four numeric GeoTIFF layers, contour GeoJSON, contour/boundary Google Earth KML, site boundary GeoJSON, four-panel PNG, `report.json`, `report.md`, original downloaded DEM when used.

## Execution

1. **Confirm the site:** parse or geocode the address; report coordinates and match confidence. If a user supplies a polygon, validate it and do not infer that it is official. If address/geocoding returns an ambiguous result, ask for coordinates or a parcel polygon.
2. **Choose input elevation data:** prefer the USGS 3DEP bare-earth DEM ImageServer for U.S. sites; record the source URL and sampling resolution. Alternatively use a local, appropriately licensed DEM GeoTIFF. Do not download/repackage Google's restricted Earth analysis layers.
3. **Project to metric coordinates:** use the local UTM CRS with a pixel grid at `resolution_m` meters. Never run slope or volume calculations in latitude/longitude degrees. Make sure DEM vertical units are meters and check the source vertical datum.
4. **Analyze:** contours at specified elevation intervals; slope in degrees from local gradients; aspect as downslope compass direction clockwise from north; cut/fill to a constant elevation plane. Default target plane is the *area-weighted mean sampled elevation* to approximately balance cut and fill for equal-area cells. Support a user-selected custom target in meters.
5. **Quality gates:** ensure DEM coverage ≥98% over target site, CRS and grid are known, site clipping is applied, slope/aspect directions are reasonable, and earthwork numbers report assumptions. A 1 m output grid is **not** proof of a 1 m source DEM or survey accuracy. Mark flat pixels as having undefined aspect.
6. **Publish:** provide terrain preview, site statistics, KML overlay, geographic files, and caveats. Explain that swale placement, drainage, grading, roads, foundations, flood risk, soils, and property lines require separate site verification and possibly a professional survey.

## Run command

Install once (Python 3.10+):

```bash
python -m pip install -r requirements.txt
```

Run from root skill folder:

```bash
python scripts/terrain_site_analysis.py \
  --address "YOUR STREET ADDRESS, CITY, STATE, USA" \
  --radius-m 120 --resolution-m 2 --contour-m 1 \
  --out results/site-001
```

For an actual parcel boundary (GeoJSON, EPSG:4326):

```bash
python scripts/terrain_site_analysis.py \
  --address "YOUR STREET ADDRESS, CITY, STATE, USA" \
  --boundary data/parcel.geojson \
  --resolution-m 2 --target-m 251.5 \
  --out results/parcel-001
```

To avoid the geocoding service and use an offline DEM:

```bash
python scripts/terrain_site_analysis.py \
  --lat 42.9634 --lon -85.6681 \
  --dem examples/synthetic_demo_dem.tif \
  --radius-m 95 --resolution-m 2 \
  --out results/offline-demo
```

First create the demo DEM with `python scripts/generate_synthetic_dem.py` (the generated file is not committed). The offline demo DEM is completely **synthetic**; its location is merely a test coordinate, **not** real elevation data for Grand Rapids.

## Google Earth manual comparison

In [Google Earth web](https://earth.google.com/web/), open a project → Analyze a site → draw or select the same polygon → choose Contours, Slope, Aspect, or Cut and Fill → set values → Create layer. Compare overall geometry and orientation. Use an imported `google_earth_contours.kml` to inspect these independently calculated contour lines, not to imply they are Google's original generated layer.

## Interpretation and safety

- Land acquisition/permaculture: check south-facing slopes, broad landform shapes, site access and preliminary earthwork, then separately evaluate soil, watercourses, erosion, drainage, vegetation, easements, flood maps and zoning.
- Output `south_facing_percent_nonflat` represents downslope aspect between 135°–225°, not a measured solar radiation or agricultural suitability model.
- Earthwork volumes assume reshaping the **whole masked area** to one horizontal plane; real swales, berms, paths, roads and pads must use their own design surfaces. Do not use these volumes for quotes, legal filings, or engineering without survey-grade input and verification.
- A spatial screening radius around the geocoding point is not a parcel boundary, and a geocoded point is not guaranteed to be at the parcel center.
- Street addresses sent to Nominatim leave the local machine. Supply lat/lon to avoid geocoding. Avoid rapid/bulk requests; abide by Nominatim usage policy and show attribution.

## Sources / restrictions

- Video: https://youtu.be/jm92Wx-yv5c
- Google's accompanying four-method field guide: https://mapsplatform.google.com/resources/blog/a-field-guide-to-terrain-analysis-tools-in-google-earth/
- Google Earth feature documentation and raw export restriction: https://developers.google.com/maps/documentation/earth/terrain-analysis
- USGS 3DEP image service: https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer
- Nominatim usage policy: https://operations.osmfoundation.org/policies/nominatim/

## Integration

The parent `skills/landscape-digital-twin/` skill delegates these four DEM-derived layers to this skill. Treat its outputs as analytical layer artifacts; never promote screening buffers to legal parcel geometries. The Hager Park public-site example lives at `examples/hager-park/README.md` and needs live OSM/USGS access or verified local terrain inputs.

The machine-readable `report.json`, GeoJSON, KML and GeoTIFF outputs can feed `landscape-digital-twin` or a site-design viewer. Run as an independent skill first and attach the outputs to the client project. Do not claim existing repository integration unless code is committed and tested in the target repository.