# Leaseinvietnam Content Rules

Content schema and writing guidelines for the `leaseinvietnam` repository, based on the `src/data` audit.

## Role Integration & Workflow

- **`content-writer`**: Must adhere to these rules and schemas when drafting posts or property listings.
- **`seo-analyst`**: Audits the content for on-page SEO, internal linking, and adherence to the daily sprint (1 post/day/site).
- **Daily Sprint**: Content production often runs in dual-site sprint mode alongside `maylanhtreotuong`. 

## Directory Structure & Assets

- **`src/data/post/`**: All blog posts must be placed inside a specific lowercase, hyphenated category subdirectory (e.g., `guides/`, `living/`, `market-radar/`). Root-level post files are strictly prohibited.
- **`src/data/property/`**: All property listings are placed directly at the root of this folder.
- **Images**: When referencing images from `src/assets/images/` inside a post, the relative path must account for the category directory nesting (e.g., `../../../assets/images/filename.jpg`).

## Post Content Schema (`src/data/post/`)

Every new blog post must include the following mandatory frontmatter:
```yaml
---
title: "..."
category: "..." # Must match the parent folder name
tags: ["...", "..."]
publishDate: "YYYY-MM-DD"
---
```

## Property Content Schema (`src/data/property/`)

Every new property listing must include the following mandatory frontmatter fields:
```yaml
---
title: "..."
publishDate: "YYYY-MM-DDTHH:MM:SSZ"
excerpt: "..."
image: "..." # Absolute URL or relative path
price: 00000000
currency: "VND"
bedrooms: 0
bathrooms: 0
area: 0
location: "..."
propertyType: "..."
tags: ["...", "..."]
---
```

## Writing Tone (Properties)

- **Transparent Analysis**: Property descriptions must go beyond standard sales pitches. Present a clear, balanced view of both the **"Value Proposition"** (What you get) and the **"Trade-offs"** (What you give up / The downsides). 
- Use headings like *"What This Location Gets You (And What It Doesn't)"* to establish trust with the expat audience.
