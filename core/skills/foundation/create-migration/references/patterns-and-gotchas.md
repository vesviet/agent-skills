# Create Migration — Reference

Deep material extracted from `SKILL.md` to keep the main file under 200 lines.
Load this file when designing a non-trivial migration, when reviewing
rollback safety, or when authoring a backfill.

## Safety Guidelines

- Prefer additive changes over destructive changes.
- Separate schema change from backfill when that reduces risk.
- Index columns that will be heavily queried after rollout.
- Avoid full-table rewrites in peak-risk paths when safer alternatives exist.
- Document assumptions for large datasets or long-running operations.

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
