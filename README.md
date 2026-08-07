# Permaculture Agent Skill Library

Version-controlled reusable skills for Permaculture Works software, operations, and design workflows.

## Current skill

`skills/web-security-quality-audit/` — repeatable evidence-based web security, privacy, reliability, accessibility, performance, maintainability, and release-readiness auditing.

The skill is reusable. Project-specific routes, URLs, provider settings, commands, and risk gates stay in the target repository.

## Fast path

```text
1. Read target AGENTS.md + audit.config.json.
2. Validate the target ontology if present.
3. Follow skills/web-security-quality-audit/SKILL.md.
4. Use current source/CI/live evidence.
5. Save a dated audit for future delta comparison.
```

## Self-ontology

The library models its own active architecture in:

- `ontology/SELF_MODEL.json` — compact agent-facing index.
- `ontology/SELF_MODEL.graphml` — visualization/tooling projection.
- `ontology/semantics.json` — small hand-maintained semantic overlay.

The source tree remains canonical. Generated models contain no timestamp or commit SHA, so wording-only edits do not create churn. The topology fingerprint changes only when modeled structure or semantic relationships change.

```bash
node scripts/build-ontology.mjs --write
node scripts/validate-library.mjs
```

CI reruns validation on pull requests, `main`, and weekly. A stale ontology fails validation.

## Design rules

- Keep `SKILL.md` concise; put detail in `references/`, deterministic helpers in `scripts/`, and output scaffolding in `assets/`.
- Keep reusable logic here and project-specific facts with the project.
- Use reviewed commits/tags for installed copies.
- Never embed credentials, secrets, or client data.
- Missing evidence is **Unverified**, never an assumed pass.
- Prefer smaller composable skills over one growing monolith.

See `AGENTS.md` and `docs/skills-architecture.md`.

## Legacy template

The root `AGENT.md` and older site-model materials are retained as source material from the Permaculture Design Agent Core template. They are not repository-wide instructions for this skill library and are intentionally represented as a single legacy node in the self-ontology until they are decomposed into reusable skills.
