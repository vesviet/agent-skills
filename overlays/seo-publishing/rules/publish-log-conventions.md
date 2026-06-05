# Publish Log Conventions — plan/baiviet/publish-log.md

Append-only log for planned vs actual publishing, AI visibility tracking, and topical authority monitoring. SEO Analyst or Task Planner updates after each publish or carry-over. Updated for 2025–2026 SEO standards.

## Location

Default: `plan/baiviet/publish-log.md` (workspace root; set `PLAN_BAIVIET_ROOT` if different).

## Entry Format

Newest dates first. One section per calendar day:

```markdown
## YYYY-MM-DD
- Lease:
  - Topic:
  - Primary keyword:
  - Slug:
  - Internal links:
  - Pillar page: [URL of pillar this article supports]
  - Cluster position: [supporting | supplementary]
  - Schema types: [Article | FAQPage | HowTo | Product]
  - GEO ready: [✅ | ❌] (answer-first + query fan-out + schema specified)
  - Experience proof: [type used: original_photo | firsthand_account | documented_test | expert_interview]
  - Status: Drafted | Draft Ready | Published | Carry-over
- May lanh:
  - Topic:
  - Primary keyword:
  - Slug:
  - Internal links:
  - Pillar page: [URL of pillar this article supports]
  - Cluster position: [supporting | supplementary]
  - Schema types: [Article | FAQPage | HowTo | Product]
  - GEO ready: [✅ | ❌]
  - Experience proof: [type used]
  - Status: Drafted | Draft Ready | Published | Carry-over
```

## Field Rules

| Field | Rule |
| ----- | ---- |
| Topic | Working headline or plan topic line |
| Primary keyword | Exact phrase targeted in title/H1/meta |
| Slug | Repo-relative path under src/data (e.g. post/guides/slug.mdx) |
| Internal links | Comma-separated paths or slugs (minimum 3 when published) |
| Pillar page | URL of the pillar page this cluster article links to |
| Cluster position | supporting or supplementary |
| Schema types | Schema types specified in brief (Article, FAQPage, HowTo, Product) |
| GEO ready | ✅ if answer-first + query fan-out + schema in brief; ❌ otherwise |
| Experience proof | Type of firsthand evidence included |
| Status | Use Carry-over when draft missed publish window |

## After Publish

- Set Status to **Published** only after live URL or repo merge confirmed by user
- Cross-check slug matches deployed route
- If audit changed metadata, note "meta updated per seo-audit-report" in Topic line or a Note bullet

## Weekly Rollup

Every 7 days, Task Planner adds a short summary block at top of publish-log or in plan file:

```markdown
## Week YYYY-MM-DD — YYYY-MM-DD rollup

### Publishing Summary
- Lease published: N / planned: M
- May lanh published: N / planned: M
- Carry-overs:

### Traditional SEO
- GSC notes (from SEO/Data Analyst):
- New keywords gained:
- CTR changes:

### AI Visibility Check
- Google AI Overview presence (top 3 keywords per site):
  - Lease: [keyword1: ✅/❌, keyword2: ✅/❌, keyword3: ✅/❌]
  - May lanh: [keyword1: ✅/❌, keyword2: ✅/❌, keyword3: ✅/❌]
- Perplexity citation check (top 3 keywords per site):
  - Lease: [keyword1: cited/not cited, keyword2: cited/not cited, keyword3: cited/not cited]
  - May lanh: [keyword1: cited/not cited, keyword2: cited/not cited, keyword3: cited/not cited]
- ChatGPT/SearchGPT spot-check (1–2 keywords per site):
- Citation gaps (competitors cited, we are not):
- AI visibility action items for next week:

### Topical Authority
- Pillar–cluster balance (per site):
  - Lease: [pillar pages with <3 supporting articles]
  - May lanh: [pillar pages with <3 supporting articles]
- Pillar pages needing updates:
- Information gain quality (any articles that were merely restating SERP results?):

### Next Week
- Next week focus clusters:
- Priority topics for AI citation gaps:
- Schema implementation needs for Frontend:
```

## Link To Contracts

When machine-readable tracking is required, mirror published rows into `seo-weekly-board.json` `entries[].status` = `published`.
