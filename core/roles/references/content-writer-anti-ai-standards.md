# Content Writer Anti-AI Standards & Editorial Discipline

This reference document defines the mandatory editorial standards, Anti-AI Clichés blacklist, burstiness targets, active voice benchmarks, and empirical proof requirements for [`content-writer`](../content-writer.md).

---

## 1. Anti-AI Clichés Blacklist & Replacement Catalog

Large Language Models (LLMs) default to predictable, high-probability tokens and figurative clichés that signal low-effort, synthetic generation. Search engine spam filters, AI search extractors, and discerning human readers aggressively penalize these patterns.

### 1.1 Zero-Tolerance Vocabulary Blacklist

The following words and phrases are prohibited in all published articles. Any draft containing them fails the Anti-AI Quality Gate:

| Forbidden Word / Phrase | Why LLMs Overuse It | Editorial Failure | Mandatory Human / Active Replacements |
| :--- | :--- | :--- | :--- |
| **delve / delve into** | High-probability academic filler | Pretentious, empty transition | inspect, analyze, test, trace, examine, profile, measure |
| **tapestry / rich tapestry** | Metaphorical hallucination | Abstract, meaningless ornamentation | architecture, system, stack, ecosystem, sequence, set |
| **testament / testament to** | Synthetic gravitas | False historical weight | shows, demonstrates, proves, confirms, highlights |
| **unlock / unlock the power** | Marketing boilerplate | Generic hype; unearned promise | configure, enable, accelerate, compute, reduce, achieve |
| **game-changer** | Sensationalism | Overblown hyperbole | major shift, decisive trade-off, 10x throughput gain, milestone |
| **beacon / beacon of** | Dramatic figurative filler | Melodramatic and vague | model, reference implementation, verified standard |
| **pinnacle / pinnacle of** | Exaggerated superlative | Unsubstantiated perfection | highest tier, upper limit, benchmark ceiling |
| **foster / foster innovation** | Corporate euphemism | Weak verb masking lack of detail | build, generate, write, produce, trigger, establish |
| **realm / in the realm of** | Archaic domain framing | Academic throat-clearing | in, across, within, for, during engineering of |
| **crucial / vital / paramount** | False urgency | Weak intensifier without proof | required, critical-path, prerequisite, blocking, necessary |
| **harness / harness the power** | Utility metaphor | Cliché tech filler | run, execute, deploy, utilize (replace with use), index, query |
| **navigating / navigating the** | Journey metaphor | Aimless narrative wandering | evaluating, migrating, choosing, auditing, configuring |
| **intertwined / interlinked** | Abstract relationship | Obscures causal mechanics | depends on, triggers, couples with, blocks, calls |
| **multifaceted** | Evasive complexity | Refuses to name specific facets | has 3 distinct layers, involves [X, Y, and Z] |
| **underpin / underpins** | Architectural metaphor | Robotic structural filler | supports, enforces, backs, runs under, powers |
| **cornerstone** | Architectural cliché | Overused foundation metaphor | primary dependency, core prerequisite, baseline model |
| **elevate / elevate your** | Marketing jargon | Patronizing, vague upgrade claim | improve, optimize, speed up, streamline, refine |
| **shed light / shed light on** | Revelation cliché | Unnecessary journalistic flourish | clarify, explain, benchmark, reveal, document |
| **ever-evolving** | Temporal platitude | Meaningless truism about tech | modern, current, 2026, active, fast-changing |
| **dive deep / deep dive** | Colloquial filler | Trite idiom replacing substance | technical teardown, code audit, line-by-line trace |
| **at the forefront** | Superiority trope | Unverified leadership claim | leads adoption of, deployed in, standardized on |
| **spearhead** | Corporate buzzword | Clunky pseudo-military phrasing | led, created, initiated, architected, authored |
| **seamless / seamlessly** | Unrealistic friction claim | Untrue marketing fiction | automatic, direct, unified, zero-copy, non-blocking |
| **robust / robustness** | Empty durability claim | Vague; avoids stating specific tolerances | resilient to network drops, memory-safe, fault-tolerant |
| **groundbreaking** | Inflated novelty | Historical exaggeration | novel, first published, unreleased, benchmark-leading |
| **revolutionary** | Promotional hype | Lack of objective perspective | architectural departure, new primitive, paradigm shift |
| **cutting-edge** | Tech brochure jargon | Dated within months | latest, late-2026, experimental, current stable |
| **a holistic approach** | Hand-waving generality | Fails to define execution scope | end-to-end plan, full-stack audit, unified architecture |
| **leverage** (as verb) | Corporate obfuscation | Pretentious substitution for "use" | use, apply, exploit, operate, build on |
| **utilize** | Bureaucratic stiffness | Unnecessary syllables | use |
| **facilitate** | Weak agency | Obscures who or what does the work | help, automate, route, coordinate, simplify |

