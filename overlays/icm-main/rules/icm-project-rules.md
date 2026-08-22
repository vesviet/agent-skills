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
