---
name: optimize-seo
description: Research search intent, define keywords, produce SEO content briefs, audit on-page elements, optimize for AI search visibility (GEO/AEO), specify structured data, enforce E-E-A-T quality gates, and deliver metadata and recommendations without owning full article drafting or technical deployment. Use when planning publishable content, reviewing drafts before release, mapping internal links, interpreting Search Console signals, or ensuring AI citation readiness.
---

# Optimize SEO

Use this skill for **search and content-structure** work — not for writing long-form copy (Content Writer) or implementing sitemaps/redirects in production (Frontend/DevOps).

## Core Rules

### Traditional SEO Foundations

- define **search intent** and **primary keyword** before recommending titles or outlines
- classify intent explicitly: informational, commercial, navigational, or transactional
- separate **evidence** (SERP snippets, GSC exports, crawlable page facts) from **recommendations**
- document **internal link targets** with anchor rationale and destination paths
- enforce on-page limits: title tag ≤ 60 chars, meta description ≤ 160 chars unless repo rules differ
- check **keyword cannibalization** against recent publishes on the same site (default: 7-day window when a topic board exists); when overlap is confirmed, name the resolution tactic explicitly — consolidate into one authoritative page, differentiate search intent, canonical to the primary URL, 301-redirect the weaker page, and clean up competing anchors
- prevent cannibalization recurrence with **keyword-to-page mapping**: exactly one primary keyword per page plus a pre-publish overlap check against the site inventory
- track **Share of Model (SoM)** alongside traditional CTR — measure how often and how accurately the brand/content is cited in Google AI Overviews, Perplexity, and ChatGPT Search using AI visibility tooling (Otterly, RankScale, or manual spot-checks)
- mandate a **30–60 day rolling freshness review** for core commercial and informational pillar pages — AI search engines heavily weight recently-updated content when retrieving citations; queue pages by decay signal first: rankings dropped >3 positions, statistics older than 2 years, or declining high-traffic URLs. On refresh, update modified/publish dates in schema, replace outdated stats and examples, and re-check internal links pointing at changed sections
- do not guarantee rankings or AI citation placement; recommend changes tied to observable gaps
- escalate **technical SEO** (canonical, schema markup, redirects, Core Web Vitals fixes) with a clear engineering brief
- use repo overlays under overlays/lease-content and overlays/vesviet-content when site-specific slug or frontmatter rules apply
- use overlays/seo-publishing for dual-site Lease + May lanh sprint boards under plan/baiviet

### GEO / AEO — AI Search Visibility

This is the canonical GEO/AEO standard for the pack — `write-article` implements these same rules during drafting and must stay in sync with this section.

Optimize for three search discovery layers simultaneously:

| Layer | Goal | Key tactic |
| ----- | ---- | ---------- |
| **SEO** (blue links) | Organic traffic | Keywords, backlinks, on-page quality |
| **AEO** (Answer Engine Optimization) | Featured snippets, direct answers | Answer-first format, FAQ blocks, step lists |
| **GEO** (Generative Engine Optimization) | AI citations (Google AI Overviews, Perplexity, ChatGPT, Bing AI) | Fact density, entity clarity, schema, source credibility |

Rules for GEO/AEO:

- mandate **answer-first structure**: open each H2 section with a direct answer (≤60 words) before elaboration
- include **query fan-out list**: 3–5 related sub-questions from People Also Ask + LLM suggestions
- specify **answer format** per section: definition, comparison table, numbered steps, or bullet list — matching the format AI engines prefer for the query type
- require **fact density**: minimum 3 verifiable data points per 500 words (statistics, expert quotes, specific numbers)
- verify **AI bot crawlability**: robots.txt must allow OAI-SearchBot, PerplexityBot, ClaudeBot, BingBot — flag blocks in audits
- measure citations **per engine, not in aggregate**: Perplexity emits numbered `[1][2]` sources while ChatGPT uses inline mentions and footnotes — sample each engine separately, tag AI-referred traffic with dedicated UTM parameters, and track "according to \<brand\>" phrasing as the citation proxy
- treat **entity consistency** as a GEO lever: identical brand facts (name, positioning, credentials) across the site, author profiles, and third-party listings consolidate entity recognition
- do not claim AI citation placement as guaranteed — present GEO/AEO as structural best practices

### Topical Authority & Entity SEO

