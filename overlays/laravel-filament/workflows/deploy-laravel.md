# Deploy Laravel (Filament Stack)

Role: `devops-engineer`

Deployment workflow for Laravel 11 + Filament v3 projects. Use after MR is merged and all tests pass locally.

## Checklist

- [ ] **Step 1** — Pre-flight checks
- [ ] **Step 2** — Pull latest code on server
- [ ] **Step 3** — Install / update dependencies
- [ ] **Step 4** — Run database migrations
- [ ] **Step 5** — Clear and rebuild caches
- [ ] **Step 6** — Restart queue workers
- [ ] **Step 7** — Verify deployment

---

## Step 1 — Pre-flight checks

Role: `devops-engineer`

Before deploying, confirm:

1. All tests pass: `php artisan test` (or `./vendor/bin/pest`).
2. Migration files reviewed — no destructive changes (DROP, TRUNCATE) without rollback plan.
3. `.env` on server has any new required variables from the release.
4. Queue jobs in-flight will tolerate a worker restart (idempotent jobs).

**Stop if any check fails.** Do not deploy with failing tests or unreviewed destructive migrations.

---

## Step 2 — Pull latest code on server

Role: `devops-engineer`

```bash
cd /var/www/<project>
git fetch origin
git pull origin main
```

Confirm the correct commit SHA is live: `git log --oneline -1`.

---

## Step 3 — Install / update dependencies

Role: `devops-engineer`

```bash
composer install --no-dev --optimize-autoloader
npm ci && npm run build   # only if assets changed
```

Use `--no-dev` in production. Never run `composer update` in production without a tested `composer.lock`.

---

## Step 4 — Run database migrations

Role: `devops-engineer`

```bash
php artisan migrate --force
```

`--force` bypasses the production confirmation prompt. Only run when migration has been reviewed.

For large tables: use `--pretend` first to preview SQL, then run batched with a maintenance window if needed.

---

## Step 5 — Clear and rebuild caches

Role: `devops-engineer`

```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan event:cache
php artisan filament:cache-components  # Filament v3 component cache
```

Run `php artisan optimize` as a shortcut when the above defaults are sufficient.

---

## Step 6 — Restart queue workers

Role: `devops-engineer`

```bash
php artisan queue:restart
```

This signals workers to gracefully finish their current job then exit. Supervisor restarts them automatically. Verify with:

```bash
sudo supervisorctl status
```

---

## Step 7 — Verify deployment

Role: `devops-engineer`

1. Open the application URL in a browser — confirm no 500 errors.
2. Log into Filament admin panel — confirm resources load.
3. Trigger a test job (if safe) to confirm queue workers are processing.
4. Check Laravel logs: `tail -50 storage/logs/laravel.log`.
5. Check Horizon dashboard (if enabled) for queue health.

**Rollback:** `git revert <commit>` + re-run steps 3–7 if a critical issue is found post-deploy.

### Failure Modes

- **Deploy with failing tests**: a release ships with red tests on the server. **Mitigation:** Step 1 (Pre-flight) requires passing tests; reject the deploy and surface the failure to the user.
- **Destructive migration without rollback**: a DROP or TRUNCATE ships without a verified rollback path. **Mitigation:** Step 1 requires a rollback plan for destructive migrations; reject the deploy when the plan is missing.
- **Missing env var on server**: a release introduces a new env var that is not set on production. **Mitigation:** Step 1 diffs `.env` against the new requirements; reject the deploy when a required env var is missing.
- **Worker restart loses in-flight jobs**: a non-idempotent job is restarted mid-execution. **Mitigation:** Step 1 requires in-flight jobs to tolerate the worker restart; reject non-idempotent jobs in the deploy window.
- **Cache stale after deploy**: a config or route cache is not rebuilt and serves old code. **Mitigation:** Step 5 clears and rebuilds every cache; reject the deploy when the cache step is skipped.
- **Verify step skipped**: a release is declared successful without an HTTP smoke test. **Mitigation:** Step 7 requires a browser check, an admin check, and a queue check; reject the deploy when any verify step is missing.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/deployment-plan.json`** — capture infrastructure changes, config updates, and the `validation_run` output proving the verify step passed.
- **`contracts/schemas/incident-report.json`** when the deploy triggers an anomaly; capture the trace id, the threshold, and the recommended action.
- For the Rollback branch, also emit `contracts/schemas/coordination-plan.json` when more than one service is affected by the revert.