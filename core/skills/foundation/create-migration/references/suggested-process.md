# Create Migration — Suggested Process (Reference)

Detailed migration workflow extracted from `SKILL.md` to keep the main file
under 200 lines. Load this file when writing a new migration, reviewing a
destructive change, or designing a backfill.

## Operating Assumptions

This skill is intentionally repo-agnostic.

- Do not assume a specific migration tool.
- Do not assume a specific database engine.
- Do not assume SQL files are the only migration format.
- Prefer the repo's existing naming, ordering, and rollback conventions.

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
