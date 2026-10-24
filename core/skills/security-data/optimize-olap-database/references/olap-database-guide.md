# OLAP Database Architecture & Optimization Guide

This reference provides technical architecture specifications, DDL patterns, and query performance tuning runbooks for high-throughput columnar analytical databases (ClickHouse, DuckDB, Apache Iceberg v3).

---

## 1. Columnar Storage Architecture

Columnar database engines organize data on physical storage by column rather than row. This architecture provides three primary performance advantages:
1. **Extreme Compression Ratios**: Storing homogenous data types contiguously allows specialized compression algorithms (LZ4, ZSTD, Delta, DoubleDelta, Gorilla, T64) to achieve 5x–15x storage reduction.
2. **I/O Projection Minimization**: Queries touch only the columns explicitly requested in `SELECT` and `WHERE` clauses, skipping unreferenced attributes entirely.
3. **SIMD Vectorized Processing**: In-memory execution engines evaluate operations over contiguous vectors of primitives using hardware SIMD (AVX-512, ARM NEON) instructions.

### Comparative Architectural Matrix

| Dimension | ClickHouse (MergeTree) | DuckDB (v1.1+) | Apache Iceberg v3 |
| :--- | :--- | :--- | :--- |
| **Primary Deployment** | Distributed high-throughput cluster & embedded chDB | In-process embedded engine | Open lakehouse format on object storage (S3/GCS) |
| **Index Granularity** | 8,192 rows per granule (`index_granularity = 8192`) | 122,880 rows per standard Parquet Row Group | Manifest file file-level and column-level stats |
| **Sorting & Clustering** | `ORDER BY (col1, col2, ...)` defines disk order | Sorting during write / ART index | Sorted / Z-Ordered / Liquid clustered data files |
| **Partition Scheme** | `PARTITION BY expr` (coarse time windows) | Directory-based Hive partitioning | Hidden partition evolution (`spec_id`) |
| **Mutation Paradigm** | Immutable parts merged asynchronously | MVCC with undo logs, local ACID | RoaringBitmap Deletion Vectors (Puffin format) |
| **Target Workload** | High-concurrency analytics, real-time ingestion | In-process analytical pipelines, zero-copy joins | Lakehouse storage, multi-engine transactions |

---

## 2. Sparse Primary Index Mechanics & 8192-Row Granules

Relational databases employ dense B-Tree indexes that store a pointer for every single row. In petabyte-scale analytics, dense indexes exceed available RAM. ClickHouse instead implements a **sparse primary index**:

```
Data Parts on Disk (Physical Column Storage):
[Granule 0: Rows 0..8191] -> [Granule 1: Rows 8192..16383] -> [Granule 2: Rows 16384..24575]
           ^                               ^                                ^
           |                               |                                |
Marks (.mrk2): Offset in .bin           Offset in .bin                   Offset in .bin
           ^                               ^                                ^
           |                               |                                |
Primary Index (primary.idx in RAM):
[Mark 0: (tenant=1, date=2026-01-01)] -> [Mark 1: (tenant=1, date=2026-01-05)] -> [Mark 2: (tenant=2, date=2026-01-01)]
```

### Granule Indexing Lifecycle
1. **Granule Marks**: ClickHouse segments column data into granules of 8,192 rows (configurable via `index_granularity`). The primary index file (`primary.idx`) stores the primary key column values only for the *first row of each granule*.
2. **Marks File (`.mrk2`)**: Acts as a lookup table bridging the in-memory `primary.idx` to exact byte offsets (both compressed block offset and uncompressed intra-block offset) in column `.bin` files.
3. **Binary Search Pruning**: When executing a query with a filter matching the primary key prefix, ClickHouse performs binary search on `primary.idx` in RAM, identifies candidate granule ranges, and streams only matching granules from disk.

### Primary Key Ordering Rules
- **Cardinality Ascending Principle**: Sort keys must be ordered from **lowest cardinality to highest cardinality**:
  ```sql
  ORDER BY (tenant_id, event_date, event_type, user_id)
  ```
- **Prefix Pruning Invariant**: If a high-cardinality column (such as UUID or millisecond timestamp) is placed at the front of the sort key, subsequent columns cannot effectively prune granules because each granule will contain different prefix values.
- **Index Granularity Tuning**: While 8192 rows is optimal for 95% of workloads, small lookup tables may use smaller granules (`index_granularity = 1024`), while wide telemetry tables may use `index_granularity = 16384` to reduce marks overhead.

---

## 3. Partition Key Cardinality Governance

Partitions in MergeTree tables are physical filesystem directories that contain data parts.

### The "Too Many Parts" Failure Mode
When a table is partitioned on a high-cardinality key (e.g. `user_id` or `toYYYYMMDDhh(event_time)`):
1. Ingestion creates a separate part file in every active partition directory for each insert batch.
2. The number of unmerged parts explodes past system thresholds.
3. Background merge threads are overwhelmed, inode consumption exhausts OS limits, and ClickHouse rejects writes with:
   `DB::Exception: Too many parts in all data parts in table (N > 300)`.

