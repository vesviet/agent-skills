---
name: database-maintenance
description: Plan and execute operational data store and modern lakehouse maintenance, including Apache Iceberg/Delta compaction, snapshot expiration, orphan vacuuming, clustering optimization, query cost monitoring/FinOps, and relational/vector DB index tuning. Use for cleanup, compaction, repair, and operational performance tasks.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, query_db, read_database, run_tests]
---

# Database Maintenance

Use this skill when planning or performing operational maintenance on relational databases, pgvector stores, or modern lakehouses to preserve health, query performance, and financial efficiency.

## When to Use

- compacting small files in Apache Iceberg or Delta Lake tables via bin-pack rewriting
- expiring stale lakehouse snapshots and vacuuming orphaned data files
- tuning multi-dimensional Z-Order clustering and partition pruning strategies
- monitoring analytical query costs, setting scan limits, and enforcing Data FinOps
- rebuilding fragmented B-tree, HNSW, or IVFFlat pgvector indexes
- executing zero-downtime database upgrades with `pg_createsubscriber`

## Core Rules

- understand operational goals and assess bloat metrics before executing maintenance
- favor non-blocking, concurrent operations: always use `REINDEX CONCURRENTLY` in relational stores
- enforce mandatory lock timeout: execute `SET lock_timeout = '2s';` on every maintenance DDL
- enforce a 7-day snapshot retention policy on Iceberg/Delta lakehouses to prevent catalog metadata bloat
- compact lakehouse Parquet files to 128 MB–512 MB target file sizes; vacuum unreferenced orphan files
- apply Data FinOps scan limits: auto-abort queries projecting >50 GB scans without partition filters
- refresh optimizer statistics with `VACUUM ANALYZE` following bulk data ingestion or vector updates
- utilize PostgreSQL 17 `pg_createsubscriber` for zero-downtime major version upgrades
- require an approved rollback and backup plan before initiating any destructive or compaction operation
- detailed SQL runbooks, procedures, and FinOps policies are maintained in [`references/lakehouse-ops-and-finops.md`](references/lakehouse-ops-and-finops.md) and [`references/relational-and-vector-maintenance.md`](references/relational-and-vector-maintenance.md)

## Suggested Process

### 1. Assess Store State & Bloat Metrics
Inspect table bloat, dead tuple ratios, fragmented vector index graphs, or lakehouse small file counts and snapshot ages.

### 2. Formulate Maintenance Window & Rollback Plan
Determine online concurrency feasibility. Establish maintenance windows, lock timeout thresholds, and rollback criteria.

### 3. Execute Compaction, Vacuum, or Index Rebuild
Run Iceberg bin-pack compaction (`rewrite_data_files`), expire stale snapshots, or rebuild pgvector indexes concurrently.

### 4. Enforce FinOps Controls & Pruning Rules
Verify warehouse auto-suspend timers (≤60s), query scan ceilings (50 GB), and partition clustering layouts.

### 5. Verify Health & Post-Maintenance SLA
Validate query latency improvements, verify optimizer statistics, and confirm table integrity before closing the window.

## Checklist

- [ ] maintenance goal and target system health indicators inspected before execution
- [ ] rollback plan and recovery posture verified before starting destructive or compaction steps
- [ ] `SET lock_timeout = '2s';` configured on all relational DDL operations to prevent connection pool starvation
- [ ] all relational and pgvector index maintenance executed with `CONCURRENTLY`
- [ ] `VACUUM ANALYZE` executed following bulk operations to update query planner statistics
- [ ] Apache Iceberg/Delta small files compacted to 128 MB–512 MB target sizes using bin-pack strategy
- [ ] stale snapshots older than 7 days expired and orphaned data files vacuumed
- [ ] Data FinOps scan limits (projected scan ≤ 50 GB) and warehouse auto-suspend (≤ 60s) enforced
- [ ] post-maintenance query benchmarks and table integrity verified against SLA targets
- [ ] deployment plan emitted and validated against `contracts/schemas/deployment-plan.json`

## Related Skills

- **create-migration**: Separate schema migrations from operational maintenance tasks
- **performance-profiling**: Measure query latencies, execution plans, and maintenance impact
- **troubleshoot-service**: Diagnose operational bottlenecks caused by index bloat or lock contention
- **review-service**: Review release and operational risks following data store maintenance
- **commit-code**: Safely commit updated maintenance runbooks and configuration scripts

## Output Contracts

When maintenance operations are coordinated with SRE, release managers, or audit agents, emit:

- `contracts/schemas/deployment-plan.json` — detailing maintenance window, target tables, execution steps, rollback procedure, and validation benchmarks.
- Markdown runbook summarizing executed maintenance SQL, pre/post latency metrics, and residual risks.

## Failure Modes

- **Exclusive lock starvation**: long-running maintenance blocks incoming application transactions. Mitigation: enforce `SET lock_timeout = '2s';` on every DDL.
- **Lakehouse metadata explosion**: unexpired snapshots slow query planning across all consumers. Mitigation: enforce automated 7-day TTL snapshot expiration.
- **Uncontrolled query scan costs**: unpartitioned queries scan entire lakehouse partitions. Mitigation: enforce 50 GB query scan ceilings and compute quota limits.
- **Corrupted snapshot cleanup**: aggressive vacuuming removes active time-travel references. Mitigation: maintain a minimum 10-snapshot retention safety floor.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: restrict maintenance roles to least-privilege operations; avoid superuser connections for routine index or compaction work.
- **ASI04 Supply Chain**: validate maintenance CLI tools, database extensions, and catalog drivers against approved manifests.
- **ASI05 RCE Guard**: parameterize all maintenance commands; never build dynamic SQL from untrusted inputs.
- **ASI07 Inter-Agent Communication**: emit structured `deployment-plan.json` so coordinating agents share identical execution parameters.
- **ASI09 Human-Agent Trust Exploitation**: surface rollback risks, expected lock impacts, and storage reclaimed honestly without omitting failure probabilities.
