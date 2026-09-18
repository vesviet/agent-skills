# Entity Grounding and Wikidata Guide

This guide provides technical reference specifications for semantic entity disambiguation via Wikidata Knowledge Graph QIDs, establishing author E-E-A-T credentials, and structuring `TechArticle` attributes.

---

## 1. Entity Grounding via Wikidata Knowledge Graph

Search engines and Generative Engine Optimization (GEO) algorithms extract entities rather than relying solely on raw keyword strings. Entity grounding eliminates semantic ambiguity by linking on-page topics to canonical machine-readable identifiers in the Wikidata Knowledge Graph.

### 1.1 Why Wikidata QIDs Matter
- **Disambiguation**: Distinguishes "Java" the programming language (Wikidata `Q251`) from "Java" the island in Indonesia (`Q3757`).
- **Knowledge Graph Ingestion**: Allows search engines (Google Knowledge Graph, Bing Entity Graph) to index relationships between topics directly into their internal ontology.
- **AI Answer Engines**: LLM retrieval engines (Perplexity, SearchGPT) use Knowledge Graph entities to calculate topical authority and passage salience.

### 1.2 Structuring the `about` and `mentions` Arrays

Schema.org provides two distinct properties for entity associations on `Article` or `TechArticle`:

- **`about` (Primary Subject Matter)**: Reserved for the 1 to 3 core topics that define the fundamental subject of the document.
- **`mentions` (Secondary / Supporting Entities)**: Used for tools, libraries, or concepts mentioned in passing.

#### Implementation Pattern
```json
{
  "@type": "TechArticle",
  "@id": "https://example.com/guides/modern-react/#article",
  "about": [
    {
      "@type": "Thing",
      "name": "React",
      "description": "JavaScript library for building user interfaces",
      "sameAs": "https://www.wikidata.org/wiki/Q6415"
    },
    {
      "@type": "Thing",
      "name": "Single-Page Application",
      "sameAs": "https://www.wikidata.org/wiki/Q215281"
    }
  ],
  "mentions": [
    {
      "@type": "Thing",
      "name": "TypeScript",
      "sameAs": "https://www.wikidata.org/wiki/Q978185"
    },
    {
      "@type": "Thing",
      "name": "Tailwind CSS",
      "sameAs": "https://www.wikidata.org/wiki/Q104840500"
    }
  ]
}
```

---

## 2. Author E-E-A-T Architecture (`Person` Node)

Google's Quality Rater Guidelines prioritize Experience, Expertise, Authoritativeness, and Trustworthiness (E-E-A-T). For YMYL (Your Money or Your Life) and technical subjects, an anonymous or ungrounded author significantly degrades trust signals.

### 2.1 The Comprehensive `Person` Node Specification

A production E-E-A-T `Person` node must contain:
1. **Core Identity**: `name`, `jobTitle`, `image`.
2. **Institutional Alignment**: `worksFor` referencing the `#organization` node.
3. **Authoritative Digital Footprint (`sameAs`)**: High-trust third-party verification profiles.
4. **Topical Competence (`knowsAbout`)**: Array of grounded entities matching the author's specialty.

```json
{
  "@type": "Person",
  "@id": "https://example.com/authors/dr-elena-rostova/#author",
  "name": "Dr. Elena Rostova",
  "jobTitle": "Principal Cryptographic Engineer",
  "description": "Cryptographic researcher specializing in zero-knowledge proofs and post-quantum key exchange algorithms.",
  "image": "https://example.com/authors/elena-rostova.jpg",
  "url": "https://example.com/authors/elena-rostova",
  "worksFor": {
    "@id": "https://example.com/#organization"
  },
  "alumniOf": {
    "@type": "EducationalOrganization",
    "name": "Massachusetts Institute of Technology",
    "sameAs": "https://www.wikidata.org/wiki/Q49108"
  },
  "sameAs": [
    "https://www.linkedin.com/in/elena-rostova-crypto",
    "https://github.com/erostova-research",
    "https://scholar.google.com/citations?user=xyz12345",
    "https://orcid.org/0000-0002-1825-0097",
    "https://twitter.com/erostova_sec"
  ],
  "knowsAbout": [
    {
      "@type": "Thing",
      "name": "Zero-Knowledge Proof",
      "sameAs": "https://www.wikidata.org/wiki/Q191924"
    },
    {
      "@type": "Thing",
      "name": "Post-Quantum Cryptography",
      "sameAs": "https://www.wikidata.org/wiki/Q2583279"
    }
  ]
}
```

### 2.2 Author Verification Guardrails
- **Zero Fabricated Authors**: Never invent fictional practitioner names or stock photo personas.
- **Profile Integrity**: Every link in `sameAs` must actively resolve and match the named individual.
- **Privacy Hygiene**: Never expose private email addresses, home addresses, or personal phone numbers in public JSON-LD schemas.

---

## 3. Organization Entity Grounding (`Organization` Node)

The `Organization` node anchors corporate authority and publisher credibility.

```json
{
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "Acme Systems Inc.",
  "legalName": "Acme Systems Incorporated",
  "url": "https://example.com",
  "logo": "https://example.com/assets/logo.png",
  "foundingDate": "2021-04-12",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q12345678",
    "https://www.linkedin.com/company/acme-systems",
    "https://github.com/acme-systems",
    "https://www.crunchbase.com/organization/acme-systems"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-800-555-0199",
    "contactType": "technical support",
    "availableLanguage": ["English"]
  }
}
```

---

## 4. `TechArticle` Semantic Properties

When documenting code, architecture, or DevOps pipelines, prefer `TechArticle` over standard `Article` or `BlogPosting`.

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `proficiencyLevel` | Text | Target technical expertise required | `"Beginner"`, `"Intermediate"`, `"Expert"` |
| `dependencies` | Text | Prerequisite libraries, runtimes, or tools | `"Node.js 20+, Docker Engine 24+, Redis 7+"` |
| `targetPlatform` | Text | Supported OS, cloud, or runtime target | `"Linux x86_64, macOS Apple Silicon, Cloudflare Workers"` |
| `about` | Array[Thing] | Primary grounded concepts with Wikidata QIDs | See Section 1.2 |
