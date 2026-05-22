---
name: write-article
description: Plan, research, outline, and draft long-form articles and blog posts with explicit evidence discipline, editorial structure, and SEO-brief alignment. Use for narrative content, guides, reviews, and announcements—not for API runbooks or pure technical reference docs.
---

# Write Article

Use this skill with the **Content Writer** role when the deliverable is a publishable article (Markdown, MDX, or Hugo/Astro content files).

## Core Rules

- clarify audience, goal, CTA, and channel before drafting
- when research is required, run **at least three to four distinct passes** (different questions, sources, or angles) unless Researcher already delivered research-report.json
- when sources are supplied, synthesize only from that material—do not duplicate research
- separate verified facts, attributed claims, and author judgment
- follow seo-content-brief.json when SEO Analyst provided a brief; do not invent keyword or link strategy
- apply site overlay skills (lease-content, vesviet-content) for frontmatter, paths, and schema
- produce `contracts/schemas/content-handoff.json` when machine handoff is required

## Research Depth Decision

| Situation | Action |
| --------- | ------ |
| User supplied complete sources or repo exemplars | No net-new research; document sources used |
| Editorial article, familiar domain, moderate claims | **3–4 passes** logged in handoff |
| Regulated, YMYL, novel market, or disputed facts | Delegate to **Researcher** first; draft from research-report.json |
| SEO sprint with seo-content-brief.json | Brief supplies outline/links; research only for gaps in brief |
| Technical behavior claims | Align with Technical Writer / engineering source-of-truth |

## Suggested Process

### 1. Consume Inputs

- seo-content-brief.json, feature-ticket.json (BA positioning), or plan/baiviet daily plan
- research-report.json from Researcher when present
- repo exemplars and overlay rules

### 2. Plan And Research

- fill Brief and Research sections in output template
- execute passes or cite Researcher synthesis

### 3. Outline And Draft

- match H2/FAQ from SEO brief when applicable
- implement internal links from brief or plan
- use overlay skill for MDX/Markdown file authoring

### 4. Package Handoff

- emit content-handoff.json with path, word count, passes, unverified claims
- request SEO Analyst audit before publish when site requires it

### 5. Publish Sprint (optional)

When overlays/seo-publishing is active, after user confirms publish, append plan/baiviet/publish-log.md per overlay conventions.

## Checklist

- [ ] audience, goal, and format explicit
- [ ] research depth appropriate (3–4 passes, Researcher, or supplied-only documented)
- [ ] SEO brief consumed when required
- [ ] overlay schema and paths validated against peers
- [ ] facts vs judgment separated
- [ ] content-handoff.json complete when JSON handoff required
- [ ] SEO audit requested before publish when required

## Related Skills

- **write-documentation**: Structure and clarity patterns; technical README/runbooks belong with Technical Writer
- **write-tech-radar**: Radar-style technology assessments (Vesviet radar subtree)
- **write-leaseinvietnam-maylanhtreotuong-data**: Astro MDX for Lease and May lanh sites (overlay)
- **write-vesviet-learn-content**: Hugo content for Vesviet and Learn (overlay)
- **analyze-business-requirements**: Align copy with business rules when BA supplied a ticket
- **meeting-review**: Resolve stakeholder conflicts before drafting sensitive claims
