# Lakehouse Storage Operations & Data FinOps — Reference

This reference details procedures, SQL runbooks, and policies for maintaining Apache Iceberg and Delta Lake storage layers, expiring historical metadata snapshots, and enforcing Data FinOps query cost guardrails.

---

## 1. Apache Iceberg & Delta Lakehouse Compaction

High-frequency streaming microbatches and frequent write operations inevitably cause the "small files problem," where thousands of sub-10 MB Parquet files degrade query planning speed and inflate cloud object storage GET/LIST costs.

### 1.1 Bin-Pack Compaction Procedure
Target file sizes must be maintained between **128 MB and 512 MB** (default standard: 256 MB) using bin-pack rewriting:

```sql
-- Iceberg SQL Compaction via Spark/Trino/DuckDB Iceberg Catalog
CALL system.rewrite_data_files(
    table => 'lakehouse.silver.orders',
    strategy => 'binpack',
    options => map(
        'min-input-files', '5',
        'target-file-size-bytes', '268435456', -- 256 MB
        'max-file-group-size-bytes', '10737418240' -- 10 GB per batch
    )
);
```

### 1.2 Orphan File Vacuuming
Failed writes, aborted transactions, and dangling commits leave unreferenced Parquet and metadata files in object storage. Purge orphaned files safely using a 3-day or 7-day safety threshold:

```sql
-- Remove unreferenced files older than 3 days
CALL system.remove_orphan_files(
    table => 'lakehouse.silver.orders',
    older_than => CURRENT_TIMESTAMP() - INTERVAL '3' DAY
);
```

---

## 2. Snapshot Expiration & Metadata Lifecycle

Unmanaged Iceberg snapshots cause metadata tree explosion, increasing query planning time from milliseconds to seconds.

### 2.1 7-Day TTL Snapshot Retention Policy
- Maintain time-travel capability for a maximum of 7 days in production.
- Retain a minimum of 10 recent snapshots regardless of age to protect rollback capability.

```sql
-- Expire stale snapshots past 7-day retention window
CALL system.expire_snapshots(
    table => 'lakehouse.silver.orders',
    older_than => CURRENT_TIMESTAMP() - INTERVAL '7' DAY,
    retain_last => 10
);
```

### 2.2 Manifest List Rewriting
Rewrite manifest files to eliminate small manifests and consolidate partition bounds:

```sql
CALL system.rewrite_manifests('lakehouse.silver.orders');
```

---

## 3. Clustering & Partitioning Key Optimization

### 3.1 Z-Order Multi-Dimensional Clustering
For tables queried frequently across multiple high-cardinality dimensions (e.g. `customer_id` and `order_date`), apply Z-Ordering during maintenance cycles:

```sql
CALL system.rewrite_data_files(
    table => 'lakehouse.silver.orders',
    strategy => 'sort',
    sort_order => 'zorder(customer_id, status)'
);
```

### 3.2 Partition Evolution
Apache Iceberg supports metadata-only partition evolution (e.g. transitioning from daily to hourly partitioning, or changing partition columns) without rewriting historical Parquet data. Historical files maintain old partition specs, while new writes adopt the evolved spec.

---

## 4. Query Cost Monitoring & Data FinOps

Cloud analytical engines (Snowflake, BigQuery, Databricks, Trino) generate runaway costs when queries execute full-table scans over billions of unpartitioned rows.

### 4.1 Query Scan Limits & Circuit-Breakers
- **Maximum Scan Ceiling**: Configure warehouse resource groups to auto-abort any query projected to scan **> 50 GB** without specifying partition filters (`event_date` or `event_time`).
- **Query Timeout Limits**: Enforce hard execution timeouts:
  - Ad-hoc analyst exploration: 120 seconds maximum.
  - Scheduled batch transformation: 1800 seconds maximum.

### 4.2 Compute Warehouse Auto-Suspension
- Set auto-suspend timers to **≤ 60 seconds** on all virtual warehouse compute clusters.
- Enforce slot limits to prevent unmonitored horizontal auto-scaling beyond budget allocations.

### 4.3 Storage Lifecycle Tiering
Automate cloud object storage transitions based on access frequency:
1. **Hot Tier**: Active Bronze, Silver, and Gold tables accessed within 30 days.
2. **Infrequent Access (IA)**: Historical snapshots and partitions between 30 and 180 days.
3. **Archive / Glacier Deep**: Cold compliance archives (e.g. EU AI Act 10-year lineage data) older than 180 days.
