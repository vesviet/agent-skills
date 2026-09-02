# Vesviet Content Overlay

This overlay contains content-specific extensions for the `vesviet` (Enterprise Technical Engineering) and `learn` (High-Quality Affiliate Marketing) Hugo sites.

## Included Components

### Rules
- `rules/content-brand.md`: Enforces schema completeness, GEO/AEO Answer-First block, 1,400+ word depth, and Affiliate Compliance.
- `rules/link-topology.md`: Defines the strict Hub-and-Spoke architecture, eliminating orphan pages.

### Workflows
- `workflows/content-audit-refresh.md`: The 4-sprint remediation workflow for `vesviet` (Schema Repair, Expansion, Topology, Consolidation).
- `workflows/affiliate-publishing.md`: Content production workflow for the `learn` affiliate site.

### Skills
- `skills/write-vesviet-learn-content`: Drafting skill ensuring compliance with both technical depth standards and affiliate trust requirements.

This overlay should be composed with the global core, not copied into the core pack.

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-09-01
