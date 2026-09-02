# Metric And Dashboard Templates — Data Analyst Stack

Copy-ready templates for metrics, Metabase handoff, and mapping to `data-analysis-report.json`.

## Metric Definition Table

Use in every analysis brief and Excel **Metrics** sheet:

| Metric | Definition | Numerator / Denominator | Filters | Grain | Time zone | Notes |
| ------ | ---------- | ----------------------- | ------- | ----- | --------- | ----- |
| Example: WAU | Distinct users with ≥1 qualifying event in ISO week | COUNT(DISTINCT user_id) / none | exclude test accounts | user_id, week_start | UTC+7 | Align with product analytics doc v2 |

## Metabase Question Spec Template

Save as `specs/metabase/<slug>.md`:

```markdown
# Metabase — <Title>

## Purpose
- Business question:
- Audience:
- Refresh: (e.g. daily 06:00 UTC+7)

## Data Source
- Database / schema:
- Table or view:
- Grain:
- Known limitations:

## Question Type
- (simple / native SQL / model)

## Dimensions
| Field | Type | Description |
| ----- | ---- | ----------- |

## Measures
| Measure | Aggregation | Definition |
| ------- | ----------- | ---------- |

## Filters (default)
- ...

## Segments
- ...

## Visualization
- Chart type:
- Sort / limit:
- Comparison period (if any):

## Acceptance
- [ ] Spot-check total matches DuckDB export for same filters
- [ ] PII columns hidden or aggregated
- [ ] Definition matches official metric catalog / BA ticket
```

## Generic BI Chart Spec (non-Metabase)

```markdown
# BI Chart — <Title>

- Chart type:
- X-axis / dimension:
- Y-axis / measure(s):
- Filters:
- Drill-down:
- Export schedule:
```

## Mapping To `data-analysis-report.json`

| Report section | JSON field |
| -------------- | ---------- |
| Business question | `business_question` |
| Metric table rows | `metrics[]` (`name`, `definition`, `value`, `grain`, `time_range`) |
| Source inventory | `sources[]` |
| Verified numbers / tables | `findings[]` |
| Narrative / options | `interpretation[]` |
| Profiling issues | `data_quality_issues[]` |
| Next steps | `recommendations[]` |
| High / Medium / Low | `confidence` |
| `exports/...`, `queries/...`, `specs/...` | `artifacts[]` |

## BA → Analyst Handoff Block

When Business Analyst delegates analysis, the brief SHOULD include:

```markdown
## Analytics Request (for Data Analyst)
- Decision supported:
- Questions (numbered):
- Proposed metrics (names only if undefined):
- Segments / actors:
- Time range and timezone:
- Sources known (paths, tables, exports):
- Constraints (PII, read-only, deadline):
- Out of scope for this analysis:
```

Analyst returns `data-analysis-report.json` plus optional Metabase spec and dated export.

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
  See `See `core/skills/foundation/analyze-data/SKILL.md` and the `data-analysis-report.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/foundation/analyze-data/SKILL.md` and the `data-analysis-report.json` schema.

Last updated: 2026-09-01