### Partitioning Rules & Guardrails
- **Cardinality Ceiling**: Total active partitions across a table's lifecycle must remain **<= 1000** (ideally between 10 and 200).
- **Standard Temporal Pattern**: Always partition by month using coarse temporal expressions:
  ```sql
  PARTITION BY toYYYYMM(event_date)
  ```
- **Prohibited Partition Keys**: Never partition by user ID, device UUID, customer ID, or timestamps finer than a single day. For sub-daily slicing, rely on the sparse primary key `ORDER BY` clause.

---

## 4. Secondary Data Skipping Indexes

When queries frequently filter on columns that cannot be placed in the primary key prefix, secondary data skipping indexes allow ClickHouse to prune granules during execution:

```sql
CREATE TABLE access_logs (
    tenant_id UInt32,
    event_time DateTime64(3),
    event_date Date DEFAULT toDate(event_time),
    client_ip String,
    http_status UInt16,
    request_path String,
    bytes_sent UInt64,
    INDEX idx_status http_status TYPE minmax GRANULARITY 2,
    INDEX idx_ip client_ip TYPE set(500) GRANULARITY 1,
    INDEX idx_path request_path TYPE tokenbf_v1(30720, 2, 0) GRANULARITY 1
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_date)
ORDER BY (tenant_id, event_date, event_time);
```

### Skipping Index Types
1. **`minmax`**: Stores minimum and maximum values for a column across $N$ granules. Best for monotonically increasing or clustered numeric and timestamp columns.
2. **`set(max_rows)`**: Stores a set of unique column values across $N$ granules. If unique values exceed `max_rows`, it falls back to minmax. Ideal for low-to-medium cardinality categorical values (e.g., status codes, region codes).
3. **`bloom_filter([false_positive])`**: Evaluates Bloom filters for exact value matching. Highly effective for selective string searches.
4. **`tokenbf_v1(size, hash_functions, seed)`**: Tokenizes strings by whitespace and punctuation and indexes tokens in a Bloom filter. Optimized for URL paths, error messages, and SQL query logs.

---

## 5. Dictionary Acceleration & LowCardinality Encodings

### `LowCardinality(String)`
For string columns containing fewer than 10,000 distinct values, wrap the type as `LowCardinality(String)`. ClickHouse stores a localized dictionary of strings per part and references entries using compact integer positions (UInt8 or UInt16):
- Reduces on-disk storage by 60%–80%.
- Accelerates string equality comparisons to integer comparisons using SIMD vector instructions.

### Memory-Resident External Dictionaries
Distributed joins in OLAP databases incur massive network shuffle costs. ClickHouse overcomes this by caching dimension tables in memory-resident dictionaries:

```sql
CREATE DICTIONARY dim_organizations (
    org_id UInt64,
    org_name String,
    plan_tier LowCardinality(String),
    is_enterprise UInt8
)
PRIMARY KEY org_id
SOURCE(CLICKHOUSE(TABLE 'organizations_source'))
LIFETIME(MIN 300 MAX 600)
LAYOUT(HASHED());
```

### Querying with `dictGet`
Replace expensive hash joins with $O(1)$ dictionary lookups:

```sql
-- Join-free dimension enrichment
SELECT
    event_date,
    dictGet('dim_organizations', 'org_name', org_id) AS organization_name,
    count() AS total_events
FROM telemetry_events
WHERE event_date >= today() - 7
GROUP BY event_date, organization_name;
```

---

## 6. Streaming Micro-Batch Buffering Architecture

Every `INSERT` statement in ClickHouse writes an immutable part file to disk. High-frequency, single-row writes (100 inserts/sec) rapidly crash the merge scheduler. High-throughput ingestion requires micro-batch buffering.

### 6.1 Buffer Table Engine
The `Buffer` table engine accumulates write traffic in memory and flushes to an underlying MergeTree table when configured thresholds are reached:

```sql
-- Target table for durable storage
CREATE TABLE raw_events_sink (
    event_time DateTime64(3),
    tenant_id UInt32,
    payload String
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(toDate(event_time))
ORDER BY (tenant_id, event_time);

-- Buffer table for client writes
CREATE TABLE raw_events_buffer AS raw_events_sink
ENGINE = Buffer(
    currentDatabase(), raw_events_sink,
    16,   -- num_layers: parallel write buffers
    10,   -- min_time: flush if older than 10s and min thresholds met
    60,   -- max_time: force flush after 60s
    10000, -- min_rows: flush if >= 10,000 rows
    1000000, -- max_rows: force flush if >= 1,000,000 rows
    10485760, -- min_bytes: flush if >= 10MB
    104857600 -- max_bytes: force flush if >= 100MB
);
```

### 6.2 Kafka Engine + Materialized View Pipeline
For direct real-time ingestion from Apache Kafka, decouple consumption from storage using the Kafka table engine and an atomic Materialized View:

