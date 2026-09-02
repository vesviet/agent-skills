# Site-Mix & Cannibalization Guardrails

Rules for ensuring topical authority growth without self-sabotage, tailored for the rolling 7-day topic board.

## 1. 7-Day Anti-Cannibalization Rule

To prevent self-cannibalization (competing with our own articles for the same search queries), the following guardrail is strictly enforced:
- **No Repeating Search Intent:** Do not publish more than one article targeting the exact same Search Intent on the same site within a 7-day window.
- **Example:** If a "Best Air Conditioners for Bedrooms" post is scheduled for Monday, do not schedule a "Top Bedroom AC Units" post for Thursday.

## 2. Pillar–Cluster Mapping

All content must belong to a predefined topical map. Random, disconnected topics are rejected.
- **Content Brief Requirement:** The `seo-analyst` MUST explicitly map every new article to a specific `Pillar` and `Cluster` within the `seo-content-brief.json`.
- **Internal Linking Enforcement:** The new cluster article must link back to its Pillar page, and the Pillar page should eventually link out to the cluster article.

## 3. Topical Authority Tracking

- Group topics to ensure we are covering the entirety of a domain (e.g., covering all aspects of "District 2 Living" or "Inverter Technology" before moving to a disjointed topic).

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
