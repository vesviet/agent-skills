# Astro Cloudflare Conventions

Strict, portable conventions for Astro v5 projects deployed to Cloudflare Pages/Workers. These rules extend `core/rules/code.md`.

## 1. Component Architecture (Astro Islands)

To maximize performance, this stack enforces a Zero-JS-by-default architecture:
- **Default Extension:** All static or server-rendered layouts and components MUST use `.astro`.
- **Interactive Components:** React/Preact (`.tsx`) must ONLY be used for interactive islands requiring client-side JS.
- **Hydration Directives:** You MUST explicitly declare hydration strategies for interactive components (e.g., `client:load`, `client:visible`, `client:idle`).
- **PROHIBITED:** Never use `client:only` unless Server-Side Rendering (SSR) is strictly impossible for that specific component.

## 2. Backend & API Routes (Cloudflare Workers)

- **API Location:** All server-side API endpoints MUST be placed inside the `src/pages/api/*.ts` directory.
- **Cloudflare Bindings:** Do not use process.env for Cloudflare resources. R2, KV, and D1 bindings MUST be accessed via the standard Astro adapter context: `Astro.locals.runtime.env`.
- **Infrastructure Config:** All Cloudflare routing, compatibility flags, and binding definitions MUST be centrally managed in `wrangler.jsonc` at the project root.

## 3. Project Structure

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

## 4. Build & Deploy Lifecycle

- `npm run dev` — local dev server.
- `npm run build` — production build.
- `npm run preview` — build + Wrangler local preview.
- `npm run deploy` — build + deploy to Cloudflare Pages via Wrangler.
- GitHub Actions CI/CD triggers on `main` branch push.

## 5. Quality Gates

- `npm run check` — runs `astro check` + ESLint + Prettier.
- Fix before commit: `npm run fix`.
- TypeScript strict mode enabled.