```sql
-- 1. Kafka consumer table (ephemeral stream)
CREATE TABLE kafka_telemetry_stream (
    event_time DateTime64(3),
    tenant_id UInt32,
    payload String
)
ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'telemetry-topic',
    kafka_group_name = 'ch_telemetry_group',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 2;

-- 2. Materialized view transforming and batching into target table
CREATE MATERIALIZED VIEW mv_telemetry_to_sink TO raw_events_sink AS
SELECT event_time, tenant_id, payload
FROM kafka_telemetry_stream;
```

---

## 7. Query Plan Profiling Runbook

Before deploying analytical queries to production dashboards or APIs, inspect the physical execution graph and index pruning efficiency:

### 7.1 `EXPLAIN ESTIMATE`
Quickly verify how many parts, marks, and rows ClickHouse will read before executing the query:
```sql
EXPLAIN ESTIMATE
SELECT count()
FROM telemetry_events
WHERE tenant_id = 42 AND event_date = '2026-09-18';
```
Output inspection:
- `parts`: Number of data parts selected (must be a small fraction of total parts).
- `rows`: Estimated row count to read.
- `marks`: Granules scanned (must verify that primary key pruning eliminates >80% of marks).

### 7.2 `EXPLAIN PIPELINE header=1`
Inspects multi-threaded pipeline execution, identifying pipeline stalls and concurrency bottlenecks:
```sql
EXPLAIN PIPELINE header=1
SELECT event_type, count()
FROM telemetry_events
WHERE tenant_id = 42
GROUP BY event_type;
```

### 7.3 `EXPLAIN PLAN indexes=1, actions=1`
Verifies whether primary keys and secondary skipping indexes were utilized:
- Look for `Selected Parts: X, Selected Marks: Y, Total Marks: Z`.
- High efficiency: `Selected Marks / Total Marks < 0.10` (90%+ marks pruned).

---

## 8. Specialized MergeTree Engines

### 8.1 `ReplacingMergeTree`
Deduplicates records sharing the same sorting key during background merges, retaining the row with the highest version (`ver`):
```sql
CREATE TABLE dimension_users (
    user_id UInt64,
    email String,
    tier LowCardinality(String),
    updated_at DateTime64(3)
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY user_id;
```

### 8.2 `SummingMergeTree`
Automatically aggregates numeric metrics across identical primary keys during background merges:
```sql
CREATE TABLE metric_hourly_rollups (
    metric_name LowCardinality(String),
    bucket_hour DateTime,
    total_count UInt64,
    error_count UInt64
)
ENGINE = SummingMergeTree((total_count, error_count))
ORDER BY (metric_name, bucket_hour);
```

### 8.3 `AggregatingMergeTree`
Stores intermediate aggregate states (`AggregateFunction`), enabling exact and approximate aggregations over billions of rows in milliseconds:
```sql
CREATE TABLE telemetry_aggregates (
    tenant_id UInt32,
    event_date Date,
    p95_latency AggregateFunction(quantile(0.95), Float64),
    unique_users AggregateFunction(uniq, UInt64)
)
ENGINE = AggregatingMergeTree()
ORDER BY (tenant_id, event_date);

-- Querying using combinators
SELECT
    tenant_id,
    event_date,
    quantileMerge(0.95)(p95_latency) AS latency_p95,
    uniqMerge(unique_users) AS total_active_users
FROM telemetry_aggregates
GROUP BY tenant_id, event_date;
```

---

## 9. Automated TTL Lifecycle & Tiered Storage Policies

Configure storage tiering and automatic partition purging directly in table DDL:

```sql
CREATE TABLE audit_telemetry (
    event_time DateTime64(3),
    event_date Date DEFAULT toDate(event_time),
    tenant_id UInt32,
    details String
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_date)
ORDER BY (tenant_id, event_date, event_time)
TTL event_date + INTERVAL 30 DAY TO VOLUME 's3_cold',
    event_date + INTERVAL 365 DAY DELETE;
```
- **NVMe to S3 Tiering**: Data older than 30 days is moved by background threads to cold S3 object storage without query interruption.
- **Automated Delete**: Partitions or rows older than 365 days are permanently dropped.

---

## 10. Document & Table Extraction Pipeline (Kreuzberg Pattern)

Unstructured operational documents (PDF/DOCX reports, regulatory filings) frequently contain tabular datasets required in OLAP systems.

### Extraction Architecture
1. **Kreuzberg Engine**: High-throughput parsing detects table boundaries, multi-line headers, and cell alignments.
2. **Schema & Contract Validation**: Extracted tabular structures are parsed into typed Apache Arrow RecordBatches and validated against Open Data Contract Standard (ODCS v3.1.0) definitions.
3. **Deterministic Natural Keys**: Rows are assigned deterministic SHA-256 composite identifiers:
   ```
   natural_key = SHA256(document_hash || '|' || table_index || '|' || row_index)
   ```
4. **Idempotent Ingestion**: Data is staged into Iceberg or ClickHouse `ReplacingMergeTree` tables using micro-batch buffers, guaranteeing zero duplicate entries upon pipeline retry.
