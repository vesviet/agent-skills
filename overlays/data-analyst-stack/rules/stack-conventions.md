# Stack Conventions — Data Analyst (DuckDB, Metabase, BI)

Strict toolchain rules for the `data-analyst` role operating with DuckDB, Metabase, and Spreadsheet BI exports.

## 1. Data Layout & Workspace Hygiene

To keep the analytics environment uncluttered, all analysis must occur strictly within the `ANALYTICS_DATA_ROOT` (default `./data/analytics`).

```text
analytics/
  raw/           # Immutable raw drops (gitignored)
  staging/       # Cleaned intermediate files
  warehouse.duckdb # Local DuckDB instance
  queries/       # Saved SQL scripts (.sql)
  exports/       # Finalized Excel/CSV outputs (gitignored if sensitive)
  specs/         # Metabase requirement docs (markdown/JSON)
```

- **Saved SQL Rules:** All analytical queries must be saved as `.sql` files inside `queries/`. Do not run ephemeral queries without saving logic.
- **SQL Headers:** Every `.sql` file MUST begin with a header specifying: `purpose`, `grain`, and `as_of` date.
- **Data Privacy:** Absolutely NO Personally Identifiable Information (PII) is allowed to be committed to version control. PII must be aggregated, masked, or kept locally in gitignored folders.

## 2. DuckDB Execution Rules

- **Connections:** Open connections using an explicit file path (`DUCKDB_PATH`), or strictly in-memory for ephemeral probes.
- **Tracing:** Always log row counts after any materializing steps (`CREATE TABLE AS`, `INSERT`, major `WHERE`).
- **Boundaries:** Analysts read from paths engineered by the `data-engineer`. Analysts DO NOT invent production ingest pipelines.

## 3. Metabase Handoff Boundaries

- **No Admin Assumptions:** The Data Analyst does NOT create dashboards directly in the production Metabase instance unless explicitly granted admin access.
- **Specification Delivery:** The analyst delivers dashboard requirements purely as **Specs** (Markdown or JSON) stored in `specs/metabase/`.
- **Spec Requirements:** Every spec MUST strictly define: the source table/view, the exact `dimensions`, `measures`, default `filters`, `segment` logic, and `refresh` intervals.

## 4. Excel / BI Export Standards

- **Output Path:** All exports must be saved to `exports/` with the filename pattern: `YYYY-MM-DD_<slug>.xlsx` (or `.csv`).
- **Mandatory "Metrics" Sheet:** Every Excel export MUST include a dedicated "Metrics" sheet that clearly documents the definitions of the numbers presented.
- **Structure:** Separate **Facts** (computed data tables) from **Notes** (analyst interpretation/insights) on distinct sheets or distinct visual sections.
- **Anonymization:** Mask or aggregate all PII columns before export unless the user explicitly confirms clearance.

## 5. Escalation To Data Engineer

Escalate to a Data Engineer if:
- New recurring ingest pipelines (Airflow, dbt) are needed.
- DuckDB hits processing limits and needs replacement with a dedicated Cloud Data Warehouse.
- Source data is missing, corrupt, or stale.
