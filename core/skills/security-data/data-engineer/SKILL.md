---
name: data-engineer
description: >
  Full-lifecycle data engineering skill covering ingestion, cleaning, transformation, storage,
  orchestration, modeling, streaming, lakehouse, and observability. Use when any task involves
  reading raw data sources, building ETL/ELT pipelines, querying with DuckDB or Spark,
  modeling data warehouses, orchestrating with Airflow, processing Kafka streams, or
  generating stakeholder-ready reports and quality gates.
---

# Data Engineer

Use this skill for any task in the data engineering lifecycle: from reading raw Excel/CSV
files through to production-grade pipelines with Parquet, DuckDB, Airflow, dbt, Kafka,
Spark, Delta Lake, and observability tooling.

## When to Use

- importing data from Excel, CSV, JSON, or API sources into a clean queryable format
- comparing two datasets to find added, removed, or changed rows
- generating formatted Excel or HTML reports for stakeholders or audit
- building ETL or ELT pipelines from raw sources to a target warehouse or lakehouse
- converting CSV/Excel to Parquet and querying with DuckDB or Polars
- authoring Airflow DAGs to schedule and orchestrate pipeline steps
- modeling star schemas, Kimball dimensional models, or dbt projects
- building Kafka producers/consumers or Faust stream processing apps
- designing Bronze → Silver → Gold Medallion architecture with Delta Lake or Iceberg
- implementing data quality gates with Great Expectations, Soda, or dbt tests
- any task described as "so sánh data", "báo cáo", "pipeline", "ETL", "warehouse", or "streaming"

## Core Rules

- **Read-only inputs**: never modify source files; treat all inputs as immutable
- **Explicit types**: do not rely on `dtype=str` as final state — cast to correct types after cleaning
- **UTF-8-SIG output**: use `utf-8-sig` encoding for all CSV/Excel to preserve Vietnamese characters
- **Log row counts**: log counts before and after every transformation for full traceability
- **Timestamp outputs**: timestamp all report and export filenames — never silently overwrite
- **No hardcoded paths**: all paths must be parameterized via `argparse`, env vars, or config files
- **No credentials in code**: all secrets go to `.env` or environment variables, never committed
- **Idempotent pipelines**: running a pipeline twice must produce the same result, not duplicate data
- **PII masking**: do not print or log PII fields; mask or aggregate before any output
- **Validate before deliver**: spot-check row counts and values against source before handing off
- **Encoding fallbacks**: implement try/except with fallback encodings (cp1252, iso-8859-1) when reading
- **Strict output templates**: never drop requested columns; prompt user if data is missing

## First Questions To Answer

1. Where are the source files and what format are they in?
2. Which sheet(s) or partition(s) should be read?
3. What column(s) form the unique key for matching or joining rows?
4. What is the target: DuckDB, Parquet, dbt model, Kafka topic, Delta table, or Excel report?
5. What output does the user need: cleaned data, diff, aggregation, or formatted report?
6. What is the expected row count — does it match after ingestion?

## Suggested Process

### Step 1 — Set Up Working Directory

Standard layout for any data engineering project:

```
<project>/
├── input/          ← raw source files (read-only)
├── store/          ← normalized Parquet files
│   └── warehouse.duckdb  ← local DuckDB warehouse
├── reports/        ← generated Excel or HTML reports
├── scripts/        ← reusable Python pipeline scripts
│   ├── 01_ingest.py        ← Excel/CSV → Parquet
│   ├── 02_load_duckdb.py   ← Parquet → DuckDB tables
│   ├── 03_aggregate.py     ← DuckDB → aggregation queries
│   └── 04_report.py        ← aggregation → Excel/HTML BOD report
├── dags/           ← Airflow DAGs (Phase 5+)
├── dbt/            ← dbt project (Phase 6+)
├── quality/        ← Great Expectations suites (Phase 9+)
└── .env.example    ← environment variable template
```

Install required packages:

```bash
pip install pandas polars duckdb pyarrow openpyxl xlsxwriter python-dotenv
# Phase 3+:  pip install duckdb polars pyarrow
# Phase 5+:  pip install apache-airflow
# Phase 6+:  pip install dbt-core dbt-duckdb
# Phase 9+:  pip install great-expectations
```

### Step 2 — Ingest: Excel/CSV → Parquet

