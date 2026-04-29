---
name: create-migration
description: Create safe schema or data migrations by following the repo's local migration tool, naming rules, rollout constraints, and rollback expectations. Use when adding, changing, backfilling, cleaning, or repairing persisted data structures.
---

# Create Migration

Use this skill when the user needs to add or review a database schema migration, backfill, or data repair step.

## Core Rules

- follow the repo's existing migration tool, naming, and ordering conventions
- prefer rollout-safe additive changes before destructive changes
- keep schema changes, backfills, and cleanup separate when that reduces risk
- make rollback behavior explicit when the repo supports rollback
- verify code and schema compatibility across staged deployment

## When to Use

- adding or changing tables, collections, or indexes
- adding, removing, or renaming fields or columns
- introducing constraints or defaults
- performing data backfills or cleanup
- preparing persistence changes for a feature rollout

## Operating Assumptions

This skill is intentionally repo-agnostic.

- do not assume a specific migration tool
- do not assume a specific database engine
- do not assume SQL files are the only migration format
- prefer the repo's existing naming, ordering, and rollback conventions

## First Questions To Answer

Before writing the migration, confirm:

1. What persistence system is being changed?
2. What tool or format does this repo use for migrations?
3. Is the change schema-only, data-only, or both?
4. Can the change be rolled out safely while old and new code coexist?
5. What is the rollback path if deployment must be reversed?

## Suggested Process

### Step 1: Inspect Existing Migrations

Find:

- migration location
- naming pattern
- sequencing or timestamp convention
- whether the repo separates schema changes from data backfills

Match the local pattern instead of inventing a new one.

### Step 2: Understand Current State

Review the latest relevant migrations and the current persistence model.

Check:

- current schema shape
- existing indexes and constraints
- data volume and table size if available
- current application assumptions in code

### Step 3: Design For Safe Rollout

Prefer migrations that are safe across staged rollout:

- additive changes before destructive ones
- nullable or defaulted fields before strict enforcement
- backfills before making new constraints mandatory
- separate risky index builds or long-running steps when needed

Avoid combining multiple high-risk changes in one migration unless the repo explicitly expects it.

### Step 4: Create The Migration

Use the repo's official mechanism, such as:

- migration generator command
- hand-written migration file
- framework migration scaffold

Follow local naming rules and keep the description precise.

### Step 5: Write Forward And Rollback Logic

The migration should make both directions explicit whenever the repo supports rollback.

Forward logic should:

- make the intended shape change
- preserve data safety
- avoid unnecessary locking or long blocking operations

Rollback logic should:

- reverse the change cleanly when practical
- document when reversal is partial or unsafe
- avoid pretending a destructive data change is fully reversible when it is not

### Step 6: Update The Code That Depends On The Schema

After the migration, update the repo-local persistence code as needed:

- models or entity mappings
- repositories or query layers
- validation or serialization logic
- feature flags or compatibility shims

Do not assume paths like `internal/data/model` or any specific layer names. Follow the local structure.

### Step 7: Verify Locally

Run the repo's normal validation flow:

- apply the migration forward
- run the relevant tests
- build the affected service
- rollback if the repo expects rollback testing

If the migration is data-sensitive or long-running, also reason through:

- ordering during deploy
- idempotency expectations
- impact on replicas, readers, or older code

## Safety Guidelines

- prefer additive changes over destructive changes
- separate schema change from backfill when that reduces risk
- index columns that will be heavily queried after rollout
- avoid full-table rewrites in peak-risk paths when safer alternatives exist
- document assumptions for large datasets or long-running operations

## Common Migration Patterns

### Additive Schema Change

Best for:

- new table or collection
- new nullable field
- new field with safe default
- new index

### Expand And Contract

Best for:

- renaming fields
- changing types
- splitting one field into several
- removing old columns safely

Typical flow:

1. add new structure
2. dual-write or backfill
3. migrate reads
4. remove old structure later

### Data Backfill

Best for:

- normalizing old values
- populating new required fields
- repairing inconsistent records

Keep the backfill restartable and observable when possible.

## Common Gotchas

1. A migration that works on an empty database may still fail on real data.
2. Destructive changes often need a multi-step rollout, not a single migration.
3. Large index builds or constraint changes may need special handling in the local tool.
4. Code and schema must remain compatible during rollout, not just after rollout.
5. Rollback may be operationally different from logical reversal when data has already changed.

## What To Capture In Your Output

When reporting migration work, include:

- what changed
- why the change is needed
- rollout safety notes
- rollback notes
- any required follow-up in code or deployment order

## Checklist

- [ ] existing migration pattern inspected
- [ ] current schema or data state understood
- [ ] rollout safety considered
- [ ] forward migration written
- [ ] rollback path written or explicitly limited
- [ ] dependent code updated
- [ ] migration verified with repo-local commands
- [ ] release ordering or backfill notes captured

## Quick Reference

Use this for rapid migration creation:

- inspect existing migrations
- match naming and ordering
- design the safest rollout shape
- write forward and rollback steps
- update dependent code
- verify locally

## Related Skills

- **troubleshoot-service**: Debug migration failures and rollout issues
- **commit-code**: Prepare migration changes for delivery
- **review-code**: Review safety, compatibility, and rollback risk
- **write-tests**: Add regression coverage for schema-sensitive behavior
- **review-service**: Validate release readiness for persistence changes
