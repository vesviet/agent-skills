---
name: database-maintenance
description: Plan or perform operational database maintenance by following the repo's safety, backup, rollback, and verification patterns. Use for cleanup, backfill, index work, repair tasks, restore preparation, or other operational data changes.
---

# Database Maintenance

Use this skill when a task is operationally focused on keeping a data store healthy, safe, or recoverable rather than just changing application schema.

## Core Rules

- understand the operational goal before running maintenance
- favor reversible or restartable actions where possible
- protect availability, integrity, and recovery first
- separate schema evolution from operational maintenance when that reduces risk
- verify outcomes with the smallest safe checks before declaring success
- Rebuild HNSW and IVFFlat pgvector indexes using `REINDEX INDEX CONCURRENTLY` after bulk embedding updates, monitoring index bloat and running `VACUUM ANALYZE`.
- Standardize on `REINDEX CONCURRENTLY` rather than plain `REINDEX` to avoid exclusive locks and keep tables accessible.
- Apply `pg_createsubscriber` in PostgreSQL 17 for zero-downtime upgrades, manually replicating and applying any DDL schema changes.

## Suggested Process

### 1. Define The Maintenance Goal

Clarify whether the task is mainly:

- cleanup
- backfill
- index or performance work
- repair or reconciliation
- backup or restore preparation
- retention or archival work

### 2. Inspect The Current State

Gather:

- affected database or storage system
- object size or data volume
- current health indicators
- maintenance windows or traffic sensitivity
- backup and restore posture

### 3. Plan The Safe Execution Path

Decide:

- what can run online versus needs a window
- whether batching or throttling is needed
- whether dry-run or preview is possible
- how progress and failure will be observed
- what the stop or rollback criteria are

### 4. Execute The Maintenance Carefully

Prefer:

- narrow scopes
- explicit ordering
- resumable steps
- progress checkpoints

Avoid large destructive operations without clear recovery steps.

### 5. Verify And Capture Follow-Up

Confirm:

- intended records or structures were updated
- performance and correctness did not regress
- backups or recovery assumptions still hold
- any deferred cleanup or monitoring follow-up is recorded

### 2026: Advanced PostgreSQL Indexing and Upgrades

- **pgvector Index Rebuilds**: Unlike B-Tree indexes, HNSW and IVFFlat pgvector indexes do not maintain optimal structure during incremental updates. Rebuild these indexes after bulk updates using `REINDEX INDEX CONCURRENTLY`. Run `VACUUM ANALYZE` to update statistical planners and monitor index bloat via `pg_stat_user_indexes`.
- **Zero-Downtime Major Upgrades (`pg_createsubscriber`)**: Utilize the PostgreSQL 17 `pg_createsubscriber` command-line utility to convert a physical standby server into a logical replica in-place. Note that logical replication does not replicate DDL; apply all schema modifications manually to the target subscriber.
- **Standardizing `REINDEX CONCURRENTLY`**: Never use the standard `REINDEX` command on production tables, as it acquires an exclusive table lock. Always use `REINDEX CONCURRENTLY` to rebuild indexes while allowing uninterrupted application read and write operations.

## Checklist

- [ ] maintenance goal defined
- [ ] current state inspected
- [ ] safe execution plan prepared
- [ ] backup or recovery posture verified before starting destructive steps
- [ ] recovery path understood
- [ ] maintenance executed with checkpoints
- [ ] post-maintenance verification completed
- [ ] pgvector indexes (HNSW/IVFFlat) are rebuilt via `REINDEX INDEX CONCURRENTLY` after bulk updates.
- [ ] `VACUUM ANALYZE` is run following bulk inserts to update optimizer statistics.
- [ ] Major database version upgrades use `pg_createsubscriber` with manual DDL replication.
- [ ] Index maintenance utilizes `CONCURRENTLY` to avoid exclusive locks.

## Related Skills

- **create-migration**: Handle schema-focused changes separately
- **performance-profiling**: Measure performance-sensitive maintenance impact
- **troubleshoot-service**: Investigate runtime issues caused by data problems
- **review-service**: Review release risk after operational data changes
- **commit-code**: Prepare any required source-of-truth updates for delivery
\n### 2026: PostgreSQL 17 and Vector Maintenance

- **pgvector index maintenance:** HNSW and IVFFlat indexes do NOT update incrementally on every insert. Rebuild indexes after bulk embedding updates (model change, dimension change) using `REINDEX INDEX CONCURRENTLY idx_embeddings`. Monitor index bloat with `pg_stat_user_indexes`. Run `VACUUM ANALYZE` after bulk inserts to ensure the query planner uses the index.
- **PostgreSQL 17 `pg_createsubscriber`:** Converts a physical standby to a logical replica subscriber in-place, enabling blue-green zero-downtime major version upgrades. Logical replication does NOT replicate DDL — apply schema changes to publisher and subscriber manually before cutover.
- **`REINDEX CONCURRENTLY` as default:** Use `REINDEX CONCURRENTLY` (not plain `REINDEX`) for all production index rebuilds. Plain `REINDEX` acquires an exclusive table lock that blocks all reads and writes. `CONCURRENTLY` allows normal table access throughout, with a small performance overhead.\n