---
name: wrangler
description: Deploys, develops, and manages Cloudflare Workers and their bindings — KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, Pipelines, and Secrets — via the Wrangler CLI. Use when setting up a new Worker project, deploying to staging or production, managing secrets, generating TypeScript types, or configuring environment-specific settings.
---

# Wrangler

Cloudflare Workers CLI for deploying, developing, and managing Workers, KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, Pipelines, and Secrets.

Your knowledge of Wrangler CLI flags, config fields, and subcommands may be outdated. **Prefer retrieval over pre-training** for any Wrangler task.

## Core Rules
- Prefer `wrangler.jsonc` over TOML configuration files.
- Set compatibility date (`compatibility_date`) to a recent stable date (within 30 days).
- Generate TypeScript types via `wrangler types` after config changes.
- Do NOT commit `.dev.vars` or `.env` files. Ensure they are in `.gitignore`.
- Use environments (`env.staging`, `env.production`) to split staging and production deployments.
- Never pass secret values directly as CLI arguments; use interactive inputs (`wrangler secret put`), file streams (`wrangler secret put API_KEY < key.txt`), or env vars in secure build runs.

## Retrieval Sources

Fetch the **latest** information before writing or reviewing Wrangler commands and config. Do not rely on baked-in knowledge for CLI flags, config fields, or binding shapes.

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| Wrangler docs | `https://developers.cloudflare.com/workers/wrangler/` | CLI commands, flags, config reference |
| Wrangler config schema | `node_modules/wrangler/config-schema.json` | Config fields, binding shapes, allowed values |
| Cloudflare docs | Search tool or `https://developers.cloudflare.com/workers/` | API reference, compatibility dates/flags |

## Suggested Process
1. Verify wrangler CLI installation (`wrangler --version`) and authenticate (`wrangler whoami`).
2. Set up or update `wrangler.jsonc` declaring required bindings (KV, R2, D1, AI, etc.).
3. Generate up-to-date local types using `wrangler types`.
4. Run the local development server using `wrangler dev` to test bindings and local storage.
5. Deploy to target environments using `wrangler deploy` (or `wrangler deploy --env staging`).

## Checklist
- [ ] Compatibility date matches a recent stable API version.
- [ ] TypeScript types are regenerated via `wrangler types`.
- [ ] Secrets are securely set using wrangler secret management commands.
- [ ] Local storage testing matches the simulation paths under `.wrangler/`.
- [ ] Deployment runs successfully and outputs a valid URL.

## Related Skills
- **workers-best-practices**: Review and implement worker codebase design patterns.
- **durable-objects**: Configure and deploy Durable Objects class instances.
- **debug-workers-edge**: Diagnose runtime execution failures.
