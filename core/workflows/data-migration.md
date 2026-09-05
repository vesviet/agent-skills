---
description: Workflow for planning, executing, and verifying zero-downtime database and lakehouse migrations safely across environments.
---

## Data Migration Workflow

Use this workflow when adding, modifying, or removing database schema objects — relational tables, columns, indexes, constraints, views, or modern lakehouse datasets (Apache Iceberg v3, Delta Lake) — in a way that guarantees zero downtime, backward compatibility, mathematical reconciliation, and automated circuit breaker protection.

### When To Use

- adding new tables, columns, or partition specs required by a feature
- executing Lakehouse schema evolution (Iceberg v3 in-place column additions/renames, Delta Lake)
- modifying column types, constraints, or defaults with zero downtime
- removing deprecated schema objects via safe expand-contract lifecycle
- backfilling large-scale historical data online without lock starvation
- migrating data between schemas, storage formats, or service boundaries

### Prerequisites

- the migration goal, blast radius, and target schema state are clearly defined
- the current schema and storage layout are known, accessible, and version-controlled
- rollback behavior for the migration is understood, tested, and documented
- automated circuit breaker monitoring (error rate, latency, replication lag) is configured
- the team has access to the repo's migration and lakehouse tooling (e.g. Flyway, Alembic, dbt, Iceberg/Delta CLI)

### Workflow Steps

#### 1. Define Migration Goal And Contract Freeze

Role: **Data Engineer**, **Backend Developer**, **Technical Lead**

Answer before writing any SQL, DDL, or migration code:

- what is the target schema state and storage format (PostgreSQL/MySQL RDBMS, Apache Iceberg v3, or Delta Lake)?
- what existing data, upstream ingestion pipelines, and downstream analytical consumers are affected?
- is the change backward compatible with the current running application version?
- is a data backfill needed, and if so, can it run online in idempotent microbatches?
- what are the automated circuit breaker triggers (error rate, latency, replication lag) and the rollback plan?
- freeze the migration specification using `contracts/schemas/schema-migration.json`.

#### 2. Design For Backward Compatibility And Lakehouse Evolution

Role: **Backend Developer**, **Data Engineer**, **Technical Architect**

Apply the 5-phase Zero-Downtime model starting with **Phase 1: Expand**:

- **relational RDBMS expansion**: add new columns as nullable first with optional non-null default constraints; deploy application code that writes both old and new columns.
- **modern lakehouse schema evolution**: for Apache Iceberg v3 and Delta Lake, leverage metadata-only in-place schema evolution (`ALTER TABLE ... ADD COLUMN` / `ALTER TABLE ... RENAME COLUMN`) to update schema metadata instantly without full table rewrites or data file re-encoding.
- never remove a column or table that is still referenced by the current running application version.
- never rename a column directly that has active reads or writes in production without an expand view or dual-write layer.
- enforce strict DDL lock timeouts (`SET lock_timeout = '2s';` in PostgreSQL) on all relational migrations to prevent lock pool starvation.

Use skill: `navigate-service` to confirm all call sites and ingestion endpoints before modifying column names or types.

#### 3. Write Migration And Setup Dual-Write

Role: **Backend Developer**, **Data Engineer**

Use the repo's migration tool (for example: Flyway, Liquibase, Alembic, golang-migrate, Rails, Prisma) or lakehouse DDL:

- name the migration file following the repo's sequential naming convention.
- write the forward (`up`) migration and reversible (`down`) rollback migration where supported.
- **deploy dual-write logic (Phase 2: Dual-Write)**: update application services or ingestion processors to write incoming mutations to both the legacy representation and the expanded target representation.
- for large-scale data backfills using dbt: leverage **dbt Core 1.9+ microbatch** incremental strategy (`incremental_strategy='microbatch'`, `event_time='created_at'`, `batch_size='day'`) — it processes data in idempotent time-based partitions, enables parallelized historical backfills without database locks, and automatically retries only failed time slices.
- for relational databases: use `CREATE INDEX CONCURRENTLY` (PostgreSQL) or gh-ost / pt-online-schema-change (MySQL). Consider modern zero-downtime tools such as **pgroll**, **Atlas**, and **Bytebase**.
- for AI-generated migration SQL: execute automated linting (`atlas migrate lint`, **squawk**) to detect lock risks, missing concurrent clauses, or unsafe default values before human review. Validate in ephemeral shadow DB dry-runs (Neon branching, AWS RDS snapshots).