### 1.2 Prohibited Rhetorical Templates

AI generators rely on boilerplate transitional structures. The following four structural formulas must be eradicated:

1. **Introduction Openers (The Broad Context Fallacy):**
   - *Prohibited:* "In today's fast-paced digital world...", "In the ever-evolving landscape of software development...", "As organizations increasingly turn to cloud computing..."
   - *Remedy:* Lead with the specific technical anomaly, operational constraint, benchmark number, or breaking change immediately in Sentence 1.
2. **Section Transition Fillers (The Artificial Tour Guide):**
   - *Prohibited:* "Now that we have explored X, let us delve into Y.", "Having covered the basics of caching, it is time to examine...", "With that in mind, let's take a closer look at..."
   - *Remedy:* Jump directly into the next core argument or technical primitive. Allow clear H2/H3 headings and natural logical flow to carry the transition.
3. **Conclusion Summaries (The Passive Regurgitation):**
   - *Prohibited:* "In conclusion, we have seen that...", "By following the steps outlined in this article, you can unlock...", "Hopefully, this guide has shed light on the multifaceted realm of..."
   - *Remedy:* Conclude with an architectural decision matrix, an explicit implementation caveat, production telemetry thresholds, or a direct call-to-action.
4. **Academic Hedge Phrases (The Responsibility Shirk):**
   - *Prohibited:* "It is worth noting that...", "Generally speaking...", "It could be argued that...", "It goes without saying that..."
   - *Remedy:* Delete the hedge entirely and make the direct factual assertion backed by data, or state the specific boundary condition under which the claim holds true.

---

## 2. Quantitative Burstiness & Natural Perplexity Standards

Robotic text is marked by flat, uniform sentence lengths (typically hovering between 15 and 20 words) and monotonic clause cadences. Human engineering prose exhibits high *burstiness* (sharp variance in sentence lengths) and natural *perplexity* (precise, domain-grounded vocabulary rather than high-probability generic tokens).

### 2.1 The 20/60/20 Sentence Distribution Standard

