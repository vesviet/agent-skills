# Golf ICM Overlay

Project-specific conventions for the Golf ICM niche website — golf apparel and resort wear catalog.

**Depends on:** `overlays/astro-cloudflare`

- **Repo:** `D:\regna\cloudflare\golf.icm`
- **Live:** Cloudflare Pages (`golf-icm.sweet-voice-f606.workers.dev`)

## Specifics

- Single-page catalog site (`src/pages/index.astro` — 27KB, all content inline)
- MDX support for blog/article content (`@astrojs/mdx`)
- Gallery generation scripts (`generate_galleries.mjs`, `clone_raw.mjs`, `apply_updates.mjs`)
- Product gallery data in `generated_galleries.json`
- Tailwind + Tabler icons (`@iconify-json/tabler`)
- Contact form via Resend API + Turnstile

## Rules

- `rules/golf-project-rules.md` — Catalog structure, gallery management, brand positioning
