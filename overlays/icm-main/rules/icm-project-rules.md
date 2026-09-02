# ICM Main — Project Rules

Project-specific conventions for the ICM Factory Direct corporate website.

## 2026 Stack Status

- **Astro**: v6+ (upgrade from v5; `Astro.locals.runtime.env` → direct `env` binding access)
- **TailwindCSS**: v4 migration recommended (`tailwind.config.js` → `@theme {}` CSS blocks)
- **Cloudflare**: Workers preferred over Pages for new features (bindings, cron, queues)

## Product Catalog

- All product data lives in `src/data/products.ts` as a typed TypeScript array.
- Each product has: `name`, `slug`, `category`, `description`, `images[]`, `features[]`, `minOrder`.
- Category SEO metadata in `src/data/category-seo.json`.
- Color charts in `src/data/colorCharts.json` with hex values and fabric references.

## Page Templates

- Static pages use `src/layouts/` base layout with consistent header/footer.
- Product category pages: `src/pages/[category].astro` — grid layout with filtering.
- Individual product pages: `src/pages/[category]/[product].astro`.
- Service pages (fabrics, sublimation, laser-punching, etc.) are standalone `.astro` files.

## Brand Voice (B2B Manufacturing)

- Professional, technical tone — target audience is brand owners and procurement teams.
- Emphasize: factory-direct pricing, Vietnam manufacturing quality, minimum order quantities.
- Keywords: custom sportswear, OEM manufacturer, private label, Vietnam factory.
- **2026 GEO/AI**: Product pages MUST have Q&A structured data for AI search citations.

## Contact Form

- Server-side handler at `src/pages/api/contact.ts`.
- Cloudflare Turnstile for anti-spam validation.
- Resend API for email delivery.
- Secrets in `.dev.vars` (local) / Cloudflare Dashboard (prod): `RESEND_API_KEY`, `TURNSTILE_SECRET_KEY`, `CONTACT_EMAIL`.

## Cloudflare Bindings (2026 API)

```ts
// ✅ Astro 6+ binding access (direct env parameter)
export const GET: APIRoute = async ({ locals }) => {
  const { env } = locals.runtime;
  const doc = await env.icm_documents.get("catalog.pdf");
  return new Response(doc?.body);
};

// ❌ Deprecated (Astro 5)
// Astro.locals.runtime.env.icm_documents
```

- Bucket: `icm-documents` (bound as `icm_documents` in wrangler.jsonc).
- Used for downloadable assets (catalogs, spec sheets).

## Build

- Custom post-build: `node scripts/inline-critical-css.cjs` inlines above-fold CSS.
- Deploy: `npm run deploy` → `astro build && wrangler pages deploy dist`.
- CI/CD: GitHub Actions on `main` branch.

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
  See `See `core/skills/foundation/setup-design-system/SKILL.md` and the `edge-deployment-spec.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/foundation/setup-design-system/SKILL.md` and the `edge-deployment-spec.json` schema.

Last updated: 2026-09-01
