# Astro Cloudflare Overlay

Generic, reusable conventions for any Astro v5/6/7 project deployed to Cloudflare Pages/Workers. This overlay is stack-specific but project-agnostic.

## Tech Stack Coverage (2026)

- **Framework:** Astro v6/v7 (SSG/SSR) — Astro 6 stable, Astro 7 current
- **Styling:** TailwindCSS **v4** (CSS-first config — `tailwind.config.js` removed)
- **Infrastructure:** Cloudflare **Workers** (preferred), Pages (legacy/static-only)
- **Build:** Vite 8 + Rolldown (Rust-based, 10–30× faster builds)
- **Node.js:** 22+ required (Node 18/20 dropped in Astro 6)
- **Email:** Resend API (optional)
- **Anti-Spam:** Cloudflare Turnstile (optional)
- **Linting:** ESLint + Prettier + astro-check

## 2026 Decision: Workers vs Pages

**Default to Cloudflare Workers for all new full-stack apps.**

| | Workers | Pages |
|---|---|---|
| Static assets | ✅ Native | ✅ |
| Durable Objects | ✅ | ❌ |
| Cron Triggers | ✅ | ❌ |
| Queues | ✅ | ❌ |
| Advanced observability | ✅ | Limited |
| Roadmap investment | ✅ Active | Maintenance |

Pages remains valid for static-first or legacy Git-push-only deployments.

## Astro 5 → 6 Breaking Changes (Action Required)

1. **Bindings**: `Astro.locals.runtime.env.MY_BINDING` → **`env.MY_BINDING`** (direct access)
2. **Content Layer API mandatory** — legacy `/content/` collections removed; migrate to `src/content.config.ts`
3. **Node.js 22+** required — drop Node 18/20 from CI pipelines
4. **`Astro.glob()`** → use `import.meta.glob()` instead
5. **Cloudflare adapter entrypoint** changed to `@astrojs/cloudflare/entrypoints/server`

## TailwindCSS v4 Migration (Breaking)

`tailwind.config.js` is **deleted** in v4 projects:

```bash
# 1. Automated migration
npx @tailwindcss/upgrade

# 2. New install
npm install tailwindcss @tailwindcss/vite
```

`astro.config.mjs`:
```js
import tailwindcss from '@tailwindcss/vite';
export default defineConfig({ vite: { plugins: [tailwindcss()] } });
```

`src/styles/global.css`:
```css
@import "tailwindcss";
@theme { --color-brand: #...; }
```

The `@astrojs/tailwind` integration is deprecated for v4 projects.

## Included

- `rules/astro-cloudflare-conventions.md` — Architecture, component patterns, deploy, Wrangler config, TailwindCSS v4

This overlay should be composed with the global core and optionally with project-specific overlays.

**Recommended roles:** `cloudflare-engineer` (edge/Wrangler/bindings) + `frontend-developer` (Astro UI).

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-09-01
