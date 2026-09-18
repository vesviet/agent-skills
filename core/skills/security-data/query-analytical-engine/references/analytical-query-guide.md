# Analytical Query Engine & Cross-Source Federation Guide

This reference provides technical architecture specifications, Python code patterns, and security guardrails for executing in-process analytical SQL (chDB, DuckDB v1.1+) and federating queries across disparate data sources without heavy ETL.

---

## 1. In-Process ClickHouse via `chDB`

`chDB` embeds the ClickHouse analytical C++ engine directly inside the host process (e.g. Python runtime). It operates without a standalone server daemon, network port, or distributed cluster.

### 1.1 Python API & Output Formats
`chDB` queries return data in zero-copy Arrow capsules, Pandas DataFrames, JSON, or CSV:

```python
import chdb

# Output formats: "Dataframe", "ArrowTable", "JSON", "CSV", "Debug"
sql = """
SELECT 
    event_type,
    count() AS total_events,
    quantileExact(0.95)(duration_ms) AS p95_latency
FROM s3('s3://analytics-lakehouse/events/2026/*.parquet', 'AWS_KEY', 'AWS_SECRET')
GROUP BY event_type
ORDER BY total_events DESC
LIMIT 10;
"""

df = chdb.query(sql, "Dataframe")
print(df)
```

### 1.2 ClickHouse Analytical Function Library
`chDB` exposes ClickHouse's complete analytical function suite:
- **Exact & Approximate Quantiles**: `quantileExact(0.95)`, `quantilesExactWeighted(0.5, 0.95, 0.99)`, `quantileTDigest`.
- **Higher-Order Array Functions**: `arrayMap(x -> x * 2, arr)`, `arrayFilter(x -> x > 0, arr)`.
- **JSON Traversal**: `JSONExtractString(raw_json, 'user', 'id')`, `JSONExtractInt(raw_json, 'metrics', 'count')`.
- **Bitwise & Cryptographic Primitives**: `bitAnd()`, `bitShiftLeft()`, `cityHash64()`, `sipHash64()`.

---

## 2. Stateful Multi-Step Pipelines via `chdb.session`

For complex exploratory analysis requiring intermediate staging tables, temporary views, and sequential transformations, `chdb.session.Session` maintains state across queries in an ephemeral in-process directory:

```python
import sys
from chdb import session

sess = session.Session()
try:
    # Step 1: Create session view reading remote S3 Parquet
    sess.query("""
        CREATE VIEW v_raw_telemetry AS
        SELECT 
            tenant_id,
            user_id,
            toDateTime(timestamp) AS ts,
            response_time_ms
        FROM s3('s3://lakehouse/telemetry/year=2026/*.parquet', 'ACCESS_KEY', 'SECRET_KEY')
        WHERE toDate(timestamp) >= today() - 14;
    """)

    # Step 2: Create memory-resident aggregation table within the session
    sess.query("""
        CREATE TABLE session_tenant_metrics ENGINE = Memory AS
        SELECT 
            tenant_id,
            count() AS request_count,
            quantileExact(0.99)(response_time_ms) AS p99_latency
        FROM v_raw_telemetry
        GROUP BY tenant_id;
    """)

    # Step 3: Run final analytical query joining session table
    result_df = sess.query("""
        SELECT 
            tenant_id,
            request_count,
            p99_latency
        FROM session_tenant_metrics
        WHERE request_count > 1000
        ORDER BY p99_latency DESC
        LIMIT 50;
    """, "Dataframe")

finally:
    # Always clean up temporary session directory to prevent disk leakage
    sess.cleanup()
```

---

## 3. DuckDB v1.1+ Vectorized Engine & Out-of-Core Execution

DuckDB is an embedded columnar OLAP engine designed for complex ANSI SQL, recursive CTEs, and deep integration with Apache Arrow and Parquet.

### 3.1 Memory Caps & NVMe Disk Spilling
To prevent queries from consuming unbounded RAM and triggering OS out-of-memory (OOM) kills, enforce memory limits and temporary disk spilling:

