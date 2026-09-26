# Acceptance Tests

## Input / boundary
- [ ] Valid address resolves to a point and either an authoritative boundary or manual-boundary fallback.
- [ ] Invalid/ambiguous address never produces an invented parcel.
- [ ] Manual rectangle can be moved and resized without losing its GPS coordinates.
- [ ] Custom polygon supports at least three distinct vertices and exports valid GeoJSON.
- [ ] User AOI and analysis buffer remain distinct.

## Data / provenance
- [ ] Every layer reports source datasets and native/effective resolution.
- [ ] Missing source data marks a dependency unavailable rather than fabricating values.
- [ ] Horizontal/vertical CRS and units are recorded when known.

## Computation
- [ ] Flat synthetic DEM returns near-zero slope.
- [ ] Planar synthetic DEM returns constant slope/aspect within numerical tolerance.
- [ ] Bowl synthetic DEM produces inward flow/depression behavior.
- [ ] Ridge synthetic DEM separates drainage basins correctly.
- [ ] Cut/fill volume matches an analytically known synthetic test surface within tolerance.

## Upgrade behavior
- [ ] Replacing DEM invalidates and recomputes terrain-dependent layers.
- [ ] User annotations and design objects survive source upgrades.
- [ ] Algorithm version is stored with each derived layer.
