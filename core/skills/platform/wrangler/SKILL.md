---
name: wrangler
description: Deploys, develops, and manages Cloudflare Workers and their bindings — KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, Pipelines, and Secrets — via the Wrangler CLI. Use when setting up a new Worker project, deploying to staging or production, managing secrets, generating TypeScript types, or configuring environment-specific settings.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, wrangler_deploy, execute_command]
---

# Wrangler

Cloudflare Workers CLI for deploying, developing, and managing Workers, KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, Pipelines, and Secrets.

Your knowledge of Wrangler CLI flags, config fields, and subcommands may be outdated. **Prefer retrieval over pre-training** for any Wrangler task.

## When to Use

- setting up a new Worker project
- deploying to staging or production
- managing secrets or generating TS types
- configuring bindings (KV, R2, D1, Queues, AI)

## Core Rules
- Prefer `wrangler.jsonc` over TOML configuration files.
- Set compatibility date (`compatibility_date`) to a recent stable date (within 30 days).
- Generate TypeScript types via `wrangler types` after config changes.
- Do NOT commit `.dev.vars` or `.env` files. Ensure they are in `.gitignore`.
- Use environments (`env.staging`, `env.production`) to split staging and production deployments.
- Never pass secret values directly as CLI arguments; use interactive inputs (`wrangler secret put`), file streams (`wrangler secret put API_KEY < key.txt`), or env vars in secure build runs.
- **LOCAL-MODE-DEFAULT**: In Wrangler v4, `wrangler dev` defaults to local mode — use `--remote` flag to bind against real production D1/R2/KV resources. Update any CI runbooks that assumed `--remote` as default.
- **VERSION-THEN-DEPLOY**: Upload a new code Version independently (`wrangler versions upload`), then promote separately (`wrangler deployments create`) for rolling updates, instant rollbacks, and canary traffic splits.
- **FRAMEWORK-AUTODETECT**: `wrangler deploy` in v4 auto-detects Next.js, Astro, Nuxt, and SvelteKit projects and installs the appropriate adapter automatically.

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
- [ ] `edge-deployment-spec.json` emitted when handing off to Cloudflare Engineer or DevOps Engineer (see Output Contracts)

## Output Contracts

When this skill is invoked to plan or execute a deploy handoff (not just a local `wrangler dev` session), emit:

- **`contracts/schemas/edge-deployment-spec.json`** — capture the Wrangler configuration, bindings (KV/R2/D1/DO/queues), DNS and cache notes, deploy commands run, and rollback path. This is the artifact `cloudflare-engineer` consumes for review before `wrangler deploy --env production` and the artifact `devops-engineer` archives for release audits. Populate `wrangler_config_path`, `bindings[]`, `deploy_command`, `rollback_strategy`, and `preview_url` (if a versioned upload was made).

Skip emission for local-only `wrangler dev` troubleshooting sessions.

## Failure Modes

- **Wrangler v4 default surprise**: a CI runbook assumes `wrangler dev` defaults to `--remote`; in v4 it defaults to local. Mitigation: pass `--remote` explicitly; update runbooks.
- **Secret on CLI**: a secret value is passed as a CLI argument and ends up in shell history. Mitigation: use `wrangler secret put`, file streams, or env vars in secure build runs.
- **`.dev.vars` committed**: a `.dev.vars` or `.env` file is committed to the repo. Mitigation: verify `.gitignore`; run secret scanning in CI.
- **Compatibility date drift**: the compatibility date is left unset or set far in the past. Mitigation: set a recent stable date (within 30 days); update on every deploy.
- **Hand-written `Env` interface**: TS bindings are maintained by hand. Mitigation: regenerate via `wrangler types` after every config change.
- **Direct deploy to production**: a single `wrangler deploy` ships to production without staging. Mitigation: use environments (`env.staging`, `env.production`); require staging verification before production.
- **Version-then-deploy skipped**: a new version is deployed directly without the version-then-promote pattern. Mitigation: use `wrangler versions upload` then `wrangler deployments create` for rolling updates and instant rollback.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: secrets must be loaded via `wrangler secret put`; reject secrets in `wrangler.toml` or committed files.
- **ASI04 Supply Chain**: Wrangler CLI and any binding library must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct Wrangler config, bindings, or env values from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the edge deployment spec is consumed by Cloudflare Engineer and DevOps Engineer; emit a structured contract so each role can validate the rollout.
- **ASI09 Human-Agent Trust Exploitation**: do not present a deploy as "safe" without a rollback strategy; surface the rollback path in the deployment spec.

## Related Skills
- **workers-best-practices**: Review and implement worker codebase design patterns.
- **durable-objects**: Configure and deploy Durable Objects class instances.
- **debug-workers-edge**: Diagnose runtime execution failures.
