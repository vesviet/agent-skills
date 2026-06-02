---
name: build-data-pipeline
description: Design and implement data ingestion, transformation, and delivery pipelines including ETL/ELT, Parquet/DuckDB warehousing, dbt modeling, Airflow orchestration, Kafka streaming, and data quality gates. Use when the work requires a repeatable, owned pipeline — not a one-off analytical query.
---

# Build Data Pipeline

Use this skill when the task requires building or maintaining repeatable data infrastructure: ingestion pipelines, warehousing, transformation models, orchestration, streaming, or quality gates.

For one-off queries, comparisons, or stakeholder reports from existing tables, use `analyze-data` instead.

## When To Use

- importing data from files (Excel, CSV, JSON) or APIs into a clean, queryable format with idempotent runs
- building ETL or ELT pipelines from raw sources to a target warehouse or lakehouse
- converting flat files to Parquet and managing with DuckDB or Polars
- authoring Airflow DAGs to schedule and orchestrate pipeline steps
- modeling star schemas, Kimball dimensional models, or dbt projects
- building Kafka producers, consumers, or Faust stream processing
- designing Bronze → Silver → Gold Medallion architecture with Delta Lake or Iceberg
- implementing data quality gates with Great Expectations, Soda, or dbt tests
- generating formatted Excel or HTML reports as a scheduled or repeatable pipeline output

## Core Rules

- treat all source inputs as **read-only** — never modify source files
- cast columns to explicit types after cleaning; do not leave `dtype=str` as the final state
- use `utf-8-sig` encoding for CSV/Excel output to preserve non-ASCII characters
- log row counts **before and after every transformation** for traceability
- timestamp all report and export filenames — never silently overwrite
- parameterize all paths via config, argparse, or env vars — no hardcoded paths
- never place credentials in code; use `.env` or environment variables, never committed
- pipelines must be **idempotent** — running twice must not duplicate data
- mask or aggregate PII before any output or logging
- spot-check row counts and values against source before handoff

## Suggested Process

### 1. Clarify Pipeline Requirements

Answer before building:

- where are the source files and in what format?
- which sheets, partitions, or API endpoints to read?
- what column(s) form the unique key for matching or joining rows?
- what is the target: DuckDB, Parquet, dbt model, Kafka topic, Delta table, or Excel report?
- what output does the consumer need: cleaned data, diff, aggregation, or formatted report?
- what is the expected row count — and does it match after ingestion?

### 2. Set Up Working Structure

Follow the repo's existing layout or establish:

- `input/` — raw source files (read-only)
- `store/` — normalized Parquet or warehouse files
- `scripts/` — numbered pipeline scripts (01_ingest, 02_load, 03_aggregate, 04_report)
- `.env.example` — environment variable template (committed); `.env` in `.gitignore`

Pin all dependencies and document install requirements.

### 3. Implement Ingestion

- read source files with encoding fallback (utf-8 → cp1252 → iso-8859-1)
- strip and normalize column names
- log initial and post-cleaning row counts
- cast types explicitly after cleaning
- write to Parquet with `engine="pyarrow"` and a timestamp suffix when needed

### 4. Load And Model

- load Parquet into warehouse (DuckDB, BigQuery, Redshift) with `CREATE OR REPLACE` for idempotency
- log table row counts after load
- apply dbt models or aggregate queries in the correct dependency order

### 5. Implement Quality Gates

At each layer boundary:

- assert expected row count within tolerance
- check for null violations in required fields
- validate key uniqueness where required
- fail fast and surface errors — do not swallow exceptions silently

### 6. Deliver Output

- generate stakeholder reports with timestamps in filenames
- produce `data-pipeline-spec.json` or equivalent contract when machine handoff is required
- update docs or README with pipeline freshness, ownership, and re-run instructions

## Common Pitfalls

- comparing floats read as strings causes false positives — normalize before diff
- Excel date serial numbers need explicit conversion with a known epoch
- large files (>100 MB) need chunked reading or Polars/DuckDB instead of pandas
- old `.xls` format requires `xlrd`, not `openpyxl`
- files open in Excel on Windows cause permission errors during read
- `dtype=str` for the entire DataFrame blocks all downstream numeric aggregation
- swallowing exceptions with bare `continue` hides failures — always log and count

## Checklist

- [ ] source files treated as read-only
- [ ] `.env.example` committed; real `.env` in `.gitignore`
- [ ] dependencies pinned in `requirements.txt` or equivalent
- [ ] ingestion logs row counts at each step
- [ ] column types explicitly cast after cleaning
- [ ] cleaned data saved as Parquet (not raw CSV) when intermediate storage used
- [ ] pipeline runs idempotently — re-run produces same result
- [ ] quality gates assert row counts and key integrity at layer boundaries
- [ ] output filenames include timestamps — no silent overwrites
- [ ] PII masked or aggregated before any report or log output
- [ ] results spot-checked against source before stakeholder delivery

## Related Skills

- **analyze-data**: One-off exploration, metrics, and reports without pipeline ownership
- **database-maintenance**: Operational changes to a running data store
- **create-migration**: Schema migrations for production databases
- **security-audit**: Review data handling for PII or sensitive exposure
- **write-documentation**: Document pipeline architecture and data dictionaries
- **review-code**: Review pipeline scripts for correctness, safety, and idempotency
- **commit-code**: Commit finalized pipeline scripts to version control
