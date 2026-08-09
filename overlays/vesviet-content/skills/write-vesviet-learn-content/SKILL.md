---
name: write-vesviet-learn-content
description: Draft or update Hugo Markdown for the Vesviet portfolio site or the Learn notes site. Use when creating or editing content under `vesviet/content` or `learn/content` (paths relative to the workspace root), including posts, series, radar entries, or learn docs.
---

# Write Vesviet Learn Content

Use this skill when new or updated articles must land in one of the two Hugo sites whose content roots are fixed below.

## Content Roots

| Site | Content path (relative to workspace root) | Public site (from `hugo.toml`) |
|------|------------------------|----------------------------------|
| Vesviet (portfolio / blog) | `vesviet/content` | `https://tanhdev.com/` |
| Learn (notes / research) | `learn/content` | `https://learn.tanhdev.com/` |

Both sites use the **PaperMod** theme, Vietnamese or English copy is acceptable when it matches sibling pages in the same folder.

## Core Rules

- **Schema Completeness**: Every file MUST include `title`, `author`, `date`, `tags`, `categories`, and `cover` in strict inline YAML (e.g., `categories: ["Backend", "Golang"]`).
- **GEO/AEO Answer-First**: Every article must open with `> **Answer-first:**` and a ≤60-word summary block immediately below the frontmatter.
- **Hub-and-Spoke Linking (`vesviet`)**: Ensure zero orphans. Every new article must link up to at least one of the 10 Anchor Pillar Hubs (e.g., `go-microservices.md`).
- **Affiliate Compliance (`learn`)**: All outbound affiliate links must use `rel="sponsored"`. Mandatory disclosures must be near recommendations.
- **Content Depth & E-E-A-T**: Target ≥ 1,400 words for technical deep-dives and reviews. Do not rely on AI hallucinations; inject real-world experience, benchmarks, or "Production Failure" templates.

## Suggested Process

### 1. Pick The Site And Subtree
Decide `vesviet` (Technical Engineering) vs `learn` (Affiliate Marketing). 

### 2. Follow Content Brand Guidelines
- **For `vesviet`**: Use the Content Audit & Refresh Workflow. Apply Hub-and-Spoke linking.
- **For `learn`**: Use the Affiliate Publishing Workflow. Categorize as Money Page, Supporting, or Trust Page.

### 3. Draft In Place
- Ensure strict YAML frontmatter.
- Start the body with the `> **Answer-first:**` block.
- Inject E-E-A-T elements (diagrams, benchmarks, pros/cons, evaluation criteria).

### 4. Wire Navigation & Topology
- **`vesviet`**: Link your article to a Pillar Hub. Update `reading-map.md` if creating a new series.
- **`learn`**: Internal link from Supporting articles to Money pages.

### 5. Sanity Check
Confirm `draft` flag, schema completeness, zero orphan status, and `rel="sponsored"` for affiliate links.

## Checklist

- [ ] Frontmatter uses strict inline YAML and contains all 6 mandatory fields (`title`, `author`, `date`, `tags`, `categories`, `cover`).
- [ ] Article opens with `> **Answer-first:**` summary block (≤60 words).
- [ ] Content depth targets ≥ 1,400 words (unless explicit programmatic/trust page).
- [ ] **`vesviet`**: Internal link points to an Anchor Pillar Hub (zero orphans).
- [ ] **`learn`**: Affiliate links use `rel="sponsored"` and include disclosure.

## Related Skills

- **write-documentation**: general doc drafting discipline and clarity patterns
- **write-tech-radar**: concise decision framing for radar-style entries
- **meeting-review**: synthesize stakeholder input before publishing sensitive claims