All drafted technical content must comply with the **20/60/20 cadence distribution**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        20/60/20 CADENCE TARGETS                        │
├───────────────────┬────────────────────────────────┬───────────────────┤
│ Short Sentences   │ Medium Sentences               │ Complex Sentences │
│ (~20% of total)   │ (~60% of total)                │ (~20% of total)   │
│ 3 to 7 words      │ 8 to 18 words                  │ 19 to 28 words    │
│ Impact & Rhythm   │ Core Technical Narrative       │ Nuanced Trade-offs│
└───────────────────┴────────────────────────────────┴───────────────────┘
```

- **Short Sentences (3–7 words) [~20%]:** Deliver impact, declare immutable facts, reset the reader's attention, and establish definitive conclusions.
  - *Example:* "Latency collapsed immediately."
  - *Example:* "Never expose secret keys client-side."
- **Medium Sentences (8–18 words) [~60%]:** Advance the primary technical explanation, describe configuration mechanics, and convey linear relationships.
  - *Example:* "The Envoy gateway routes inbound gRPC requests directly to worker pods using consistent hashing."
- **Complex Sentences (19–28 words) [~20%]:** Unpack architectural trade-offs, conditional failure modes, and multi-variable constraints.
  - *Example:* "While asynchronous replication eliminates write latency on the primary node, network partitions can force replicas to serve stale reads during leader election."

### 2.2 Rhythm Rules & Anti-Monotony Guardrails

- **The Three-Sentence Monotony Rule:** Never write three consecutive sentences of approximately the same length (within ±2 words of each other).
- **Opening Variety:** Vary sentence starters across every paragraph:
  - Open with an action verb or imperative command.
  - Open with a prepositional or conditional clause ("Under high packet loss, ...").
  - Open with a quantitative metric ("Across 10,000 requests, ...").
  - Prohibit opening consecutive sentences with "The [noun]...", "This [noun]...", or "By [verb]ing...".

### 2.3 Natural Perplexity Heuristic

- Replace high-probability generic verbs (*enhance, facilitate, optimize, manage*) with mechanical, domain-exact verbs (*clamp, truncate, buffer, demultiplex, serialize, pipeline, cache, evict*).
- Never use a three-word abstract phrase when a single standard industry noun exists (e.g., replace "system for managing distributed transactions" with "two-phase commit coordinator").

---

## 3. Active Voice & Subject Agency Playbook

Passive voice obscures technical accountability and dilutes reader confidence. In software architecture and engineering documentation, readers need to know exactly *who* or *what* executes an action.

### 3.1 The ≥85% Active Voice Benchmark

- Across all narrative sections, at least **85% of sentences must be in active voice**.
- Passive voice is permissible only when the receiver of the action is the strict focal point and the actor is truly unknown or irrelevant (e.g., "Packets dropped by upstream ISP hardware cannot be recovered").

### 3.2 Strict Subject Agency

Every sentence must identify the concrete subject performing the action:
- *Weak / Passive:* "A 40% reduction in memory overhead was observed when compression was enabled."
- *Active / Agentic:* "Enabling zstd compression slashed worker memory overhead by 40%."
- *Weak / Agentless:* "Configurations should be updated before deployments are initiated."
- *Active / Agentic:* "DevOps engineers must update the Helm values file before initiating the Canary deployment."

### 3.3 Active Voice Transformation Table

| Passive / Evasive Construction | Active / Agentic Transformation | Mechanical Improvement |
| :--- | :--- | :--- |
| "It was decided that PostgreSQL would be adopted." | "The team selected PostgreSQL to handle relational consistency." | Names the decision-maker and operational rationale. |
| "Errors are caught and handled by the middleware." | "The middleware catches unhandled panics and returns HTTP 500." | Specifies exact error state and concrete HTTP response. |
| "Performance improvements can be achieved through caching." | "Redis caching cuts database query latency from 85ms to 4ms." | Replaces vague potential with verified metric proof. |
| "Logs should be reviewed when latency spikes occur." | "Inspect Grafana tail logs the moment p99 latency exceeds 200ms." | Replaces passive suggestion with imperative operational threshold. |

---

## 4. Mandatory First-Hand Empirical Proof (E-E-A-T) Framework

Modern search engines and AI generative engines (Google AI Overviews, Perplexity, SearchGPT) aggressively devalue commoditized paraphrases. Every technical article must integrate **at least two distinct forms of empirical proof**.

### 4.1 Taxonomy of Empirical Proof Types

```
┌────────────────────────────────────────────────────────────────────────┐
│                   4 FORMS OF EMPIRICAL PROOF (MIN 2)                   │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ 1. Primary Data    │ 2. System Logs     │ 3. Production Case Study     │
│ Telemetry & Stats  │ Traces & Repros    │ Real Architectural Trade-off │
├────────────────────┴────────────────────┴──────────────────────────────┤
│ 4. Visual Proof with C2PA Provenance Metadata                          │
│ Architecture Diagrams, Verified Screenshots, Execution Flamegraphs     │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Primary Data with Timestamps & Sources:**
   - Exact numerical metrics, latency benchmarks, throughput numbers, or cost figures.
   - Must cite the test environment, sample size, hardware profile, and timestamp.
   - *Example:* "Benchmarked on AMD EPYC 7763 (64 cores, 256GB RAM), Ubuntu 24.04, k6 v0.50.0, 10,000 virtual users sustained over 15 minutes."
