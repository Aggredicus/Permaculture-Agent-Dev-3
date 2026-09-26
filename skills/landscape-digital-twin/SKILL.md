---
name: landscape-digital-twin
version: 0.1.0
description: Build a provenance-aware landscape digital twin from an address or adjustable GPS boundary, then compute reusable geospatial analysis layers for regenerative and permaculture design.
---

# landscape-digital-twin

## Purpose
Turn a place into a computable landscape model that can be progressively improved from public data to field observations, drone photogrammetry, LiDAR, and survey-grade inputs.

Keep two kinds of geometry separate:
1. **visual geometry** for the 2D/3D viewer; and
2. **scientific geometry** for elevation, hydrology, soils, solar, and design calculations.

Preserve provenance, resolution, assumptions, units, and uncertainty for every derived layer.

## When to use
Use this skill when the user asks to build, analyze, or improve a site-scale digital twin, 3D site model, terrain model, hydrology/solar/soil overlay system, or address/GPS-bounded landscape analysis. Typical trigger language includes “digital twin,” “3D site model,” “analyze this property,” “terrain layers,” “flow accumulation,” “slope/aspect,” “address to site model,” or “manual GPS boundary.”

## Required evidence
Before claiming a layer is available, establish the area of interest (AOI), coordinate reference context, source provenance, effective resolution, and assumptions that materially affect interpretation. Missing evidence stays unavailable or Unverified; never fill gaps with invented parcel, elevation, soil, climate, or hydrology values.

## Input resolution protocol

### A. Address-first mode
1. Geocode the address or named place to latitude/longitude.
2. Attempt to resolve an authoritative parcel/property boundary when a suitable source exists.
3. If parcel geometry is unavailable, ambiguous, stale, or unsuitable, do **not** guess the boundary.
4. Fall back to `manual_boundary` mode centered on the geocoded point.
5. Keep the user-selected AOI separate from an analysis buffer because terrain, water, shade, wind, and access processes cross property lines.

### B. Manual-boundary mode
Accept:
- `center_radius`: center longitude/latitude + radius;
- `rectangle`: center + width/height + optional rotation, or explicit corners;
- `polygon`: at least three longitude/latitude vertices;
- `geojson`: Polygon or MultiPolygon geometry.

When the host supports maps, provide an adjustable boundary with draggable handles/vertices and live area/perimeter. Support moving the center, resizing/rotating a rectangle, adding/removing polygon vertices, changing buffer distance, pasting coordinates, and importing/exporting GeoJSON.

If an interactive map is unavailable, accept coordinates numerically and emit valid GeoJSON. See `assets/manual-boundary.geojson`, `assets/site-request.example.json`, and `assets/site-request.schema.json`.

## AOI validation
Before analysis:
- validate coordinate ranges and polygon topology;
- require at least three distinct vertices for polygons;
- use GeoJSON longitude/latitude ordering for interchange;
- preserve the exact user boundary and store any analysis buffer separately;
- warn when AOI size makes high-resolution work expensive;
- record area, perimeter, bounding box, centroid, CRS, and requested buffer.

## Ordered workflow
1. Resolve or collect the AOI.
2. Validate geometry and select a projected local CRS for computation while preserving WGS84 for interchange.
3. Discover the highest-resolution legally usable terrain, soils, hydrography, landcover/canopy, climate, and imagery needed for the requested layers.
4. Normalize source metadata into a site manifest.
5. Build the computational terrain independently from any photorealistic display mesh.
6. Compute only requested layers and their dependencies.
7. Store algorithm/version, parameters, units, resolution, provenance, confidence, and caveats with each layer.
8. Return a portable site manifest plus layer manifest suitable for a browser map/3D viewer.
9. If higher-fidelity data arrive later, invalidate and recompute only dependent layers while preserving annotations and design objects.

## Data hierarchy
Prefer the best legally usable source available for the AOI.

- **Terrain/elevation:** USGS 3DEP LiDAR/DEM in the United States; superior state/local open LiDAR/DEM when clearly licensed; reputable public DEMs as fallback.
- **Visual context:** licensed aerial/satellite basemap or 3D tiles. Never assume the visual mesh is the scientific surface.
- **Soils:** USDA NRCS SSURGO/gSSURGO in the United States.
- **Hydrography:** authoritative mapped hydrography plus terrain-derived drainage as separate evidence layers.
- **Climate/weather/solar:** authoritative gridded normals, observations, and solar geometry; record the represented period.

## Canonical site model
Normalize sources into a site manifest containing, when available:
- AOI polygon and analysis buffer;
- horizontal CRS and vertical datum;
- DEM + cell size;
- optional surface model/photogrammetry mesh;
- soil polygons/attributes;
- hydrography;
- landcover/canopy;
- source provenance and acquisition/publication dates;
- uncertainty and caveats.

Prefer SI internally and convert for display.

