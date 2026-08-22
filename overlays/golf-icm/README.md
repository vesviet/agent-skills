# Golf ICM Overlay

Project-specific conventions for the Golf ICM niche website — golf apparel and resort wear catalog.

**Depends on:** `overlays/astro-cloudflare`

- **Live:** Cloudflare Pages (`golf-icm.sweet-voice-f606.workers.dev`)

## 2026 Stack Status

| Component | Current | Target |
|-----------|---------|--------|
| Astro | v5 | **v6/v7** — Content Layer API, direct `env` binding access |
| TailwindCSS | v3 | **v4** — CSS-first, no `tailwind.config.js` |
| Node.js | 18/20 | **22+** (required by Astro 6) |

## Specifics

- Single-page catalog site (`src/pages/index.astro` — primary content inline)
- MDX support for blog/article content (`@astrojs/mdx`)
- Gallery generation scripts (`generate_galleries.mjs`, `clone_raw.mjs`, `apply_updates.mjs`)
- Product gallery data in `generated_galleries.json`
- Tailwind + Tabler icons (`@iconify-json/tabler`)
- Contact form via Resend API + Turnstile

## Rules

- `rules/golf-project-rules.md` — Catalog structure, gallery management, brand positioning
