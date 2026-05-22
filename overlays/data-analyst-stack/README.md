# Data Analyst Stack — DuckDB, Metabase, BI Overlay

Stack overlay for the `data-analyst` role. Extends `core/roles/data-analyst.md` with
conventions for local analytics (DuckDB), dashboard requirements (Metabase), and
generic BI chart specs — without replacing the portable core role.

This overlay applies when analysis work uses the **DuckDB + Metabase + spreadsheet/BI**
toolchain. It does NOT replace `core/roles/data-analyst.md`; it composes on top of it.

Pairs naturally with `overlays/data-engineer-rabity` when the same practitioner runs
engineered tables (engineer) and stakeholder reports (analyst) on shared DuckDB assets.

## Scope

- **Base role:** `core/roles/data-analyst.md`
- **Primary skill:** `analyze-data`
- **Default compute:** DuckDB (file-backed or in-memory)
- **Dashboard handoff:** Metabase question/card requirements (spec only — not prod admin)
- **Stakeholder exports:** Excel/CSV with dated filenames

## Stack Summary

| Layer | Tool | Analyst use |
| ----- | ---- | ------------- |
| Explore & SQL | DuckDB | Ad-hoc queries, profiling, metric SQL on Parquet/CSV |
| Orchestration of reads | `data-engineer` (core skill) | Load Parquet layers, refresh paths — escalate pipelines |
| Dashboards | Metabase | Requirements for questions, filters, segments, cards |
| Presentation | Excel / generic BI | Formatted exports; chart spec when Metabase is not used |

## Included

- `rules/stack-conventions.md` — Paths, env vars, SQL layout, export naming, PII
- `rules/metric-dashboard-templates.md` — Metric tables, Metabase spec template, JSON mapping

## Activation

When operating with this stack, load:

```
Role: data-analyst
Overlay: overlays/data-analyst-stack
```

The agent MUST apply stack conventions before writing SQL, specs, or exports.

## Environment Variables (recommended)

| Variable | Purpose | Example |
| -------- | ------- | --------- |
| `ANALYTICS_DATA_ROOT` | Root for inputs (CSV, Parquet) | `./data/analytics` |
| `DUCKDB_PATH` | File-backed DuckDB database | `./data/analytics/warehouse.duckdb` |
| `METABASE_INSTANCE_URL` | Base URL for linking specs (read-only) | `http://localhost:3000` |

If unset, default to `ANALYTICS_DATA_ROOT=./data/analytics` relative to the active repo.
