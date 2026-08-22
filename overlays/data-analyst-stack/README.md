# Data Analyst Stack — DuckDB, Metabase, BI Overlay

Stack overlay for the `data-analyst` role. Extends `core/roles/data-analyst.md` with conventions for local analytics (DuckDB), dashboard requirements (Metabase), and generic BI chart specs.

## Tech Stack (2026)

| Layer | Tool | Version | Notes |
|-------|------|---------|-------|
| Explore & SQL | DuckDB | Latest | File-backed or in-memory; Iceberg REST catalog support |
| Transformation | dbt Core | **1.9** | Microbatch incremental strategy, dbt Fusion engine |
| Lakehouse format | Apache Iceberg | — | Production standard for analytics at scale |
| Dashboards | Metabase | 1.x | Business KPIs for non-technical stakeholders |
| Infrastructure | Grafana | — | Service observability, time-series (NOT business KPIs) |
| Presentation | Excel/CSV | — | Dated exports with Metrics sheet |

## 2026 Key Updates

### dbt Core 1.9 — Microbatch Incremental Strategy
```yaml
# dbt_project.yml — microbatch for large Iceberg tables
models:
  my_model:
    materialized: incremental
    incremental_strategy: microbatch
    event_time: created_at
    batch_size: day
    begin: '2024-01-01'
```
Microbatch runs are **parallelizable** — critical performance win for large Iceberg tables.

### Apache Iceberg + DuckDB (Production Standard)
```python
# Production requirements for Iceberg:
# 1. Use Iceberg REST Catalog (not path-based scanning)
import duckdb
con = duckdb.connect()
con.execute("INSTALL iceberg; LOAD iceberg;")
con.execute("""
    CREATE SECRET iceberg_catalog (
        TYPE S3,
        REGION 'us-east-1',
        KEY_ID '...',
        SECRET '...'
    )
""")
# 2. Implement compaction + snapshot expiration + orphan file removal
# 3. Medallion architecture: Staging → Intermediate → Marts
```

### Metabase vs Grafana (Clear Separation)
| Tool | Use For |
|------|---------|
| **Metabase 1.x** | Business KPIs, non-technical users, SQL-based analytics |
| **Grafana** | Infrastructure metrics, time-series, Loki logs, operational observability |

Do NOT use Grafana for business dashboards — escalate to Metabase spec.

## Base Role & Scope

- **Base role:** `core/roles/data-analyst.md`
- **Primary skill:** `analyze-data`
- **Default compute:** DuckDB (file-backed or Iceberg-backed)
- **Dashboard handoff:** Metabase question/card requirements (spec only)
- **Stakeholder exports:** Excel/CSV with dated filenames

## Included

- `rules/stack-conventions.md` — Paths, env vars, SQL layout, export naming, PII
- `rules/metric-dashboard-templates.md` — Metric tables, Metabase spec template, JSON mapping

## Activation

```
Role: data-analyst
Overlay: overlays/data-analyst-stack
```

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `ANALYTICS_DATA_ROOT` | Root for inputs (CSV, Parquet) | `./data/analytics` |
| `DUCKDB_PATH` | File-backed DuckDB database | `./data/analytics/warehouse.duckdb` |
| `METABASE_INSTANCE_URL` | Base URL for linking specs (read-only) | `http://localhost:3000` |
| `DBT_PROFILES_DIR` | dbt profiles directory | `~/.dbt` |

Default: `ANALYTICS_DATA_ROOT=./data/analytics` relative to active repo.