```python
import duckdb

con = duckdb.connect()

# Set memory limit and spill directory
con.execute("SET max_memory = '4GB';")
con.execute("SET temp_directory = '/tmp/duckdb_spill';")
con.execute("SET threads = 4;")
con.execute("SET preserve_insertion_order = false;")

# Execute out-of-core aggregation over a 50GB Parquet dataset
query = """
SELECT 
    customer_id,
    date_trunc('month', order_date) AS order_month,
    sum(order_total) AS monthly_spend,
    rank() OVER (PARTITION BY date_trunc('month', order_date) ORDER BY sum(order_total) DESC) AS rank_in_month
FROM read_parquet('s3://ecommerce-lakehouse/orders/*.parquet')
GROUP BY customer_id, order_month
QUALIFY rank_in_month <= 10;
"""

result = con.execute(query).arrow()
```

---

## 4. Zero-Copy Memory Interchange via Apache Arrow C Data Interface

Modern data pipelines avoid serializing data to disk or IPC sockets when passing tables between execution engines. The Apache Arrow C Data Interface provides a zero-copy protocol via C ABI structs (`ArrowArray` and `ArrowSchema`).

### Zero-Copy Pipeline Flow
```
[ chDB Query Engine ]
         |
    (PyCapsule: Arrow Stream)
         v
[ DuckDB Vectorized Engine ]  <-- Scans memory pointer directly
         |
    (PyCapsule: Arrow Table)
         v
[ Polars DataFrame ]          <-- Zero-copy memory view
```

### Python Implementation Pattern
```python
import chdb
import duckdb
import polars as pl

# 1. Query chDB returning an Apache Arrow Table
chdb_arrow = chdb.query("""
    SELECT tenant_id, avg(latency) AS avg_lat
    FROM s3('s3://bucket/metrics/*.parquet', 'KEY', 'SECRET')
    GROUP BY tenant_id
""", "ArrowTable")

# 2. Register chDB Arrow Table into DuckDB zero-copy
con = duckdb.connect()
con.register("chdb_metrics", chdb_arrow)

# 3. Perform ANSI SQL window operation in DuckDB
duck_arrow = con.execute("""
    SELECT 
        tenant_id, 
        avg_lat, 
        ntile(4) OVER (ORDER BY avg_lat) AS latency_quartile
    FROM chdb_metrics
""").arrow()

# 4. Zero-copy ingest into Polars for statistical analysis
polars_df = pl.from_arrow(duck_arrow)
print(polars_df)
```

---

## 5. Cross-Source Federation Without Heavy ETL

Embedded engines eliminate the need to schedule batch ETL pipelines when joining transactional databases with historical lakehouse object storage.

### ClickHouse / chDB Federation Example
```sql
SELECT 
    u.user_id,
    u.email,
    u.plan_tier,
    l.total_events,
    l.last_login_time
FROM postgresql('replica.db.internal:5432', 'prod_db', 'users', 'readonly_analyst', 'Secr3tToken') AS u
INNER JOIN (
    SELECT 
        user_id,
        count() AS total_events,
        max(event_time) AS last_login_time
    FROM s3('s3://data-lakehouse/user_activity/year=2026/*.parquet', 'ACCESS_KEY', 'SECRET_KEY')
    WHERE event_date >= today() - 30
    GROUP BY user_id
) AS l ON u.user_id = l.user_id
WHERE u.status = 'ACTIVE'
ORDER BY l.total_events DESC
LIMIT 500;
```

### Predicate Pushdown Invariants
1. **Push Down Filters Early**: Filter transactional tables inside the table function (`postgresql(...)`) rather than filtering after a full table scan.
2. **Subquery Projections**: Never `JOIN` against an unprojected `s3(...)` call. Always project only necessary columns within an inner subquery.

---

## 6. Kreuzberg Document & Table Extraction Pipeline

Unstructured documents (PDFs, Word documents, annual reports) contain valuable tabular data that must be ingested into analytical engines.

### 6.1 Extraction Mechanics
- **Kreuzberg Rust Parser**: Extracts structural layout, tables, and bounding boxes at high throughput.
- **Header & Merge Resolution**: Normalizes multi-level headers and merged cells into flat columnar schemas.
- **Contract Enforcement**: Output is validated against Open Data Contract Standard (ODCS v3.1.0) definitions before storage.

