---
name: develop-golf-feature
description: Develop features for the Golf ICM niche catalog — an Astro v5 golf apparel site on Cloudflare Pages. Use when adding pages, gallery content, MDX articles, or components for the golf apparel niche.
---

# Develop Golf Feature

Use this skill when building or modifying features in the Golf ICM catalog site.

**Prerequisites:** Read `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md` for generic Astro patterns.

## Core Rules

- Follow all rules from `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md`
- Follow all rules from `overlays/golf-icm/rules/golf-project-rules.md`
- Gallery data auto-generated via `generate_galleries.mjs` — do not edit `generated_galleries.json` manually
- MDX articles use `@tailwindcss/typography` for body styling
- Brand tone: premium, sophisticated, golf/resort focused

## Suggested Process

### 1. Identify scope — page content, gallery update, MDX article, or component
### 2. Read existing patterns in `src/pages/`, `src/components/`
### 3. For galleries: run `node generate_galleries.mjs` after adding images to `public/`
### 4. Run `npm run check` before commit

## Checklist

- [ ] correct location in `src/` structure
- [ ] gallery data generated via script, not manual JSON edits
- [ ] MDX frontmatter matches existing articles (title, date, description, image, tags)
- [ ] SEO metadata on every page
- [ ] brand tone matches golf/resort positioning
- [ ] `npm run check` passes

## Related Skills

- **review-code**: review against Astro and project conventions
- **navigate-service**: understand the codebase structure
- **commit-code**: commit with proper conventions
- **write-documentation**: update content or catalog documentation
- **troubleshoot-service**: debug build or deploy issues
