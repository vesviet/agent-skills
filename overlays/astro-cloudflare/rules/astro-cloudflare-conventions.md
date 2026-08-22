# Astro Cloudflare Conventions

Strict, portable conventions for Astro v5/6/7 projects deployed to Cloudflare Workers/Pages. These rules extend `core/rules/code.md`.

## 2026 Version Context

- **Astro**: v6 (stable) / v7 (current) — Cloudflare-owned since Jan 2026
- **Vite**: v8 + Rolldown (Rust bundler — use `rolldownOptions` instead of `rollupOptions`)
- **TailwindCSS**: v4 CSS-first (no `tailwind.config.js`)
- **Node.js**: 22+ required

## 1. Component Architecture (Astro Islands)

To maximize performance, enforce **Zero-JS-by-default** architecture:
- **Default Extension:** All static or server-rendered layouts MUST use `.astro`.
- **Interactive Components:** React/Preact (`.tsx`) ONLY for interactive islands requiring client-side JS.
- **Hydration Directives:** Explicitly declare hydration strategy: `client:load`, `client:visible`, `client:idle`.
- **PROHIBITED:** Never use `client:only` unless SSR is strictly impossible for that component.
- **React 19:** Fully compatible with Astro Islands — use standard directives.

## 2. Cloudflare Bindings (2026 API)

**Astro 6+:** Access bindings via direct `env` parameter — `Astro.locals.runtime.env` is deprecated:

```ts
// ✅ Astro 6+ / Cloudflare Workers (CORRECT)
export const GET: APIRoute = async ({ locals }) => {
  const { env } = locals.runtime;  // or direct in Workers context
  const data = await env.MY_KV.get("key");
  const obj = await env.MY_R2.get("file.txt");
  const result = await env.MY_D1.prepare("SELECT 1").first();
  return new Response(JSON.stringify(data));
};

// ❌ DEPRECATED (Astro 5 pattern)
// Astro.locals.runtime.env.MY_KV
```

- **Wrangler config:** Always use `wrangler.jsonc` at project root.
- Set `compatibility_date = "2026-08-22"` (or latest).
- For Workers: update `main` to `dist/_worker.js/index.js` in `wrangler.jsonc`.

## 3. TailwindCSS v4 Config (Breaking Change from v3)

```bash
# Migrate existing projects automatically
npx @tailwindcss/upgrade
```

**New setup** (`astro.config.mjs`):
```js
import tailwindcss from '@tailwindcss/vite';
export default defineConfig({
  vite: { plugins: [tailwindcss()] }
});
```

**CSS** (`src/styles/global.css`):
```css
@import "tailwindcss";

@theme {
  --color-brand: #1B2A4A;
  --color-accent: #2BA5B5;
  --font-body: 'Outfit', sans-serif;
}
```

**Rules:**
- `tailwind.config.js` → delete it; use `@theme {}` blocks.
- `@astrojs/tailwind` integration → deprecated for v4; remove it.
- `@tailwindcss/typography` → import via `@import "tailwindcss/typography"` in CSS.

## 4. Content Layer API (Astro 6 — Mandatory)

Legacy `/src/content/` config removed. Use `src/content.config.ts`:

```ts
// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

export const collections = {
  posts: defineCollection({
    loader: glob({ pattern: '**/*.{md,mdx}', base: './src/data/posts' }),
    schema: z.object({
      title: z.string(),
      date: z.coerce.date(),
      description: z.string(),
    }),
  }),
};
```

- Use `getEntry()` NOT deprecated `getEntryBySlug()`.
- All loaders run in **parallel** at build time.
- Remove `experimental.contentLayer` flags (now default in Astro 6).

## 5. Project Structure

```
src/
├── assets/           ← Static assets (Astro-processed, images optimized at build)
├── components/       ← Reusable .astro and framework components (.tsx, .jsx)
├── content.config.ts ← Content Layer collection definitions (Astro 6+)
├── data/             ← TypeScript/JSON data files (products, config, content)
├── layouts/          ← Page layouts (BaseLayout.astro, etc.)
├── pages/            ← File-based routing (.astro, .ts for API routes)
│   └── api/          ← Server-side API endpoints (Cloudflare Workers)
├── styles/           ← Global CSS / TailwindCSS v4 imports + @theme blocks
└── env.d.ts          ← Astro environment type declarations
public/               ← Static files served as-is (favicon, robots.txt, media)
wrangler.jsonc        ← Cloudflare Workers/Pages config (single source of truth)
```

## 6. Build & Deploy Lifecycle

- `npm run dev` — local dev server (Vite 8 + Rolldown).
- `npm run build` — production build.
- `npm run preview` — build + Wrangler local preview.
- `npm run deploy` — build + deploy via Wrangler.
- GitHub Actions CI/CD on `main` branch push.

**Vite 8 + Rolldown migration:**
- Replace `rollupOptions` → `rolldownOptions` in `astro.config.mjs`.
- Replace `esbuild` plugin usage with Rolldown-native equivalents.
- Expected: 10–30× faster builds, 30–50% faster cold starts.

## 7. Quality Gates

- `npm run check` — `astro check` + ESLint + Prettier.
- Fix before commit: `npm run fix`.
- TypeScript strict mode enabled.
- No `any` types in API routes or data files.

## 8. Security

- Secrets in `.dev.vars` (local) / Cloudflare Dashboard secrets (production).
- Never commit `.dev.vars` — it is in `.gitignore`.
- Turnstile server-side validation at every form API endpoint.
- Resend API key server-side only — never in client bundles.
