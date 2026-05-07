---
name: develop-sport-feature
description: Develop features for the Sport ICM niche catalog — an Astro v5 sportswear site on Cloudflare Pages. Use when adding pages, MDX articles, migrating WordPress content, or building components for the sportswear niche.
---

# Develop Sport Feature

Use this skill when building or modifying features in the Sport ICM catalog site.

**Prerequisites:** Read `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md` for generic Astro patterns.

## Core Rules

- Follow all rules from `overlays/astro-cloudflare/rules/astro-cloudflare-conventions.md`
- Follow all rules from `overlays/sport-icm/rules/sport-project-rules.md`
- WordPress migration via `clean_wp.mjs` — output as MDX
- MDX articles use `@tailwindcss/typography` for body styling
- Brand tone: dynamic, performance-driven, sportswear focused

## Suggested Process

### 1. Identify scope — page content, WP migration, MDX article, or component
### 2. Read existing patterns in `src/pages/`, `src/components/`
### 3. For WP migration: use `clean_wp.mjs` to transform content, then review output
### 4. Run `npm run check` before commit

## Checklist

- [ ] correct location in `src/` structure
- [ ] WP migrated content cleaned and validated
- [ ] MDX frontmatter matches existing articles (title, date, description, image, tags)
- [ ] SEO metadata on every page
- [ ] brand tone matches sportswear/activewear positioning
- [ ] `npm run check` passes

## Related Skills

- **review-code**: review against Astro and project conventions
- **navigate-service**: understand the codebase structure
- **commit-code**: commit with proper conventions
- **write-documentation**: update content or catalog documentation
- **troubleshoot-service**: debug build or deploy issues
