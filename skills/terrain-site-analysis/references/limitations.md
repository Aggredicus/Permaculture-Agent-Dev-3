# Terrain analysis validity and operational limits

- Input elevations must represent meters and have an appropriate georeferencing CRS. USGS 3DEP exports require a live request; a finer requested output grid does not improve source accuracy.
- Address lookup is a point estimate, not a legal boundary. Polygon provenance and valid DEM coverage must be retained separately.
- Slope and aspect are derivatives of a sampled elevation surface. They are not measurements of runoff infiltration, soil quality, solar radiation, or legal drainage boundaries.
- Cut/fill models a single horizontal plane over the entire supplied polygon for illustration, not actual earthworks or legal authorization.
- Do not infer permission to modify public land, wetlands, surface waters, roads, utilities, or structures.
- The Hager Park example is a **public-site reproducibility fixture**. It has not produced measured terrain numbers until real USGS elevation data are successfully fetched and validated.