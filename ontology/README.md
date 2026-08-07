# Repository Self-Ontology

`SELF_MODEL.json` is the compact agent-facing model. `SELF_MODEL.graphml` is the visualization/tooling projection.

The repository tree remains canonical. The model is regenerated deterministically from active skill-library structure plus the small semantic overlay in `semantics.json`.

## Commands

```bash
node scripts/build-ontology.mjs --write
node scripts/build-ontology.mjs --check
node scripts/validate-library.mjs
```

Generated files contain no timestamps or commit SHA, so routine content edits do not create ontology churn. The fingerprint changes only when modeled topology or semantic relationships change.

The legacy root `AGENT.md` is represented as one semantic node but is not scanned into the active skill topology.