## Layer families
Detailed initial layers are in `references/layer-catalog.md`.

### Terrain
Elevation, hillshade, contours, slope, aspect, curvature, relief, and roughness.

### Hydrology
Depression diagnostics, flow direction/accumulation, contributing area, catchments, stream candidates, wetness index, runoff pathways, ponding candidates, upslope area, and transect flux estimates when assumptions are supplied.

### Solar / microclimate
Potential solar radiation, seasonal sun exposure, shadow duration when supported, and clearly labeled cold-air, frost-pocket, and wind-exposure heuristics.

### Soils / water
Soil map units, hydrologic soil group, drainage class, available water capacity, texture/depth, infiltration suitability proxies, and erosion susceptibility proxies.

### Design / earthworks
Swale candidates, pond/terrace suitability, access/path slope, cut/fill, storage volume, and overflow routing.

### Permaculture suitability
Expose component factors and weights rather than hiding them behind a single opaque score. Examples include food-forest, orchard, annual-crop, water-harvesting, and structure/access suitability.

## Mathematical conventions
Use numerical methods appropriate to raster/vector data rather than symbolic calculus on real sites.

- area accumulation approximates double integrals with raster-cell sums;
- time accumulation approximates temporal integrals with timestep sums;
- flow across a transect approximates line/flux integrals;
- cut/fill volume integrates existing-minus-proposed elevation over area;
- divergence/curl use finite-difference operators on vector fields where meaningful.

Track units through every operation.

## Layer contract
Each derived layer should conceptually include:

```ts
interface AnalysisLayer {
  id: string;
  name: string;
  category: string;
  sourceType: "raster" | "vector" | "mesh" | "pointcloud" | "timeseries";
  units?: string;
  resolution?: string;
  dependencies: string[];
  algorithm: string;
  algorithmVersion?: string;
  parameters: Record<string, unknown>;
  provenance: SourceRecord[];
  confidence: "high" | "medium" | "low";
  caveats: string[];
}
```

The portable JSON contract is `assets/layer-result.schema.json`.

## Progressive fidelity
- **Level 0 — public rough model:** address/manual AOI + public DEM/soils/imagery.
- **Level 1 — observed model:** user GPS points, photos, site notes, drains/structures, field measurements.
- **Level 2 — high-resolution model:** drone photogrammetry, RTK/GNSS, LiDAR, survey, measured infiltration/soil samples.

Upgrades should not change the logical project structure. Recompute dependent layers and retain prior versions when useful for comparison.

## Safe failure behavior
- Never invent parcel boundaries or site measurements.
- Never present a public DEM or heuristic suitability layer as survey-grade engineering.
- If a source cannot be accessed, mark the dependency unavailable and continue with the remaining valid workflow.
- Permit manual GPS boundaries and partial datasets.
- Earthworks, dams, drainage structures, septic, foundations, or regulated work require appropriate site investigation and professional/permit review.

## Browser-first implementation guidance
Prefer browser-local work for lightweight raster/vector operations and a geospatial service for heavy LiDAR, conditioning, watershed, or large-raster tasks. Common implementation choices include CesiumJS or MapLibre/Three.js for viewing, Web Workers/WebAssembly for local computation, and Python geospatial tooling for heavy processing. Use portable formats such as Cloud Optimized GeoTIFF, GeoJSON/FlatGeobuf, 3D Tiles, and LAZ where appropriate.

The viewer should expose layer toggles, opacity, legends, units, provenance, and parameter controls.

## Stable output and completion criteria
A run is complete when:
- the site extent is resolved or explicitly left in manual-boundary mode;
- requested layers are computed or marked unavailable with reasons;
- provenance, units, resolution, algorithm/version, confidence, and caveats are recorded;
- the user AOI remains distinct from the analysis buffer; and
- a portable site/layer manifest can be handed to the host viewer or downstream agent.

Use `references/architecture.md` for the system shape, `references/acceptance-tests.md` for verification, and `references/changelog.md` for skill history.

## Improvement loop
After substantial use:
1. record the missing capability or failure mode;
2. classify it as data-source, algorithm, UX, validation, or performance work;
3. add or update an acceptance test before changing behavior;
4. update the relevant contract/reference;
5. bump `VERSION` according to repository semantic-version rules;
6. record the change in `references/changelog.md`;
7. preserve backwards compatibility for saved site manifests when practical.

Do not silently change an existing layer’s meaning. Record material algorithm changes with an algorithm version or a new layer version.

## Default minimum prototype
When asked for the minimum useful implementation, build:
1. address geocoding;
2. adjustable manual GPS AOI fallback;
3. GeoJSON import/export;
4. public DEM acquisition;
5. 3D terrain visualization;
6. elevation, slope, aspect, contours, flow accumulation, and soils;
7. layer toggles, legends, and opacity;
8. downloadable site/layer manifest with provenance.
