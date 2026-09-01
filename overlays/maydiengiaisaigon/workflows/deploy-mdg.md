# Deploy MDG (cPanel + Git)

Role: `devops-engineer`

Deployment workflow for the Máy Điện Giải Sài Gòn Laravel e-commerce. Uses cPanel Git Version Control or SSH pull model.

## Checklist

- [ ] **Step 1** — Pre-flight checks
- [ ] **Step 2** — Pull latest code via cPanel or SSH
- [ ] **Step 3** — Install / update dependencies
- [ ] **Step 4** — Run database migrations (PostgreSQL)
- [ ] **Step 5** — Clear and rebuild caches
- [ ] **Step 6** — Build frontend assets if changed
- [ ] **Step 7** — Verify deployment

---

## Step 1 — Pre-flight checks

Role: `devops-engineer`

1. Tests pass locally: `php artisan test` or `./vendor/bin/pest`.
2. `.env.production` on server has any new env vars from the release.
3. PostgreSQL migration reviewed — no destructive changes without rollback plan.
4. VietQR / payment integration env vars present if payment flow changed.

**Stop if any check fails.**

---

## Step 2 — Pull latest code

Role: `devops-engineer`

**Via cPanel Git Version Control:**
1. Log into cPanel → Git Version Control.
2. Select the repo → click **Update from Remote**.
3. Confirm HEAD SHA matches expected commit.

**Via SSH (if available):**
```bash
cd ~/public_html
git pull origin main
```

---

## Step 3 — Install / update dependencies

Role: `devops-engineer`

```bash
composer install --no-dev --optimize-autoloader
```

Do not run `composer update` in production. If `composer.lock` changed, review before deploying.

---

## Step 4 — Run database migrations (PostgreSQL)

Role: `devops-engineer`

```bash
php artisan migrate --force
```

For large product/order tables: run `--pretend` first, then use a maintenance window if the migration locks rows.

---

## Step 5 — Clear and rebuild caches

Role: `devops-engineer`

```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan event:cache
php artisan filament:cache-components
```

---

## Step 6 — Build frontend assets (if changed)

Role: `devops-engineer`

```bash
npm ci && npm run build
```

Only needed when `resources/css/`, `resources/js/`, or `vite.config.js` changed. Commit compiled assets if the server has no Node.js — build locally and push.

---

## Step 7 — Verify deployment

Role: `devops-engineer`

1. Browse product listing pages and one PDP — no 500 errors.
2. Add item to cart (Livewire CartDrawer) — confirm Livewire loads correctly.
3. Check Filament admin: `yourdomain.com/admin` — login and confirm resources.
4. Check `storage/logs/laravel.log` for errors.
5. If VietQR changed: test QR generation endpoint with a safe test order.

**Rollback:** Revert via cPanel Git or `git revert`, re-run steps 3–7.

### Failure Modes

- **Deploy with failing tests**: a release ships with red tests. **Mitigation:** Step 1 (Pre-flight) requires passing tests; reject the deploy when they fail.
- **Destructive PostgreSQL migration without rollback**: a DROP, TRUNCATE, or large data migration ships without a verified rollback path. **Mitigation:** Step 1 requires a rollback plan; use `--pretend` for large tables in Step 4; reject the deploy when the plan is missing.
- **VietQR or payment env vars missing**: a payment flow change ships without VietQR credentials on the server. **Mitigation:** Step 1 diffs `.env.production`; reject the deploy when a payment env var is missing.
- **HEAD SHA mismatch after pull**: the deployed commit does not match the expected release. **Mitigation:** Step 2 requires an explicit SHA confirmation; reject the deploy when the SHA does not match.
- **Composer update run in production**: `composer update` is used instead of `composer install`. **Mitigation:** Step 3 forbids it; verify the lock file is unchanged before deploy.
- **Filament v3 cache command run on v4**: the v3 component cache command fails on v4. **Mitigation:** Step 5 is a Filament v3 cache command; replace with v4 equivalent (`filament:cache-components` may differ) and verify before deploy.
- **Frontend assets out of sync with server**: server has no Node.js and the build was not run locally. **Mitigation:** Step 6 requires the build to be run locally when the server has no Node.js; commit compiled assets.
- **VietQR change untested in production**: a QR generation change ships without a test order. **Mitigation:** Step 7 requires a VietQR smoke test when the integration changed; reject the deploy when the test is missing.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/deployment-plan.json`** — capture infrastructure changes, config updates, and the `validation_run` output proving the verify step passed.
- **`contracts/schemas/api-contract-spec.json`** when the deploy introduces a new public API or a changed FormRequest contract.
- **`contracts/schemas/incident-report.json`** when the deploy triggers an anomaly; capture the trace id, the threshold, and the recommended action.