# Architecture

```text
Address or Manual GPS AOI
          |
          v
   Site Resolver / Editor
          |
          v
      Site Manifest
          |
  +-------+---------+-----------+
  |                 |           |
  v                 v           v
Terrain           Soils      Hydrography
  |                 |           |
  +--------+--------+-----------+
           v
     Computation Graph
           |
  +--------+--------+-------------------+
  |        |        |                   |
Terrain  Water    Solar             Design
  |        |        |                   |
  +--------+--------+-------------------+
           v
      Layer Manifest
           |
           v
 MapLibre/Cesium 2D/3D Viewer
```

## Critical design rule
The visual 3D mesh is never assumed to be the scientific elevation surface. A textured 3D model can be shown for context while a DEM or LiDAR-derived terrain drives calculations.

## Dependency graph
Derived layers declare dependencies. Replacing a DEM with a higher-resolution survey DEM invalidates only the dependent layers, which are recomputed while unrelated annotations and design objects remain intact.
