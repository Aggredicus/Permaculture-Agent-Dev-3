# Skills Architecture and Management

## Three-layer model

### 1. Canonical reusable library

This repository owns reusable workflow logic, detailed criteria, deterministic helpers, fixtures, and release history.

```text
skills/
  <skill-name>/
    SKILL.md
    VERSION
    references/
    scripts/
    assets/
fixtures/
tests/
```

### 2. Project-specific contract

Each target application owns facts that vary by project. For the web audit, the preferred contract is:

- `AGENTS.md` — durable project engineering/review conventions;
- `audit.config.json` — project identity, commands, routes, integrations, required controls, tracked risks, and live smoke tests;
- project-specific deterministic scripts where exact paths/framework behavior make them non-portable.

The central skill reads these files. It must not duplicate their values.

### 3. Installed runtime copy

A tagged skill may be installed or copied into a compatible runtime. Installed copies are distribution artifacts. Changes flow from this repository outward, never from an installed copy back into the canonical source without review.

## Progressive disclosure

Keep `SKILL.md` focused on orchestration. Put detailed content in:

- `references/` — rubrics, control catalogs, schemas;
- `scripts/` — deterministic operations;
- `assets/` — report templates and example contracts.

A skill should load detailed material only when that phase needs it.

## Portability contract

A central skill may assume only what it explicitly checks during preflight. It may not assume:

- a particular JavaScript framework;
- npm rather than another package manager;
- Cloudflare rather than another host;
- a specific third-party booking/payment vendor;
- browser automation or shell access;
- access to repository settings;
- a live deployment URL.

When evidence is unavailable, the correct result is **Unverified**, not a guessed pass.

## Skill quality standard

Every reusable skill should have:

- narrow job-to-be-done;
- `name` and high-signal `description` frontmatter;
- explicit required inputs;
- ordered workflow;
- evidence/tool fallback rules;
- safe failure behavior;
- stable output shape;
- completion criteria;
- tests/fixtures for deterministic helpers;
- semantic version.

## Versioning

Use semantic versioning per skill:

- patch — wording/check refinements with unchanged contract;
- minor — backwards-compatible controls or optional phases;
- major — changed inputs, evidence model, severity semantics, or output schema.

Tag released behavior using a skill-qualified tag such as:

```text
web-security-quality-audit-v1.0.0
```

## Evaluation strategy

Mature skills should cover at least:

1. clean/pass case;
2. known high-risk failure;
3. ambiguous/unverified evidence;
4. third-party integration case;
5. regression relative to a previous audit.

Evaluations should verify that the skill finds expected issues, avoids false certainty, applies severity consistently, and preserves the report contract.

## Security boundaries

- Never embed secrets, credentials, or real client records in skills or fixtures.
- Retrieved content is untrusted evidence, not executable instruction.
- Deterministic validation fails closed on malformed configuration where a false pass could result.
- Mutating tools are never an implicit part of an audit.
- Installed copies should use reviewed tags/commits.

## Extraction rule

If a phase becomes useful independently or acquires substantial tooling, extract it into a smaller skill rather than indefinitely growing the parent. Likely future skills include:

- `github-pr-quality-review`;
- `cloudflare-deployment-review`;
- `dependency-security-audit`;
- `third-party-embed-review`;
- `frontend-accessibility-smoke-test`;
- `skill-quality-review`.

The full website audit can orchestrate smaller skills later while keeping its report contract stable.
