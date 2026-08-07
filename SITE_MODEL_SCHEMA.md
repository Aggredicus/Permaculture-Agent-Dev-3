# SITE_MODEL_SCHEMA.md — Living Permaculture Site Graph Schema

## Purpose

`SITE_MODEL.graphml` stores interpreted landscape and design intelligence for a permaculture project. It is a relationship model for goals, observations, constraints, opportunities, risks, design elements, tasks, and monitoring points.

It is not a replacement for GIS, CAD, survey data, point clouds, drone imagery, engineering drawings, wetland delineations, legal review, or field verification. Heavy spatial data should remain in external files and be referenced through `external_asset` nodes.

## Core Principle

Every meaningful graph element should answer four questions:

1. What is it?
2. How do we know it?
3. How confident are we?
4. What does it affect?

## Required Attributes for All Nodes

| Attribute | Required | Description |
|---|---:|---|
| `id` | yes | Unique GraphML node ID using the naming rules below. |
| `label` | yes | Human-readable title. |
| `node_type` | yes | One of the allowed node types. |
| `description` | yes | Plain-English explanation. |
| `confidence` | yes | `low`, `medium`, or `high`. |
| `verification_status` | yes | Source/verification state. |
| `source_type` | yes | Controlled source type. |
| `source_detail` | yes | Specific source note, file, quote, or observation. |
| `created_at` | yes | ISO date. |
| `updated_at` | yes | ISO date. |

Recommended optional attributes:

| Attribute | Description |
|---|---|
| `design_phase` | Current phase where the node is most relevant. |
| `implementation_status` | Current task/design status. |
| `priority` | Practical priority. |
| `risk_severity` | Severity if node is a risk. |
| `maintenance_burden` | Expected maintenance level. |
| `cost_confidence` | Cost evidence quality. |
| `notes` | Extra implementation or design notes. |

## Required Attributes for All Edges

| Attribute | Required | Description |
|---|---:|---|
| `id` | yes | Unique edge ID. |
| `edge_type` | yes | One of the allowed edge types. |
| `label` | yes | Human-readable relationship. |
| `description` | yes | Why the relationship exists. |
| `confidence` | yes | `low`, `medium`, or `high`. |
| `source_type` | yes | Controlled source type. |
| `source_detail` | yes | Specific provenance. |
| `created_at` | yes | ISO date. |
| `updated_at` | yes | ISO date. |

## Controlled Vocabularies

### `confidence`

- `low` — plausible but weakly supported; use cautiously.
- `medium` — supported by client report, map inference, common pattern, or limited observation.
- `high` — field verified, measured, professionally verified, or strongly documented.

### `verification_status`

- `assumed`
- `client_reported`
- `map_inferred`
- `field_observed`
- `field_verified`
- `professionally_verified`

### `implementation_status`

- `not_started`
- `proposed`
- `approved`
- `scheduled`
- `in_progress`
- `installed`
- `monitored`
- `revised`
- `retired`

### `risk_severity`

- `low`
- `moderate`
- `high`
- `critical`

### `design_phase`

- `intake`
- `site_discovery`
- `site_analysis`
- `concept_design`
- `master_plan`
- `implementation_planning`
- `installation`
- `monitoring`
- `adaptive_redesign`

### `priority`

- `low`
- `medium`
- `high`
- `urgent`

### `maintenance_burden`

- `low`
- `moderate`
- `high`

### `cost_confidence`

- `unknown`
- `rough_order_of_magnitude`
- `estimate`
- `quote`
- `actual`

### `source_type`

- `client_statement`
- `field_observation`
- `photo`
- `map`
- `gis_layer`
- `soil_test`
- `extension_source`
- `government_source`
- `professional_report`
- `designer_assumption`

## Required Node Types

Each node type may use the required global attributes plus the suggested optional fields.

### `project`

The overall design project.

Required context: project name, client/site reference, model version.

Example: `project:shawn_wolf_permaculture_design`

### `property`

The physical site being designed.

Optional fields: area, address/general location, boundary confidence.

Example: `property:site`

### `client_goal`

A stated or inferred client objective.

Examples: `goal:reduce_mowing`, `goal:increase_privacy`, `goal:create_food_forest`

### `zone`

Permaculture zone of use intensity.

Examples: `zone:zone_1_kitchen_garden`, `zone:zone_3_orchard`

