# Validation Checklist

Use this checklist before sending any client-facing deliverable. Mark unresolved items clearly. A design can be useful before every item is complete, but it must not be misrepresented as implementation-ready when critical unknowns remain.

## Readiness Summary

| Gate | Yes/No | Notes |
|---|---|---|
| Ready for concept review |  |  |
| Ready for implementation planning |  |  |
| Ready for installation |  |  |

## 1. Intake Completeness

- [ ] Client name and project type are recorded.
- [ ] Client goals are documented in plain language.
- [ ] Budget range or budget uncertainty is recorded.
- [ ] Timeline is recorded.
- [ ] Maintenance capacity is recorded.
- [ ] Labor availability is recorded.
- [ ] Aesthetic preferences are recorded.
- [ ] Food, habitat, privacy, water, soil, access, and educational goals are recorded where relevant.
- [ ] Non-negotiables, fears, and constraints are recorded.
- [ ] Consent for photos, portfolio use, and documentation is recorded where relevant.

## 2. Base Map Readiness

- [ ] Property boundary or working design boundary is shown.
- [ ] Boundary confidence is stated.
- [ ] North arrow is present.
- [ ] Scale or measurement basis is stated.
- [ ] Structures are shown.
- [ ] Driveways, gates, paths, and access points are shown.
- [ ] Major existing trees or vegetation areas are shown.
- [ ] Water features and visible drainage areas are shown.
- [ ] Utilities, septic, wells, easements, and hazards are shown or marked unknown.
- [ ] Areas requiring field verification are clearly labeled.

**Hard stop:** Do not treat screenshots or hand sketches as survey-grade boundaries.

## 3. Site Analysis Completeness

- [ ] Water movement is described.
- [ ] Soil conditions are described or marked unknown.
- [ ] Sun/shade patterns are described or marked unknown.
- [ ] Slope/landform is described or marked unknown.
- [ ] Wind/microclimate is described or marked unknown.
- [ ] Existing vegetation is described.
- [ ] Wildlife/pest pressure is described or marked unknown.
- [ ] Human use patterns are described.
- [ ] Access and maintenance routes are described.
- [ ] Risks and opportunities are explicitly separated.

## 4. Water and Soil First Check

- [ ] Water has been analyzed before final planting recommendations.
- [ ] Overflow routes are considered for water interventions.
- [ ] Soil testing or field soil assessment is recommended where needed.
- [ ] Compaction and erosion are considered.
- [ ] Mulch, organic matter, living roots, and soil cover are considered.
- [ ] Planting zones match likely soil moisture and drainage.

**Hard stop:** Do not recommend earthworks as implementation-ready without checking utilities, overflow, slope risk, property impacts, and regulatory triggers.

## 5. Zone and Sector Logic

- [ ] High-care elements are near frequent human activity.
- [ ] Lower-care elements are placed farther away where appropriate.
- [ ] Sun, wind, water, views, noise, privacy, wildlife, and access sectors are considered.
- [ ] Zone placement matches client routines and maintenance reality.

## 6. Plant Selection Safety

- [ ] Plant choices match sun/shade.
- [ ] Plant choices match soil moisture and drainage.
- [ ] Plant choices match hardiness and climate.
- [ ] Deer/wildlife pressure is considered.
- [ ] Mature size and spacing are considered.
- [ ] Maintenance burden is realistic.
- [ ] Edible/medicinal claims are cautious and verified.

## 7. Native / Invasive / Toxicity Review

- [ ] Locally invasive species are avoided or flagged for verification.
- [ ] Toxicity risks to children, pets, livestock, or clients are flagged.
- [ ] Native species opportunities are considered.
- [ ] Non-native species are justified by function and low risk.
- [ ] Local extension, conservation district, native plant society, or government sources are used for uncertain plant risk claims.

**Hard stop:** Do not recommend potentially invasive or toxic plants without explicit caution and verification.

## 8. Climate Resilience Review

- [ ] Drought resilience is considered.
- [ ] Extreme rain and flooding are considered.
- [ ] Wind exposure is considered.
- [ ] Heat and reflected heat are considered.
- [ ] Freeze-thaw and winter instability are considered where relevant.
- [ ] Species diversity and redundancy are included.
- [ ] Backup watering or establishment watering is addressed.

## 9. Maintenance Reality Review

- [ ] Maintenance tasks are listed.
- [ ] First-year watering is addressed.
- [ ] Mulch and weed management are addressed.
- [ ] Pruning or training needs are addressed where relevant.
- [ ] Client labor capacity matches design complexity.
- [ ] High-maintenance elements are either justified or simplified.

**Hard stop:** Do not deliver an installation plan without a maintenance plan.

## 10. Budget and Labor Reality Review

- [ ] Materials are listed or estimated.
- [ ] Labor phases are described.
- [ ] DIY vs contractor tasks are separated.
- [ ] Cost ranges are labeled as rough, estimate, quote, or actual.
- [ ] Dependencies are identified.
- [ ] First-year priorities are separated from optional upgrades.
- [ ] Unsupported yield or profit claims are avoided.

**Hard stop:** Do not imply guaranteed profit, yield, savings, carbon credit, or grant outcomes without evidence.

## 11. Regulatory / Professional Review Triggers

Flag professional review if any are present:

- [ ] Wetland, shoreline, stream, ditch, floodplain, or regulated waterbody work.
- [ ] Large swales, ponds, dams, spillways, retaining walls, terraces, or slope stabilization.
- [ ] Work near foundations, septic, wells, utilities, easements, driveways, culverts, or public roads.
- [ ] Herbicide/pesticide recommendations.
- [ ] Livestock, veterinary, food safety, or toxic plant concerns.
- [ ] High-risk trees near people, buildings, roads, or utilities.
- [ ] Legal, zoning, HOA, grant compliance, or permitting claims.

## 12. GraphML Model Integrity

- [ ] All important graph nodes use allowed node types.
- [ ] All important graph edges use allowed edge types.
- [ ] Required node attributes are present.
- [ ] Required edge attributes are present.
- [ ] Confidence values are set.
- [ ] Verification status is set.
- [ ] Source type and source detail are included.
- [ ] Unknowns are represented as nodes.
- [ ] Critical risks are connected to affected design elements or tasks.
- [ ] Versioned export is created after meaningful changes.

## 13. Decision Log Integrity

- [ ] Major decisions have entries in `DESIGN_DECISIONS.md`.
- [ ] Alternatives are recorded where meaningful.
- [ ] Risks and unknowns are recorded.
- [ ] Implementation implications are recorded.
- [ ] Monitoring implications are recorded.
- [ ] Graph updates are referenced.

## 14. Client Report Readiness

- [ ] Executive summary is clear.
- [ ] Client goals are restated accurately.
- [ ] Design thesis is understandable.
- [ ] Assumptions are visible.
- [ ] Field-verification needs are visible.
- [ ] Risks are not hidden.
- [ ] Next steps are practical.
- [ ] Tone is professional and client-ready.

## 15. Final Delivery Gate

Before delivery, confirm:

- [ ] The design is labeled correctly as concept, master plan, implementation-ready, or monitoring update.
- [ ] No unresolved hard stop is hidden.
- [ ] The latest model version is exported.
- [ ] `PROJECT_STATE.md` matches the deliverable.
- [ ] `CHANGELOG.md` includes the latest meaningful changes.
- [ ] Client-facing documents distinguish recommendations from verification needs.

## Final Notes

A design may be ready for concept review even when it is not ready for installation. Never collapse those stages.
