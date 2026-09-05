# Entity Salience & Schema.org JSON-LD Microdata Standards

Reference technical specification for `optimize-seo` and the `seo-analyst` role. Governs knowledge graph alignment, entity salience optimization, and connected Schema.org `@graph` implementations.

---

## 1. Entity Salience & Knowledge Graph Alignment

Entity salience measures how prominently a specific real-world entity (person, technology, organization, algorithm) is positioned within a document's semantic structure.

### Salience Optimization Rules
1. **Wikidata QID Disambiguation**: Map all core technologies, libraries, and frameworks to their canonical Wikidata entity URIs (e.g., Rust is `Q575650`, PostgreSQL is `Q276093`).
2. **Syntactic Subject Placement**: Place the primary entity as the grammatical subject in the document H1, introductory sentence, and H2 headers.
3. **Pronoun Elimination**: Minimize ambiguous pronouns ("it", "they", "this tool"). Repeat the explicit entity noun to prevent coreference breakdown during LLM passage parsing.
4. **Semantic Triples**: Structure key factual definitions into clean Subject-Predicate-Object triples (e.g., `[Redis] [implements] [in-memory key-value caching]`).

---

## 2. Connected Schema.org `@graph` Specification

All technical articles must emit a single, interconnected JSON-LD `@graph` linking the article, author, and interactive FAQs:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "TechArticle",
      "@id": "https://tanhdev.com/posts/event-sourcing-rust#article",
      "isPartOf": {
        "@type": "WebSite",
        "@id": "https://tanhdev.com/#website",
        "name": "tanhdev",
        "url": "https://tanhdev.com/"
      },
      "headline": "Production Event Sourcing in Rust: Latency & Storage Benchmarks",
      "description": "Empirical architectural benchmarks and memory trade-offs for CQRS and event sourcing in Rust systems.",
      "datePublished": "2026-09-05T10:00:00+07:00",
      "dateModified": "2026-09-05T10:00:00+07:00",
      "author": {
        "@type": "Person",
        "@id": "https://tanhdev.com/about/#author",
        "name": "Lê Tuấn Anh",
        "jobTitle": "Principal Systems Architect",
        "sameAs": [
          "https://github.com/vesviet",
          "https://linkedin.com/in/vesviet",
          "https://orcid.org/0009-0002-1234-5678"
        ]
      },
      "about": [
        {
          "@type": "Thing",
          "name": "Event Sourcing",
          "sameAs": "https://www.wikidata.org/wiki/Q105639736"
        },
        {
          "@type": "Thing",
          "name": "Rust",
          "sameAs": "https://www.wikidata.org/wiki/Q575650"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "@id": "https://tanhdev.com/posts/event-sourcing-rust#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is the p99 write latency penalty of event sourcing in Rust?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "In production benchmarks on NVMe storage, appending serialized events to an append-only log introduces an 8ms p99 write latency penalty compared to direct in-place database updates."
          }
        }
      ]
    }
  ]
}
```

---

## 3. Microdata Validation Protocol

- Validate all emitted JSON-LD through the Google Rich Results Test API with 0 errors and 0 warnings.
- Ensure `@id` references cleanly cross-reference internal nodes without broken internal anchors.
- Author `Person` entity must link to verifiable external authority profiles (`sameAs`).
