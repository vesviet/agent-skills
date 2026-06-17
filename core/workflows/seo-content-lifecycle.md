---
description: End-to-end workflow for SEO analysis, deep data research, content drafting, auditing, and publishing.
---

## SEO Content Lifecycle Workflow

Use this workflow when a new content initiative is starting from a general topic and needs to go all the way through SEO briefing, deep research, drafting, auditing, and final publication.

### When To Use

- a new topic needs an SEO brief, deep research, and drafting in one continuous cycle
- a sprint requires end-to-end execution of a content piece
- multiple specialist roles need to collaborate from ideation to deployment

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

#### 3. Draft The Article

Role: **Content Writer**

Use skill: `write-article`

- consume both the `seo-content-brief.json` and `research-report.json`
- draft the article following the answer-first structure and word count targets
- embed required internal links and on-page formatting

#### 4. SEO And Quality Audit

Role: **SEO Analyst**, **Reviewer**

Use skill: `optimize-seo`

- audit the written draft against the brief to ensure on-page spec compliance
- check keyword density, internal links, and answer-first formatting
- emit `seo-audit-report.json` with findings categorized as Blocking, Important, or Follow-Up
- emit `seo-metadata.json` with final title, meta description, and slug

#### 5. Revise And Handoff

Role: **Content Writer**

- address any Blocking findings from the SEO audit
- emit `content-handoff.json` confirming that the brief was followed and the audit was passed
- explicitly wait for user approval before moving to publish

#### 6. Publish And Record

Role: **Technical Lead**, **Content Writer**

- deploy the content only after explicit user approval
- append `publish-log.md` with the publish date, article title, keyword, and internal links
- update `content-handoff.json` to mark the publish log as updated

### Checklist

- [ ] topic planned and intent clarified
- [ ] seo-content-brief.json produced with keyword and link targets
- [ ] research-report.json produced with data points and E-E-A-T evidence
- [ ] draft written according to brief guidelines
- [ ] seo-audit-report.json and seo-metadata.json produced
- [ ] Blocking issues from audit resolved
- [ ] content-handoff.json emitted
- [ ] article published with explicit user approval
- [ ] publish-log.md appended with final URL and keyword

### Related Workflows

- [seo-keyword-brief](seo-keyword-brief.md)
- [content-publishing](content-publishing.md)
- [qa-validation](qa-validation.md)

### Related Skills

- **optimize-seo**: Audit drafts and produce SEO briefs
- **conduct-research**: Gather evidence for E-E-A-T requirements
- **write-article**: Plan, research, and draft long-form content
