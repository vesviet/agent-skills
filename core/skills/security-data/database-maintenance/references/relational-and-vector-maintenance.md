# Relational & Vector Database Maintenance — Reference

This reference provides operational runbooks, index tuning protocols, lock contention guardrails, and zero-downtime upgrade procedures for relational (PostgreSQL) and vector (pgvector) database systems.

---

## 1. pgvector & Relational Index Tuning

High-throughput vector ingestion, embedding re-indexing, and bulk relational updates degrade query planner performance and cause severe B-tree and vector index bloat.

### 1.1 pgvector Index Maintenance (HNSW & IVFFlat)
Vector distance calculations (cosine, L2 distance) depend on balanced index graphs:
- **HNSW Rebuilds**: Hierarchical Navigable Small World graphs become fragmented after thousands of deletes or updates. Rebuild concurrently:
  ```sql
  -- Rebuild vector index concurrently to prevent table write locks
  REINDEX INDEX CONCURRENTLY idx_documents_embedding_hnsw;
  ```
- **IVFFlat Centroid Recalibration**: Inverted File Flat indexes require periodic reclustering to recompute optimal centroids when embedding distribution shifts:
  ```sql
  -- Drop and recreate IVFFlat concurrently or with low lock timeout
  REINDEX INDEX CONCURRENTLY idx_documents_embedding_ivfflat;
  ```

### 1.2 Bloat Detection & VACUUM ANALYZE
- **Bloat Measurement**: Monitor dead tuples and unvacuumed pages:
  ```sql
  SELECT
      relname AS table_name,
      n_dead_tup,
      n_live_tup,
      round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 2) AS dead_tuple_pct,
      last_vacuum,
      last_analyze
  FROM pg_stat_user_tables
  ORDER BY n_dead_tup DESC;
  ```
- **Optimizer Statistics Refresh**: Run `VACUUM ANALYZE` following bulk data loads to refresh histogram statistics, preventing poor join plan selection:
  ```sql
  VACUUM (ANALYZE, VERBOSE) core_entities;
  ```

---

## 2. Lock Contention Guardrails & Safe DDL Execution

Long-running maintenance operations (adding indexes, rebuilding tables, vacuum full) acquire table locks that can block incoming application connections and starve the connection pool.

### 2.1 Mandatory Lock Timeout Standard
Every maintenance script or operational transaction must explicitly configure a strict lock timeout:

```sql
-- Abort immediately if unable to acquire table lock within 2 seconds
SET lock_timeout = '2s';
SET statement_timeout = '300s';

-- Example: Add non-blocking foreign key constraint
ALTER TABLE orders
  ADD CONSTRAINT fk_orders_customer_id
  FOREIGN KEY (customer_id) REFERENCES customers(id) NOT VALID;

-- Validate constraint asynchronously without table locks
ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_customer_id;
```

### 2.2 Reindex Concurrently Rule
Never execute plain `REINDEX TABLE` or `REINDEX INDEX` in production environments. Always specify `REINDEX CONCURRENTLY` to allow read and write queries to proceed normally while the new index structure is built.

---

## 3. PostgreSQL 17 Zero-Downtime Upgrades

When executing major PostgreSQL version upgrades (e.g. Postgres 15/16 → Postgres 17):

### 3.1 Logical Replication via `pg_createsubscriber`
1. **Provision Target Node**: Deploy new PostgreSQL 17 replica matching existing cluster specifications.
2. **Convert to Subscriber**: Execute `pg_createsubscriber` to transform physical standby into logical subscriber:
   ```bash
   pg_createsubscriber -D /var/lib/postgresql/17/data -P "host=primary-db port=5432 user=replicator"
   ```
3. **Synchronize Sequences & DDL**: Manually replicate and apply DDL schema changes and advance sequence values.
4. **Traffic Cutover**: Switch application connection pools to PostgreSQL 17 target with sub-second downtime.