2. **System Execution Artifacts (Logs, Traces, Diffs):**
   - Verbatim terminal commands, shell outputs, configuration diffs (`git diff`), or minimal reproducible code examples.
   - Real error stack traces accompanied by the exact remediation patch.
3. **Production Case Studies & Concrete Trade-offs:**
   - Firsthand accounts of architectural migrations, incident postmortems, or breaking changes.
   - Honest enumeration of downsides, edge-case failure modes, and what broke during initial rollouts.
4. **Visual Proof with C2PA Provenance:**
   - Original architectural flowcharts, database entity relationship diagrams, or memory profiling flamegraphs.
   - Must include descriptive alt text, captions explaining the data flow, and C2PA Content Credentials metadata (`digitalSourceType` compliant).

---

## 5. Four-Pass Editorial Research Protocol

To ensure articles exhibit genuine depth rather than superficial AI synthesis, Content Writers must execute (or verify Researcher completion of) the **Four-Pass Editorial Protocol**:

| Pass | Focus | Deliverables & Verification |
| :--- | :--- | :--- |
| **Pass 1: Architecture & Intent Mapping** | Map user search intent, query fan-out sub-questions, and competitor SERP landscape. | Structured outline with H2/H3 hierarchy; intent classification; identified SERP gaps. |
| **Pass 2: Empirical Proof & Asset Gathering** | Collect primary data, reproduction code, execution logs, and architectural diagrams. | Minimum 2 empirical proof assets verified; hardware/environment specs documented. |
| **Pass 3: Answer-First (BLUF) Drafting** | Draft section by section with ≤30w definitive answer + ≤30w metric proof; enforce 20/60/20 burstiness. | Draft body; answer-first blocks complete; quantitative comparison tables constructed. |
| **Pass 4: Anti-AI Line Polish & Gate Audit** | Run full blacklist scan; check active voice ≥85%; eliminate boilerplate; verify citations. | Anti-AI Gate passed (`gate_passed: true`); word substitution complete; handoff generated. |

---

## 6. Anti-Slop Self-Scan Procedure & Verification Gates

Before submitting any deliverable or emitting `content-handoff.json`, the Writer must complete this mandatory self-scan:

1. **The Isolation Test:** Read each section independently outside the context of the article. Ask: *"Could this paragraph appear unchanged on a competitor's blog or a generic AI summary?"* If yes, it is boilerplate. Rewrite with specific codebase, product, or benchmark details.
2. **The Blacklist Grep:** Run an exact string search across the markdown draft for all prohibited words in Section 1.1. Zero occurrences are permitted.
3. **The Active Voice Audit:** Calculate the percentage of passive constructions in narrative text. Ensure active voice exceeds 85%.
4. **The Cadence Audit:** Check sentence length variance. Confirm short punchy sentences (3–7 words) and complex sentences (19–28 words) bracket the medium narrative sentences.
5. **The Empirical Gate:** Confirm at least 2 distinct empirical proof items are present, attributed, and verified.
6. **Handoff Documentation:** Record results in the `Anti-Slop Gate` block of the Output Template and emit structured fields into `contracts/schemas/content-handoff.json`.

---

Last updated: 2026-09-05
