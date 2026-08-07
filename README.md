# Permaculture Design Agent Core

**Permaculture Design Agent Core** is a minimalist, agent-ready operating system for professional permaculture design. It combines one core `AGENT.md`, one living GraphML site model, and a small set of strict companion documents so a human designer and AI agents can coordinate from intake through monitoring without losing provenance, uncertainty, or design rationale.

## What This Is

This is a lean documentation and model-management system for regenerative site design. It helps a designer or AI agent:

- maintain a living model of a property,
- track goals, observations, assumptions, risks, unknowns, and decisions,
- distinguish client-reported information from field-verified facts,
- generate client-facing reports from a single source of truth,
- validate design quality before delivery,
- coordinate across Cursor, ChatGPT, GitHub, local files, and future agent workflows.

## What This Is Not

This is not GIS software, a survey, a legal opinion, an engineering plan, a wetland delineation, a pesticide recommendation system, or a substitute for professional field verification. The GraphML model stores interpreted design intelligence and relationships, not raw point clouds, rasters, drone imagery, or survey-grade geometry.

## Folder Structure

```txt
permaculture-design-agent-core/
├─ AGENT.md
├─ README.md
├─ model/
│  ├─ SITE_MODEL.graphml
│  ├─ SITE_MODEL_SCHEMA.md
│  ├─ PROJECT_STATE.md
│  ├─ CHANGELOG.md
│  └─ DESIGN_DECISIONS.md
├─ quality/
│  └─ VALIDATION_CHECKLIST.md
├─ templates/
│  ├─ CLIENT_REPORT_TEMPLATE.md
│  ├─ SITE_INTAKE_TEMPLATE.md
│  ├─ SITE_VISIT_CHECKLIST.md
│  └─ MONITORING_REPORT_TEMPLATE.md
└─ exports/
   └─ .gitkeep
```

## Quick Start

1. Open the folder in Cursor or another IDE.
2. Read `AGENT.md` first.
3. Fill out `templates/SITE_INTAKE_TEMPLATE.md` for the client.
4. Use `templates/SITE_VISIT_CHECKLIST.md` during field observation.
5. Update `model/SITE_MODEL.graphml` as meaningful facts, assumptions, risks, and design elements emerge.
6. Keep `model/PROJECT_STATE.md` current after each design session.
7. Record major decisions in `model/DESIGN_DECISIONS.md`.
8. Run `quality/VALIDATION_CHECKLIST.md` before client delivery.
9. Generate the client report using `templates/CLIENT_REPORT_TEMPLATE.md`.
10. Export versioned snapshots to `exports/`.

## Design Workflow

Recommended sequence:

1. Intake and project framing
2. Base map and site discovery
3. Field observation
4. Bioregional context brief
5. Goals-to-functions mapping
6. Zone and sector analysis
7. Concept master plan
8. Plant guild and species logic
9. Water and soil strategy
10. Climate resilience layer
11. Implementation reality sheet
12. Client stewardship guidance
13. Design defense meeting
14. Installation support
15. Year 1 monitoring and adaptive redesign

## Living Site Graph

`model/SITE_MODEL.graphml` is the working model. It stores relationships such as:

- `client_goal:reduce_mowing` → `justifies` → `design_element:front_yard_meadow`
- `risk:deer_browse` → `risks` → `plant_guild:young_orchard`
- `unknown:soil_ph` → `constrains` → `proposed_plant:blueberry`
- `task:soil_test` → `required_before` → `task:final_plant_selection`
- `water_flow:roof_runoff` → `flows_to` → `water_feature:rain_garden`

The graph should model ecological and design causality, not merely visual layout.

## Versioning Rules

Keep the working model at:

```txt
model/SITE_MODEL.graphml
```

Export snapshots to:

```txt
exports/SITE_MODEL_v0.1.0.graphml
exports/PROJECT_STATE_v0.1.0.md
exports/CLIENT_REPORT_v0.1.0.md
```

Suggested lifecycle:

- `v0.1.0` — initial starter model
- `v0.2.0` — first real client/site model
- `v0.3.0` — concept design model
- `v0.4.0` — implementation planning model
- `v1.0.0` — first client-ready delivery model

Use patch versions for corrections, source updates, or small refinements.

## Quality Control

Before any client delivery, run `quality/VALIDATION_CHECKLIST.md`. Do not treat a design as implementation-ready if it has unverified utilities, unresolved water overflow, unreviewed regulated areas, unverified high-risk earthworks, unsafe plant recommendations, or no maintenance plan.

## Client Deliverables

Use the templates to produce:

- intake summaries,
- site visit notes,
- regenerative site design reports,
- monitoring reports,
- task lists,
- decision summaries,
- GraphML model summaries.

## Professional Boundaries

This system supports design thinking and documentation. It must flag when licensed or specialized review is needed, especially for regulated waterways, wetlands, shorelines, major earthworks, drainage changes, utilities, structures, toxic plants, invasive species control, pesticides, livestock health, food safety, or legal compliance.

## Minimal Operating Rule

A design update is complete only when the model, state, changelog, and decision log agree.

Generated: 2026-05-04
