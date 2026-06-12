# Vesviet Content Rules

Voice, style, structure, and publishing constraints for the Vesviet portfolio site and Learn site.

## Role Integration

- **`content-writer`**: Must adhere to these rules when drafting content.
- **`seo-analyst`**: Must audit against these rules (frontmatter, GEO/AEO answer-first formats, internal linking) before publish.

## Directory Structure

Content on Vesviet must be organized into these three directories based on purpose:
- **`posts/`**: In-depth technical articles and tutorials.
- **`radar/`**: Periodic Tech Radar newsletters (e.g., industry news, tool updates).
- **`series/`**: Linked chains of articles on a specific topic.

## Frontmatter Requirements

Every new file must include the following mandatory frontmatter fields:
```yaml
---
title: "..."
slug: "..."
date: "YYYY-MM-DDTHH:MM:SS+07:00"
lastmod: "YYYY-MM-DDTHH:MM:SS+07:00"
draft: false
description: "..."
tags: ["...", "..."]
categories: ["...", "..."]
ShowToc: true
TocOpen: true
---
```
*Note: Add `mermaid: true` if the post contains Mermaid diagrams.*

## Writing Style & Formatting

- **Answer-First**: The introduction MUST begin with `**Answer-first:**` followed by a direct, concise answer to the topic's core question in ≤60 words.
- **Tone**: Professional, technical deep-dive. Get straight to the point, no fluff.
- **Alerts**: Use GitHub Markdown Alerts strategically (`> [!NOTE]`, `> [!WARNING]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!CAUTION]`) to highlight key information instead of bold text.

## Assets & Internal Linking

- **Images**: Store all image files in `static/images/` or `assets/images/`.
- **Image Links**: Use absolute root-relative paths in Markdown (e.g., `![Alt Text](/images/filename.png)`).
- **Internal Links**: Use standard Markdown linking pointing directly to the slug (e.g., `[Link Text](/posts/magento-still-worth-investing-2026)`).

## Series & Production Failure Rules (Legacy)

- **Production Failure stories**: Use the standardized template:
  ```
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
