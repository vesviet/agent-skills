# Connected Graph Schema Architecture Guide

This guide provides technical reference specifications for architecting a single unified Schema.org `@graph` in JSON-LD syntax, eliminating fragmented schema islands, and establishing deterministic `@id` URI node relationships.

---

## 1. The Schema Island Problem vs. Unified `@graph`

### 1.1 The Anti-Pattern: Disconnected Schema Islands
Historically, websites inject multiple isolated `<script type="application/ld+json">` blocks across different layout partials:
- Tag 1 in header: Generic `Organization` schema.
- Tag 2 in breadcrumbs component: `BreadcrumbList` schema.
- Tag 3 in article body: `Article` schema with a plain text author string.
- Tag 4 in footer: `FAQPage` schema.

Search engines (Googlebot, Bingbot) and AI retrieval engines (Perplexity, SearchGPT) parse these as isolated, unlinked semantic fragments. They cannot infer with certainty whether the author in Tag 3 belongs to the organization in Tag 1, or whether the FAQ in Tag 4 belongs to the article in Tag 3.

### 1.2 The Solution: Single Interconnected `@graph`
By wrapping all entities inside a single top-level `@graph` array under `@context: "https://schema.org"`, every entity becomes a node in an interconnected Knowledge Graph linked via deterministic `@id` URIs.

```
       [WebSite (#website)]
          ↓ isPartOf
       [WebPage (#webpage)]
          ↓ mainEntity
   [TechArticle (#article)] ──── publisher ────→ [Organization (#organization)]
          ↓ author                                        ↑ worksFor
   [Person (#author)] ────────────────────────────────────┘
          ↓
  [BreadcrumbList (#breadcrumb)] & [FAQPage (#faq)]
```

---

## 2. Canonical `@id` URI Anchor Conventions

To link entities unambiguously without duplicating nested objects, every node must declare a globally unique `@id` URI composed of the canonical document URL plus a fragment identifier.

| Node Type | Canonical `@id` Format | Purpose / Role |
|-----------|------------------------|----------------|
| `WebSite` | `https://example.com/#website` | Root site container with search action |
| `Organization` | `https://example.com/#organization` | Publisher / corporate entity credentials |
| `Person` | `https://example.com/authors/<slug>/#author` | Author E-E-A-T credentials and social proof |
| `WebPage` | `<page-canonical-url>#webpage` | Document container linking breadcrumbs and primary entity |
| `TechArticle` / `Article` | `<page-canonical-url>#article` | Primary informational asset with semantic topics |
| `BreadcrumbList` | `<page-canonical-url>#breadcrumb` | Navigational hierarchy |
| `FAQPage` | `<page-canonical-url>#faq` | Structured Q&A microdata for generative search extraction |

---

## 3. Production Unified `@graph` Reference Implementation

The following complete JSON-LD specification demonstrates the production standard for an engineering article.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "url": "https://example.com",
      "name": "Engineering Insights",
      "description": "High-performance systems and search engineering",
      "publisher": {
        "@id": "https://example.com/#organization"
      }
    },
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example Technologies Inc.",
      "url": "https://example.com",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://example.com/#logo",
        "url": "https://example.com/assets/logo.png",
        "caption": "Example Technologies Logo",
        "width": 600,
        "height": 60
      },
      "sameAs": [
        "https://www.linkedin.com/company/example-tech",
        "https://github.com/example-tech",
        "https://twitter.com/exampletech"
      ]
    },
    {
      "@type": "Person",
      "@id": "https://example.com/authors/alex-mercer/#author",
      "name": "Alex Mercer",
      "jobTitle": "Principal Systems Architect",
      "worksFor": {
        "@id": "https://example.com/#organization"
      },
      "image": "https://example.com/assets/authors/alex-mercer.webp",
      "sameAs": [
        "https://www.linkedin.com/in/alex-mercer-systems",
        "https://github.com/alexmercer-dev",
        "https://scholar.google.com/citations?user=alexmercer"
      ],
      "knowsAbout": [
        {
          "@type": "Thing",
          "name": "PostgreSQL",
          "sameAs": "https://www.wikidata.org/wiki/Q192490"
        },
        {
          "@type": "Thing",
          "name": "Distributed Systems",
          "sameAs": "https://www.wikidata.org/wiki/Q242187"
        }
      ]
    },
    {
      "@type": "WebPage",
      "@id": "https://example.com/blog/distributed-postgres-patterns/#webpage",
      "url": "https://example.com/blog/distributed-postgres-patterns",
      "name": "Distributed PostgreSQL Architecture and Connection Pooling",
      "isPartOf": {
        "@id": "https://example.com/#website"
      },
      "breadcrumb": {
        "@id": "https://example.com/blog/distributed-postgres-patterns/#breadcrumb"
      },
      "mainEntity": {
        "@id": "https://example.com/blog/distributed-postgres-patterns/#article"
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://example.com/blog/distributed-postgres-patterns/#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://example.com"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "https://example.com/blog"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": "Distributed PostgreSQL Patterns",
          "item": "https://example.com/blog/distributed-postgres-patterns"
        }
      ]
    },
    {
      "@type": "TechArticle",
      "@id": "https://example.com/blog/distributed-postgres-patterns/#article",
      "isPartOf": {
        "@id": "https://example.com/#website"
      },
      "mainEntityOfPage": {
        "@id": "https://example.com/blog/distributed-postgres-patterns/#webpage"
      },
      "headline": "Distributed PostgreSQL Architecture and Connection Pooling",
      "description": "Architectural guide for scaling PostgreSQL connection pools with transaction mode and zero-downtime migrations.",
      "image": [
        "https://example.com/images/postgres-pooling-16x9.webp",
        "https://example.com/images/postgres-pooling-4x3.webp",
        "https://example.com/images/postgres-pooling-1x1.webp"
      ],
      "datePublished": "2026-09-18T08:00:00+00:00",
      "dateModified": "2026-09-18T10:30:00+00:00",
      "author": {
        "@id": "https://example.com/authors/alex-mercer/#author"
      },
      "publisher": {
        "@id": "https://example.com/#organization"
      },
      "proficiencyLevel": "Expert",
      "dependencies": "PostgreSQL 16+, PgBouncer 1.21+ or Supavisor",
      "targetPlatform": "Linux / Docker / Kubernetes",
      "about": [
        {
          "@type": "Thing",
          "name": "PostgreSQL",
          "sameAs": "https://www.wikidata.org/wiki/Q192490"
        },
        {
          "@type": "Thing",
          "name": "Connection Pool",
          "sameAs": "https://www.wikidata.org/wiki/Q1125203"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "@id": "https://example.com/blog/distributed-postgres-patterns/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is the recommended PgBouncer pool mode for serverless functions?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Transaction mode is the recommended pool mode for serverless functions because connections are returned to the pool immediately after each transaction completes, maximizing concurrency."
          }
        }
      ]
    }
  ]
}
```

---

## 4. Referential Integrity Rules

When generating connected graphs:
1. **Zero Dangling Pointers**: Every `@id` referenced in an object pointer (e.g. `"publisher": {"@id": "https://example.com/#organization"}`) **must** exist as a top-level node definition in the same `@graph` array or be resolvable at that exact absolute URI.
2. **Circular Reference Safety**: Relational references using `@id` pointers prevent recursive JSON serialization depth errors while maintaining full bi-directional relationship graphs for search spiders.
3. **Array Type Declarations**: Multi-type entities can be declared using an array: `["TechArticle", "BlogPosting"]`.
