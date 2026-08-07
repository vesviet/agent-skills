---
description: End-to-end workflow for SEO analysis, deep data research, content drafting, auditing, and publishing.
---

## SEO Content Lifecycle Workflow

Use this workflow when a new content initiative is starting from a general topic — before an SEO brief even exists — and needs to go all the way through briefing, deep research, drafting, auditing, and final publication in one continuous cycle.

This workflow wraps [content-publishing](content-publishing.md): steps 1–2 here create the brief and research that `content-publishing` assumes as a prerequisite. Once the brief exists, steps 3–6 here are the same drafting → audit → publish sequence as `content-publishing` steps 3–8, just summarized — follow `content-publishing` for the detailed sub-steps, self-check items, and exact `content-handoff.json` field requirements.

### When To Use

- a new topic needs an SEO brief, deep research, and drafting in one continuous cycle
- a sprint requires end-to-end execution of a content piece
- multiple specialist roles need to collaborate from ideation to deployment

If a brief already exists and only drafting/audit/publish remain, use [content-publishing](content-publishing.md) directly instead.

### Prerequisites

- the broad topic, target audience, and business goals are defined
- the target site and content repository are known
- the publisher (user or pipeline) has deploy access to the site

### Workflow Steps

#### 1. Plan The Topic And SEO Brief

Role: **Task Planner**, **SEO Analyst**

- clarify the content intent and business outcome
- the SEO Analyst executes the SEO briefing process to produce `seo-content-brief.json`
- verify the primary keyword and internal linking strategy

#### 2. Deep Data Research

Role: **Researcher**

Use skill: `conduct-research`

- investigate the topic to gather data, statistics, competitor analysis, or expert quotes
- focus on fulfilling the E-E-A-T experience proof requirements specified in the SEO brief
- document findings and verifiable data points in `research-report.json`

#### 3. Draft, Audit, And Publish

Role: **Content Writer**, **SEO Analyst**, **Content Manager**, **Technical Lead**

Follow [content-publishing](content-publishing.md) steps 3–8 in full: draft against the brief, self-check, SEO audit, revise, and publish with explicit user approval. That workflow owns the detailed checklist and field-level requirements for `content-handoff.json`, `seo-audit-report.json`, and `publish-log.md` — this entry point exists only to prepend the planning and research steps above it.

### Checklist

- [ ] topic planned and intent clarified
- [ ] seo-content-brief.json produced with keyword and link targets
- [ ] research-report.json produced with data points and E-E-A-T evidence
- [ ] draft written per content-publishing workflow steps 3–5 (brief-aligned, self-checked)
- [ ] SEO audit and metadata produced per content-publishing workflow step 5
- [ ] Blocking findings resolved per content-publishing workflow step 6
- [ ] article published and publish-log.md updated per content-publishing workflow steps 7–8

### Related Workflows

- [content-publishing](content-publishing.md) — the draft-through-publish sequence this workflow hands off to after step 2
- [seo-keyword-brief](seo-keyword-brief.md)
- [content-audit](content-audit.md)
- [qa-validation](qa-validation.md)

### Related Skills

- **optimize-seo**: Audit drafts and produce SEO briefs
- **conduct-research**: Gather evidence for E-E-A-T requirements
- **write-article**: Plan, research, and draft long-form content
