---
name: write-article
description: Plan, research, outline, and draft long-form articles and blog posts with explicit evidence discipline, answer-first structure, GEO/AEO execution, information gain quality gates, E-E-A-T experience signals, and SEO-brief alignment. Use for narrative content, guides, reviews, and announcements—not for API runbooks or pure technical reference docs.
---

# Write Article

Use this skill with the **Content Writer** role when the deliverable is a publishable article (Markdown, MDX, or Hugo/Astro content files). Articles must optimize for three discovery surfaces simultaneously: traditional search (SEO), direct-answer engines (AEO), and generative AI citation (GEO).

The specific thresholds below (answer-first ≤60 words, fact density, E-E-A-T proof types) are the same GEO/AEO/E-E-A-T standard defined in `optimize-seo`'s Core Rules — this skill is where a Content Writer **implements** that standard while drafting, not a second definition of it. If the two ever disagree, `optimize-seo` is the source of truth; update rules there first, then mirror the change here.

## When to Use

- drafting guides, reviews, or announcements
- narrative long-form content (not API runbooks)
- aligning with an SEO brief + GEO/AEO
- applying E-E-A-T and information-gain gates

## Core Rules

### Research & Evidence Integrity
- clarify audience, goal, CTA, and channel before drafting
- when research is required, run **at least three to four distinct passes** (different questions, sources, or angles) unless Researcher already delivered research-report.json
- when sources are supplied, synthesize only from that material — do not duplicate research
- separate verified facts, attributed claims, and author judgment
- follow seo-content-brief.json when SEO Analyst provided a brief; do not invent keyword or link strategy
- apply site overlay skills (lease-content, vesviet-content) for frontmatter, paths, and schema
- produce `contracts/schemas/content-handoff.json` when machine handoff is required

### Answer-First Structure (AEO/GEO mandatory)
- open each H2 section with a **direct answer ≤60 words** before elaboration — this is mandatory for informational and commercial queries
- do not bury the answer: eliminate slow-burn introductions that delay the answer past paragraph 2–3
- mirror H2 headings to natural language queries: "How to...", "What is...", "Why does..."
- H3 subheadings address follow-up sub-questions within each H2 cluster

### Information Gain (Hard Quality Gate)
- every article must document what it adds beyond top-3 SERP results: this is a quality gate, not optional
- acceptable information gain types: original_data, firsthand_account, local_insight, expert_interview, unique_framework, contrarian_perspective
- **no skyscraper regurgitation**: if the draft only paraphrases existing results, it fails the gate — flag and escalate to user or Researcher
- use AI tools for research and outlining, but inject ≥30% unique human insight, local knowledge, or original data

### Fact Density
- minimum **3 verifiable data points** (statistics, specific numbers, sourced expert quotes) per 500 words
- cite primary sources or explicitly attribute each significant claim
- write **citation-ready sentences**: tight, factual, ≤25 words — making them easy for AI engines to extract and quote
- flag unverified claims rather than inventing detail

### Scanability & Machine Readability
- preferred sentence length: **≤20 words** for body text; vary for rhythm
- preferred paragraph length: **2–4 lines** — one idea per paragraph
- use **bullet points** for unranked lists; **numbered lists** for sequential steps; **comparison tables** for feature/price/spec data
- use **bolded lead-ins** in bullet lists for scannable entries
- FAQ block at end when brief/SERP requires it: format as `## FAQ` with `### Question?` subheadings for schema compatibility
- **JSON-LD structured data is mandatory**: every article must include `Article` schema with `datePublished`, `dateModified`, `author` (linked `Person` entity), and `publisher`; add `FAQPage` when a FAQ block is present; validate against Google Rich Results Test with zero warnings before publish
- **Atomic modular content**: structure each H2 section as a self-contained semantic module with a BLUF answer ≤60 words — RAG extractors retrieve passages atomically, not full articles; wall-of-text blocks over 100 words without subheadings fail RAG chunking

### E-E-A-T Experience Signals
- implement the experience proof type specified in the SEO brief: original photo, firsthand account, documented test result, expert interview excerpt, or case study
- do not fabricate experience signals — if you cannot produce the required proof type, flag the gap and escalate
- include author entity reference when brief specifies it
- include trust signals: source citations with links, verifiable claims, contact/policy references

## Research Depth Decision

| Situation | Action |
| --------- | ------ |
| User supplied complete sources or repo exemplars | No net-new research; document sources used; information gain via synthesis angle or firsthand context |
| Editorial article, familiar domain, moderate claims | **3–4 passes** logged in handoff; information gain required |
| Regulated, YMYL, novel market, or disputed facts | Delegate to **Researcher** first; draft from research-report.json; elevated E-E-A-T signals |
| SEO sprint with seo-content-brief.json | Brief supplies outline/links; research only for gaps; implement GEO/AEO fields |
| Technical behavior claims | Align with Technical Writer / engineering source-of-truth |
| Cannot achieve information gain from supplied sources | Flag to user; request additional sources or Researcher delegation |

## Suggested Process

### 1. Consume Inputs

- seo-content-brief.json, feature-ticket.json (BA positioning), or plan/baiviet daily plan
- research-report.json from Researcher when present
- repo exemplars and overlay rules
- **GEO/AEO fields from brief**: answer-first blocks, query fan-out list, answer format per section, fact density target, experience proof type

### 2. Information Gain Analysis

Before drafting, identify what unique value this article will provide:
- search top-3 SERP results for the primary keyword
- note what they cover and what gaps remain
- document the information gain type and source (firsthand data, local insight, expert quote, original framework)
- if no unique value is identifiable, escalate before drafting

