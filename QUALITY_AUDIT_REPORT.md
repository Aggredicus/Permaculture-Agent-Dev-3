# Quality Audit Report — Permaculture Design Agent Core

**Audit date:** 2026-05-04  
**Package:** `permaculture_design_agent_core.zip`  
**Result:** PASS with one minor GraphML attribute-name correction applied.

## Executive Summary

The package contains the complete lean companion system requested for the Permaculture Design Agent: the core `AGENT.md`, a living GraphML site model, strict schema, project state, changelog, design decision log, validation checklist, client report template, intake template, site visit checklist, monitoring report template, and versioned starter exports.

The package is structurally sound, agent-ready, and appropriate to use as a Cursor/Codex-style repository seed. The starter GraphML parses successfully as XML, uses directed edges, includes a starter version, and has valid edge references.

## Checks Performed

| Check | Result | Notes |
|---|---:|---|
| Required file tree present | PASS | All required files and folders exist. |
| Markdown documents populated | PASS | No empty required Markdown files. |
| Starter GraphML XML parse | PASS | `model/SITE_MODEL.graphml` and export snapshot parse successfully. |
| Directed graph model | PASS | Graph uses `edgedefault="directed"`. |
| Graph node count | PASS | Starter graph includes 10 nodes. |
| Graph edge count | PASS | Starter graph includes 6 edges. |
| Edge source/target references | PASS | No dangling edge references. |
| Required node attributes | PASS | All starter nodes include required attributes. |
| Required edge attributes | PASS after correction | Edge attribute names were normalized to schema terms. |
| Schema node-type coverage | PASS | All required node types are documented. |
| Schema edge-type coverage | PASS | All required edge types are documented. |
| Controlled vocabulary coverage | PASS | Required vocabularies are present. |
| AGENT.md protocol section | PASS | `GraphML Site Model Protocol` appears once. |
| Versioned exports | PASS | Starter GraphML and project state export are included. |
| Obvious TODO/FIXME placeholders | PASS | None found outside intentional template blanks. |

## Correction Applied

The first generated GraphML used edge data attributes with names like `edge_label`, `edge_description`, and `edge_confidence`. These parsed correctly in NetworkX, but they did not exactly match the schema requirement that edge attributes be named `label`, `description`, `confidence`, `source_type`, `source_detail`, `created_at`, and `updated_at`.

Correction applied:

- `edge_label` → `label`
- `edge_description` → `description`
- `edge_confidence` → `confidence`
- `edge_source_type` → `source_type`
- `edge_source_detail` → `source_detail`
- `edge_created_at` → `created_at`
- `edge_updated_at` → `updated_at`

This was corrected in both:

- `model/SITE_MODEL.graphml`
- `exports/SITE_MODEL_v0.1.0.graphml`

## File Inventory

| File | Bytes | Approx. Lines |
|---|---:|---:|
| `AGENT.md` | 27,017 | 1,158 |
| `README.md` | 5,034 | 139 |
| `exports/.gitkeep` | 0 | 0 |
| `exports/PROJECT_STATE_v0.1.0.md` | 3,372 | 95 |
| `exports/SITE_MODEL_v0.1.0.graphml` | 13,222 | 2 |
| `model/CHANGELOG.md` | 2,378 | 79 |
| `model/DESIGN_DECISIONS.md` | 6,991 | 292 |
| `model/PROJECT_STATE.md` | 3,372 | 95 |
| `model/SITE_MODEL.graphml` | 13,222 | 2 |
| `model/SITE_MODEL_SCHEMA.md` | 12,721 | 556 |
| `quality/VALIDATION_CHECKLIST.md` | 7,675 | 184 |
| `templates/CLIENT_REPORT_TEMPLATE.md` | 6,216 | 223 |
| `templates/MONITORING_REPORT_TEMPLATE.md` | 3,557 | 171 |
| `templates/SITE_INTAKE_TEMPLATE.md` | 5,302 | 253 |
| `templates/SITE_VISIT_CHECKLIST.md` | 6,551 | 267 |


## GraphML Inventory

| Item | Count |
|---|---:|
| GraphML keys | 23 |
| Nodes | 10 |
| Edges | 6 |
| Invalid edge references | 0 |

## Starter Graph Nodes

- `project:starter_permaculture_design`
- `property:site`
- `goal:increase_ecological_resilience`
- `unknown:property_boundary_verification`
- `unknown:soil_test_needed`
- `observation:site_data_not_yet_collected`
- `task:collect_client_intake`
- `task:create_base_map`
- `task:perform_site_visit`
- `task:final_plant_selection`

## Starter Graph Edges

- `e001`: `project:starter_permaculture_design` → `property:site`
- `e002`: `property:site` → `unknown:property_boundary_verification`
- `e003`: `unknown:soil_test_needed` → `task:final_plant_selection`
- `e004`: `task:collect_client_intake` → `task:create_base_map`
- `e005`: `task:create_base_map` → `task:perform_site_visit`
- `e006`: `goal:increase_ecological_resilience` → `task:perform_site_visit`

## Product Quality Notes

### Strengths

- The package is lean and coherent: it avoids extra scripts, databases, or unnecessary tooling.
- The GraphML schema is strict enough to prevent uncontrolled graph drift.
- Unknowns are treated as first-class model objects, which improves safety and design honesty.
- The validation checklist contains appropriate hard stops for earthworks, utilities, regulated areas, plant safety, unsupported yield claims, water overflow, and missing maintenance planning.
- The templates are immediately usable for real client work and agent workflows.
- The project state and changelog make multi-agent coordination much clearer.

### Remaining Improvement Opportunities

1. Add an optional lightweight `scripts/validate_site_model.py` later, if you want automated QA inside Cursor.
2. Add a small `examples/` folder later with one fictional sample project after the core stabilizes.
3. Add a `GRAPH_UPDATE_PROMPT.md` later for agents that only update the GraphML model.
4. Add a `CLIENT_REPORT_EXPORT_PROMPT.md` later for generating final reports from the graph and project state.

These are optional. The current package is already ready for practical testing.

## Final Verdict

**Approved for use as a v0.1.0 repository seed.**

Recommended next step: test the package in Cursor by giving the agent a simple fictional client scenario and asking it to update the GraphML, project state, changelog, and decision log together.
