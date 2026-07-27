# Astro v5 Content Collection Schema

This rule enforces the mandatory schema requirements for Astro v5 `content` collections used in `leaseinvietnam` and `maylanhtreotuong`. 

## 1. Post Collection (`src/content/post/`)
Every blog post or article must include the following YAML frontmatter exactly as defined in the Zod schema (`src/content/config.ts`):

```yaml
---
title: "Primary H1 Title (60 chars max)"
description: "SEO Meta Description (150 chars max, must contain primary keyword)"
pubDate: 2026-07-27T08:00:00Z
updatedDate: 2026-07-27T10:00:00Z # Optional but recommended for refreshed content
heroImage: "/images/posts/your-image.jpg"
categories: ["Architecture", "Backend"] # Explicit inline array required
tags: ["Astro", "Cloudflare"] # Explicit inline array required
canonicalURL: "https://example.com/original-source/" # Use only if syndicated
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
- **No HTML Mixed**: Rely strictly on Markdown. Astro MDX handles components if needed, but standard `.md` files should be pure markdown.
- **Internal Links**: Must point to absolute paths without extensions (e.g., `[Máy lạnh Inverter](/danh-muc/may-lanh-inverter/)`).
