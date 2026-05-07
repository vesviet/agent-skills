# Golf ICM — Project Rules

Project-specific conventions for the Golf ICM niche catalog site.

## Site Architecture

- Primary content in `src/pages/index.astro` — single-page catalog with sections.
- Additional pages for 404, API endpoints, blog articles (MDX).
- Components in `src/components/` — Astro-only (no React islands needed).
- Styles in `src/styles/` — Tailwind base + custom theme.

## Product Galleries

- Gallery data auto-generated to `generated_galleries.json` via build scripts.
- `generate_galleries.mjs` — scans `public/` media for product images, outputs JSON.
- `clone_raw.mjs` — clones raw product images from source.
- `apply_updates.mjs` — applies batch updates to gallery metadata.
- Image assets in `public/` — served as-is through Cloudflare CDN.

## Brand Positioning

- Niche: Golf apparel, polo shirts, resort wear, country club uniforms.
- Tone: Premium, sophisticated, performance-focused.
- Target: Golf clubs, resorts, corporate events, tournament organizers.
- Keywords: custom golf apparel, polo shirts manufacturer, resort wear OEM.

## Content (MDX)

- Blog articles use MDX format with reading-time estimation.
- Typography plugin enabled (`@tailwindcss/typography`) for article body.
- Frontmatter: `title`, `date`, `description`, `image`, `tags`.

## Deploy

- `npm run deploy` → `astro build && wrangler pages deploy dist`.
- GitHub Actions on `main` branch.
