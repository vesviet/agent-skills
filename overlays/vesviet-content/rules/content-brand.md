# Vesviet Content Rules

Voice, style, structure, and publishing constraints for the Vesviet portfolio site and Learn site.

## Role Integration

- **`content-writer`**: Must adhere to these rules when drafting content.
- **`seo-analyst`**: Must audit against these rules (frontmatter, GEO/AEO answer-first formats, internal linking) before publish.
- **`reviewer`**: Must enforce AI Governance, Information Gain, and E-E-A-T requirements before code review passes.

## Directory Structure

Content on Vesviet must be organized into these three directories based on purpose:
- **`posts/`**: In-depth technical articles and tutorials.
- **`radar/`**: Periodic Tech Radar newsletters (e.g., industry news, tool updates).
- **`series/`**: Linked chains of articles on a specific topic.

## Frontmatter Requirements

Every new file must include the following mandatory frontmatter fields to pass the 100% Schema Completeness audit:
```yaml
---
title: "..."
slug: "..."
author: "..."
date: "YYYY-MM-DDTHH:MM:SS+07:00"
lastmod: "YYYY-MM-DDTHH:MM:SS+07:00"
draft: false
description: "..."
tags: ["...", "..."]
categories: ["...", "..."]
cover: 
  image: "images/posts/cover-image.png"
  alt: "..."
ShowToc: true
TocOpen: true
---
```
*Note: Add `mermaid: true` if the post contains Mermaid diagrams.*

## Content Depth & Formatting (GEO/AEO)

- **Answer-First**: The introduction MUST begin with `> **Answer-first:**` followed by a direct, concise answer to the topic's core question in ≤60 words.
- **Content Depth**: All technical articles and pillar posts must target a minimum length of **≥ 1,400 words**. Do not publish thin content (<1,000w) as standalone pages.
- **Tone**: Professional, technical deep-dive. Get straight to the point, no fluff.
- **Alerts**: Use GitHub Markdown Alerts strategically (`> [!NOTE]`, `> [!WARNING]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!CAUTION]`) to highlight key information instead of bold text.

## Affiliate Compliance (Learn Site)

- **Link Tagging**: All outbound affiliate links must use `rel="sponsored"`.
- **Disclosures**: A clear affiliate disclosure must be present on any page containing affiliate links, located near the recommendation.

## 2026 Information Gain & E-E-A-T Requirements

To combat the commoditization of AI-generated content, all in-depth articles MUST include explicit Information Gain:
- **Firsthand Experience**: The writer must include real-world anecdotes or "Production Failure" stories to prove human expertise.
- **Expert Quotes & Sourcing**: If applicable, quote Subject Matter Experts (SMEs). Never rely solely on AI-synthesized knowledge.
- **Zero Raw Hallucinations**: Do not inject generic boilerplate phrasing. Every technical claim must be verifiable.

## Assets & Internal Linking

- **Images**: Store all image files in `static/images/` or `assets/images/`.
- **Image Links**: Use absolute root-relative paths in Markdown (e.g., `![Alt Text](/images/filename.png)`).
- **Internal Links**: Use standard Markdown linking pointing directly to the slug (e.g., `[Link Text](/posts/magento-still-worth-investing-2026)`).

## Series & Production Failure Rules

- **Production Failure stories**: Use the standardized template:
  ```markdown
  > 🔥 **[Production Failure]: <Title>**
  > **Symptom:** ...
  > **Root Cause:** ...
  > 📊 **Impact:** ...
  > 📈 **Resolution:** ...
  > *(Source: ...)*
  ```
- **Prerequisite block**: Every series part must open with a `> **Prerequisite:**` blockquote.
- **CTA**: Every series part must close with `🔗 **Next Step:**` linking to the next part.
- **Bilingual Rule**: Use Vietnamese colloquial phrasing where it aids clarity, but keep technical terminology in English (e.g., "Context Window", "Prompt Injection") and provide English equivalents on first mention.
