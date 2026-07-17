# Sport ICM — Project Rules

Project-specific conventions for the Sport ICM niche catalog site.

## Site Architecture

- Single-page or multi-page catalog built on Astro + Cloudflare Pages.
- Components in `src/components/` — Astro-only (no React islands unless required for interactivity).
- Styles: Tailwind base + custom sport/athletic theme overrides.
- Static product pages with dynamic category routes where defined.

## Product Catalog

- Product data in `src/data/` — typed TypeScript or JSON catalog files.
- Category and collection structure mirrors ICM Factory Direct parent brand conventions.
- Image assets in `public/` — served via Cloudflare CDN; optimize before commit.
- Gallery or product listing data should be generated/managed via build scripts when volume is high.

## Brand Positioning

- Niche: Custom sportswear, athletic uniforms, performance activewear.
- Tone: Energetic, performance-focused, professional team/club audience.
- Target: Sports clubs, schools, corporate teams, tournament organizers.
- Keywords: custom sportswear, athletic uniforms manufacturer, team jersey OEM.

## Content

- Blog or article content uses MDX if enabled (`@astrojs/mdx`).
- Frontmatter standard: `title`, `date`, `description`, `image`, `tags`.
- SEO metadata per page — no missing `<title>` or `<meta name="description">`.

## Deploy

- Follows `overlays/astro-cloudflare` deploy conventions.
- `npm run deploy` → `astro build && wrangler pages deploy dist`.
- Environment variables via Wrangler secrets — never hardcoded.

## Guardrails

- Do not apply ICM Factory Direct (`icm-main`) brand copy or product data directly — sport-icm is a distinct niche catalog.
- Keep product catalog data out of component files; use `src/data/` as single source of truth.
- Contact form (if present) must use Turnstile anti-spam and a server-side API route.
