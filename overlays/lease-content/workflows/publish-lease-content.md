# Publish Lease Content

Role: `content-writer`

Workflow for adding or updating content in the Lease in Vietnam and Máy Lạnh Treo Tường Astro sites. Use when publishing new posts, property listings, or product pages.

## Checklist

- [ ] **Step 1** — Identify target site and content type
- [ ] **Step 2** — Read schema and sibling content
- [ ] **Step 3** — Draft frontmatter
- [ ] **Step 4** — Write content body
- [ ] **Step 5** — Run local Astro build check
- [ ] **Step 6** — Review and commit

---

## Step 1 — Identify target site and content type

Role: `content-writer`

Confirm:
- **Site**: Lease in Vietnam (`leaseinvietnam`) or Máy Lạnh Treo Tường (`maylanhtreotuong`)?
- **Content type**: `post`, `property` (lease), or `product` (maylanh)?
- **File path**: follow dated folder pattern `src/data/post/YYYY-MM-DD/<slug>.mdx` for posts.

| Site | Data root | Collections |
|------|-----------|-------------|
| Lease in Vietnam | `src/data/` | `post`, `property` |
| Máy Lạnh Treo Tường | `src/data/` | `post`, `product` |

---

## Step 2 — Read schema and sibling content

Role: `content-writer`

1. Open `src/content/config.ts` — read the Zod schema for the target collection.
2. Open 1–2 sibling files in the same collection to match:
   - Frontmatter keys, date format, `dataSources` pattern
   - MDX import lines (only add imports already used by siblings)
   - Layout type (`GuideLayout`, `MarketRadarLayout`, etc. for lease posts)

**Do not add frontmatter fields not present in the schema** unless `passthrough()` is confirmed.

---

## Step 3 — Draft frontmatter

Role: `content-writer`

Use the schema-required fields first, then optional fields if available:

```mdx
---
title: ""
description: ""
publishDate: "YYYY-MM-DD+07:00"
updateDate: "YYYY-MM-DD+07:00"
# property / product specific fields below
# price, bedrooms, brand, model, hp, bestFor, notFor, dataSources ...
---
```

- Use `+07:00` timezone offset consistently (Vietnam local time).
- Ground specs and prices in `dataSources` array — flag uncertain values instead of inventing them.

---

## Step 4 — Write content body

Role: `content-writer`

1. Follow the tone and structure of sibling posts in the same site.
2. Use MDX components (`PostCallToAction`, etc.) only when already imported by sibling posts — copy the exact import path.
3. For legal/rental/product claims: cite `dataSources` or mark as approximate.
4. SEO: confirm `<title>` and `description` match search intent for the target keyword.

---

## Step 5 — Run local Astro build check

Role: `devops-engineer`

```bash
cd /path/to/site
npm run build
```

Fix any Zod schema validation errors before committing. Common errors:
- Missing required field → add it
- Wrong type (number vs string) → match schema
- Invalid date format → use ISO with `+07:00`

---

## Step 6 — Review and commit

Role: `content-writer`

1. Review rendered output locally (`npm run dev` → preview URL).
2. Confirm no broken links, missing images, or placeholder text.
3. Commit: `git add src/data/<path> && git commit -m "feat(content): add <slug>"`.
4. Push to trigger Cloudflare Pages deploy (or deploy manually via Wrangler).

**Stop** if build fails — do not commit broken content.
