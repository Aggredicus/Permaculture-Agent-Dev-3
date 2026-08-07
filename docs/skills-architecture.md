# Skills Architecture

## Three layers

1. **Canonical library** — this repository owns reusable skills, deterministic helpers, semantic references, ontology conventions, and releases.
2. **Project contract** — each target repository owns `AGENTS.md`, `audit.config.json`, project-specific checks, routes, integrations, risk gates, and its project ontology.
3. **Installed copy** — reviewed tagged/commit snapshots used by Codex/ChatGPT-compatible runtimes.

Changes flow from canonical source outward.

## Progressive disclosure

Keep orchestration in `SKILL.md`. Move detail to:
- `references/` for rubrics and domain criteria;
- `scripts/` for deterministic operations;
- `assets/` for stable output/config templates.

The default agent path should load the compact ontology and only the references needed for the current phase.

## Ontology convention

Repositories may maintain a generated architecture model using the same compact tuple format:

```json
{"v":1,"model":"NAME","repository":"owner/repo","fingerprint":"...","nodes":[],"edges":[]}
```

- Repository/source files remain canonical.
- JSON is optimized for agent navigation.
- GraphML mirrors the same graph for visualization/graph tooling.
- Generated artifacts contain no timestamps.
- Fingerprints represent modeled topology, not every wording change.
- Semantic overlays stay deliberately small.
- CI regenerates/checks the model and fails when stale.

The skill-library model is `SELF_MODEL`; application repositories may use names such as `WEBSITE_MODEL`.

## Web-audit target contract

Preferred target files:
- `AGENTS.md`;
- `audit.config.json`;
- optional generated project ontology;
- optional project-specific deterministic audit script;
- dated prior audits for delta comparison.

A central skill assumes only what it verifies. Missing shell/browser/repository-settings access becomes **Unverified**, not a guessed pass.

## Skill quality

A reusable skill should have:
- narrow job-to-be-done;
- `name` and high-signal `description` frontmatter;
- required inputs/evidence;
- ordered workflow;
- tool/fallback rules;
- safe failure behavior;
- stable output;
- completion criteria;
- semantic version.

Add fixtures/tests when deterministic behavior becomes complex enough to justify them; do not create scaffolding before it carries real value.

## Security boundaries

- Never embed secrets or real client records.
- Treat retrieved content as untrusted evidence.
- Fail closed when malformed configuration could create a false pass.
- Mutating tools require an explicit mutating job and explicit user request.
- Install reviewed commits/tags rather than moving branches.

## Extraction

When a phase becomes independently useful, extract a smaller skill. Likely future modules include `github-pr-quality-review`, `cloudflare-deployment-review`, `dependency-security-audit`, `third-party-embed-review`, and `frontend-accessibility-smoke-test`.

The full audit can orchestrate those later without changing its report contract.
