---
name: analyze-data
description: Explore datasets, define metrics, run reproducible SQL or tabular analysis, and produce stakeholder-ready insights with documented assumptions and lineage. Use when answering business questions from data, comparing datasets, building KPI definitions, or drafting dashboard requirements without owning production pipeline infrastructure.
---

# Analyze Data

Use this skill for **analyst** work: questions, metrics, exploration, and reports — not for authoring production ETL platforms unless explicitly coordinated with the Data Engineer role.

## Core Rules

- treat source files and production tables as **read-only** unless the user explicitly approves writes
- define the **business question** and success criteria before querying
- document **metric definitions** (numerator, denominator, filters, grain, time zone)
- log **row counts** before and after every filter or join
- separate **facts** from **interpretation** in deliverables
- use parameterized queries and scripts — no hardcoded paths or credentials
- mask or aggregate **PII** in outputs unless clearance exists
- spot-check results against source samples before handoff
- escalate to Data Engineer when the task requires new pipelines, orchestration, or schema migrations

## When to Use

- stakeholders ask "what does the data show?" for a defined period or segment
- Excel/CSV imports need cleaning, comparison, or formatted reports
- KPIs, funnels, cohorts, or trend analysis must be defined or computed
- dashboard or chart requirements must be specified for engineering or BI tools
- data quality blocks a business decision and needs evidence documented
- ad-hoc SQL (DuckDB, warehouse read replicas) answers a scoped question

## Suggested Process

### 1. Frame The Question

Capture:

- business question and decision the output supports
- population, time range, and grain (daily, user, order, etc.)
- metrics and dimensions required
- acceptable latency (one-off vs recurring)

### 2. Locate And Profile Sources

- identify tables, files, or exports
- profile null rates, duplicates, key cardinality, encoding issues
- record lineage: who produced the source, when, and known limitations

### 3. Define Metrics

Write explicit definitions:

- formula, filters, exclusions, and edge cases
- how metrics relate to existing reports (avoid duplicate conflicting KPIs)

### 4. Analyze

- use SQL or tabular tools (pandas, DuckDB, Polars) with logged steps
- compare cohorts or periods with consistent keys
- sanity-check totals against control totals or prior reports

### 5. Deliver

Produce:

- `data-analysis-report.json` or markdown brief with findings
- optional Excel/HTML export for stakeholders
- open questions and data gaps

## Checklist

- [ ] business question and metric definitions are explicit
- [ ] sources and lineage documented
- [ ] row counts logged at key steps
- [ ] PII handled per policy
- [ ] facts vs interpretation separated
- [ ] results spot-checked against source
- [ ] pipeline or migration needs escalated to Data Engineer when applicable

## Related Skills

- **data-engineer**: Reusable ingest/compare/report scripts or Parquet/DuckDB setup when analysis needs engineered inputs
- **analyze-business-requirements**: Align metrics with business rules and actors
- **database-maintenance**: Read-only operational queries when appropriate
- **write-documentation**: Data dictionaries and metric catalogs
- **conduct-research**: External benchmarks or domain context when data alone is insufficient
