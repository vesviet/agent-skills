# Astro v5 Content Collection Schema

This rule enforces the mandatory schema requirements for Astro v5 `content` collections used in `leaseinvietnam` and `maylanhtreotuong`. 

## 1. Post Collection (`src/content/post/` or `src/data/post/`)
Every blog post or article must include the following YAML frontmatter exactly as defined in the Zod schema (`src/content/config.ts`):

```yaml
---
title: "Primary H1 Title (strictly <= 60 chars, ZERO trailing ...)"
description: "SEO Meta Description (120-155 chars, must contain primary keyword)"
pubDate: 2026-07-27T08:00:00Z
updatedDate: 2026-07-27T10:00:00Z # Optional but recommended for refreshed content
heroImage: "/images/posts/your-image.jpg"
categories: ["guides"] # Explicit inline array required
tags: ["expat", "visa"] # Explicit inline array required
unique_angle: "Specific, non-generic information gain statement."
anti_slop_gate: 
  gate_passed: true
draft: false
---
```

## 2. Property / Product Collection (`src/content/property/` or `src/content/product/`)
Commercial/transactional pages have strict requirements for localized metadata:

```yaml
---
title: "Product/Property Name"
price: 15000000
currency: "VND"
location: "District 1, HCMC" # For leaseinvietnam
specs: 
  capacity: "1 HP" # For maylanhtreotuong
  inverter: true
images: ["/images/products/main.jpg", "/images/products/detail.jpg"]
draft: false
---
```

## 3. JSON-LD & Schema.org Integration
- **`post` collection**: Automatically mapped to `TechArticle` or `Article` by the SEO layout component.
- **`product` collection**: Must provide `price` and `currency` for the `Product` JSON-LD schema generation.
- **NEVER** use manual `<script type="application/ld+json">` tags in Astro Markdown unless explicitly bypassing the built-in SEO component.

## 4. Markdown Formatting Rules
- **No HTML Mixed**: Rely strictly on Markdown for generic formatting. 
- **AnswerFirst Component (MANDATORY)**: All articles must use the `<AnswerFirst>` MDX component instead of markdown blockquotes (e.g., `> **Quick Answer:**`) for the ≤60-word summary.
  ```astro
  import AnswerFirst from '../../components/AnswerFirst.astro';

  <AnswerFirst>
  Summary answer text here...
  </AnswerFirst>
  ```
- **Internal Links**: Must point to absolute paths without extensions (e.g., `[District 1 Rentals](/post/apartment-for-rent-district-1-hcmc)`).
