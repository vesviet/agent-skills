---
name: configure-cloudflare-bindings
description: Declare and wire Cloudflare runtime bindings (R2, KV, D1, services, queues) in Wrangler and application code. Use when Astro API routes or Workers need env access via Astro.locals.runtime.env or worker bindings.
---

# Configure Cloudflare Bindings

Use with the **Cloudflare Engineer** role. Application business logic stays with Backend or Frontend developers; this skill owns binding correctness and Wrangler declarations.

## Core Rules

- declare every binding in Wrangler config — do not rely on dashboard-only wiring without repo sync
- access bindings via `Astro.locals.runtime.env` in Astro API routes or worker `env` in pure Workers
- never expose binding credentials or secret values in client bundles or logs
- match binding names exactly between Wrangler, TypeScript `env.d.ts`, and runtime access
- list binding changes in `edge-deployment-spec.json` bindings array

## Suggested Process

### 1. Inventory Runtime Needs

From feature or API design, list:

- storage (R2), cache (KV), SQL (D1), service bindings, queues
- read vs write patterns and bucket/key conventions

### 2. Update Wrangler Declarations

Add or modify:

- `r2_buckets`, `kv_namespaces`, `d1_databases`, `services`, `queues`
- preview vs production resource IDs when they differ
- `compatibility_flags` if Node APIs required

### 3. Align Application Types

Update:

- `src/env.d.ts` or generated types for `Runtime`
- API route imports and error handling for missing bindings in dev

### 4. Validate Locally

Run:

- `npm run dev` / `npm run preview` with `.dev.vars` for local secrets
- minimal read/write smoke against dev resources

### 5. Hand Off

Document bindings in `edge-deployment-spec.json`; notify Frontend/Backend of contract fields consumed.

## Checklist

- [ ] all required bindings declared in Wrangler
- [ ] TypeScript env types updated
- [ ] no secrets in client-side code
- [ ] local `.dev.vars` documented (names only in handoff)
- [ ] edge-deployment-spec.json bindings array populated
- [ ] downstream dev roles notified of env field names

## Related Skills

- **manage-wrangler-deploy**: Deploy after bindings change
- **debug-workers-edge**: Fix binding-not-found or permission errors
- **manage-secrets**: Coordinate secret rotation policy with Security Engineer
- **integrate-api-client**: Frontend consumes APIs that use bindings (collaboration)
