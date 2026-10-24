# Rich Results and Schema Validation Guide

This guide provides technical reference specifications for achieving Google Rich Results compliance, enforcing 1:1 on-page content mirroring, and eliminating schema syntax drift.

---

## 1. Google Rich Results Requirements

To qualify for enhanced search displays (Rich Snippets, Knowledge Panels, Carousel features), structured data must adhere to strict Google Search Central specifications.

### 1.1 Article and TechArticle Rich Results Requirements

| Property | Requirement Level | Constraints and Formatting |
|----------|-------------------|----------------------------|
| `headline` | **Required** | Max 110 characters recommended; must match on-page H1 or title. |
| `image` | **Required** | Array of high-resolution images in 3 aspect ratios: `16x9`, `4x3`, and `1x1`. Min width: 1200px. Must be crawlable and indexable. |
| `datePublished` | **Required** | Valid ISO-8601 string (e.g. `2026-09-18T08:00:00+00:00`). Must include timezone offset. |
| `dateModified` | **Recommended** | Valid ISO-8601 string; required if content has been refreshed or revised. |
| `author` | **Required** | Must resolve to a `Person` or `Organization` object (or `@id` pointer). Plain string names are discouraged. |
| `publisher` | **Required** | Must resolve to an `Organization` object with a valid `logo` (ImageObject). |

### 1.2 BreadcrumbList Requirements
- Each item in `itemListElement` must have:
  - `@type`: `"ListItem"`
  - `position`: Integer starting at `1` and incrementing sequentially (`1, 2, 3...`).
  - `name`: Breadcrumb label matching on-page navigation text.
  - `item`: Canonical absolute URL (the last item representing the current page may omit `item` or point to self).

### 1.3 FAQPage: SERP Restrictions vs. Generative Engine Optimization (GEO)
- **Traditional Google SERP**: In August 2023, Google restricted standard FAQ rich snippet displays in SERP search results primarily to authoritative government and health websites.
- **Generative AI Engines (Perplexity, SearchGPT, Google AI Overviews)**: FAQPage JSON-LD remains one of the highest-weight semantic sources for direct passage retrieval, synthesized answers, and multi-turn conversational follow-ups.
- **Guideline**: Implement `FAQPage` schema on comprehensive guides and technical docs for AI discoverability, while setting accurate client expectations regarding traditional Google SERP drop-down pills.

---

## 2. The 1:1 Content Mirroring Rule (Anti-Spam Compliance)

Google's structured data guidelines strictly prohibit injecting schema markup for content that is not visible to human users. Violating this rule triggers manual algorithmic actions for "Spammy Structured Markup".

### 2.1 The Golden Invariant
$$\text{Schema Markup Content} \subseteq \text{Human-Visible Rendered Content}$$

- **FAQ Pairs**: Every Question and Answer declared in the `FAQPage` schema must be displayed on the page text verbatim or near-verbatim. Hidden accordion text that is never rendered or text hidden via `display: none` intended solely for bots violates policy.
- **Author Identity**: If the schema lists "Alex Mercer, Principal Architect", the rendered page must display Alex Mercer's byline and role.
- **Review / Ratings**: Product or article ratings must correspond to genuine, inspectable user reviews on the page. Fictitious aggregate ratings (`5.0 with 9,999 reviews`) trigger immediate penalty.

---

## 3. Eliminating Schema Drift

Schema drift occurs when site content or frontmatter is updated, but the static JSON-LD block remains untouched, resulting in conflicting signals.

### 3.1 Common Drift Scenarios and Safeguards

| Drift Vector | Manifestation | Prevention / Remediation |
|--------------|---------------|--------------------------|
| **Date Desynchronization** | Frontmatter updated to `2026-09-18`, but JSON-LD still reports `2024-01-10`. | Bind JSON-LD generation directly to Astro/Next.js content collection schemas. |
| **Headline Mismatch** | Editor updates H1 title, but hardcoded JSON-LD headline displays old title. | Inject `headline: entry.data.title` dynamically in template layouts. |
| **Dangling Author `@id`** | Author slug changed in CMS, breaking `@id` relational binding in schema graph. | Automate author node ID generation from canonical author slugs. |
| **Stale Pricing / Inventory** | Schema reports `$49 InStock`, but page displays `$79 OutOfStock`. | Fetch schema data from the live product inventory state. |

---

## 4. Validation Workflow and Tooling

Structured data must pass both standard syntax validation and search-engine-specific eligibility gates.

### 4.1 Validation Tool Matrix

1. **Schema.org Validator (validator.schema.org)**:
   - Validates JSON-LD syntax, Schema.org type inheritance, and property vocabulary.
   - Confirms that `@graph` arrays and `@id` relational references resolve cleanly without errors.
2. **Google Rich Results Test (search.google.com/test/rich-results)**:
   - Evaluates compliance with Google-specific rich snippet requirements.
   - Flags missing required properties (fatal error) and recommended properties (warning).

### 4.2 Automated Pre-Publish Assertion Checklist
Before submitting schema code for production:
1. `jq .` or `json.loads()` passes syntax check with zero JSON parse errors.
2. `@context` is exactly `"https://schema.org"`.
3. `@graph` is a non-empty array of objects.
4. All `@id` references in relational fields (`author`, `publisher`, `isPartOf`) match an existing `@id` declaration.
5. All dates conform to `YYYY-MM-DDTHH:mm:ssZ` or `YYYY-MM-DDTHH:mm:ss+HH:MM`.
