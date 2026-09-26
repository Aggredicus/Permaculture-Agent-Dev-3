# Initial Layer Catalog

| Layer | Primary inputs | Typical method | Output |
|---|---|---|---|
| Elevation | DEM/LiDAR | resample/normalize | raster |
| Slope | DEM | finite differences | raster degrees/% |
| Aspect | DEM | gradient direction | raster degrees |
| Contours | DEM | isolines | vector |
| Hillshade | DEM + sun geometry | surface illumination | raster |
| Flow direction | conditioned DEM | D8/D-infinity | raster/vector |
| Flow accumulation | flow direction | upstream accumulation | raster |
| Catchments | flow graph + outlets | watershed delineation | polygons |
| TWI | contributing area + slope | ln(a/tan(beta)) | raster |
| Solar potential | terrain + sun path | horizon/incident radiation | raster/time series |
| Soil attributes | SSURGO/gSSURGO | spatial join | polygons/raster |
| Pond suitability | terrain + soils + setbacks | transparent weighted factors | raster/polygons |
| Swale candidates | contours + catchment + slope | candidate search | vectors |
| Cut/fill | existing + proposed surface | cellwise elevation difference | raster + volumes |

## Layer design rule
Every suitability or heuristic layer must expose the factors, weights, source datasets, algorithm/version, and caveats used to create it. Do not hide uncertain assumptions behind a single score.
