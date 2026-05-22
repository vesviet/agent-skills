# Publishing Cadence — Dual-Site SEO Sprint

Operational cadence for Lease in Vietnam and May Lanh Treo Tuong. Extends workspace publishing defaults and `plan/baiviet/publishing-cadence-defaults-checklist.md`.

## Sprint Modes

| Mode | Posts/day | Notes |
| ---- | --------- | ----- |
| Dual-site active | 2 | 1 Lease + 1 May lanh |
| Single-site | 1 | Other site carry-over or rest day |
| Delayed draft | 1 published | Publish on-time post; carry delayed topic to next day board |

## Time Windows (UTC+7)

| Phase | Window |
| ----- | ------ |
| Draft | 08:00–11:00 |
| Publish | 11:30–14:00 |

If one article slips, publish the other on schedule and mark the delayed item **Carry-over** on the board and publish log.

## Daily Runbook

1. Confirm sprint mode (dual vs single) and date on the 7-day board.
2. SEO Analyst: assign primary keyword, check 7-day cannibalization, produce briefs for today's posts.
3. Content Writer: draft from briefs inside the draft window.
4. SEO Analyst: audit draft → seo-audit-report.json and seo-metadata.json.
5. Publish inside publish window (user or publisher executes deploy).
6. **Content Writer** (or SEO Analyst) appends publish-log.md with topic, keyword, slug, internal links, status; set `publish_log_updated` in content-handoff.json.

## Per-Post SEO Baseline

Every post MUST document:

- 1 **primary keyword** and **2–4 secondary** keywords
- **1,400+ words** unless a shorter scoped update is explicitly approved in the brief
- **≥3 internal links** to relevant existing pages (product/property when high-value)
- **Meta description** ≤160 chars containing primary keyword
- Scannable **H2** structure; **FAQ** when SERP/intent expects it

## Weekly Review (every 7 days)

- Summarize planned vs published from publish-log.md
- Review Search Console: impressions, CTR, new queries (Data Analyst optional for tables)
- Lock next 7 topics with SEO Analyst using cluster mix rules in `site-mix-and-cannibalization.md`
- Update `plan/baiviet/plan-YYYY-MM-DD.md` or export `contracts/schemas/seo-weekly-board.json`

## Schema And Format Gate

Before marking **Published**:

- Lease post path under leaseinvietnam/src/data/post/ per collection conventions
- May lanh post path under maylanhtreotuong/src/data/post/
- Frontmatter valid per each repo src/content/config.ts
- Research-heavy posts: 3–4 research passes documented OR explicit use of supplied data noted in plan

## Anti-Patterns

- Publishing without publish-log entry
- Same primary keyword intent twice on one site within 7 days without documented exception
- Drafting before SEO brief when sprint overlay is active
- Skipping internal links to high-value property/product pages for a full week
