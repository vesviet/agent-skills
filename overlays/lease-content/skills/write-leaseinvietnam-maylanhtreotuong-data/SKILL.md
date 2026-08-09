---
name: write-leaseinvietnam-maylanhtreotuong-data
description: Draft or update Astro Content Collection Markdown/MDX for the Lease in Vietnam and Máy Lạnh Treo Tường sites. Use when editing files under `leaseinvietnam/src/data` or `maylanhtreotuong/src/data` (paths relative to the workspace root).
---

# Write Leaseinvietnam Maylanhtreotuong Data

Use this skill when posts, listings, or product pages must be added or revised in the Astro `src/data` trees below.

## Content Roots

| Site | Data path (relative to workspace root) | Collections (`src/content/config.ts`) |
|------|-------------------|----------------------------------------|
| Lease in Vietnam | `leaseinvietnam/src/data` | `post`, `property` |
| Máy Lạnh Treo Tường | `maylanhtreotuong/src/data` | `post`, `product` |

Both projects load `**/*.{md,mdx}` from those folders via Astro glob loaders; frontmatter must satisfy the Zod schemas in each repo’s `src/content/config.ts`.

## Core Rules

- **confirm schema before new fields**: `post` and `property` / `product` schemas differ; optional `metadata` blocks follow the shared `metadataDefinition()` shape (`metadata.description`, OpenGraph, etc.)
- **Lease in Vietnam posts** usually live under `post/YYYY-MM-DD/<slug>.mdx`; mirror the dated folder pattern when adding new posts unless the user specifies otherwise
- **Lease `post` schema** uses `.passthrough()` for layout-specific keys (e.g. `layout`, guide/radar fields)—copy the same pattern as sibling posts with the same template (`GuideLayout`, `MarketRadarLayout`, `ScamAlertLayout`, `NeighborhoodLayout`)
- **property** (lease) vs **product** (maylanh): use the correct numeric/string fields (`price`, `bedrooms`, `brand`, `model`, `hp`, `dataSources`, `bestFor`, `notFor`, …) and match units/currency conventions from neighboring files
- **MDX**: only add `import` lines (e.g. `PostCallToAction`) when comparable posts in that site already do; keep import paths exactly as in those files
- **dates**: use `publishDate` / `updateDate` / `priceCheckedDate` in ISO-like strings consistent with peers (`+07:00` or `Z` as used locally)
- **claims and specs**: for products and legal/rental content, ground statements in `dataSources`, official links, or user-provided research; flag uncertain specs instead of inventing them

## 2026 GEO/AEO & E-E-A-T Standards (Leaseinvietnam)

- **GEO/AEO Answer-First**: Mandatory ≤60-word direct answer block immediately following H2 headings using the `<AnswerFirst>` component.
- **Fact Density**: Minimum 3 verifiable data points per 500 words.
- **E-E-A-T Experience Proof**: 
  - Neighborhood guides: Original photos or firsthand visit accounts.
  - Price/Market data: Documented research with citations.
  - Scam alerts: Anonymized real case studies.
  - Legal/Visa: Official government source links.
- **Internal Links**: At least 3 internal links to existing pages + 1 link to a commercial property/product page (Total ≥4).
- **Anti-Slop Gate**: Zero generic filler, repetitive phrasing, or meta-talk.

## Suggested Process

### 1. Select Repo And Collection
Pick leaseinvietnam vs maylanhtreotuong, then `post` vs `property` or `product`.

### 2. Apply the Correct Template (For leaseinvietnam posts)
Select one of the 4 core templates based on user request:
1. **Market Radar / Price Hub**: Uses `category: market-radar`. Focuses on data tables, district breakdowns, and specific price ranges.
2. **Comprehensive Guide**: Uses `category: guides`. Step-by-step processes, cost tables, red flags, and FAQs.
3. **Scam Alert / Trust Guide**: Uses `category: scam` or `trust-safety`. Requires TL;DR, "How It Works", Red Flags, and Recovery Steps.
4. **Neighborhood Guide**: Uses `category: neighborhood`. Focuses on lifestyle fit, rent prices, pros/cons, and transport.

### 3. Read Schema And Exemplars
Check `src/content/config.ts` and recent files. Ensure `title` ≤ 60 chars, `unique_angle` is set, and `anti_slop_gate: { gate_passed: true }` is present in frontmatter for leaseinvietnam posts.

### 4. Author The File
- Use `.mdx` for posts to allow `<AnswerFirst>` and other components.
- Do NOT use markdown blockquotes `> **Quick Answer:**` for summaries.
- Apply the Content Writer discipline: multi-pass research and anti-slop self-scan.

### 5. Validate Implicit Contracts
Check slugs, internal link paths, and ensure affiliate links use the `/go/partner` cloaking standard.

## Checklist

- [ ] Edits target the correct `src/data` root and collection type.
- [ ] Frontmatter matches `config.ts` (including `unique_angle`, `anti_slop_gate`, and `title` length).
- [ ] `<AnswerFirst>` component is used instead of blockquotes.
- [ ] Prices, specs, and legal/rental claims are sourced with E-E-A-T Experience Proof.
- [ ] Internal links (≥4) and affiliate links (max 2, via `/go/`) follow rules.
- [ ] SEO minimums met (1,400+ words, fact density targets achieved).

## Related Skills

- **write-documentation**: clarity, structure, and checklist-style rigor for long guides
- **write-vesviet-learn-content**: sibling pattern for static-site Markdown in other personalized repos
- **analyze-business-requirements**: align rental/commerce copy with audience and compliance expectations
