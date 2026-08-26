# AI Drafting Playbook

Reference playbook for `write-article`. Loaded on demand — the SKILL.md body
summarizes the discipline; this file carries the full templates:

- **AI-Assisted Outline Protocol** — SERP-grounded iteration loop for outlines
- **AI Image Generation Brief** — structured prompts for brief-driven imagery
- **Prompt Framework For AI-Assisted Drafting** — 5-component frame that minimizes slop

---

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
