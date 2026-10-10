# Hager Park / Terrain Site Analysis

**Address:** 8212 28th Avenue, Jenison, MI 49428 (Georgetown Charter Township, Ottawa County).  
**Site type:** public county park, reported by Ottawa County Parks as **104 acres**.  
**Status in delivered archive:** input site resolved, documented scripts and tests prepared; **real elevation analysis pending** a network-enabled run. No synthetic terrain has been misrepresented as actual Hager Park elevations.

## Run it

Python 3.10+ and internet access:

```bash
pip install -r requirements.txt
python examples/hager-park/run_hager_park.py
```

Outputs appear in `examples/hager-park/results/hager_park/`: four-panel `terrain_preview.png`, `report.json` and `report.md`, `elevation_m.tif`, `slope_deg.tif`, `aspect_deg.tif`, `cutfill_depth_m.tif`, `contours.geojson`, `google_earth_contours.kml`, GIS outlines, original `dem_source.tif`, and a `provenance.json` noting land footprint/coverage.

To use a local **authentic** elevation raster, not the synthetic skill demo:

```bash
python examples/hager-park/run_hager_park.py --dem /path/to/real_dem.tif
```

To avoid live requests entirely after obtaining a real DEM plus real GeoJSON polygon:

```bash
python examples/hager-park/run_hager_park.py --boundary /path/to/park.geojson --dem /path/to/real_dem.tif --offline
```

Increase spatial detail or change contour interval (these do not increase native DEM accuracy):

```bash
python examples/hager-park/run_hager_park.py --resolution-m 2 --contour-m 0.5
```

## Geographic identity and site boundaries

* **Authoritative name/address:** [Ottawa County Parks / Hager Park](https://miottawa.org/park-locations/hager-park/). The county reports 104 acres; its trail description mentions hardwood forest.
* **Center reference:** approximate OSM-derived park point `42.91721, -85.84874`, not a building or site-survey control point.
* **Default park outline:** OpenStreetMap [way 158802227](https://www.openstreetmap.org/way/158802227). Downloaded from the OSM API on the first successful live run; geometry is a community-mapped recreational perimeter, not legal title boundaries. The corresponding `provenance.json` records its computed acreage separately from the county's published 104 acres.
* **County parcel cross-check:** [Ottawa County public parcels GIS](https://gis.miottawa.org/arcgis/rest/services/HostedServices/ParcelsPublic/FeatureServer/0). Georgetown Township 2023 tax/address report lists 8212 28th Ave at candidate PIN `70-14-09-400-001` under Ottawa County Parks. That PIN is **not presumed to encompass the entire park** and remains secondary to the park footprint. The runner saves the county candidate geometry if available.
* **Elevation:** [USGS 3DEP bare-earth elevation image service](https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer), with original imagery and original export URL saved.

## What the resulting numbers mean

The gradient fields are model-derived **downslope aspect** and **degree slope**, not ground-truthed flow paths; 1 m contours don't imply 1 m source accuracy. The cut/fill demonstration grades the *entire polygon* to a hypothetical horizontal plane. It is deliberately not an earthwork recommendation for a protected public park. The output includes approximate data coverage and georeferencing to support future independent verification.

## Research possibilities

Investigate north/south forest slopes, Hager Creek topographic connectivity near the north side, dry ridge paths versus hollows, tree diversity by aspect, and whether trail elevations correlate with runoff concentration. Neither jurisdictional wetlands nor legal drainage conclusions can be drawn from the elevation model alone.

## Test

```bash
python -m pytest -q tests
```

`tests/` checks parsing and boundary validation locally without any network; it does **not** validate a live USGS download. Network access to USGS/OSM/Ottawa County is necessary for measured parcel maps and numeric results, unless those real datasets are provided locally.