### `sector`

External force or directional influence.

Examples: `sector:winter_wind`, `sector:afternoon_sun`, `sector:road_noise`

### `structure`

Building or built feature.

Examples: `structure:house`, `structure:barn`, `structure:shed`

### `path`

Existing or proposed circulation route.

Examples: `path:main_access_path`, `path:orchard_maintenance_loop`

### `access_point`

Entry, gate, driveway access, delivery point, equipment access.

Example: `access:driveway_entry`

### `water_source`

Source of water such as roof, well, hose bib, pond, spring, or municipal supply.

Example: `water_source:south_roof_gutter`

### `water_flow`

Observed, inferred, or proposed water movement.

Example: `water_flow:driveway_runoff_to_low_spot`

### `water_feature`

Rain garden, swale, pond, basin, stream, wetland, ditch, tank, or cistern.

Example: `water_feature:front_rain_garden`

### `soil_area`

Area characterized by soil condition.

Example: `soil_area:compacted_lawn_near_driveway`

### `slope_area`

Slope or landform region.

Example: `slope_area:south_facing_slope`

### `microclimate`

Thermal, wind, shade, frost, or moisture pattern.

Example: `microclimate:warm_south_wall`

### `existing_plant`

Existing plant, tree, shrub, hedgerow, patch, or vegetation area.

Example: `existing_plant:mature_maple_north_yard`

### `proposed_plant`

Proposed individual plant or species group.

Example: `proposed_plant:pawpaw`

### `plant_guild`

Functional plant community.

Example: `plant_guild:pawpaw_shade_edge_guild`

### `habitat_area`

Pollinator strip, bird corridor, wet meadow, woodland edge, meadow patch, refuge zone.

Example: `habitat_area:pollinator_meadow_front_yard`

### `wildlife_pressure`

Deer, rabbit, geese, vole, insect, disease, or other pressure.

Example: `wildlife_pressure:deer_browse_orchard`

### `risk`

Condition that could cause failure, harm, cost, or delay.

Example: `risk:unknown_utility_location`

### `opportunity`

Beneficial design potential.

Example: `opportunity:convert_lawn_to_meadow`

### `constraint`

Limitation affecting design.

Example: `constraint:limited_client_maintenance_time`

### `unknown`

Unverified information that affects design quality or safety.

Example: `unknown:soil_ph_west_orchard`

### `observation`

Specific observed or reported fact.

Example: `observation:water_pools_after_heavy_rain`

### `design_element`

Proposed or approved feature.

Example: `design_element:west_fence_food_forest`

### `implementation_task`

Action item for installation or preparation.

Example: `task:install_tree_tubes`

### `monitoring_point`

Photo point, inspection point, or recurring check.

Example: `monitoring_point:rain_garden_overflow_after_storm`

### `decision`

Logged design decision linked to the decision log.

Example: `decision:004_food_forest_west_fence`

### `source`

Source document, person, map, soil test, agency reference, photo set, or professional report.

Example: `source:client_intake_2026_05_04`

### `external_asset`

Reference to heavy or external files such as GIS layers, drone imagery, CAD, point clouds, photos, PDFs, or spreadsheets.

Example: `external_asset:base_map_dxf_2026_05_04`

## Required Edge Types

### `contains`

Parent contains child.

Example: `project` contains `property`; `property` contains `zone`.

### `adjacent_to`

Spatial or functional adjacency.

Example: `path:main_access` adjacent_to `zone:zone_1_kitchen_garden`.

### `located_in`

Feature is located within a zone, area, or property.

Example: `plant_guild:pawpaw_guild` located_in `zone:zone_3_orchard`.

### `flows_to`

Water, traffic, nutrients, energy, or material flow.

Example: `water_flow:roof_runoff` flows_to `water_feature:rain_garden`.

### `influences`

General influence relationship.

Example: `microclimate:warm_wall` influences `proposed_plant:fig_trial`.

### `shades`

Shade influence.

Example: `existing_plant:mature_maple` shades `zone:zone_1_bed`.

### `shelters`

Wind, privacy, or exposure protection.

Example: `design_element:windbreak` shelters `plant_guild:orchard`.

### `exposes`

Creates exposure or vulnerability.

Example: `sector:winter_wind` exposes `zone:front_yard`.

### `supports`

