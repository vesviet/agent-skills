# Stack Conventions — Data Analyst (DuckDB, Metabase, BI)

Extends `core/roles/data-analyst.md` and `analyze-data` with toolchain-specific rules.

## Data Layout

Under `ANALYTICS_DATA_ROOT` (default `./data/analytics`):

```
analytics/
  raw/           # Immutable drops (gitignored)
  staging/       # Cleaned single-table files
  warehouse.duckdb
  queries/       # Saved .sql — one logical query per file
  exports/       # Dated Excel/CSV outputs (gitignored if sensitive)
  specs/         # Metabase and BI requirement markdown/JSON
```

- Never commit `raw/`, `exports/`, or `warehouse.duckdb` when they contain PII or production snapshots.
- Prefer Parquet over CSV for repeated analysis; document encoding for CSV (UTF-8 default).

## DuckDB Rules

- Open connections with explicit path: `DUCKDB_PATH` or in-memory only for tiny probes.
- Use parameterized views or documented filters — no string-concatenated user input in SQL files.
- Log row counts after each materializing step (`CREATE TABLE AS`, `INSERT`, major `WHERE`).
- Name saved queries `queries/<slug>.sql` with a header comment: purpose, grain, as-of date.
- Read from engineered paths produced by Data Engineer; do not invent production ingest jobs in analyst scope.

Example header:

```sql
-- purpose: weekly active users by segment
-- grain: user_id, week_start (ISO Monday)
-- as_of: 2026-05-22
```

## Metabase Rules (requirements only)

- Analyst delivers **specs** under `specs/metabase/<slug>.md` or structured JSON in the spec template.
- Do not assume Metabase admin API access unless the user explicitly grants it.
- Every card/question spec MUST list: data source (table/view), dimensions, measures, default filters, segment definitions, and refresh expectation.
- Link expected Metabase collection or dashboard name when known; use `METABASE_INSTANCE_URL` for human-readable references.

## Excel / BI Export Rules

- Filename pattern: `exports/YYYY-MM-DD_<slug>.xlsx` (or `.csv` when Excel is not required).
- Include a **Metrics** sheet or appendix with definitions copied from the analysis report.
- Separate **Facts** (computed values) from **Notes** (interpretation) on distinct sheets or sections.
- Mask or aggregate PII columns unless the user confirms clearance.

## Session Checklist (stack overlay)

1. Confirm `ANALYTICS_DATA_ROOT` and sources exist or request Data Engineer path.
2. Frame business question and metric definitions (see `metric-dashboard-templates.md`).
3. Run DuckDB analysis with logged steps and saved SQL under `queries/`.
4. Produce `data-analysis-report.json` when machine handoff is required.
5. Add Metabase or BI spec if dashboards are in scope.
6. Write dated export under `exports/` when stakeholders need spreadsheets.

## Escalation To Data Engineer

Escalate when any of the following apply:

- New recurring ingest, Airflow/dbt job, or Kafka/stream source is needed
- Schema migration or production table write is required
- DuckDB must be replaced by a shared warehouse with SLA and access control
- Source data is missing, corrupt, or stale and needs pipeline fix

Provide: business question, desired grain, sample row counts, failing query, and target table names.

## Anti-Patterns (stack)

- Embedding absolute machine-specific paths in committed SQL (use env or repo-relative roots)
- Building Metabase questions in prose without measure/filter definitions
- Shipping Excel without metric definitions or as-of date
- Using analyst session to author Airflow DAGs or production migrations
- Comparing two exports without documenting key normalization and timezone
