# ICM Factory Direct — Main Site Overlay

Project-specific conventions for the ICM Factory Direct corporate website — the master brand site for B2B custom sportswear manufacturing.

**Depends on:** `overlays/astro-cloudflare`

- **Live:** Cloudflare Pages (`icm.sweet-voice-f606.workers.dev`)
- **Domain:** icmfactorydirect.com

## 2026 Stack Status

| Component | Current | Target |
|-----------|---------|--------|
| Astro | v5 | **v6/v7** — Content Layer API mandatory, `env` bindings |
| TailwindCSS | v3 | **v4** — CSS-first, `@theme {}`, no tailwind.config.js |
| Node.js | 18/20 | **22+** (required by Astro 6) |
| Deployment | Pages | Pages (static-first OK; Workers if adding Cron/DO) |

## Specifics

- ~22 static pages (product categories, fabrics, color charts, services)
- Product data in `src/data/products.ts` (TypeScript, typed catalog)
- Category SEO in `src/data/category-seo.json`
- Color chart data in `src/data/colorCharts.json`
- Contact form via Resend API + Turnstile anti-spam (`src/pages/api/contact.ts`)
- R2 bucket `icm-documents` for downloadable assets
- Inline critical CSS post-build (`scripts/inline-critical-css.cjs`)
- Dynamic category routes: `src/pages/[category].astro`, `src/pages/[category]/[product].astro`

## Rules

- `rules/icm-project-rules.md` — Brand voice, product catalog conventions, page templates, 2026 binding API