### 6.2 Ingestion Pattern
```python
import hashlib
import json

def generate_natural_key(doc_hash: str, table_idx: int, row_idx: int) -> str:
    """Generate deterministic composite natural key for extracted rows."""
    payload = f"{doc_hash}|{table_idx}|{row_idx}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def process_extracted_tables(tables: list[dict], doc_id: str):
    rows = []
    for t_idx, table in enumerate(tables):
        for r_idx, row in enumerate(table["rows"]):
            row_dict = {
                "natural_key": generate_natural_key(doc_id, t_idx, r_idx),
                "document_id": doc_id,
                "table_index": t_idx,
                "row_index": r_idx,
                "data": json.dumps(row)
            }
            rows.append(row_dict)
    return rows
```

---

## 7. Safe Read-Only Analytics & Connection Governance

### 7.1 Read-Only Connection Scoping
- **ClickHouse / chDB**: Set `SET readonly = 1;` on the connection to reject all DDL (`CREATE`, `DROP`, `ALTER`) and DML (`INSERT`, `UPDATE`, `DELETE`) operations.
- **PostgreSQL**: Always configure analytical sessions as read-only:
  ```sql
  SET TRANSACTION READ ONLY;
  SET statement_timeout = '30s';
  ```

### 7.2 Connection Pooling Sizing
Deploy connection poolers (PgBouncer, Supavisor) in **transaction pooling mode** for analytical workloads. Size pools using the standard formula:
$$N_{\text{pool}} = \min(2 \times \text{CPU Cores} + \text{Spindles}, \text{Max Backend Connections})$$

---

## 8. Production AST Query Validation Engine

Before executing any agent-generated or dynamic SQL string, validate the Abstract Syntax Tree (AST) using `sqlglot`:

```python
import sqlglot
from sqlglot import exp

def validate_and_clamp_analytical_query(sql_text: str, dialect: str = "clickhouse") -> str:
    """Validates SQL AST to guarantee safe, read-only analytical execution."""
    try:
        parsed = sqlglot.parse_one(sql_text, read=dialect)
    except Exception as e:
        raise ValueError(f"Invalid SQL syntax: {e}")

    # 1. Assert query is a SELECT or EXPLAIN statement
    if not isinstance(parsed, (exp.Select, exp.Explain)):
        raise ValueError("Security violation: Only SELECT or EXPLAIN statements are permitted.")

    # 2. Reject all mutating and administrative DDL/DML expressions
    forbidden_types = (
        exp.Insert, exp.Update, exp.Delete, exp.Create, exp.Drop,
        exp.Alter, exp.Command, exp.Truncate, exp.Transaction
    )
    if parsed.find(*forbidden_types):
        raise ValueError("Security violation: Mutating or DDL operations are strictly forbidden.")

    # 3. Limit Join Complexity (maximum 3 joins)
    joins = list(parsed.find_all(exp.Join))
    if len(joins) > 3:
        raise ValueError(f"Complexity violation: Query exceeds join depth limit of 3 (found {len(joins)}).")

    # 4. Enforce or clamp LIMIT clause <= 1000
    limit_node = parsed.find(exp.Limit)
    if not limit_node:
        parsed = parsed.limit(1000)
    else:
        try:
            limit_val = int(limit_node.expression.this)
            if limit_val > 1000:
                limit_node.expression.set("this", 1000)
        except (AttributeError, ValueError):
            limit_node.expression.set("this", 1000)

    return parsed.sql(dialect=dialect)
```

---

## 9. Query Timeout Governance & Circuit Breakers

To prevent runaway analytical queries or unindexed full table scans from blocking resources:
- ClickHouse / chDB:
  ```sql
  SET max_execution_time = 30;
  SET max_memory_usage = 4294967296; -- 4GB
  ```
- PostgreSQL:
  ```sql
  SET statement_timeout = '30s';
  SET idle_in_transaction_session_timeout = '10s';
  ```
- Circuit Breaker: If an exploratory query exceeds the 30-second execution budget, terminate the connection, log the query AST in `data-analysis-report.json`, and advise table partitioning or pre-aggregation.
