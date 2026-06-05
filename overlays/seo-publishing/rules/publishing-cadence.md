# Publishing Cadence — Dual-Site SEO Sprint

Operational cadence for Lease in Vietnam and May Lanh Treo Tuong. Extends workspace publishing defaults and `plan/baiviet/publishing-cadence-defaults-checklist.md`. Updated for 2025–2026 SEO standards including GEO/AEO optimization, E-E-A-T quality gates, and AI search visibility.

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

### Traditional SEO
- 1 **primary keyword** and **2–4 secondary** keywords
- **1,400+ words** unless a shorter scoped update is explicitly approved in the brief
- **≥3 internal links** to relevant existing pages (product/property when high-value)
- **Meta description** ≤160 chars containing primary keyword
- Scannable **H2** structure; **FAQ** when SERP/intent expects it

### GEO / AEO (AI Search Visibility)
- **Answer-first opening** (≤60 words) after each H2 section heading
- **Query fan-out**: 3–5 related sub-questions (from PAA + LLM suggestions) addressed within the article
- **Fact density**: minimum 3 verifiable data points per 500 words (statistics, expert quotes, specific numbers)
- **Answer format** specified per section: definition, comparison table, numbered steps, or bullet list

### Topical Authority
- **Pillar page** assigned — explicit link from cluster article to pillar
- **Information gain** documented: what this content adds beyond existing top SERP results
- **Content freshness type**: new_topic | evergreen_refresh | data_update | experience_addition

### E-E-A-T Quality Gates
- **Experience proof**: at least one signal per post — original photo, firsthand account, documented test/comparison, or expert interview
- **Author entity**: author name with link to profile page (Person schema recommended)
- **Trust signals**: source citations, verifiable claims, contact info

### Schema / Structured Data
- **Schema types** recommended in brief for Frontend: Article (always), FAQPage (when FAQ present), HowTo (when step-by-step), Product (when linking product pages)
- Schema implementation escalated to Frontend — SEO Analyst specifies types, Frontend implements JSON-LD

## Weekly Review (every 7 days)

### Traditional SEO Metrics
- Summarize planned vs published from publish-log.md
- Review Search Console: impressions, CTR, new queries (Data Analyst optional for tables)
- Lock next 7 topics with SEO Analyst using cluster mix rules in `site-mix-and-cannibalization.md`
- Update `plan/baiviet/plan-YYYY-MM-DD.md` or export `contracts/schemas/seo-weekly-board.json`

### AI Visibility Check (new)
- **Google AI Overviews**: search top 3 primary keywords from this week — note if site appears in AI Overview
- **Perplexity**: search top 3 primary keywords — note citation presence and competing sources
- **ChatGPT/SearchGPT**: spot-check 1–2 primary keywords for brand/site citation
- Document findings in weekly rollup section of publish-log.md
- Track **citation gaps**: keywords where competitors are cited but we are not → priority for next week content

### Topical Authority Review
- Verify pillar–cluster balance: each pillar page has ≥3 supporting articles with internal links
- Identify pillar pages that need new cluster content
- Check information gain: are published articles providing unique value vs SERP competitors?

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
- Publishing briefs without answer-first structure guidance for informational/commercial queries
- Skipping information gain analysis — producing content that merely restates existing SERP results
- Ignoring AI bot crawlability (OAI-SearchBot, PerplexityBot, ClaudeBot blocked in robots.txt)
- Omitting schema type recommendations when FAQ blocks or structured content are in the brief
- Never checking AI search presence — at least weekly manual check required
- Treating pillar–cluster mapping as optional — every article must have explicit cluster assignment
