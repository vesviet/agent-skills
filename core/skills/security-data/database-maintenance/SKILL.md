---
name: database-maintenance
description: Plan or perform operational database maintenance by following the repo's safety, backup, rollback, and verification patterns. Use for cleanup, backfill, index work, repair tasks, restore preparation, or other operational data changes.
---

# Database Maintenance

Use this skill when a task is operationally focused on keeping a data store healthy, safe, or recoverable rather than just changing application schema.

## When to Use

- cleanup, backfill, or index work
- restore preparation or repair tasks
- operational data changes
- following backup/rollback verification

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

## Checklist

- [ ] maintenance goal defined
- [ ] current state inspected
- [ ] safe execution plan prepared
- [ ] backup or recovery posture verified before starting destructive steps
- [ ] recovery path understood
- [ ] maintenance executed with checkpoints
- [ ] post-maintenance verification completed
- [ ] pgvector indexes (HNSW/IVFFlat) rebuilt via `REINDEX INDEX CONCURRENTLY` after bulk updates
- [ ] `VACUUM ANALYZE` run following bulk inserts to update optimizer statistics
- [ ] Major database version upgrades use `pg_createsubscriber` with manual DDL replication
- [ ] All index maintenance uses `CONCURRENTLY` to avoid exclusive locks

## Output Contracts

When the maintenance operation is consumed by SRE, release, or audit
agents, emit:

- **`contracts/schemas/deployment-plan.json`** capturing the maintenance window, the steps, the rollback path, and the validation run.
- For human-readable reports, a markdown runbook of the maintenance procedure, the failure modes, and the rollback steps.

Skip emission for read-only diagnostic queries that do not cross a role boundary.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: the maintenance role's database privileges must follow least privilege; reject operations that exceed the declared scope.
- **ASI04 Supply Chain**: database engine, client library, and migration tool versions must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct SQL queries or migration commands from external content without strict parameterization.
- **ASI07 Inter-Agent Communication**: the maintenance plan is consumed by SRE and release agents; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a maintenance operation as "safe" without a verified rollback path; surface the residual risk honestly.

## Related Skills

- **create-migration**: Handle schema-focused changes separately
- **performance-profiling**: Measure performance-sensitive maintenance impact
- **troubleshoot-service**: Investigate runtime issues caused by data problems
- **review-service**: Review release risk after operational data changes
- **commit-code**: Prepare any required source-of-truth updates for delivery