- assign each article to a **pillar–cluster position**: pillar, supporting, or supplementary
- link each article explicitly to its **pillar page URL**
- document **information gain**: what this content adds beyond top-3 SERP results (unique data, firsthand experience, original analysis)
- specify **content freshness type**: new_topic, evergreen_refresh, data_update, or experience_addition
- define key **entities** (people, brands, concepts, locations) that must appear for topical coverage
- recommend **schema types** for each article: Article, FAQPage, HowTo, Product, BreadcrumbList, Person (author), Organization
- use stable `@id` patterns for entity references (e.g. `https://site.com/#organization`)

### Internal Linking Discipline

Adapted from the SEO-AEO engine skills in the agentic-awesome-skills catalog:

- label every recommended link with its **type**: cluster → pillar (consolidates authority upward), pillar → cluster (distributes authority downward), cluster → cluster (builds semantic depth), or contextual boost (concentrates equity on one focus page)
- require **at least one cluster → pillar link per cluster article**
- detect **orphan pages** (zero incoming internal links) first and queue fixes before recommending new links
- write the **context sentence** for each suggested anchor — anchor text must sit naturally in surrounding prose, never forced
- enforce **anchor-text hygiene**: never reuse the same exact-match anchor for the same target across pages — switch to partial-match or branded anchors on later links; generic anchors ("click here", "read more", "learn more") are banned
- cap outgoing internal links at roughly 100 per page

### E-E-A-T Quality Gates

- require **experience proof signals**: original photos, firsthand accounts, documented tests/comparisons, expert interviews, or case studies
- specify **author entity requirements**: link to author profile page with Person schema, credentials, and relevant publications
- flag **YMYL-adjacent content** (financial, health, safety, legal) for elevated research depth and human review
- mandate **trust signals**: source citations with links, contact information, policy pages, verifiable claims
- enforce **claim policy**: every major factual claim must have a credible source or specific data point
- do not treat a single SERP pass as sufficient for YMYL or regulated topics — escalate depth to Researcher

## When to Use

- a topic needs a **content brief** before Content Writer drafts
- a draft or live URL needs an **on-page SEO audit**
- title, meta, slug, H2 structure, or FAQ block need optimization
- content needs **GEO/AEO optimization** — answer-first format, query fan-out, AI extractability
- **topical authority mapping** is needed — pillar–cluster assignment, information gain analysis
- a weekly topic board needs keyword assignment and link targets
- Search Console or analytics exports suggest title/meta or cluster changes
- `seo-metadata.json`, `seo-content-brief.json`, or `seo-audit-report.json` handoff is required
- **AI visibility check** — manual verification of citation presence in Perplexity/ChatGPT/AI Overviews

## Suggested Process

### 1. Frame Intent

Capture:

- target URL or planned slug
- audience and business outcome (lead, trust, education)
- primary and secondary keywords
- locale and competing pages on the same site
- search intent classification: informational, commercial, navigational, or transactional
- YMYL-adjacent flag (yes/no)

### 2. Research (SERP + AI-focused)

- review top SERP titles, snippets, and common H2 patterns (lightweight passes — not full Researcher depth)
- note content gaps versus intent (informational, commercial, navigational)
- record cannibalization risk against existing URLs
- **AI search check**: search primary keyword in Google AI Overview, Perplexity, and ChatGPT to observe citation patterns, source types, and answer formats used
- **information gain analysis**: identify what existing top results cover and what unique value this content can add
- note **entity coverage**: which entities (brands, concepts, people, locations) appear consistently in AI answers

### 3. Topical Authority Assignment

- identify the **pillar page** this content belongs to (or flag need to create one)
- assign **cluster position**: pillar, supporting, or supplementary
- specify **content freshness type**: new_topic, evergreen_refresh, data_update, or experience_addition
- list key **entities** the content must cover for topical completeness

### 4. Brief Or Audit

**Brief path:** outline H2s with answer-first guidance, FAQ, internal links, word-count band, out-of-scope topics, GEO/AEO fields, schema requirements, E-E-A-T gates → `seo-content-brief.json`

Required GEO/AEO fields in brief:
- answer-first block (≤60 words) for each H2
- query fan-out list (3–5 sub-questions)
- answer format per section (definition, table, steps, bullets)
- fact density target
- schema types: Article, FAQPage, HowTo, etc.
- experience proof type required

