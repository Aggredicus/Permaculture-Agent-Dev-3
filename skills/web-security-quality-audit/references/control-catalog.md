# Audit Control Catalog

Load only the sections relevant to the target.

## Governance and supply chain
- protected default branch and required checks;
- locked/reproducible dependency install;
- least-privilege CI permissions;
- immutable action/scanner pins where practical;
- full-history secret scan;
- blocking production advisory threshold plus visible full advisory output;
- coordinated major framework/toolchain upgrades;
- reviewed install scripts and deprecated/unmaintained packages;
- no forced dependency-resolution shortcuts.

## Server/browser security
- restrictive CSP or equivalent policy;
- nonce/hash control for executable inline script where used;
- framing/clickjacking protection;
- HSTS, MIME-sniffing, referrer, permissions, and opener policies;
- consistent hardening on success/error/HEAD/redirect responses where appropriate;
- no production stack-trace or framework leakage;
- fixed/allowlisted redirects and bounded user-controlled values;
- no unsafe HTML/script construction without explicit justification.

## Third-party and privacy boundaries
For each external script/frame/form/API:
- purpose and data sent;
- load timing;
- CSP/origin scope;
- referrer/query forwarding;
- fallback behavior;
- browser-exposed credentials/tokens;
- provider disclosure to users;
- failure behavior.

Privileged automation additionally needs consent/retention rules, least privilege, token storage/rotation, webhook verification, replay/idempotency protection, audit logging, approval boundaries, and a kill switch.

## Reliability/accessibility
- public routes and recovery paths work;
- essential actions retain fallbacks;
- semantic headings/landmarks;
- keyboard and visible focus;
- usable touch targets;
- meaningful alt/decorative semantics;
- reduced-motion support;
- accessible loading/error states;
- no horizontal overflow or obscured controls.

## Performance/maintainability
- bundles/assets proportionate to page function;
- heavy third-party code delayed when practical;
- cacheable/local assets where they materially simplify privacy/performance;
- shared business facts centralized;
- route/component responsibilities understandable;
- unnecessary framework/dependency layers removed;
- dead starter/configuration code removed;
- project contract/ontology updated when architecture changes.
