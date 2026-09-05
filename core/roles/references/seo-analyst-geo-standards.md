# SEO Analyst GEO Standards & Generative Search Architecture

This reference document defines the technical operating standards for [`seo-analyst`](../seo-analyst.md) in Generative Engine Optimization (GEO), Entity-First SEO, Answer-First (BLUF) structuring, connected Schema.org `@graph` architecture, and agentic discovery protocols (`llms.txt`).

---

## 1. Entity-First SEO & Entity Salience Architecture

Traditional search engines matched keyword strings; modern generative engines (Google AI Overviews, SearchGPT, Perplexity) construct knowledge representations from recognized semantic entities and relationship triples. SEO Analysts must anchor all content in explicit Knowledge Graph entities.

### 1.1 Entity Disambiguation & Wikidata QID Mapping

Every content brief and technical audit must disambiguate primary and secondary entities using authoritative Knowledge Graph identifiers:

- **Primary Subject Entity:** Map the core topic to its unique **Wikidata QID** (e.g., `PostgreSQL` → `Q182496`, `Kubernetes` → `Q22661304`, `GraphQL` → `Q20108180`).
- **Semantic Triples Formulation:** Model the core thesis of each article as explicit Subject-Predicate-Object triples:
  - `[Subject: Envoy Proxy (Q11289196)]` -> `[Predicate: implements]` -> `[Object: gRPC Web Protocol (Q24885820)]`.
  - `[Subject: Redis (Q116373)]` -> `[Predicate: achieves]` -> `[Object: Sub-millisecond Latency]`.
- **Topical Entity Co-Occurrence:** Map 5–8 related secondary entities that must naturally appear in the text to satisfy topical completeness and semantic proximity.

### 1.2 Entity Salience & Syntactic Placement Rules

Entity salience determines how prominently Natural Language Processing (NLP) models score an entity within a text passage. To maximize extraction confidence:

1. **Lead Grammatical Subject:** Position the primary entity as the grammatical subject of the opening sentence under each H2 heading.
   - *Poor Salience:* "In high-throughput microservice architectures, developers often choose **gRPC** for efficient RPC communication."
   - *High Salience:* "**gRPC** reduces microservice serialization latency by utilizing HTTP/2 transport and Protocol Buffers."
2. **Heading Leading Position:** Place the entity at or near the beginning of H2 and H3 headings rather than trailing behind filler phrases.
   - *Poor:* "An In-Depth Overview of Features in Kubernetes v1.32"
   - *High:* "Kubernetes v1.32 Architectural Features and DRA Enhancements"
3. **Pronoun Deprecation in Critical Passages:** Avoid vague pronouns ("it", "this tool", "the system") in the opening 50 words of any section. Explicitly repeat the entity noun or approved alias to maintain context window clarity for chunk extractors.

---

## 2. "Answer-First" (BLUF) Structure Formulation Guide

Generative engines extract discrete text chunks to synthesize AI answers. Content that buries the answer behind background exposition is ignored. Every H2 section must implement the **Bottom Line Up Front (BLUF)** anatomy.

### 2.1 The Two-Sentence BLUF Anatomy (≤60 Words Total)

Immediately below each H2 heading, provide a dedicated BLUF answer block adhering to this strict division:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ANATOMY OF AN H2 BLUF                           │
├───────────────────────────────────┬────────────────────────────────────┤
│ Sentence 1 (≤30 words)            │ Sentences 2–3 (≤30 words)          │
│ The Direct, Definitive Answer     │ Quantified Metric Proof & Context  │
└───────────────────────────────────┴────────────────────────────────────┘
```

- **Sentence 1: The Direct Answer (≤30 words):**
  - Answers the heading query immediately and conclusively.
  - Contains no throat-clearing, no historical context, and no rhetorical questions.
  - Can stand completely alone as an extracted quote.
- **Sentences 2–3: Quantified Proof & Boundary Condition (≤30 words):**
  - Injects specific numerical benchmarks, hardware parameters, or operational constraints.
  - Verifies the assertion made in Sentence 1.

### 2.2 BLUF Formulation Example

- **H2 Heading:** `## How Does HTTP/3 Reduce Head-of-Line Blocking?`
- **Sentence 1 (Direct Answer - 21 words):** "HTTP/3 eliminates head-of-line blocking by replacing TCP with QUIC, running independent multiplexed streams over UDP with per-stream packet loss isolation."
- **Sentence 2 (Quantified Proof - 22 words):** "In production benchmarks under 2% packet loss, QUIC maintains 99% stream throughput where HTTP/2 over TCP suffers a 42% latency penalty."
- **Modular Expansion (Body):** Proceed immediately into a comparison table contrasting TCP vs QUIC packet recovery mechanics, followed by configuration steps.

---

## 3. Advanced Schema.org Connected Graph Architecture

Disconnected, flat schema blocks fail to communicate contextual authority. SEO Analysts specify a unified JSON-LD `@graph` linking the website, publisher, author, and technical article entities.

### 3.1 Unified `@graph` Specification Structure

