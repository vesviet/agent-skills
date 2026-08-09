---
name: workers-best-practices
description: Reviews and authors Cloudflare Workers code against production best practices — covering async patterns, global state isolation, secret handling, compatibility flags, and TypeScript bindings. Use when writing new Workers, reviewing existing code for production readiness, or correcting violations of Cloudflare's canonical Workers patterns.
---

# Workers Best Practices

Reviews and authors Cloudflare Workers code against production best practices.

Your knowledge of Cloudflare Workers APIs, types, and configuration may be outdated. **Prefer retrieval over pre-training** for any Workers code task — writing or reviewing.

## When to Use

- writing new Cloudflare Workers
- reviewing Workers for production readiness
- fixing async/global-state/secret violations
- applying canonical Workers TypeScript patterns

## Core Rules
- Enable Node.js compatibility using the `nodejs_compat` flag in `wrangler.jsonc` when libraries depend on Node.js built-ins.
- Stream large or unknown payloads; never call `await response.text()` on unbounded data.
- Never store request-scoped data in module-level mutable variables (global state).
- Use `ctx.waitUntil()` for post-response async tasks; do not destructure `ctx` object directly.
- Use cryptographic random values from Web Crypto (`crypto.randomUUID()`) instead of standard `Math.random()`.
- Run `wrangler types` to generate typings automatically — do not hand-write `Env` bindings interfaces.
- Enable Smart Placement by adding `"placement": { "mode": "smart" }` to `wrangler.jsonc` to route Workers to the closest data center to primary data sources.
- Implement request coalescing using Durable Objects or KV to deduplicate concurrent identical requests.
- Optimize CPU time billing by using `TextDecoder` instead of repeated string concatenation and profiling hot loops.

## Retrieval Sources

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| Workers best practices | `https://developers.cloudflare.com/workers/best-practices/workers-best-practices/` | Canonical rules, patterns, anti-patterns |
| Wrangler config schema | `node_modules/wrangler/config-schema.json` | Config fields, binding shapes, allowed values |
| Cloudflare docs | Search tool or `https://developers.cloudflare.com/workers/` | API reference, compatibility dates/flags |

## Suggested Process
1. Inspect the compatibility date and Node.js compat flags in wrangler configuration.
2. Run typings generation commands to check TS bindings correctness.
3. Review worker handlers for async execution blocks, avoiding floating promises.
4. Verify request scope structures, ensuring request data isn't leaked globally.
5. Inspect crypto routines and validation checks for timing safe comparisons.

### 2026: Smart Placement, Request Coalescing, and CPU Billing

- **Smart Placement (GA 2025)**: Enable Smart Placement via `"placement": { "mode": "smart" }` in `wrangler.jsonc` configuration. This routes Workers to the data center closest to primary data sources (such as D1 databases, KV namespaces, and R2 buckets), reducing P99 latency by 30-60% for data-heavy Workers.
- **Request Coalescing**: Deduplicate concurrent identical requests to backend APIs or databases using Durable Objects or KV. The first request computes the value and caches the result, while subsequent concurrent identical requests read the cached result.
- **CPU Time Billing (June 2026)**: Workers are billed on actual CPU execution time rather than wall-clock time. Optimize performance by using `TextDecoder` for text processing instead of string concatenation, and profile execution via `wrangler dev --inspect` to identify and optimize CPU-intensive hot loops.

## Checklist
- [ ] Compatibility date is configured to a recent stable release.
- [ ] TypeScript typings match active Wrangler bindings.
- [ ] Request handlers avoid global mutable variables.
- [ ] Async promises are wrapped in await or pass to ctx.waitUntil.
- [ ] Secrets and tokens are securely loaded via wrangler secrets variables.
- [ ] Smart placement is enabled in `wrangler.jsonc` configuration via placement mode.
- [ ] Request coalescing is implemented to deduplicate identical concurrent requests.
- [ ] CPU time billing is optimized via TextDecoder and dev inspect profiling.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Related Skills
- **wrangler**: Deploy, test, and manage bindings via CLI.
- **durable-objects**: Build stateful coordination systems.
- **debug-workers-edge**: Resolve edge execution errors.
\n### 2026: Workers Optimization

- **Smart Placement (GA 2025):** Enable via `"placement": { "mode": "smart" }` in `wrangler.jsonc`. Cloudflare automatically routes Worker invocations to the data center closest to the Worker's primary data source (D1, KV, R2 bucket region) rather than the requesting client. This reduces P99 latency for data-heavy Workers by 30 to 60 percent.
- **Request coalescing for expensive computations:** Use Durable Objects or KV as a coalescing layer to deduplicate concurrent identical requests. The first request triggers computation and stores the result; subsequent requests wait on the DO/KV read instead of re-running the computation.
- **CPU time billing (June 2026):** Workers are now billed on CPU time consumed, not wall-clock time. Optimize compute-heavy Workers with `TextDecoder` instead of string concatenation, avoid synchronous regex on large inputs, and profile with `wrangler dev --inspect` to identify hot loops.\n
