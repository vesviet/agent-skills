# Astro Cloudflare Conventions

Portable conventions for Astro v5 projects deployed to Cloudflare Pages/Workers. These extend `core/rules/code.md`.

## Project Structure

```
src/
├── assets/         ← Static assets processed by Astro (images optimized at build)
├── components/     ← Reusable .astro and framework components (.tsx, .jsx)
├── data/           ← TypeScript/JSON data files (products, config)
├── layouts/        ← Page layouts (BaseLayout.astro, etc.)
├── pages/          ← File-based routing (.astro, .ts for API routes)
│   └── api/        ← Server-side API endpoints (Cloudflare Workers)
├── styles/         ← Global CSS / Tailwind base styles
└── env.d.ts        ← Astro environment type declarations
public/             ← Static files served as-is (favicon, robots.txt, media)
```

## Component Architecture

- `.astro` components for static/server-rendered content — zero JS shipped to client.
- React/Preact components (`.tsx`) only for interactive islands requiring client-side JS.
- Use `client:load`, `client:visible`, or `client:idle` directives intentionally — never `client:only` unless SSR is impossible.
- Keep island components small and focused — one interactive concern per island.

## Data Layer

- Product catalogs and static data live in `src/data/` as TypeScript or JSON.
- Use Astro Content Collections for MDX/Markdown content when present.
- Type all data with TypeScript interfaces — no `any`.

## Styling (Tailwind CSS)

- Use Tailwind utility classes in components.
- Custom design tokens in `tailwind.config.js` (`extend.colors`, `extend.fontFamily`).
- Global base styles in `src/styles/global.css`.
- Use `@apply` sparingly — prefer utility classes directly in templates.

## API Routes (Cloudflare Workers)

- Server endpoints in `src/pages/api/*.ts`.
- Access Cloudflare bindings via `Astro.locals.runtime.env` (R2, KV, D1, etc.).
- Environment secrets in `.dev.vars` (local) and Cloudflare Dashboard (production).
- Never expose API keys in client-side code.

## Wrangler Configuration

- Config in `wrangler.jsonc` at project root.
- Use `compatibility_flags: ["nodejs_compat"]` for Node.js API access.
- R2 buckets, KV namespaces, D1 databases declared in wrangler config.
- Deploy with `npm run deploy` → `astro build && wrangler pages deploy dist`.

## Build & Deploy

- `npm run dev` — local dev server.
- `npm run build` — production build.
- `npm run preview` — build + Wrangler local preview.
- `npm run deploy` — build + deploy to Cloudflare Pages.
- GitHub Actions CI/CD triggers on `main` branch push.

## Performance

- Prefer static (SSG) pages over SSR unless dynamic data is required.
- Use `astro:assets` Image component for automatic optimization.
- Inline critical CSS for above-the-fold content when applicable.
- Lazy-load below-fold images with `loading="lazy"`.

## SEO

- Every page must have unique `<title>` and `<meta name="description">`.
- Use `@astrojs/sitemap` for automatic sitemap generation.
- Implement structured data (JSON-LD) for product and article pages.
- Canonical URLs on all pages.

## Quality Gates

- `npm run check` — runs `astro check` + ESLint + Prettier.
- Fix before commit: `npm run fix`.
- TypeScript strict mode enabled.
