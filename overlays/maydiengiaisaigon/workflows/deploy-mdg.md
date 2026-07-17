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
