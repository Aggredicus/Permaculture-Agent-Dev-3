# Design Decisions

This file records major design decisions, tradeoffs, rejected alternatives, risk acceptances, and operating principles. It uses an Architecture Decision Record style adapted for permaculture design.

## Decision Template

### Decision ID

`decision:###_short_name`

### Date

YYYY-MM-DD

### Status

Proposed | Accepted | Rejected | Superseded | Retired

### Design Phase

intake | site_discovery | site_analysis | concept_design | master_plan | implementation_planning | installation | monitoring | adaptive_redesign

### Decision

State the decision in one or two clear sentences.

### Context

Explain the project conditions, goals, constraints, or uncertainty that led to this decision.

### Site Evidence

List the field observations, client statements, maps, photos, soil tests, or other sources supporting the decision.

### Client Goal Supported

Name the client goal or goals this decision serves.

### Alternatives Considered

List options considered and why they were not chosen.

### Risks

List design, ecological, maintenance, budget, legal, safety, or implementation risks.

### Unknowns / Verification Needed

List what must still be verified.

### Implementation Implications

Explain effects on sequencing, cost, labor, materials, contractors, or installation.

### Monitoring Implications

Explain how success or failure will be tracked.

### Graph Updates

List the nodes and edges added, changed, or retired.

---

## decision:001_water_and_soil_before_plant_selection

### Date

2026-05-04

### Status

Accepted

### Design Phase

intake

### Decision

Prioritize water behavior, soil condition, access, and site constraints before final plant selection.

### Context

Permaculture designs often fail when the process begins with a dream plant list rather than observed site relationships. Water, soil, sun, slope, deer pressure, and maintenance capacity determine whether plantings succeed.

### Site Evidence

No site evidence has been collected yet. This is a general operating rule for the design workflow.

### Client Goal Supported

Supports long-term resilience, lower maintenance, better plant survival, and safer implementation.

### Alternatives Considered

- Begin with a preferred plant list immediately. Rejected because it can create poor site/species fit.
- Create a visual design before site analysis. Rejected because it may hide major constraints.

### Risks

May feel slower to clients who want immediate planting recommendations.

### Unknowns / Verification Needed

All site-specific water, soil, sun, slope, and maintenance factors.

### Implementation Implications

Plant procurement should wait until site analysis is adequate.

### Monitoring Implications

Plant survival and water behavior should validate whether the initial sequence was sufficient.

### Graph Updates

- `unknown:soil_test_needed`
- `task:final_plant_selection`
- Edge: `unknown:soil_test_needed` constrains `task:final_plant_selection`

---

## decision:002_unknowns_are_first_class_nodes

### Date

2026-05-04

### Status

Accepted

### Design Phase

intake

### Decision

Model unknowns explicitly as graph nodes rather than burying uncertainty in prose.

### Context

Permaculture design involves incomplete information. Hidden uncertainty can lead to unsafe earthworks, poor plant choices, unrealistic budgets, and weak client trust.

### Site Evidence

Starter model includes unknowns for property boundary verification and soil testing.

### Client Goal Supported

Supports professional transparency and safer implementation.

### Alternatives Considered

- Track unknowns only in notes. Rejected because notes are easy to miss.
- Wait to model until all data exists. Rejected because design conversations evolve iteratively.

### Risks

Too many unknowns can clutter the graph if not curated.

### Unknowns / Verification Needed

Unknown nodes should be reviewed and retired, resolved, or updated during each major design phase.

### Implementation Implications

Implementation-ready recommendations require resolving critical unknowns.

### Monitoring Implications

Monitoring can reveal previously unknown site behavior and convert unknowns into observations.

### Graph Updates

- Unknown nodes become valid first-class graph objects.

---

## decision:003_graphml_for_interpreted_design_relationships

### Date

2026-05-04

### Status

Accepted

### Design Phase

intake

### Decision

Use GraphML to store interpreted design relationships, not raw GIS data or heavy spatial datasets.

### Context

A property design includes ecological causality and design reasoning that ordinary maps do not capture. However, GraphML is not the best place for raw point clouds, rasters, drone photos, CAD, or survey geometry.

### Site Evidence

No site-specific evidence. This is a system architecture decision.

### Client Goal Supported

Supports multi-agent coordination, provenance, and clean deliverable generation.

### Alternatives Considered

- Store all spatial data directly in GraphML. Rejected because it would bloat the model.
- Use only Markdown notes. Rejected because relationships become harder to query.

### Risks

GraphML may require discipline and schema enforcement to remain clean.

### Unknowns / Verification Needed

Future tooling may require import/export conventions for GIS assets.

### Implementation Implications

Use `external_asset` nodes to reference heavy files.

### Monitoring Implications

Monitoring points can be represented in GraphML while photos and raw data remain external.

### Graph Updates

- Added schema support for `external_asset` nodes.

---

## decision:004_field_verification_before_implementation_ready_recommendations

### Date

2026-05-04

### Status

Accepted

### Design Phase

intake

### Decision

Do not present recommendations as implementation-ready until key site conditions and safety constraints have been field verified or professionally verified.

### Context

Maps, screenshots, client descriptions, and AI inference are useful but cannot replace field observation for site-sensitive decisions.

### Site Evidence

No client-specific evidence yet.

### Client Goal Supported

Supports safety, accuracy, ecological fit, and professional trust.

### Alternatives Considered

- Allow implementation plans from remote analysis alone. Rejected for high-risk items.
- Use broad disclaimers without modeling verification needs. Rejected because it is less actionable.

### Risks

May limit remote-only package scope.

### Unknowns / Verification Needed

Boundaries, utilities, drainage, soil, regulated areas, slope risks, and plant suitability should be verified as needed.

### Implementation Implications

Some deliverables should be labeled concept-level until verification is complete.

### Monitoring Implications

Post-installation monitoring can update confidence and verification status.

### Graph Updates

- Reinforces verification status fields and professional review triggers.