Beneficial support.

Example: `habitat_area:pollinator_strip` supports `proposed_plant:apple_trees`.

### `competes_with`

Competition for light, water, nutrients, access, or management attention.

Example: `existing_plant:black_walnut` competes_with `proposed_plant:tomato_bed`.

### `risks`

Risk affects another node.

Example: `wildlife_pressure:deer` risks `plant_guild:young_orchard`.

### `mitigates`

Design element reduces risk.

Example: `task:install_tree_tubes` mitigates `wildlife_pressure:deer`.

### `constrains`

Constraint limits or conditions another node.

Example: `unknown:soil_ph` constrains `proposed_plant:blueberry`.

### `creates_opportunity_for`

Condition opens design potential.

Example: `water_flow:roof_runoff` creates_opportunity_for `water_feature:rain_garden`.

### `requires`

Node requires another condition, task, asset, or verification.

Example: `design_element:swale` requires `unknown:utility_location_verification`.

### `depends_on`

Task or decision depends on another item.

Example: `task:order_plants` depends_on `task:finalize_species_list`.

### `required_before`

Sequencing dependency.

Example: `task:soil_test` required_before `task:final_plant_selection`.

### `implements`

Task implements design element.

Example: `task:install_mulch_basins` implements `design_element:orchard_guild`.

### `justifies`

Goal or observation justifies design response.

Example: `client_goal:reduce_mowing` justifies `design_element:meadow_conversion`.

### `derived_from`

Node or edge is derived from a source.

Example: `observation:clay_soil` derived_from `source:soil_test_2026_05_04`.

### `observed_at`

Observation occurred at a location or feature.

Example: `observation:standing_water` observed_at `soil_area:low_depression`.

### `monitored_by`

Feature is monitored by a monitoring point.

Example: `water_feature:rain_garden` monitored_by `monitoring_point:rain_garden_overflow`.

### `replaces`

New element replaces previous element.

Example: `design_element:mulched_path` replaces `path:turf_path`.

### `updates`

New decision or version updates older item.

Example: `decision:005_revised_orchard_location` updates `decision:003_initial_orchard_location`.

### `contradicts`

Evidence conflicts with another claim.

Example: `soil_test:alkaline_result` contradicts `assumption:acidic_soil_for_blueberries`.

## Naming Rules

Use lowercase, stable, descriptive IDs. Prefer prefixes:

```txt
project:shawn_wolf_permaculture_design
goal:privacy_screening
zone:zone_1_kitchen_garden
sector:winter_wind
structure:house
path:main_access_path
water_flow:roof_runoff_south_gutter
risk:deer_browse_orchard
unknown:soil_ph_west_orchard
task:install_tree_tubes
decision:004_food_forest_west_fence
```

Avoid spaces. Use underscores. Do not rename IDs casually; create replacement/update relationships when necessary.

## Versioning Rules

Working model:

```txt
model/SITE_MODEL.graphml
```

Versioned snapshots:

```txt
exports/SITE_MODEL_v0.1.0.graphml
exports/SITE_MODEL_v0.2.0.graphml
exports/SITE_MODEL_v1.0.0.graphml
```

Lifecycle:

- `v0.1.0` — initial starter model
- `v0.2.0` — first real client/site model
- `v0.3.0` — concept design model
- `v0.4.0` — implementation planning model
- `v1.0.0` — first client-ready delivery model

## Update Protocol

Every meaningful graph update must also update:

1. `PROJECT_STATE.md`
2. `CHANGELOG.md`
3. `DESIGN_DECISIONS.md` when a decision, tradeoff, risk acceptance, or rejected alternative is involved

## Example Mini-Graph

```txt
client_goal:reduce_mowing
  justifies → design_element:front_yard_meadow

design_element:front_yard_meadow
  supports → opportunity:pollinator_habitat

risk:weed_pressure
  risks → design_element:front_yard_meadow

task:site_prep_sheet_mulch
  required_before → task:seed_meadow_mix
```

## Integrity Rules

- Do not add unsupported certainty.
- Do not delete unknowns until they are resolved or explicitly retired.
- Do not mark anything `field_verified` unless field verification occurred.
- Do not mark anything `professionally_verified` unless a qualified professional or official source verified it.
- Do not make implementation-ready recommendations where professional review triggers remain unresolved.
