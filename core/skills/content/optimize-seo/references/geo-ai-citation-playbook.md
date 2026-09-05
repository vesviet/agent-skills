# GEO AI Citation Playbook (Perplexity, SearchGPT, Google AI Overviews)

Reference manual for `optimize-seo` and the `seo-analyst` role. Establishes generative engine optimization (GEO) mechanics, engine-specific citation triggers, and formatting standards for tables and quantitative data.

---

## 1. Engine-Specific Citation Architectures

Different generative engines utilize distinct retrieval algorithms and passage extraction models:

| AI Engine | Primary Retrieval Mechanics | Citation Trigger Standards | Optimization Formatting |
| :--- | :--- | :--- | :--- |
| **Perplexity** | Fast RAG scraping top organic URLs; weights opening paragraph statistics and structured comparisons. | Numbered source brackets `[1][2]` anchored directly to verified claims and quantitative data. | - Atomic H2 opening statements (≤60 words).<br>- Markdown comparison tables.<br>- Explicit numerical units (ms, %, QPS). |
| **SearchGPT (OpenAI)** | Semantic index + Bing API retrieval; emphasizes conversational entity fidelity and structured microdata. | Inline footnote citations and domain attribution based on knowledge graph entities. | - Answer-first BLUF summaries.<br>- Connected Schema.org JSON-LD (`@graph`).<br>- Entity disambiguation (Wikidata QIDs). |
| **Google AI Overviews** | Gemini multi-modal RAG grounded in Google Knowledge Graph and Search index. | Synthesizes multi-source consensus; extracts lists and tables directly into top-of-SERP snapshots. | - Ordered `<ol>` lists for procedural queries.<br>- Markdown tables for multi-attribute specs.<br>- Fact density ≥3 verified numbers per 500 words. |

---

## 2. Comparison Tables & Quantitative Lists Standards

Generative engines preferentially extract tabular data because tables eliminate ambiguity in multi-attribute entity comparisons.

### Comparison Table Formatting Standards
1. **Header Hygiene**: Clear, descriptive column headers with units specified (e.g., `Latency (p99)`, `Throughput (QPS)`, `Memory (MB)`).
2. **Deterministic Values**: Avoid subjective qualifiers ("fast", "cheap", "good"). Use exact empirical metrics (`< 45ms`, `$0.02 / GB`, `99.99%`).
3. **Primary Entity First**: The subject entity must occupy the first comparison column.

### Quantitative List Standards
- Minimum **3 verifiable data points** (percentages, latency benchmarks, cost figures, version numbers) per 500 words.
- Formatted with **bold lead-ins** for fast token scanning by LLM chunkers:
  - **Latency Floor**: Sub-10ms p99 response time across warm cache hits.
  - **Memory Footprint**: 180MB baseline RAM utilization under 10,000 active WebSocket connections.
- Keep citation-ready sentences tight (≤25 words) to facilitate zero-paraphrase quotation by AI engines.

---

## 3. Generative Engine Citation Testing Protocol

To verify GEO citability before publishing:
1. **Query Framing**: Convert the primary target keyword into 3 natural language question prompts (e.g., "What are the production trade-offs between X and Y?").
2. **Simulation Run**: Submit prompts to Perplexity Pro, ChatGPT Search, and Google AI Overviews.
3. **Attribution Audit**: Verify whether the brand or domain is cited as a primary source, and ensure the extracted snippet preserves entity fidelity.