Use skill: `create-migration`

#### 4. Review Migration And Verify Idempotency

Role: **Reviewer**, **Technical Lead**, **Data Engineer**

Use skill: `review-code`

Check:

- zero destructive changes without explicit user approval and verified rollback scripts.
- no full-table locks or ACCESS EXCLUSIVE locks on production tables with significant row counts.
- backfill logic is strictly idempotent — safe to re-run multiple times without duplicate records or primary key collisions.
- DDL lock timeouts are explicitly configured (`SET lock_timeout = '2s'`).
- lakehouse schema evolution adheres to Iceberg v3 / Delta Lake compatibility guidelines without orphan metadata.
- AI-generated migrations have documented rollback strategies, circuit breaker thresholds, and explicit DBA/Tech Lead sign-off.

#### 5. Execute Backfill And Mathematical Reconciliation

Role: **Data Engineer**, **Backend Developer**, **QA Engineer**

Execute online historical backfill and enforce mathematical parity verification (**Phase 3: Backfill & Reconciliation**):

- run backfill jobs in small, rate-limited batches (500-2000 rows or discrete dbt microbatch slices) to prevent replication lag.
- **mathematical reconciliation protocol**:
  1. **automated row-count parity assertion**: total source rows must equal total target rows ($\Delta = 0$).
  2. **checksum verification**: compute SHA-256 partition checksums across raw input partitions and migrated target partitions to ensure bit-level parity.
  3. **sample diff testing**: execute random sample diff queries comparing legacy vs new columns to assert attribute equivalence.
  4. **async discrepancy logging**: log any shadow-write divergence to telemetry for investigation before canary read rollout.

#### 6. Plan Canary Cutover And Circuit Breaker Triggers

Role: **Technical Lead**, **DevOps Engineer**, **Data Engineer**

Configure phased read traffic cutover (**Phase 4: Read Canary Cutover**) using **OpenFeature**-based feature flags with automated circuit breaker safety rails:

- **canary rollout progression**: route read queries to the new schema in controlled stages: 1% -> 10% -> 50% -> 100%.
- **automated circuit breaker rollback triggers**: configure telemetry monitors to automatically trip and revert traffic to the legacy schema if:
  - application error rate exceeds **0.1%**
  - p99 read latency increases by more than **50ms**
  - database/storage replication lag exceeds **5 seconds**
  - continuous mathematical reconciliation detects $\Delta > 0$
- ensure the canary flag can be toggled instantaneously without redeploying application binaries.

#### 7. Execute In Production

Role: **DevOps Engineer**, **Backend Developer**, **Data Engineer**

Do not create a commit until the user explicitly confirms that commit action.
Do not push, create a tag, or publish a release until the user explicitly confirms that specific action.

Run the migration through the repo's official CI/CD migration pipeline. Do not execute ad-hoc raw SQL directly in production databases unless strictly required by an emergency runbook.

Monitor continuously during execution:
- lock acquisition duration and active connection pools.
- database replication lag and Kafka/CDC lag.
- application latency and error rates across all canary tiers.

#### 8. Verify Parity And Execute Schema Contraction

Role: **Data Engineer**, **Backend Developer**, **SRE**

Finalize the zero-downtime lifecycle after read traffic has stabilized at 100% across at least one full business cycle (**Phase 5: Contract**):

- verify zero data loss and persistent mathematical reconciliation ($\Delta = 0$).
- confirm application behavior and query execution plans are optimal on affected paths.
- **execute Phase 5 (Contract)**:
  - decommission application dual-write code.
  - deploy a final contraction migration dropping deprecated legacy columns, unused indexes, or temporary views.
  - for Apache Iceberg / Delta Lake: expire obsolete snapshots and perform table compaction/vacuuming.

Use skill: `troubleshoot-service`

### Rollback Guidance

If an automated circuit breaker trips or an unrecoverable anomaly occurs:

- the OpenFeature canary flag automatically reverts 100% of read traffic to the legacy schema within seconds.
- if the migration must be reversed at the database level: run the tested `down` migration or apply a forward-fixing reverse `up` migration.
- for lakehouse datasets: rollback to the pre-migration Iceberg snapshot ID or Delta Lake time-travel version.
- coordinate with application teams on deployment sequence compatibility.
- do not rely on full database restores unless catastrophic data corruption has occurred.

