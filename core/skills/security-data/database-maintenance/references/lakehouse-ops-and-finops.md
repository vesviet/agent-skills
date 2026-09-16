# Lakehouse Storage Operations & Data FinOps — Reference

This reference details procedures, SQL runbooks, and policies for maintaining Apache Iceberg and Delta Lake storage layers, expiring historical metadata snapshots, merging Deletion Vectors, and enforcing Data FinOps query cost guardrails.

---

## 1. Apache Iceberg & Delta Lakehouse Compaction

High-frequency streaming microbatches and frequent write operations inevitably cause the "small files problem," where thousands of sub-10 MB Parquet files degrade query planning speed and inflate cloud object storage GET/LIST costs.

### 1.1 Bin-Pack Compaction Procedure & Deletion Vector Resolution
Target file sizes must be maintained between **128 MB and 512 MB** (default standard: **256 MB**) using bin-pack rewriting. In Apache Iceberg v3, bin-pack compaction automatically resolves and merges active **Deletion Vectors** (Puffin RoaringBitmaps) into newly rewritten base Parquet data blocks, eliminating read amplification:

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
Failed writes, aborted transactions, and dangling commits leave unreferenced Parquet and metadata files in object storage. Purge orphaned files safely using a strict **72-hour safety grace window** (`INTERVAL '72' HOUR`) to safeguard in-flight concurrent writes:

```sql
-- Remove unreferenced files older than 72 hours
CALL system.remove_orphan_files(
    table => 'lakehouse.silver.orders',
    older_than => CURRENT_TIMESTAMP() - INTERVAL '72' HOUR
);
```

---

## 2. Snapshot Expiration & Metadata Lifecycle

Unmanaged Iceberg snapshots cause metadata tree explosion, increasing query planning time from milliseconds to seconds.

### 2.1 7-Day TTL Snapshot Retention Policy
- Maintain time-travel capability for a maximum of 7 days in production.
- Retain a minimum safety floor of **50 recent snapshots** (`retain_last => 50`) regardless of age to protect rollback capability and ongoing downstream batch pipelines.

```sql
-- Expire stale snapshots past 7-day retention window while preserving 50-snapshot floor
CALL system.expire_snapshots(
    table => 'lakehouse.silver.orders',
    older_than => CURRENT_TIMESTAMP() - INTERVAL '7' DAY,
    retain_last => 50
);
```

### 2.2 Manifest List Rewriting
Rewrite manifest files to eliminate micro-batch manifests and consolidate partition bounds:

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

### 3.2 Partition Evolution & S3 Object Storage Prefix Hashing
Apache Iceberg supports metadata-only partition evolution (tracked by integer `spec-id`) without rewriting historical Parquet data. 

To eliminate AWS S3 `503 Slow Down` request throttling caused by high-throughput streaming writes to single directory prefixes, activate S3 prefix hashing:
```sql
ALTER TABLE lakehouse.silver.orders SET TBLPROPERTIES (
    'write.object-storage.enabled' = 'true',
    'write.data.path' = 's3://data-lake-bucket/tables/orders/data'
);
```

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

### 4.4 FinOps ROI Attribution & Resource Tagging
Quantify the return on investment of lakehouse table maintenance using standard FinOps equations:
1. **File Reduction Ratio**:
   $$\text{Reduction Ratio} = \frac{\text{Files}_{\text{before}} - \text{Files}_{\text{after}}}{\text{Files}_{\text{before}}}$$
2. **Storage Reclaimed (GB)**:
   $$\text{Storage Reclaimed (GB)} = \frac{\text{Bytes Reclaimed from Compaction and Vacuum}}{1024^3}$$
3. **Projected Monthly S3 API GET Request Savings**:
   $$\text{Monthly Requests Saved} = (\text{Files}_{\text{before}} - \text{Files}_{\text{after}}) \times \text{Estimated Monthly Queries}$$
   $$\text{Savings (USD)} = \left(\frac{\text{Monthly Requests Saved}}{1,000}\right) \times $0.0004$$
4. **Mandatory Tagging**:
   Tag all maintenance runs, runbooks, and audit events with metadata:
   - `CostCenter`: e.g. `data-platform-engineering`
   - `Environment`: `production` | `staging` | `development`
   - `TableOwner`: e.g. `analytics-engineering`
