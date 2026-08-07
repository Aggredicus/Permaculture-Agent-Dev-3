# Changelog

This changelog records meaningful design-model changes. Every change that affects goals, observations, assumptions, unknowns, risks, design elements, implementation tasks, or client deliverables should be logged here.

## Versioning Guide

- `v0.1.0` — initial starter model
- `v0.2.0` — first real client/site model
- `v0.3.0` — concept design model
- `v0.4.0` — implementation planning model
- `v1.0.0` — first client-ready delivery model
- Patch versions such as `v0.3.1` — small corrections, labels, source details, or validation fixes

## v0.1.0 — Starter Model

**Date:** 2026-05-04

### Added

- Created starter repository structure.
- Added `AGENT.md` with GraphML Site Model Protocol appended.
- Added `model/SITE_MODEL_SCHEMA.md`.
- Added valid starter `model/SITE_MODEL.graphml`.
- Added starter nodes for project, site, ecological resilience goal, unknowns, observations, and workflow tasks.
- Added starter edges for containment, sequencing, constraints, and goal justification.
- Added `PROJECT_STATE.md`, `DESIGN_DECISIONS.md`, `VALIDATION_CHECKLIST.md`, and client-facing templates.

### Changed

- Established GraphML as the living source of truth for interpreted site/design relationships.

### Removed

- Nothing removed.

### Verification Notes

- Starter GraphML was generated and XML-parsed successfully.
- No client-specific claims are included.
- All site-specific content is marked as placeholder, assumed, or unknown.

### Exported Files

- `exports/SITE_MODEL_v0.1.0.graphml`

---

## Example Future Entry — v0.3.0 Concept Food Forest Addition

**Date:** YYYY-MM-DD

### Added

- Added `design_element:west_fence_food_forest`.
- Added `risk:deer_browse_orchard`.
- Added `unknown:soil_drainage_west_fence`.
- Added `task:verify_sun_exposure_west_fence`.
- Added `task:install_tree_tubes`.

### Changed

- Updated project state to reflect a proposed food forest concept near the west fence.
- Updated implementation sequence to require drainage and sun verification before final species selection.

### Removed

- None.

### Verification Notes

- Food forest location is proposed, not field verified.
- Deer risk is client-reported or regionally plausible until confirmed.
- Soil drainage requires field observation after rain.

### Exported Files

- `exports/SITE_MODEL_v0.3.0.graphml`
- `exports/PROJECT_STATE_v0.3.0.md`
