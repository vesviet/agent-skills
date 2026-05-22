---
name: optimize-seo
description: Research search intent, define keywords, produce SEO content briefs, audit on-page elements, and deliver metadata and recommendations without owning full article drafting or technical deployment. Use when planning publishable content, reviewing drafts before release, mapping internal links, or interpreting Search Console signals for content changes.
---

# Optimize SEO

Use this skill for **search and content-structure** work — not for writing long-form copy (Content Writer) or implementing sitemaps/redirects in production (Frontend/DevOps).

## Core Rules

- define **search intent** and **primary keyword** before recommending titles or outlines
- separate **evidence** (SERP snippets, GSC exports, crawlable page facts) from **recommendations**
- document **internal link targets** with anchor rationale and destination paths
- enforce on-page limits: title tag ≤ 60 chars, meta description ≤ 160 chars unless repo rules differ
- check **keyword cannibalization** against recent publishes on the same site (default: 7-day window when a topic board exists)
- do not guarantee rankings; recommend changes tied to observable gaps
- escalate **technical SEO** (canonical, schema markup, redirects, Core Web Vitals fixes) with a clear engineering brief
- use repo overlays under overlays/lease-content and overlays/vesviet-content when site-specific slug or frontmatter rules apply
- use overlays/seo-publishing for dual-site Lease + May lanh sprint boards under plan/baiviet

## When to Use

- a topic needs a **content brief** before Content Writer drafts
- a draft or live URL needs an **on-page SEO audit**
- title, meta, slug, H2 structure, or FAQ block need optimization
- a weekly topic board needs keyword assignment and link targets
- Search Console or analytics exports suggest title/meta or cluster changes
- `seo-metadata.json`, `seo-content-brief.json`, or `seo-audit-report.json` handoff is required

## Suggested Process

### 1. Frame Intent

Capture:

- target URL or planned slug
- audience and business outcome (lead, trust, education)
- primary and secondary keywords
- locale and competing pages on the same site

### 2. Research (SERP-focused)

- review top SERP titles, snippets, and common H2 patterns (lightweight passes — not full Researcher depth)
- note content gaps versus intent (informational, commercial, navigational)
- record cannibalization risk against existing URLs

### 3. Brief Or Audit

**Brief path:** outline H2s, FAQ, internal links, word-count band, out-of-scope topics → `seo-content-brief.json`

**Audit path:** score title, meta, headings, links, schema needs → `seo-audit-report.json` + updated `seo-metadata.json` when ready to publish

### 4. Hand Off

- to **Content Writer** with brief and metadata draft
- to **Task Planner** when board order or topic mix must change
- to **Frontend/DevOps** for technical SEO implementation tickets
- to **Data Analyst** when metric definitions for GSC comparisons need formalization

## Checklist

- [ ] search intent and primary keyword explicit
- [ ] secondary keywords listed (typically 2–4)
- [ ] internal link targets named (minimum 3 when site baseline requires it)
- [ ] title and meta within length limits and aligned with keyword
- [ ] cannibalization check documented
- [ ] facts separated from recommendations
- [ ] technical items escalated, not silently implemented in prod

## Related Skills

- **conduct-research**: deeper domain or competitor context when SERP scan is insufficient
- **analyze-business-requirements**: align SEO goals with business rules and actors
- **analyze-data**: formal GSC/CTR tables when SEO Analyst needs verified baselines
- **write-documentation**: metric catalogs or SEO playbooks for a site
- **agent-delegation**: delegate drafting to Content Writer or technical work to Frontend
