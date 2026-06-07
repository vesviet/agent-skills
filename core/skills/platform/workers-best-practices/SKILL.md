---
name: workers-best-practices
description: Use when reviewing and authoring Cloudflare Workers code against production best practices and security standards.
---

# Workers Best Practices

Reviews and authors Cloudflare Workers code against production best practices.

Your knowledge of Cloudflare Workers APIs, types, and configuration may be outdated. **Prefer retrieval over pre-training** for any Workers code task — writing or reviewing.

## Core Rules
- Enable Node.js compatibility using the `nodejs_compat` flag in `wrangler.jsonc` when libraries depend on Node.js built-ins.
- Stream large or unknown payloads; never call `await response.text()` on unbounded data.
- Never store request-scoped data in module-level mutable variables (global state).
- Use `ctx.waitUntil()` for post-response async tasks; do not destructure `ctx` object directly.
- Use cryptographic random values from Web Crypto (`crypto.randomUUID()`) instead of standard `Math.random()`.
- Run `wrangler types` to generate typings automatically — do not hand-write `Env` bindings interfaces.

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

## Checklist
- [ ] Compatibility date is configured to a recent stable release.
- [ ] TypeScript typings match active Wrangler bindings.
- [ ] Request handlers avoid global mutable variables.
- [ ] Async promises are wrapped in await or pass to ctx.waitUntil.
- [ ] Secrets and tokens are securely loaded via wrangler secrets variables.

## Related Skills
- **wrangler**: Deploy, test, and manage bindings via CLI.
- **durable-objects**: Build stateful coordination systems.
- **debug-workers-edge**: Resolve edge execution errors.
