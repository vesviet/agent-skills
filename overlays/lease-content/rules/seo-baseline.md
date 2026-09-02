# SEO and GEO Baseline Standards

This rule defines the mandatory baseline for Generative Engine Optimization (GEO) and traditional SEO for all new content in `leaseinvietnam` and `maylanhtreotuong`.

## 1. Content Depth and Scannability
- **Length**: Minimum 1,400+ words.
- **Structure**: Scannable structure with H2 sections and FAQ blocks when relevant.

## 2. Answer-First Format (GEO)
- **Direct Answer**: ≤60 words direct answer opening each H2.
- **Fluff Elimination**: No "hedge" words or long preambles. Dive straight into the core information.

## 3. Fact Density and E-E-A-T
- **Data Points**: Minimum 3 verifiable data points per 500 words.
- **Experience Proof**: Neighborhood guides need firsthand accounts or original photos. Price/market data needs documented research with sources.
- **Sources**: YMYL topics (legal, money) MUST cite official government sources.

## 4. Internal Linking
- **Quantity**: At least 3 internal links to relevant existing pages, plus at least 1 link to a property listing page when contextual (total minimum 4).
- **Target Link Flow**: Guide & Neighborhood Articles must actively link up to Property Listing Pages.

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
  See `See `core/skills/content/optimize-seo/SKILL.md` and the `seo-audit-report.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/content/optimize-seo/SKILL.md` and the `seo-audit-report.json` schema.

Last updated: 2026-09-01
