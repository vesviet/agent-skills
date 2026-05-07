---
name: develop-icm-feature
description: Develop features for the ICM Factory Direct main site — an Astro v5 B2B manufacturing catalog on Cloudflare Pages. Use when adding pages, product data, components, contact forms, or R2 integrations in this project.
---

# Develop ICM Feature

Use this skill when building or modifying features in the ICM Factory Direct corporate website.

**Prerequisites:** Read `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md` for generic Astro patterns.

## Core Rules

- Follow all rules from `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md`
- Follow all rules from `overlays/icm-main/rules/icm-project-rules.md`
- Product data lives in `src/data/products.ts` — typed TypeScript, never loose JSON
- Contact form backend at `src/pages/api/contact.ts` — Turnstile + Resend
- R2 assets accessed via `Astro.locals.runtime.env.icm_documents`
- B2B professional tone in all copy and component text

## Suggested Process

### 1. Identify scope — new page, component, data update, or API endpoint
### 2. Read existing patterns in `src/pages/`, `src/components/`, `src/data/`
### 3. Implement matching established conventions
### 4. Run `npm run check` before commit

## Checklist

- [ ] correct location in `src/` structure
- [ ] product data typed in `src/data/products.ts`
- [ ] SEO metadata (title, description) on every page
- [ ] Tailwind utility classes, design tokens from `tailwind.config.js`
- [ ] R2 bindings accessed server-side only
- [ ] secrets in `.dev.vars`, never in client code
- [ ] `npm run check` passes (astro check + eslint + prettier)

## Related Skills

- **review-code**: review against Astro and project conventions
- **navigate-service**: understand the codebase structure
- **commit-code**: commit with proper conventions
- **troubleshoot-service**: debug build or deploy issues
- **write-documentation**: update product catalog docs
