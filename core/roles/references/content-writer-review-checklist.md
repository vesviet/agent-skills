## Content Writer Review Checklist

This reference checklist provides comprehensive, actionable criteria for evaluating long-form editorial articles, direct-response conversion copy, landing pages, and multi-channel derivative assets.

### 1. Editorial Drafting & Narrative Standards
- **BLUF Answer-First Execution**: The opening block immediately under each H2 heading provides a concise, direct answer (≤30 words) followed by quantified metric proof (≤30 words, total ≤60 words) prior to narrative expansion.
- **Fact Density Benchmark**: Narrative sections maintain a minimum of 3 verifiable, concrete data points (measurements, versions, benchmark numbers, sourced statistics) per 500 words.
- **Logical Query Hierarchy**: H2 headings map cleanly to primary user query intents; H3 subheadings isolate and resolve discrete query fan-out sub-questions.
- **Structural Scanability**: Complex configurations, comparative metrics, and multi-step procedures use structured Markdown comparison tables, numbered sequences, or tight bulleted modules instead of walls of unbroken text.
- **Entity Salience & Clarity**: Primary domain entities (Wikidata QIDs, exact architectural component names, protocol standards) are introduced early, disambiguated, and used consistently throughout.

### 2. Direct-Response Copywriting Frameworks
- **Framework Intent Fit**: Copy cleanly adopts a direct-response framework matched to prospect awareness stage:
  - *AIDA (Attention, Interest, Desire, Action)*: For cold/unaware audiences seeking comprehensive transformation.
  - *PAS (Problem, Agitation, Solution)*: For problem-aware audiences requiring acute pain identification and relief.
  - *BAB (Before, After, Bridge)*: For aspirational audiences demonstrating the current friction vs. ideal future state.
  - *FAB (Features, Advantages, Benefits)*: For feature announcements translating technical specs into business advantages.
  - *Hook-Story-Offer*: For narrative landing pages and executive emails building trust before presenting commercial value.
- **Value Proposition Clarity**: The core value proposition is distinct, quantified, and immediately discernible within the hero section (above the fold) without ambiguous buzzwords.
- **Objection Handling**: Common friction points (implementation complexity, pricing transparency, security compliance, data ownership, switching costs) are proactively raised and neutralized.
- **Friction-Free CTAs**: Calls-to-action utilize unambiguous action verbs, state immediate next steps, eliminate micro-friction ("No credit card required", "Deploy in 3 minutes"), and avoid generic "Click here" or "Submit".

### 3. Behavioral Marketing Psychology & Ethical Persuasion
- **Authentic Social Proof**: Customer testimonials, adoption statistics, case study metrics, and client logos reflect verified users; zero simulated quotes, invented testimonials, or inflated customer counts.
- **Legitimate Authority**: Trust cues reference genuine practitioner credentials, published research, independent audit certifications, or open-source repo telemetry.
- **Verifiable Scarcity & Urgency**: Deadlines, inventory counts, and cohort caps correspond to actual physical, operational, or scheduling limitations; zero synthetic countdown timers, fake "only 2 seats remaining" banners, or deceptive exit modals.
- **Radical Risk Reversal**: Guarantees, trial terms, cancellation policies, and rollback paths are explicitly defined in plain English with zero hidden lock-in clauses.
- **Ethical Reciprocity & Loss Aversion**: Substantive value (actionable checklists, calculators, templates) is delivered before any commercial request; loss aversion highlights genuine risks of inaction (e.g. security vulnerabilities, maintenance overhead) without fear-mongering or shame framing ("No, I don't want to grow").

### 4. Anti-AI Humanizer Verification & Cadence Discipline
- **Zero Blacklisted AI Clichés**: Grep audit verifies 0 occurrences of banned robotic tropes ("delve", "tapestry", "testament", "unlock", "game-changer", "beacon", "foster", "realm", "crucial", "harness", "navigating", "intertwined", "multifaceted", "underpin", "cornerstone", "elevate", "shed light", "ever-evolving", "in today's digital landscape").
- **20/60/20 Burstiness Distribution**: Sentence lengths follow natural human variation (~20% punchy short sentences 3–7 words, ~60% medium expository sentences 8–18 words, ~20% complex analytical sentences 19–28 words; cadence standard deviation ≥6.5 words).
- **Anti-Monotony Guardrail**: Draft contains zero instances of 3 or more consecutive sentences of identical word length (within ±2 words).
- **Active Voice Benchmark (≥85%)**: All narrative and conversion sections achieve ≥85% active voice with explicit subject agency (naming the specific engineer, tool, protocol, or system component executing the action).
- **Four Boilerplate Types Cut**: Complete elimination of broad context openers, tour-guide section transitions ("Now that we have explored..."), conclusion regurgitations ("In summary, we have discussed..."), and evasive hedge phrases ("It is worth noting that...").

### 5. Empirical Proof & E-E-A-T Authenticity
- **Dual Empirical Proof Mandate**: Every technical or evaluative piece incorporates at least two distinct types of verified empirical evidence:
  1. *Primary Data & Telemetry*: Documented benchmarks, latency profiles, load test results with explicit hardware/testbed specifications.
  2. *System Execution Artifacts*: Shell command outputs, terminal transcripts, configuration diffs (`git diff`), or minimal reproducible code examples.
  3. *Production Case Studies*: Real architectural trade-offs, incident postmortems, or migration retrospectives documenting operational downsides.
  4. *Visual Proof with Provenance*: Architectural diagrams, flamegraphs, or screenshots compliant with C2PA Content Credentials.
- **Zero Fabricated Evidence**: All claims trace directly to reproducible evidence or verified SME transcripts; hypothetical data is explicitly labeled as such.

### 6. Information Gain & SERP Differentiation
- **Non-Commodity Threshold (≥75/100)**: Evaluated against the top 10 search competitors; content must achieve an Information Gain score ≥75 by offering net-new knowledge unavailable in ranking competitor pages.
- **Substantive Differentiation Vectors**: Content delivers genuine delta across at least one vector: novel benchmark data, proprietary architectural patterns, counter-consensus trade-off analyses, production failure postmortems, or custom interactive calculators.
- **Zero Skyscraper Paraphrasing**: Outright rejection of articles that merely synthesize, summarize, or reword existing top-10 search results without introducing original primary insights.

### 7. Omnichannel Repurposing & Semantic Drift Prevention
- **Preservation of Technical Invariants**: Derivative assets (LinkedIn posts, X/Twitter threads, newsletters, short video scripts) strictly preserve all core architectural trade-offs, security warnings, prerequisite dependencies, and failure modes.
- **Entity & Version Fidelity**: Exact version numbers, configuration flags, and performance figures remain identical between parent articles and short-form snippets.
- **Channel-Native Structuring**: Variants respect native platform formats (hook + value + discussion prompt for LinkedIn, threaded tension + proof + CTA for X) without copying and pasting raw article excerpts.

### 8. Technical & Format Hygiene
- **Frontmatter Schema Compliance**: Target CMS frontmatter (Astro MDX, Hugo YAML) validates with mandatory explicit `slug`, author entity, canonical URL, and tag arrays.
- **Machine Contract Emission**: `contracts/schemas/content-handoff.json` is fully populated with empirical proof items, anti-AI gate status, burstiness scores, and active voice percentages.
- **Media Asset Provenance**: All illustrations, charts, and diagrams feature descriptive alt text (80–125 characters), kebab-case filenames, and verified C2PA provenance records.
