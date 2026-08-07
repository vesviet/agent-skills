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
- check **keyword cannibalization** against recent publishes on the same site (default: 7-day window when a topic board exists)
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
- do not claim AI citation placement as guaranteed — present GEO/AEO as structural best practices

### Topical Authority & Entity SEO

- assign each article to a **pillar–cluster position**: pillar, supporting, or supplementary
- link each article explicitly to its **pillar page URL**
- document **information gain**: what this content adds beyond top-3 SERP results (unique data, firsthand experience, original analysis)
- specify **content freshness type**: new_topic, evergreen_refresh, data_update, or experience_addition
- define key **entities** (people, brands, concepts, locations) that must appear for topical coverage
- recommend **schema types** for each article: Article, FAQPage, HowTo, Product, BreadcrumbList, Person (author), Organization
- use stable `@id` patterns for entity references (e.g. `https://site.com/#organization`)

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

**Audit path:** score title, meta, headings, links, schema needs, **AI extractability** → `seo-audit-report.json` + updated `seo-metadata.json` when ready to publish

AI extractability audit elements:
- answer-first structure present (yes/no)
- heading hierarchy clean (H1→H2→H3)
- fact density sufficient (verifiable data points per section)
- schema markup present and valid
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

## Related Skills

- **conduct-research**: deeper domain or competitor context when SERP scan is insufficient
- **analyze-business-requirements**: align SEO goals with business rules and actors
- **analyze-data**: formal GSC/CTR tables and AI citation tracking when SEO Analyst needs verified baselines
- **write-documentation**: metric catalogs or SEO playbooks for a site
- **agent-delegation**: delegate drafting to Content Writer or technical work to Frontend
