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
