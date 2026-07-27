---
name: write-leaseinvietnam-maylanhtreotuong-data
description: Draft or update Astro Content Collection Markdown/MDX for the Lease in Vietnam and Máy Lạnh Treo Tường sites. Use when editing files under `/home/user/personalized/leaseinvietnam/src/data` or `/home/user/personalized/maylanhtreotuong/src/data`.
---

# Write Leaseinvietnam Maylanhtreotuong Data

Use this skill when posts, listings, or product pages must be added or revised in the Astro `src/data` trees below.

## Content Roots

| Site | Absolute data path | Collections (`src/content/config.ts`) |
|------|-------------------|----------------------------------------|
| Lease in Vietnam | `/home/user/personalized/leaseinvietnam/src/data` | `post`, `property` |
| Máy Lạnh Treo Tường | `/home/user/personalized/maylanhtreotuong/src/data` | `post`, `product` |

Both projects load `**/*.{md,mdx}` from those folders via Astro glob loaders; frontmatter must satisfy the Zod schemas in each repo’s `src/content/config.ts`.

## Core Rules

- **confirm schema before new fields**: `post` and `property` / `product` schemas differ; optional `metadata` blocks follow the shared `metadataDefinition()` shape (`metadata.description`, OpenGraph, etc.)
- **Lease in Vietnam posts** usually live under `post/YYYY-MM-DD/<slug>.mdx`; mirror the dated folder pattern when adding new posts unless the user specifies otherwise
- **Lease `post` schema** uses `.passthrough()` for layout-specific keys (e.g. `layout`, guide/radar fields)—copy the same pattern as sibling posts with the same template (`GuideLayout`, `MarketRadarLayout`, `ScamAlertLayout`, `NeighborhoodLayout`)
- **property** (lease) vs **product** (maylanh): use the correct numeric/string fields (`price`, `bedrooms`, `brand`, `model`, `hp`, `dataSources`, `bestFor`, `notFor`, …) and match units/currency conventions from neighboring files
- **MDX**: only add `import` lines (e.g. `PostCallToAction`) when comparable posts in that site already do; keep import paths exactly as in those files
- **dates**: use `publishDate` / `updateDate` / `priceCheckedDate` in ISO-like strings consistent with peers (`+07:00` or `Z` as used locally)
- **claims and specs**: for products and legal/rental content, ground statements in `dataSources`, official links, or user-provided research; flag uncertain specs instead of inventing them

## 2026 SEO & AI Governance Baselines

- **Content Length & Depth**: Informational guides (`post`) must target a minimum of 1,400+ words unless tightly scoped.
- **Internal Linking**: You must include at least 3 internal links. Specifically, link from informational posts to high-value commercial pages (`property` or `product`).
- **No Raw AI Hallucinations**: Do not inject generic filler, repetitive phrasing, or hallucinated facts. Rely strictly on multi-pass research and provided sources.

## Suggested Process

### 1. Select Repo And Collection

Pick leaseinvietnam vs maylanhtreotuong, then `post` vs `property` or `product`.

### 2. Read Schema And Exemplars

Open that repo’s `src/content/config.ts` and two or three recent files in the target folder; align frontmatter keys, optional `metadata`, and body structure.

### 3. Apply Content Writer Discipline

Use the active **Content Writer** role: multi-pass research when evidence is required; otherwise synthesize only from supplied data and existing patterns.

### 4. Author The File

Use `.mdx` for posts when JSX/components may appear; `.md` is common for property/product—match siblings. For lease posts in dated trees, create the `YYYY-MM-DD` directory when that is the established convention.

### 5. Validate Implicit Contracts

Check slug/file naming against how routes list pages, internal links use paths like `/bang-gia-...` or product slugs, and images use stable URLs or assets per local practice.

### 6. Leave Handoff Notes

List fields that need SME verification (prices, legal claims, model numbers) for the user or reviewer.

## Checklist

- [ ] edits target the correct absolute `src/data` root and collection type
- [ ] frontmatter matches `config.ts` and peers in the same folder
- [ ] lease posts use dated path layout when siblings do
- [ ] MDX imports and components match existing posts in that site
- [ ] prices, specs, and legal/rental claims are sourced or explicitly flagged
- [ ] internal links and slugs follow patterns used in nearby content
- [ ] SEO minimums met (1,400+ words, 3+ internal links to commercial pages)
- [ ] AI governance rules followed (zero raw hallucinations or generic filler)

## Related Skills

- **write-documentation**: clarity, structure, and checklist-style rigor for long guides
- **write-vesviet-learn-content**: sibling pattern for static-site Markdown in other personalized repos
- **analyze-business-requirements**: align rental/commerce copy with audience and compliance expectations
