# TERRAIN / SITE ATLAS — v1.0.0

A repeatable **address → four terrain analyses → exportable deliverables** Python skill.

**Reproduces:** elevation contours, slope, downslope aspect, and conceptual cut/fill from the official Google Earth terrain-analysis tutorial. Its calculations use **USGS 3DEP** (for U.S. locations) or a user-provided single-band elevation GeoTIFF. It does **not** copy or extract Google Earth's non-exportable proprietary layers.

## Quick start

Requires Python 3.10 or newer and access to the Internet for live DEM/address queries. A Python environment with GIS-compatible binary packages is easiest to install using `conda` or modern wheels; install `requirements.txt`.

```bash
python -m pip install -r requirements.txt
python scripts/terrain_site_analysis.py --address "Your address, City, State, USA" --out results/my-site
```

Or run without network, using generated synthetic test data:

```bash
python scripts/generate_synthetic_dem.py
python scripts/terrain_site_analysis.py --lat 42.9634 --lon -85.6681 --dem examples/synthetic_demo_dem.tif --radius-m 95 --out results/demo
```

**Important:** Without `--boundary parcel.geojson`, the analysis is a **120-meter radius surrounding a geocoded point**, not the parcel itself. Specify an official parcel polygon if exact area matters. Boundary files must contain one valid GeoJSON polygon or multipolygon in longitude/latitude WGS84, not a Google Earth screenshot.

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--address` | Full address, geocoded once via Nominatim | None |
| `--lat --lon` | Geographic coordinates instead of address | None |
| `--boundary` | GeoJSON site outline, WGS84 | Circular screening buffer |
| `--radius-m` | Buffer radius if polygon missing | 120 |
| `--dem` | Local elevation GeoTIFF (meters) | USGS 3DEP API |
| `--resolution-m` | Raster output pixel spacing in meters | 2 |
| `--contour-m` | Elevation contour interval | 1 |
| `--target-m` | Target level for flat grading analysis | Sampled site mean |
| `--out` | Output directory | `terrain_site_output` |
| `--user-agent` | Identification for public web requests | Desktop skill agent |

## Results

`terrain_preview.png` includes elevation and contours, slope, aspect and cut/fill depth. GeoTIFF rasters use local metric UTM, while GeoJSON and KML vectors use WGS84. `report.json` contains statistics and provenance. Import `google_earth_contours.kml` into Google Earth or `contours.geojson` into QGIS and other GIS software.

This software estimates the target elevation for **balanced flat grading** using the area-weighted mean. Although a net cut minus fill near zero is achievable mathematically, construction results differ due to compaction, soil shrink/swell, structures, environmental constraints, and the precision of source data. This is a desktop preliminary screening tool, **not survey-grade advice**.

## Validation

```bash
python -m pytest -q tests
```

Offline test suite checks slope angle, aspect direction, cut/fill and flat-cell handling. Integration-tested against synthetic GeoTIFF. Download and geocoding require real network access and were not executed in the packaging environment.

## Licensing and sources

The original code in this package is made available under the MIT License. Generated elevation content retains the source's separate terms. The included synthetic DEM is original, randomly designed for tests; **it does not depict actual terrain anywhere**.

Sources: [Google Earth field guide](https://mapsplatform.google.com/resources/blog/a-field-guide-to-terrain-analysis-tools-in-google-earth/), [Google Earth terrain documentation](https://developers.google.com/maps/documentation/earth/terrain-analysis), [USGS 3DEP](https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer), [OSM Nominatim policy](https://operations.osmfoundation.org/policies/nominatim/).

Canonical installation: `skills/terrain-site-analysis/` in `Permaculture-Agent-Dev-3`. Example site scripts live under `examples/hager-park/` and are not automatically executed.