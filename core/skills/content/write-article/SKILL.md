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

## AI-Assisted Outline Protocol

When drafting with AI support, generate the outline through a **SERP-grounded iteration loop**, not a one-shot prompt. This is the discipline that separates SEO-grade outlines from AI boilerplate.

### Step 1 — Build the context-rich prompt

Construct the outline prompt with **all five components** before invoking the LLM:

```markdown
# Role
You are an experienced SEO content strategist and subject-matter editor,
skilled at extracting intent from SERP patterns and structuring long-form articles for both human readers and AI answer engines.

# Brief
- Topic: <working title / primary keyword>
- Primary search intent: [informational | commercial | transactional | navigational]
- Target audience: <persona, locale, expertise level>
- Tone & voice: <brand voice guide reference>
- Business goal / CTA:
- Information gain required: <what this article must add beyond top-3 SERP results>

# Constraints
- Length target: <word count or section count>
- Answer-first structure required: yes (≤60 words per section)
- E-E-A-T experience proof required: <type from brief>
- Internal link targets to include: <list from SEO brief>
- YMYL-adjacent: [yes/no]

# Reference SERP (top 5)
<summarize each: title, structure, what's good, what's missing>

# Output format requested
H1 → H2 sections with intent labels → H3 sub-questions per section → suggested answer format per section (definition / steps / table / bullets)
```

Without all five components the LLM will produce generic structure.

### Step 2 — SERP grounding pass

Before prompting, manually scan top 5–10 SERP results for the primary keyword and document:
- common H2 sections across the top 3 (these are table stakes — must cover)
- gaps where top results are thin, outdated, or missing firsthand signal (these are information-gain slots)
- the dominant content format winning for this intent (long-form guide, comparison, listicle, how-to)

The outline must include every "table stakes" section **plus at least one information-gain section** the top results do not have.

### Step 3 — Heading hygiene audit

After the LLM produces the outline, validate before drafting:

- [ ] exactly one H1 (matches page title intent)
- [ ] each H2 maps to a distinct sub-intent, not a rephrased variant of an adjacent H2
- [ ] H3 sub-headings are real sub-questions of their parent H2 — not topic shifts
- [ ] query fan-out sub-questions from the SEO brief are all assigned to an H3 or integrated into an H2
- [ ] no orphan headings (a heading whose section would not change the article's answer if removed)

### Step 4 — Iterate until depth, not length

If the outline is thin, **refuse to draft and re-prompt** with one of these targeted requests:

- "Add one H3 under each H2 that addresses a follow-up question a user would ask after reading the H2 answer."
- "For each H2 marked `[depth-thin]`, list three concrete examples, data points, or firsthand scenarios the section needs."
- "Reorder sections to follow logical progression: definition → mechanism → application → comparison → decision."
- "Identify which H2 currently restates the top SERP result and replace with a section that adds information gain."

Continue iterating until: every H2 has a clear answer path, every brief-required sub-question has a placement, and at least one section contributes documented information gain.

### Step 5 — Outline sign-off captured in handoff

Before drafting, record in `content-handoff.json`:
- `outline_iteration_count`: how many LLM outline revisions were required
- `serp_top_references[]`: URLs inspected for grounding
- `information_gain_sections[]`: which H2 sections carry the unique angle
- `anti_slop_prompt_notes`: which prompt components were included to prevent boilerplate (role frame, audience, tone, structure constraints)

## AI Image Generation Brief

When unique imagery is required (and original photography is not available), generate **brief-driven AI images** instead of generic stock. Each image is a content asset — treat its prompt with the same care as a section outline.

### Prompt template for image generation

```markdown
# Subject
<what literally is in the image — avoid abstractions>

# Composition
- framing: [close-up | medium | wide]
- focal point: <specific element>
- foreground / midground / background layers

# Style
- medium: [photorealistic | editorial illustration | isometric | flat vector]
- lighting: [natural daylight | studio soft | dramatic]
- color palette: <align with brand or topic mood, e.g. "warm neutrals + accent orange">

# Context & mood
- setting: <environment, time of day>
- emotion: <curious, calm, urgent, authoritative>

# Technical
- aspect ratio: [16:9 hero | 1:1 social | 4:5 mobile]
- output intent: [hero image | inline illustration | social variant]
- avoid: <overused tropes, hands-with-too-many-fingers, text-in-image, brand logos>

# Alt-text anchor (SEO)
<draft the alt-text now — embed the primary or secondary keyword naturally — 80–125 chars>
```

### Image SEO rules

- **Filename**: kebab-case matching the keyword cluster (e.g. `may-lanh-treo-tuong-1-5hp-rewiew.jpg`); never `image-001.png` or `untitled.png`.
- **Alt text**: 80–125 chars, primary keyword or closely-related entity, describe the actual image content.
- **Format**: WebP preferred (80–90% quality); PNG only when transparency is required.
- **Placement**: hero image near the top; inline images adjacent to the section they illustrate; never force unrelated imagery for visual filler.
- **Originality vs AI risk**: prefer original screenshots, product photos, or author-captured media for E-E-A-T evidence; label AI-generated illustrations in caption when the topic is YMYL-adjacent.
- **Provenance flag**: when shipping to a pipeline that validates C2PA Content Credentials, emit `image_provenance` field in `content-handoff.json` with values `original_photo | ai_generated | licensed_stock | unknown`.

## Prompt Framework For AI-Assisted Drafting

When handing the outline to an LLM for first-draft generation, wrap the request in this **5-component frame** to minimize slop:

| Component | Content | Why it matters |
| --------- | ------- | -------------- |
| 1. **Role** | "You are <SEO specialist / subject-matter expert / investigative journalist> with <N years> experience in <domain>" | Anchors the model's generated voice and benchmark for topical depth |
| 2. **Brief** | audience + goal + tone + business outcome + YMYL flag from `seo-content-brief.json` | Prevents generic tone and mispositioned CTAs |
| 3. **Structure** | the signed-off outline (H1/H2/H3 with answer format per section) | Keeps the LLM from reorganizing into a worse flow |
| 4. **Keyword policy** | primary + secondary keywords, density target, placement rules (H2, first 100 words, conclusion), "do not stuff" explicit | Aligns output with SEO brief and prevents keyword-stuffing failure modes |
| 5. **Visual & media spec** | list of AI image prompts per section (from the Image Generation Brief), callouts, code blocks, tables to insert | Ensures visuals are placed at the right depth, not appended at end |

A prompt missing **any** of the five components statistically produces boilerplate. Keep all five inline with each section-level drafting call when invoking sub-agents.

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

## Related Skills

- **write-documentation**: Structure and clarity patterns; technical README/runbooks belong with Technical Writer
- **write-tech-radar**: Radar-style technology assessments (Vesviet radar subtree)
- **analyze-business-requirements**: Align copy with business rules when BA supplied a ticket
- **meeting-review**: Resolve stakeholder conflicts before drafting sensitive claims
- **agent-delegation**: Delegate drafting or specialist work to other roles

> **Site-specific authoring skills** (Astro MDX for Lease/May lanh, Hugo for Vesviet/Learn) live in overlays — see `overlays/lease-content/` and `overlays/vesviet-content/` README for the skill names to activate.
