# Write Article — Suggested Process (Reference)

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