All technical articles must emit a single, connected JSON-LD script block containing mutually referenced entities:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Engineering Portal",
      "url": "https://example.com",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://example.com/#logo",
        "url": "https://example.com/logo.png"
      }
    },
    {
      "@type": "Person",
      "@id": "https://example.com/authors/johndoe#author",
      "name": "John Doe",
      "jobTitle": "Principal Infrastructure Engineer",
      "worksFor": { "@id": "https://example.com/#organization" },
      "sameAs": [
        "https://github.com/johndoe",
        "https://www.linkedin.com/in/johndoe",
        "https://scholar.google.com/citations?user=xyz"
      ],
      "knowsAbout": [
        "https://www.wikidata.org/wiki/Q22661304",
        "https://www.wikidata.org/wiki/Q11289196"
      ]
    },
    {
      "@type": "TechArticle",
      "@id": "https://example.com/posts/quic-http3-performance#article",
      "isPartOf": { "@id": "https://example.com/#website" },
      "headline": "HTTP/3 and QUIC Performance Architecture Under Packet Loss",
      "author": { "@id": "https://example.com/authors/johndoe#author" },
      "publisher": { "@id": "https://example.com/#organization" },
      "proficiencyLevel": "Expert",
      "dependencies": "Linux Kernel 6.8+, Envoy v1.31+, OpenSSL 3.2+",
      "about": [
        {
          "@type": "Thing",
          "name": "HTTP/3",
          "sameAs": "https://www.wikidata.org/wiki/Q58462002"
        },
        {
          "@type": "Thing",
          "name": "QUIC",
          "sameAs": "https://www.wikidata.org/wiki/Q18153406"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "@id": "https://example.com/posts/quic-http3-performance#faq",
      "isPartOf": { "@id": "https://example.com/posts/quic-http3-performance#article" },
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Does HTTP/3 improve performance on reliable fiber connections?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "On zero-loss connections, HTTP/3 performs comparably to HTTP/2; its primary throughput advantages emerge on cellular and lossy networks exceeding 1% packet drop."
          }
        }
      ]
    }
  ]
}
```

---

## 4. Standardized `llms.txt` and `llms-full.txt` Specification

The SEO Analyst governs the site's machine discoverability architecture for autonomous AI agents (SearchGPT agentic search, Anthropic Claude, Perplexity Pages, Cursor, Claude Code).

### 4.1 Authoring Standards & Distinctions

- **Strategic Scope Clarification:** `llms.txt` is strictly an **agentic AI discovery manifest**, NOT a Google Search ranking factor or Google AI Overviews ranking signal. Google has explicitly verified that `llms.txt` does not influence web search indexing.
- **File Structure & Syntax:**
  - `/llms.txt`: A lightweight, curated markdown index containing site metadata, primary architecture links, and concise summaries (<200 words per section).
  - `/llms-full.txt`: A comprehensive, concatenated context file containing full clean markdown documentation for offline RAG ingestion by developer agents.
- **Layout Specification for `/llms.txt`:**
  ```markdown
  # Site or Project Name

  > Brief 1-2 sentence project mission and primary architectural scope.

  ## Core Architecture Docs
  - [Kubernetes Networking](https://example.com/docs/k8s-net.md): Core CNI and service routing specifications.
  - [gRPC Gateway](https://example.com/docs/grpc-gw.md): Envoy-based transcoding and HTTP/2 proxy configuration.

  ## Optional Modules
  - [Observability](https://example.com/docs/telemetry.md): OpenTelemetry collector pipelines.
  ```

---

## 5. GEO Extractability Index & Citation Audit (0–100 Rubric)

The SEO Analyst uses the **GEO Extractability Index** to evaluate whether an article is structured for maximum machine extractability and citation likelihood across AI search surfaces:

| Dimension | Weight | Evaluation Criteria |
| :--- | :--- | :--- |
| **1. BLUF Clarity & Conciseness** | **25 pts** | Sentence 1 is ≤30w direct answer; Sentences 2–3 provide ≤30w metric proof; total block ≤60w. |
| **2. Fact Density & Empirical Proof** | **25 pts** | Minimum 3 verifiable data points per 500 words; hardware/environment parameters cited. |
| **3. Entity Salience & Wikidata Mapping** | **25 pts** | Primary entity placed as grammatical subject; Wikidata QIDs bound in Schema and brief. |
| **4. Modular Formatting & Scannability** | **25 pts** | Quantitative comparison tables used for spec sets; numbered steps used for procedures; clean H2→H3 tree. |

### 5.1 Extractability Thresholds
- **Score ≥80:** **High Extractability Passed.** Content is primed for Google AI Overviews and SearchGPT direct snippet extraction.
- **Score 65–79:** **Moderate Extractability.** Good information density, but sentences require pruning to meet the ≤30-word BLUF threshold.
- **Score <65:** **Extractability Failed.** Text is discursive, answers are buried in paragraph bodies, or entities lack syntactic salience. Blocked from publish.

---

Last updated: 2026-09-05