```python
# scripts/01_ingest.py
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import logging, os, argparse
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DTYPE_MAP = {
    # Override per column: {"col_name": "float64", "date_col": "datetime64[ns]"}
}

def ingest(input_path: Path, output_dir: Path, skiprows: int = 0):
    xl = pd.ExcelFile(input_path, engine="calamine")
    for sheet in xl.sheet_names:
        df = pd.read_excel(input_path, sheet_name=sheet, skiprows=skiprows, engine="calamine")
        initial = len(df)
        df = df.dropna(how="all")
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns.astype(str)]
        for col, dtype in DTYPE_MAP.items():
            if col in df.columns:
                df[col] = pd.to_datetime(df[col]) if "datetime" in dtype else df[col].astype(dtype)
        slug = sheet.strip().lower().replace(" ", "_")
        out = output_dir / f"{input_path.stem}_{slug}.parquet"
        df.to_parquet(out, index=False, engine="pyarrow")
        logging.info(f"{input_path.name} | {sheet} | rows: {initial} → {len(df)} | {out.name}")
```

### Step 3 — Load: Parquet → DuckDB

```python
# scripts/02_load_duckdb.py
import duckdb
from pathlib import Path

DB_PATH = "store/warehouse.duckdb"
STORE_DIR = Path("store")

con = duckdb.connect(DB_PATH)
for parquet_file in STORE_DIR.glob("*.parquet"):
    table = parquet_file.stem.replace("-", "_")
    con.execute(f"""
        CREATE OR REPLACE TABLE {table} AS
        SELECT * FROM read_parquet('{parquet_file}')
    """)
    count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"Loaded {table}: {count:,} rows")
con.close()
```

### Step 4 — Aggregate: DuckDB → Result Sets

```python
# scripts/03_aggregate.py
import duckdb, pandas as pd

con = duckdb.connect("store/warehouse.duckdb")

# Example: revenue by channel
revenue_by_channel = con.execute("""
    SELECT
        kenh_ban_hang,
        SUM(doanh_thu) AS tong_doanh_thu,
        COUNT(*) AS so_don
    FROM orders
    GROUP BY kenh_ban_hang
    ORDER BY tong_doanh_thu DESC
""").df()

con.close()
```

### Step 5 — Report: Aggregation → BOD Excel

```python
# scripts/04_report.py — professional formatted BOD report
import xlsxwriter, pandas as pd
from datetime import datetime

def write_sheet(wb, name: str, df: pd.DataFrame):
    ws = wb.add_worksheet(name)
    header_fmt = wb.add_format({
        "bold": True, "bg_color": "#1F3864", "font_color": "#FFFFFF",
        "border": 1, "align": "center", "valign": "vcenter"
    })
    data_fmt = wb.add_format({"border": 1, "valign": "vcenter"})
    currency_fmt = wb.add_format({"border": 1, "num_format": "#,##0 ₫"})

    for col_idx, col in enumerate(df.columns):
        ws.write(0, col_idx, col, header_fmt)
    for row_idx, row in df.iterrows():
        for col_idx, val in enumerate(row):
            fmt = currency_fmt if "doanh_thu" in df.columns[col_idx] else data_fmt
            ws.write(row_idx + 1, col_idx, val, fmt)
    ws.autofilter(0, 0, len(df), len(df.columns) - 1)
    ws.freeze_panes(1, 0)

ts = datetime.now().strftime("%Y%m%d_%H%M")
wb = xlsxwriter.Workbook(f"reports/BOD_Report_{ts}.xlsx")
# add sheets per aggregation result
wb.close()
```

### Step 6 — Verify And Hand Off

- Row counts at each stage are logged and match expectations
- Vietnamese characters render correctly in output Excel
- All requested sheets and columns are present
- BOD report opens without errors; stakeholder can understand without extra context

## Pipeline Architecture Reference

```
Excel files
    ↓  scripts/01_ingest.py
Raw Folder (store/*.parquet)
    ↓  scripts/02_load_duckdb.py
DuckDB warehouse (store/warehouse.duckdb)
    ↓  scripts/03_aggregate.py
Aggregation results (DataFrames)
    ↓  scripts/04_report.py
BOD Report (reports/BOD_Report_YYYYMMDD.xlsx)
```

Optionally orchestrated via Airflow DAG (Phase 5+) or dbt models (Phase 6+).

