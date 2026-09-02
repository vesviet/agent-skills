# Topic Board Template & Operations

The `task-planner` and `seo-analyst` must maintain a rolling 7-day topic board to manage the Dual-Site Sprint cadence.

## 1. 7-Day Rolling Board

The board dictates exactly what will be drafted, audited, and published over the next 7 days across the two sites.

**Mandatory Guardrails for the Board:**
- Exactly 1 post per day for `Lease in Vietnam`.
- Exactly 1 post per day for `Máy Lạnh Treo Tường`.
- Ensure no Search Intent is repeated within a 7-day window on the same site (Anti-Cannibalization check).

## 2. Template Structure (`plan-YYYY-MM-DD.md`)

When creating the weekly topic board, use the following structure for each entry to ensure all AEO/GEO and Topical rules are met:

```markdown
### [Date: YYYY-MM-DD] - [Site Name]

- **Target Keyword:** ...
- **Search Intent:** ...
- **Pillar / Cluster:** [Pillar Name] -> [Cluster Name]
- **GEO/AEO Requirement:** Ensure Answer-first intro. Specify exact data for Fact Density.
- **E-E-A-T Target:** Identify the Experience Proof to inject (e.g., "Personal visit to the showroom", "Reviewing our internal 2026 sales data").
- **Assigned Writer:** ...
- **Status:** [Planned / Briefed / Drafting / Auditing / Published]
```

## 3. Workflow Handoff

1. **`task-planner`** initializes the board and sets the dates/cadence.
2. **`seo-analyst`** fills in the Keywords, Intents, Pillar/Cluster, and E-E-A-T targets.
3. The brief is generated (`seo-content-brief.json`) and handed off to the **`content-writer`**.

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
  See `See `core/skills/content/optimize-seo/SKILL.md` and the `seo-weekly-board.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/content/optimize-seo/SKILL.md` and the `seo-weekly-board.json` schema.

Last updated: 2026-09-01
