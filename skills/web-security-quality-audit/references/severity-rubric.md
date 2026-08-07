# Severity and Evidence Rubric

Severity describes realistic impact and urgency, not fix difficulty.

- **Critical** — immediate severe compromise such as privileged RCE, active production-secret exposure, destructive unauthenticated writes, payment compromise, or confirmed large sensitive-data disclosure. Block release and contain immediately.
- **High** — realistically exploitable high-impact defect, privacy exposure, authorization failure, or reachable dangerous production dependency. Remediate before normal release.
- **Medium** — meaningful defense/privacy gap, vulnerable but currently unreachable production code, brittle third-party behavior, significant accessibility/reliability issue, or governance gap likely to create incidents. Track and remediate soon.
- **Low** — limited hardening, documentation drift, modest performance/maintainability problem, or low-impact governance improvement.
- **Informational** — observation, positive control, monitoring item, or opportunity without a demonstrated defect.

Evidence state is separate:
- **Verified pass** — demonstrated by current source, command output, CI, or live behavior.
- **Verified finding** — directly demonstrated problem.
- **Tracked risk** — unresolved and explicitly tracked; reconfirm the underlying condition.
- **Unverified** — evidence/tooling unavailable; state what would resolve it.

Rank remediation by realistic harm, likelihood/exploitability, breadth, whether it gates planned work, then simplicity/reversibility.
