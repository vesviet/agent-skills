# Sport ICM Overlay

Project-specific conventions for the Sport ICM niche website — sportswear and activewear catalog.

**Depends on:** `overlays/astro-cloudflare`

- **Repo:** `D:\regna\cloudflare\sport.icm`
- **Live:** Cloudflare Pages (`sport-cm.sweet-voice-f606.workers.dev`)

## Specifics

- Single-page catalog site (`src/pages/index.astro` — 38KB, all content inline)
- MDX support for blog/article content (`@astrojs/mdx`)
- WordPress content migration tool (`clean_wp.mjs`, `scraper.js`)
- Tailwind + Tabler icons (`@iconify-json/tabler`)
- Contact form via Resend API + Turnstile

## Rules

- `rules/sport-project-rules.md` — Catalog structure, brand positioning, WP migration
