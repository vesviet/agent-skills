# Core Pack

This directory is the portable source of truth for the global engineering pack.

> **Core Catalog**: **35 Roles** | **126 Portable Core Skills** (across 19 categories) | **25 Workflows** | **54 Data Contract Schemas**  
> **Master Index & Discovery**: [`INDEX.md`](../INDEX.md) | **Machine Registry**: [`a2a/.well-known/role-skill-index.json`](a2a/.well-known/role-skill-index.json)  
> **Authoritative SOTA Audit**: [`reports/role-skill-matrix-sota-audit-2026-2027.md`](../reports/role-skill-matrix-sota-audit-2026-2027.md)

Everything in `core/` satisfies these invariants:

- no repo-specific absolute paths
- no brand-specific content assumptions
- no site-specific publish logic
- reusable across multiple repositories with local adaptation only
- 100% core skills owned by at least one Primary role

## Structure

- [rules](rules/README.md): global always-on engineering rules and code guidelines
- [roles](roles/README.md): 35 principal-level role definitions with 19 dedicated review checklists
- [skills](skills/README.md): 126 portable skills across 19 categories
- [workflows](workflows/README.md): 25 end-to-end multi-agent operating procedures
- [contracts](contracts/README.md): 54 JSON Schema Draft 2020-12 data contract specifications
- [policies](policies/README.md): machine-readable action boundaries and data classification
- [a2a](a2a/README.md): Agent-to-Agent 1.0 JSON-RPC/SSE protocol and agent registry
- [prompts](prompts/README.md): prompt engineering assets and PromptOps evals
- [scripts](scripts/README.md): 17 automated core validators and registry generators
- [config](config/README.md): optional environment helpers
- [adapter-parity](adapter-parity.md): multi-agent adapter parity tracking

Use `core/` when you want the generic engineering foundation without any org-local overlay.

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

Last updated: 2026-09-02
