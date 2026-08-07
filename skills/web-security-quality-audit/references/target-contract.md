# Target Project Contract

The audit skill can work without a contract, but a small project-owned contract makes runs faster and more consistent.

Preferred target files:
- `AGENTS.md` — durable engineering/review rules.
- `audit.config.json` — machine-readable project facts.
- optional project ontology — generated architectural index.
- optional project-specific deterministic audit script.

Useful `audit.config.json` fields:
- project name/repository/default branch/runtime/live URL;
- supported runtime/toolchain version;
- deterministic commands;
- public routes;
- required CI checks;
- required security headers;
- third-party integrations and allowed query/origin boundaries;
- tracked risk gates;
- live smoke tests;
- quality principles.

Rules:
1. Treat configuration as declared intent, not proof.
2. Verify configured controls against current source/CI/live behavior.
3. Project-specific URLs, issue numbers, provider accounts, and routes remain in the target repository.
4. Missing fields become Unverified/Not applicable as appropriate; do not invent values.
5. If an ontology exists, verify it is current before relying on it for navigation.
