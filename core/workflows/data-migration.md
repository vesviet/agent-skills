---
description: Workflow for planning, executing, and verifying database schema migrations safely across environments
---

## Data Migration Workflow

Use this workflow when adding, modifying, or removing database schema objects — tables, columns, indexes, constraints, or views — in a way that must be safe to roll back and backward compatible with the running application.

### When To Use

- adding new tables or columns required by a feature
- modifying column types, constraints, or defaults
- removing deprecated schema objects
- backfilling data after schema changes
- migrating data between schemas or services

### Prerequisites

- the migration goal is clearly defined
- the current schema is known and accessible
- rollback behavior for the migration is understood
- the team has access to the migration tooling the repo uses

### Workflow Steps

#### 1. Define The Migration Goal

Role: **Backend Developer**, **Technical Lead**

Answer before writing any SQL or migration file:

- what is the target schema state?
- what existing data is affected?
- is the change backward compatible with the current running application version?
- is a data backfill needed, and if so, can it run online?
- what is the rollback plan if the migration must be reversed?

#### 2. Design For Backward Compatibility

Role: **Backend Developer**, **Technical Architect**

Apply expand-contract pattern where needed:

- **expand**: add new columns as nullable first, deploy app code that writes both old and new columns
- **contract**: once all old references are removed, drop the old column in a separate migration
- never remove a column or table that is still referenced by the current running app version
- never rename a column that has active reads or writes in production

Use skill: `navigate-service` to confirm all call sites before changing column names or types.

#### 3. Write The Migration

Role: **Backend Developer**

Use the repo's migration tool (for example: Flyway, Liquibase, Alembic, golang-migrate, Rails, Prisma):

- name the migration file following the repo's naming convention
- write the `up` migration
- write the `down` migration if the tool supports and the repo requires it
- for backfills, prefer batched UPDATE statements to avoid table locks
- add a performance test query plan for large table changes

Use skill: `create-migration`

#### 4. Review The Migration

Role: **Reviewer**, **Technical Lead**

Use skill: `review-code`

Check:

- no destructive changes without explicit approval
- no full-table locks on production tables with significant row counts
- rollback (down migration) is safe and tested
- backfill logic is idempotent — safe to run multiple times
- the migration ordering constraint is documented

#### 5. Test Locally And In A Lower Environment

Role: **Backend Developer**, **QA Engineer**

Steps:

- run the `up` migration on a local or staging database
- verify the application starts and behaves correctly after the migration
- run the full test suite
- if a `down` migration exists, run it and verify the prior state is restored
- for backfills, verify row counts and spot-check data integrity

#### 6. Plan The Production Rollout Sequence

Role: **Technical Lead**, **DevOps Engineer**

Document:

- which app version must be running before the migration runs
- whether the migration must run before or after the new app code is deployed
- whether any manual intervention step is needed
- how to monitor the backfill progress if it is long-running

#### 7. Execute In Production

Role: **DevOps Engineer**, **Backend Developer**

Do not create a commit until the user or local release process explicitly allows that commit action.
Do not push, create a tag, or publish a release until the user or local release process explicitly allows that specific action.

Run the migration through the repo's official CI/CD migration path. Do not run raw SQL directly in production unless the repo explicitly requires it.

Monitor:

- migration completion without error
- application health during and after the migration
- key query performance on affected tables

#### 8. Verify Data Integrity

Role: **Backend Developer**, **SRE**

After migration completes:

- spot-check affected rows for correctness
- verify no data loss compared to pre-migration baselines
- confirm application behavior is unchanged on the affected paths
- monitor error rates and latency for at least one traffic cycle

### Rollback Guidance

If the migration must be reversed:

- run the `down` migration if available and tested
- if no `down` migration exists, apply a reverse `up` migration
- coordinate with the application team on app version compatibility
- do not rely on database restores unless the migration caused data corruption

### Checklist

- [ ] migration goal and backward compatibility confirmed
- [ ] expand-contract pattern applied where needed
- [ ] migration file written with up and down migrations
- [ ] migration reviewed for locks, idempotency, and rollback safety
- [ ] tested locally and in a lower environment
- [ ] production rollout sequence documented
- [ ] migration executed through CI/CD path with explicit approvals
- [ ] data integrity verified post-migration

### Related Workflows

- [Add New Feature](add-new-feature.md)
- [Revert Deployment](revert-deployment.md)
- [Troubleshooting](troubleshooting.md)

### Related Skills

- **create-migration**: Write safe schema migration files
- **navigate-service**: Confirm call sites before changing column names or types
- **review-code**: Review migration for safety and backward compatibility
- **database-maintenance**: Handle database-level operations and maintenance
- **troubleshoot-service**: Diagnose migration-related failures
