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

- map H2 structure to GEO/AEO brief: each H2 begins with an atomic **BLUF answer block (≤60 words)** before narrative elaboration
- match query fan-out sub-questions from brief to H3 subheadings or inline answers
- implement answer format per section (definition, steps, comparison table, quantitative bullets) from brief
- implement internal links from brief or plan (minimum 3, prioritize high-value product/property pages)
- source all technical claims using `references/authentic-source-matrix.md` (Tier 1/2 sources mandatory)
- inject at least two empirical proof types (telemetry, reproduction logs, benchmark numbers) per E-E-A-T requirement

### 5. Scanability & Anti-AI Style Pass

After drafting, run the mandatory quality gate:
- **BLUF Verification**: confirm every H2 opens with a direct, quotable answer ≤60 words
- **Anti-AI Clichés Scan**: verify 0 occurrences of banned buzzwords ("delve", "tapestry", "unlock", "game-changer") against `references/anti-ai-style-guide.md`
- **Burstiness & Rhythm Check**: enforce 20/60/20 sentence length distribution (<12 words: ~20%, 12–25 words: ~60%, >25 words: ~20%)
- **Active Voice Benchmark**: verify ≥85% active voice with explicit subject agency
- **Scanability**: paragraphs 2–4 lines, list-worthy items converted to bullets/tables with bolded lead-ins
- **FAQ Block**: validate against Schema.org FAQPage requirements when present

### 6. Package Handoff

Emit content-handoff.json with:
- path, word_count, passes, unverified claims
- `ai_semantic_flaw_score`: flaw score (≤15 to pass), cliché count (0), active voice percentage (≥85%)
- `information_gain`: unique value added, type, and competitor SERP overlap analysis
- `answer_first_implemented`: true/false (BLUF verified across all H2s)
- `geo_aeo_fields_applied`: [answer-first, fan-out, answer_format, fact_density, comparison_tables]
- `eeat_signals`: experience proof types + implemented (true/false)
- request SEO Analyst audit before publish when site requires it

### 7. Publish Sprint (optional)

When overlays/seo-publishing is active, after user confirms publish, append plan/baiviet/publish-log.md per overlay conventions including GEO ready status.


