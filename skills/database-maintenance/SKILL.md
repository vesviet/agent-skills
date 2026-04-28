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
- [ ] recovery path understood
- [ ] maintenance executed with checkpoints
- [ ] post-maintenance verification completed

## Related Skills

- **create-migration**: Handle schema-focused changes separately
- **performance-profiling**: Measure performance-sensitive maintenance impact
- **troubleshoot-service**: Investigate runtime issues caused by data problems
- **review-service**: Review release risk after operational data changes
- **commit-code**: Prepare any required source-of-truth updates for delivery
