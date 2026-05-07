# Sport ICM — Project Rules

Project-specific conventions for the Sport ICM niche catalog site.

## Site Architecture

- Primary content in `src/pages/index.astro` — single-page catalog with product sections.
- Additional pages for 404, API endpoints, blog articles (MDX).
- Components in `src/components/` — Astro-only (no React islands needed).
- Styles in `src/styles/` — Tailwind base + custom theme.
- Assets in `src/assets/` — processed by Astro image pipeline.

## WordPress Migration

- `clean_wp.mjs` — cleans and transforms exported WordPress content for Astro.
- `scraper.js` — scrapes additional content from legacy WordPress site.
- Migration output should target MDX format for blog articles.

## Brand Positioning

- Niche: Sportswear, activewear, team uniforms, fitness apparel.
- Tone: Dynamic, performance-driven, technical quality.
- Target: Sports teams, fitness brands, athletic event organizers, private label buyers.
- Keywords: custom sportswear manufacturer, activewear OEM, team uniforms Vietnam.

## Content (MDX)

- Blog articles use MDX format with reading-time estimation.
- Typography plugin enabled (`@tailwindcss/typography`) for article body.
- Frontmatter: `title`, `date`, `description`, `image`, `tags`.

## Deploy

- `npm run deploy` → `astro build && wrangler pages deploy dist`.
- GitHub Actions on `main` branch.