## Output Format

When presenting results always include:

- source files used and row counts at each stage
- schema of each loaded table (column names + inferred types)
- summary of aggregations computed
- path to generated report
- any data quality issues or type coercion warnings discovered

## Comparison Modes

| Mode        | When to use                             | What it produces                          |
| ----------- | --------------------------------------- | ----------------------------------------- |
| Row diff    | finding added or removed records        | list of keys only in one dataset          |
| Cell diff   | finding changed values in matching rows | key, column, old value, new value         |
| Summary     | quick overview                          | counts only                               |
| Full audit  | detailed stakeholder report             | all of the above in formatted Excel       |

## Report Formatting Standards

| Element       | Standard                                              |
| ------------- | ----------------------------------------------------- |
| Header        | bold, white on `#1F3864`, centered, bordered          |
| Data cells    | thin borders, text wrap, vertical center              |
| Numbers       | `#,##0` for integers, `#,##0.00` for decimals         |
| Currency      | `#,##0 ₫` for VND                                    |
| Changed cells | yellow background `#FFF2CC`                           |
| Error cells   | red background `#FFE0E0`                              |
| OK cells      | green background `#E2EFDA`                            |
| Column width  | auto-fit with max 50 chars                            |
| Freeze        | always freeze header row                              |
| Filter        | always enable auto-filter on all data sheets          |
| Summary sheet | metadata: source files, row counts, run timestamp     |

## Tool Stack By Phase

| Phase | Tools                                                     |
| ----- | --------------------------------------------------------- |
| 1     | PostgreSQL / DuckDB CLI, DBeaver                          |
| 2     | pandas, numpy, matplotlib, openpyxl, xlsxwriter           |
| 3     | DuckDB (Python), Polars, PyArrow, Parquet                 |
| 4     | Python ETL scripts, logging, dotenv, argparse             |
| 5     | Apache Airflow 2.x, Docker Compose, Astro CLI             |
| 6     | dbt Core, dbt-duckdb, star schema, Kimball modeling       |
| 7     | Apache Kafka, kafka-python, Faust, Schema Registry, Avro  |
| 8     | PySpark, Delta Lake, Apache Iceberg, MinIO, Medallion     |
| 9     | Great Expectations, Soda Core, dbt tests, alerting hooks  |
| 10+   | Full stack — portfolio projects combining all layers      |

## Common Pitfalls

- comparing floats read as strings causes false positives — normalize before diff
- Excel date serial numbers need explicit conversion with a known epoch
- large files (>100 MB) need chunked reading or Polars/DuckDB instead of pandas
- old `.xls` format requires `xlrd`, not `openpyxl`
- files open in Excel on Windows cause permission errors during read
- `dtype=str` for the entire DataFrame blocks all downstream numeric aggregation
- hardcoded `skiprows` by filename breaks when files are renamed — use config dict
- missing `logging` module means no timestamps or levels in pipeline output
- swallowing exceptions with bare `continue` hides failures — always log + count

## Checklist

- [ ] working directory structure created (`input/`, `store/`, `reports/`, `scripts/`)
- [ ] `.env.example` committed; `.env` in `.gitignore`
- [ ] required packages installed and pinned in `requirements.txt`
- [ ] source files placed in `input/` and treated as read-only
- [ ] `01_ingest.py` reads data with correct row counts logged
- [ ] column names cleaned; dtypes explicitly cast after cleaning
- [ ] cleaned data saved to `store/` as Parquet (not CSV)
- [ ] `02_load_duckdb.py` loads all Parquet files into named DuckDB tables
- [ ] `03_aggregate.py` produces correct aggregation results verified by spot-check
- [ ] `04_report.py` generates professional Excel with headers, borders, filters
- [ ] report filename includes timestamp; no silent overwrites
- [ ] Vietnamese characters display correctly in output
- [ ] all scripts are parameterized — no hardcoded paths or secrets
- [ ] all scripts run idempotently (safe to re-run)
- [ ] results verified against source data before stakeholder delivery

## Related Skills

- **database-maintenance**: Use when cleaned data needs to move into a production database
- **security-audit**: Review data handling for PII or sensitive content
- **write-documentation**: Document pipeline architecture and data dictionaries
- **review-code**: Review data processing scripts for correctness and safety
- **commit-code**: Commit finalized scripts to version control