**Audit path:** score the page on four axes out of 100 — overall, SEO, AEO, readability — using pass bands: 85–100 strong (publish-ready), 70–84 acceptable, 50–69 needs work, below 50 do-not-publish. Rank issues as Blocking / Important / Follow-Up with exact fix instructions, and report the projected score once fixes are applied so prioritization is data-driven → `seo-audit-report.json` + updated `seo-metadata.json` when ready to publish

AI extractability audit elements:
- TL;DR / direct-answer block present near the top (2–3 sentences answerable without context)
- answer-first structure present (yes/no)
- heading hierarchy clean (H1→H2→H3)
- fact density sufficient (verifiable data points per section)
- schema markup present and valid
- FAQ block carries at least 4 entries when present — fewer signals shallow coverage to extraction systems
- AI bot crawlability (robots.txt check)
- content uniqueness / information gain vs SERP competitors

### 5. Hand Off

- to **Content Writer** with brief, metadata draft, and E-E-A-T requirements
- to **Task Planner** when board order, topic mix, or pillar–cluster balance must change
- to **Frontend/DevOps** for technical SEO implementation tickets including schema specifications
- to **Data Analyst** when metric definitions for GSC comparisons or AI citation tracking need formalization

## Checklist

### Traditional SEO
- [ ] search intent classified (informational/commercial/navigational/transactional) and primary keyword explicit
- [ ] secondary keywords listed (typically 2–4)
- [ ] internal link targets named (minimum 3 when site baseline requires it)
- [ ] title and meta within length limits and aligned with keyword
- [ ] cannibalization check documented
- [ ] facts separated from recommendations
- [ ] technical items escalated, not silently implemented in prod

### GEO / AEO
- [ ] answer-first block present (≤60 words after H2)
- [ ] query fan-out list included (3–5 sub-questions from PAA + LLM)
- [ ] answer format specified per section
- [ ] fact density requirement documented
- [ ] AI bot crawlability verified (OAI-SearchBot, PerplexityBot, ClaudeBot, BingBot)
- [ ] citation sampling done per engine (numbered vs inline styles noted), not in aggregate
- [ ] audit scored on four axes with projected post-fix score reported

### Internal Linking
- [ ] every link recommendation labeled by type (cluster→pillar / pillar→cluster / cluster→cluster / contextual boost)
- [ ] orphan pages detected and queued before new links proposed
- [ ] no duplicated exact-match anchors to the same target; no generic anchor text
- [ ] context sentence written for each anchor suggestion
- [ ] cluster articles each carry at least one cluster → pillar link

### Topical Authority & Entity
- [ ] pillar page URL assigned; cluster position documented
- [ ] information gain clearly stated
- [ ] content freshness type specified
- [ ] key entities listed for topical coverage
- [ ] schema types recommended for Frontend (Article, FAQPage, HowTo, etc.)

### E-E-A-T
- [ ] experience proof type specified (original_photo, firsthand_account, documented_test, expert_interview, case_study)
- [ ] author entity and profile linkage documented
- [ ] YMYL-adjacent flag set when applicable
- [ ] trust signals required (source citations, contact info, policy page)
- [ ] claim policy stated

## Output Contracts

When completing search intent analysis, keyword planning, on-page audits, or multi-site editorial scheduling, emit:

- **`contracts/schemas/seo-audit-report.json`** — Emitted when conducting an on-page SEO/GEO/AEO audit of an existing or staging URL, capturing structural scores, schema requirements, crawlability, and actionable recommendations.
- **`contracts/schemas/seo-content-brief.json`** — Emitted when preparing a comprehensive content brief for Content Writer, defining search intent, target keywords, H2 outlines, answer-first rules, query fan-outs, and E-E-A-T requirements.
- **`contracts/schemas/seo-metadata.json`** — Emitted when delivering publish-ready title tags, meta descriptions, canonical URLs, Open Graph tags, and structured schema specifications.
- **`contracts/schemas/seo-weekly-board.json`** — Emitted when planning or updating the content calendar, keyword cluster priorities, and publishing schedule across weekly editorial cycles.

Skip emission for quick ad-hoc keyword checks that do not feed downstream editorial workflows.

## Related Skills

- **conduct-research**: deeper domain or competitor context when SERP scan is insufficient
- **analyze-business-requirements**: align SEO goals with business rules and actors
- **analyze-data**: formal GSC/CTR tables and AI citation tracking when SEO Analyst needs verified baselines
- **write-documentation**: metric catalogs or SEO playbooks for a site
- **agent-delegation**: delegate drafting to Content Writer or technical work to Frontend

