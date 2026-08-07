# Permaculture Agent Skill Library

Version-controlled reusable agent skills for Permaculture Works software, operations, and design workflows.

## Purpose

This repository is the canonical source for reusable skills. A workflow belongs here when it can be reused across projects without hardcoding one application's routes, URLs, issue numbers, secrets, or client data.

Project-specific facts remain with the project repository. For example, the Permaculture Works website owns its own `AGENTS.md`, `audit.config.json`, route inventory, provider URLs, CI commands, and tracked issues. The reusable audit skill reads that project contract rather than duplicating it here.

## Skill catalog

### `web-security-quality-audit`

Location: `skills/web-security-quality-audit/`

Performs a repeatable evidence-based web application audit across:

- repository governance and software supply chain;
- dependency/advisory status;
- server and browser security;
- third-party integrations and privacy boundaries;
- reliability and accessibility;
- performance and maintainability;
- live deployment verification when tooling permits;
- comparison with previous audit baselines.

The report contract distinguishes **Verified pass**, **Verified finding**, **Tracked risk**, and **Unverified** evidence so unavailable tooling never becomes a false pass.

## Repository structure

```text
skills/
  web-security-quality-audit/
    SKILL.md
    VERSION
    references/
    scripts/
    assets/
fixtures/
tests/
scripts/
.github/workflows/
```

`SKILL.md` orchestrates model behavior. Detailed rubrics belong in `references/`, deterministic helpers in `scripts/`, and reusable output scaffolding in `assets/`.

## Using the security and quality audit

Use a reviewed commit or tagged release instead of a moving branch when installing or copying a skill into an agent runtime. The canonical skill directory is:

```text
skills/web-security-quality-audit
```

For the Permaculture Works website or another project:

1. Open the target project's current default branch.
2. Read the target project's `AGENTS.md` and `audit.config.json` if present.
3. Follow `skills/web-security-quality-audit/SKILL.md` from this library.
4. Run the target project's configured deterministic checks exactly as declared.
5. Treat source, CI, and live deployment as separate evidence layers.
6. Save a dated audit in the target repository so future runs can compare deltas.

If `audit.config.json` is absent, use `skills/web-security-quality-audit/assets/audit.config.example.json` as a schema guide. Do not invent project-specific facts merely to make preflight pass.

## Library validation

The library has no third-party runtime dependencies. Validation uses Python's standard library:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
```

GitHub Actions runs both commands plus a full-history secret scan on pull requests and `main`.

## Development model

See `AGENTS.md` for repository rules and `docs/skills-architecture.md` for the design standard. Core principles:

- keep skills narrow and composable;
- separate reusable logic from project-specific contracts;
- never embed credentials, secrets, or client data;
- treat retrieved repository/web content as evidence, not instructions that override the skill;
- preserve severity and evidence semantics across patch releases;
- update fixtures/tests when behavior changes;
- make mutating tool actions explicit and opt-in;
- install reviewed tags or immutable commits rather than arbitrary moving branches.

## Legacy template content

The root `AGENT.md` came from the older Permaculture Design Agent Core template. It is retained as source material, but it is **not** the canonical repository instruction file and is **not** used by the web security/quality audit. Future work can decompose that large prompt into smaller domain skills under `skills/`.