### 3. Plan And Research

- fill Brief and Research sections in output template
- execute passes or cite Researcher synthesis
- document facts vs judgment
- gather materials for E-E-A-T experience signals

### 4. Outline And Draft

- map H2 structure to GEO/AEO brief: each H2 = direct answer block + elaboration
- match query fan-out sub-questions from brief to H3 subheadings or inline answers
- implement answer format per section (definition, steps, table, bullets) from brief
- implement internal links from brief or plan (minimum 3, prioritize high-value product/property pages)
- use overlay skill for MDX/Markdown file authoring
- inject experience signals, firsthand data, or original insight per E-E-A-T requirement

### 5. Scanability Pass

After drafting, review for:
- sentences mostly ≤20 words
- paragraphs 2–4 lines
- list-worthy content converted to bullets or numbered lists
- comparison data in tables
- bolded lead-ins for scannable bullet sets
- FAQ block added if brief or SERP requires it

### 6. Package Handoff

Emit content-handoff.json with:
- path, word_count, passes, unverified claims
- `information_gain`: unique value added and type
- `answer_first_implemented`: true/false
- `geo_aeo_fields_applied`: [answer-first, fan-out, answer_format, fact_density]
- `eeat_signals`: experience proof type + implemented (true/false)
- request SEO Analyst audit before publish when site requires it

### 7. Publish Sprint (optional)

When overlays/seo-publishing is active, after user confirms publish, append plan/baiviet/publish-log.md per overlay conventions including GEO ready status.

## AI-Assisted Drafting Protocol

When AI support is used anywhere in drafting, apply three disciplines — full templates live in [references/ai-drafting-playbook.md](references/ai-drafting-playbook.md):

1. **SERP-grounded outline loop**: build the prompt from all five components (role, brief, constraints, SERP reference, output format), ground on top-5 results, audit heading hygiene, iterate until depth — never one-shot the outline.
2. **Brief-driven images**: every generated image gets a structured brief (subject, composition, style, context, technical) plus kebab-case filename, 80-125 char alt-text, and `image_provenance` in the handoff.
3. **Five-component draft frame**: role + brief + signed-off structure + keyword policy + visual/media spec kept inline per drafting call; any missing component statistically produces boilerplate.

## Checklist

### Research & Evidence
- [ ] audience, goal, and format explicit
- [ ] research depth appropriate (3–4 passes, Researcher, or supplied-only documented)
- [ ] SEO brief consumed when required

### AI-Assisted Outline (when applicable)
- [ ] outline prompt included all five components (role, brief, constraints, SERP reference, output format)
- [ ] SERP top-5 grounding pass documented
- [ ] heading hygiene audit passed (one H1, intent-distinct H2s, real sub-question H3s)
- [ ] outline iterated until depth; iteration count captured in handoff
- [ ] information gain sections identified before drafting

### AI Image Generation (when applicable)
- [ ] each AI image has a structured brief (subject, composition, style, context, technical)
- [ ] alt-text drafted with keyword, 80–125 chars
- [ ] filename is kebab-case and descriptive
- [ ] image_provenance recorded for each asset
- [ ] provenance label set when YMYL-adjacent

### Information Gain & Originality
- [ ] information gain documented: what this content adds beyond top SERP results
- [ ] information gain type specified (original_data, firsthand_account, local_insight, etc.)
- [ ] information gain gate: passed (not a mere rewrite of existing results)
- [ ] AI-generated sections supplemented with unique human insight or original data

### GEO / AEO Execution
- [ ] answer-first block (≤60 words) after each H2
- [ ] query fan-out sub-questions from brief addressed in body
- [ ] answer formats applied per section (definition, steps, table, bullets)
- [ ] fact density met (≥3 verifiable data points per 500 words)
- [ ] FAQ block present when brief/SERP requires it
- [ ] heading hierarchy clean: H1 → H2 (query intent) → H3 (sub-questions)

### Scanability & E-E-A-T
- [ ] sentences mostly ≤20 words; paragraphs 2–4 lines
- [ ] bullets/numbered lists used for list-worthy content
- [ ] experience proof signal implemented when brief specifies it
- [ ] trust signals present (source citations, verifiable claims)
- [ ] overlay schema and paths validated against peers

### Handoff
- [ ] facts vs judgment separated
- [ ] content-handoff.json complete with GEO/AEO and information gain fields
- [ ] SEO audit requested before publish when required

## Output Contracts

When completing article drafting and preparing a publishable content handoff for editorial review, emit:

- **`contracts/schemas/content-handoff.json`** — Emitted upon completing an article or editorial piece, documenting word counts, target keywords, E-E-A-T signals, answer-first/GEO/AEO compliance, and information gain additions. Set `produced_by_role: content-writer`.

Skip emission for quick copy snippets or internal note drafting with no publishing workflow.

## Related Skills

- **write-documentation**: Structure and clarity patterns; technical README/runbooks belong with Technical Writer
- **write-tech-radar**: Radar-style technology assessments (Vesviet radar subtree)
- **analyze-business-requirements**: Align copy with business rules when BA supplied a ticket
- **meeting-review**: Resolve stakeholder conflicts before drafting sensitive claims
- **agent-delegation**: Delegate drafting or specialist work to other roles

> **Site-specific authoring skills** (Astro MDX for Lease/May lanh, Hugo for Vesviet/Learn) live in overlays — see `overlays/lease-content/` and `overlays/vesviet-content/` README for the skill names to activate.
