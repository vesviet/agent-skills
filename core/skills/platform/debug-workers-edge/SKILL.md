---
name: debug-workers-edge
description: Diagnose Cloudflare Pages and Workers failures at the edge — 5xx, binding errors, Wrangler deploy failures, DNS/cache issues, and context loss. Use when symptoms appear after deploy or only on Cloudflare runtime, not in local dev alone.
---

# Debug Workers Edge

Use with the **Cloudflare Engineer** role for platform-layer failures. Escalate to `troubleshoot-service` when evidence points to application logic inside API handlers.

## When to Use

- 5xx or binding errors on Cloudflare runtime
- Wrangler deploy failures
- DNS/cache issues only on edge
- context loss after deploy

## Core Rules

- compare local preview vs deployed behavior before changing production
- read Workers/Pages logs and request IDs — do not guess from status codes alone
- separate binding misconfiguration from application exceptions
- prefer rollback or route disable for production incidents when blast radius is unclear
- get approval for production DNS, cache purge, or binding deletes per policy

## Suggested Process

### 1. Capture Symptom

Record:

- URL, status code, environment (preview/production)
- time of first failure vs last deploy
- whether static assets vs API/Worker routes fail

### 2. Check Deploy And Config Drift

Verify:

- last successful deployment ID / commit
- wrangler config vs dashboard bindings
- secret presence (names only) in Dashboard vs `.dev.vars` locally
- `nodejs_compat` and compatibility date issues

### 3. Isolate Layer

| Signal | Likely layer |
| ------ | ------------- |
| Binding not found | Wrangler / env types |
| 1101 / script error | Worker code — collaborate with dev |
| SSL / DNS | dns_and_routing in edge spec |
| Stale asset | cache rules or purge scope |
| Turnstile failure | turnstile site keys / domains |

### 4. Apply Smallest Safe Fix

Examples:

- fix binding name or resource ID in repo
- redeploy previous artifact
- narrow cache purge (not whole zone without approval)
- adjust route pattern

### 5. Verify And Document

Run smoke_tests from edge-deployment-spec; update residual_risks for SRE/DevOps.

## Checklist

- [ ] environment and route scope captured
- [ ] deploy revision compared to failing window
- [ ] bindings and secrets checked (names only in notes)
- [ ] platform vs application layer decided
- [ ] smallest safe fix applied
- [ ] smoke tests pass after recovery

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Related Skills

- **wrangler**: Wrangler CLI for deploying, developing, and managing Workers
- **debug-runtime-platform**: Broader platform issues shared with DevOps/SRE
- **troubleshoot-service**: Application-level API or Astro handler bugs
\n### 2026: Remote Bindings and Observability Updates

- **Remote Bindings (GA 2025/2026):** `wrangler dev` now supports running code locally while binding to REAL production D1/R2/KV without seeding local databases. This eliminates the "works locally, broken in prod" binding drift. Use the `--remote` flag explicitly in Wrangler v4 (which defaults to local-only mode).
- **Workers Observability dashboard:** A new centralized dashboard provides custom P99 CPU charts, JSON/CSV log export, shareable trace URLs, and per-Durable-Object instance metric filtering. Use this dashboard instead of `wrangler tail` for structured investigation.
- **Enabling log collection:** An `"observability": { "enabled": true }` configuration block is required in `wrangler.jsonc` to activate automatic log collection. Note that `wrangler tail` alone does not persist logs without this configuration.\n
