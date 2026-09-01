# Optimize SEO — Reference

Detailed process and checklist extracted from `SKILL.md` to keep the main
file under 200 lines. Load this file when running the full 5-step
optimize-seo workflow, when auditing a page across all four axes, or
when training a new SEO analyst.

## Suggested Process

### 1. Frame

Capture:

- audience and business outcome (lead, trust, education)
- primary and secondary keywords
- locale and competing pages on the same site
- search intent classification: informational, commercial, navigational, or transactional
- YMYL-adjacent flag (yes/no)

### 2. Research (SERP + AI-focused)

- Review top SERP titles, snippets, and common H2 patterns (lightweight passes — not full Researcher depth).
- Note content gaps versus intent (informational, commercial, navigational).
- Record cannibalization risk against existing URLs.
- **AI search check**: search primary keyword in Google AI Overview, Perplexity, and ChatGPT to observe citation patterns, source types, and answer formats used.
- **Information gain analysis**: identify what existing top results cover and what unique value this content can add.
- Note **entity coverage**: which entities (brands, concepts, people, locations) appear consistently in AI answers.

### 3. Topical Authority Assignment

- Identify the **pillar page** this content belongs to (or flag need to create one).
- Assign **cluster position**: pillar, supporting, or supplementary.
- Specify **content freshness type**: new_topic, evergreen_refresh, data_update, or experience_addition.
- List key **entities** the content must cover for topical completeness.

### 4. Brief Or Audit

**Brief path:** outline H2s with answer-first guidance, FAQ, internal links, word-count band, out-of-scope topics, GEO/AEO fields, schema requirements, E-E-A-T gates → `seo-content-brief.json`.

Required GEO/AEO fields in brief:

- answer-first block (≤60 words) for each H2
- query fan-out list (3–5 sub-questions)
- answer format per section (definition, table, steps, bullets)
- fact density target
- schema types: Article, FAQPage, HowTo, etc.
- experience proof type required

**Audit path:** score the page on four axes out of 100 — overall, SEO, AEO, readability — using pass bands: 85–100 strong (publish-ready), 70–84 acceptable, 50–69 needs work, below 50 do-not-publish. Rank issues as Blocking / Important / Follow-Up with exact fix instructions, and report the projected score once fixes are applied so prioritization is data-driven → `seo-audit-report.json` + updated `seo-metadata.json` when ready to publish.

AI extractability audit elements:

- TL;DR / direct-answer block present near the top (2–3 sentences answerable without context)
- answer-first structure present (yes/no)
- heading hierarchy clean (H1→H2→H3)
- fact density sufficient (verifiable data points per section)
- schema markup present and valid
- FAQ block carries at least 4 entries when present
- AI bot crawlability (robots.txt check)
- content uniqueness / information gain vs SERP competitors

### 5. Hand Off

- to **Content Writer** with brief, metadata draft, and E-E-A-T requirements
- to **Task Planner** when board order, topic mix, or pillar–cluster balance must change
- to **Frontend/DevOps** for technical SEO implementation tickets including schema specifications
- to **Data Analyst** when metric definitions for GSC comparisons or AI citation tracking need formalization

## Detailed Checklist

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