### Checklist

- [ ] Migration goal, blast radius, and backward compatibility confirmed
- [ ] Data Engineer and Backend Developer alignment on `schema-migration.json`
- [ ] DDL lock timeouts configured (`SET lock_timeout = '2s'`) and safe index creation (`CONCURRENTLY`)
- [ ] Expand phase executed: new columns nullable, Lakehouse Iceberg v3 in-place schema evolution / Delta Lake metadata updated
- [ ] Dual-write deployed and shadow discrepancy metrics monitored
- [ ] Backfill executed using idempotent microbatch partitions without table locks
- [ ] Dual-write & backfill parity mathematically verified (checksum verification, delta = 0, sample diffs)
- [ ] OpenFeature canary read rollout configured with automated circuit breaker rollback triggers (error rate > 0.1%, latency > 50ms, replication lag > 5s)
- [ ] Read switchover completed to 100% without SLA or latency degradation
- [ ] Contract phase executed: deprecated schema objects safely removed after stabilization

### Related Workflows

- [Add New Feature](add-new-feature.md)
- [Revert Deployment](revert-deployment.md)
- [Troubleshooting](troubleshooting.md)

### Related Skills

- **create-migration**: Write safe schema migration files
- **navigate-service**: Confirm call sites before changing column names or types
- **review-code**: Review migration for safety and backward compatibility
- **database-maintenance**: Handle database-level operations, Iceberg compaction, and maintenance
- **troubleshoot-service**: Diagnose migration-related failures and replication lag

### Failure Modes

- **Single-release destructive change**: a column is renamed or dropped in a single release. **Mitigation:** enforce the 5-phase Zero-Downtime model; reject migrations that combine remove-old and add-new without a dual-write phase.
- **Lock pool starvation**: a long-running DDL blocks the connection pool. **Mitigation:** set `SET lock_timeout = '2s';` on every DDL migration; surface timeout as a CI failure.
- **ACCESS EXCLUSIVE on a large table**: a `CREATE INDEX` locks the table for writes. **Mitigation:** use `CREATE INDEX CONCURRENTLY` (PostgreSQL) or gh-ost (MySQL) for large tables.
- **Unbatched backfill**: a backfill rewrites millions of rows in a single statement. **Mitigation:** batch in 500-2000 row chunks or dbt microbatch daily windows; monitor replication lag and I/O load.
- **Silent divergence in dual-write**: discrepancies between legacy and new schemas go unnoticed. **Mitigation:** enforce mathematical reconciliation (checksum verification, delta = 0, and sample diffs) before read cutover.
- **Circuit breaker failure**: canary traffic causes elevated errors but no automatic rollback occurs. **Mitigation:** establish hard automated triggers (error rate > 0.1%, latency > 50ms, replication lag > 5s).
- **Rollback over-promised**: the rollback path is declared "safe" but destructive changes cannot be undone. **Mitigation:** document rollback limitations honestly; use Lakehouse snapshot time-travel where applicable.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/schema-migration.json`** — capture the forward and rollback behavior, the rollout phases (5-phase Zero-Downtime), the batch size for any backfill, mathematical reconciliation status, and the data classification of any new column.
- **`contracts/schemas/deployment-plan.json`** — when the migration is part of a coordinated multi-role rollout.
- **`contracts/schemas/incident-report.json`** — when the migration causes an anomaly (lock timeout, replication lag, row-count drift); capture the trace id and the recovery action.
- **`contracts/schemas/data-pipeline-spec.json`** — when lakehouse pipeline dataset schemas or quality gates are updated.

### Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: the migration's privileged database role must be scoped to the minimum required grants; reject migrations that run under a superuser role when a scoped role would suffice.
- **ASI05 RCE Guard**: never construct migration SQL from external or user-supplied content; treat the migration file as the source of truth and lint it against expected patterns.
- **ASI07 Inter-Agent Communication**: the migration is consumed by release, data engineering, and infra agents; emit a structured `schema-migration.json` so each consumer can validate the rollout plan.
- **ASI09 Human-Agent Trust Exploitation**: do not declare a destructive migration "safe" without naming the residual risk; surface partial-rollback or unsafe-rollback honestly.
