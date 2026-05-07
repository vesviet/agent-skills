# ICM Main — Project Rules

Project-specific conventions for the ICM Factory Direct corporate website.

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

## Contact Form

- Server-side handler at `src/pages/api/contact.ts`.
- Cloudflare Turnstile for anti-spam validation.
- Resend API for email delivery.
- Secrets in `.dev.vars` (local) / Cloudflare Dashboard (prod): `RESEND_API_KEY`, `TURNSTILE_SECRET_KEY`, `CONTACT_EMAIL`.

## R2 Storage

- Bucket: `icm-documents` (bound as `icm_documents` in wrangler).
- Used for downloadable assets (catalogs, spec sheets).
- Access via `Astro.locals.runtime.env.icm_documents`.

## Build

- Custom post-build: `node scripts/inline-critical-css.cjs` inlines above-fold CSS.
- Deploy: `npm run deploy` → `astro build && wrangler pages deploy dist`.
