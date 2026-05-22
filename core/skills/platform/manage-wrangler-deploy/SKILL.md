---
name: manage-wrangler-deploy
description: Configure and execute Cloudflare Pages or Workers deployments via Wrangler and repo source of truth. Use when updating wrangler.jsonc, deploy scripts, preview vs production targets, or rollout steps for Astro-on-Cloudflare projects.
---

# Manage Wrangler Deploy

Use with the **Cloudflare Engineer** role for edge deploy paths. DevOps owns generic CI wiring; this skill owns Wrangler and Cloudflare deploy surfaces.

## Core Rules

- treat `wrangler.jsonc` / `wrangler.toml` and `package.json` deploy scripts as source of truth
- never commit secret values — reference secret names only in handoffs
- align `astro build` output with Pages `dist` or Workers entry expectations
- document preview vs production targets in `contracts/schemas/edge-deployment-spec.json`
- require approval before production deploy or destructive rollback per policy

## Suggested Process

### 1. Inspect Deploy Surface

Identify:

- Pages vs Workers vs Workers for Platforms
- existing `npm run deploy`, `preview`, and CI steps
- compatibility flags (`nodejs_compat`, etc.)
- custom domains and routes

### 2. Update Wrangler And Scripts

Change only what the release needs:

- bindings block (R2, KV, D1, services)
- routes, `pages_build_output_dir`, or worker entry
- environment-specific vars (non-secret)
- deploy/preview script alignment

### 3. Plan Rollout Order

Sequence:

- build verification (`astro check`, lint)
- binding or secret prerequisites
- deploy to preview before production when risk is non-trivial
- smoke tests after each stage

### 4. Emit Edge Handoff

Produce `contracts/schemas/edge-deployment-spec.json` with deploy_steps, rollback_plan, and smoke_tests.

### 5. Verify

Confirm:

- local `npm run preview` or dry-run succeeds when applicable
- bindings match code (`Astro.locals.runtime.env` / worker env)
- rollback path documented

## Checklist

- [ ] deployment target (pages/workers) identified
- [ ] wrangler config updated in repo
- [ ] secret names listed without values
- [ ] preview-before-prod considered for risky changes
- [ ] edge-deployment-spec.json complete when machine handoff required
- [ ] smoke tests defined

## Related Skills

- **configure-cloudflare-bindings**: Add or fix R2/KV/D1/service bindings
- **debug-workers-edge**: Investigate failed deploys or 5xx at edge
- **setup-deployment**: Coordinate with DevOps on CI job changes
- **commit-code**: Deliver config changes safely
