---
name: develop-golf-feature
description: Develop features for the Golf ICM niche catalog — an Astro v5 golf apparel site on Cloudflare Pages. Use when adding pages, gallery content, MDX articles, or components for the golf apparel niche.
---

# Develop Golf Feature

Use this skill when building or modifying features in the Golf ICM catalog site.

**Prerequisites:** Read `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md` for generic Astro patterns.

## When to Use

- adding or restructuring pages under `src/pages/`
- adding images to a gallery or regenerating gallery data
- publishing MDX articles or catalog components
- debugging build failures specific to this site

## Core Rules

- Follow all rules from `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md`
- Follow all rules from `overlays/golf-icm/rules/golf-project-rules.md`
- Gallery data auto-generated via `generate_galleries.mjs` — do not edit `generated_galleries.json` manually
- MDX articles use `@tailwindcss/typography` for body styling
- Brand tone: premium, sophisticated, golf/resort focused

## Suggested Process

### 1. Identify scope

Classify the change as page content, gallery update, MDX article, or component; it determines the directories touched and whether gallery regeneration is needed.

### 2. Read existing patterns

Inspect neighboring files in `src/pages/`, `src/components/`, and existing MDX articles; mirror their frontmatter, imports, and styling before writing new code.

### 3. Implement and regenerate galleries

Make the change following project conventions. For galleries: add images to `public/`, then run `node generate_galleries.mjs` and commit the regenerated data.

### 4. Validate

Run `npm run check` before commit; fix type, Astro, and lint errors until clean.

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
