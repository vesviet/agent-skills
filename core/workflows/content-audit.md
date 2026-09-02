---
description: Content Manager-led refresh cycle for existing published content — baseline audit, read, research the latest standards, update, and re-audit for SEO/GEO/AEO before republish.
---

## Content Audit Workflow

Use this workflow when the Content Manager audits existing published content to decide what to keep, refresh, expand, consolidate, or retire — then drives the refresh of the pieces worth updating through to a post-update SEO/GEO/AEO audit and republish. It is the operational expression of the `audit-content` skill and coordinates Data Analyst, Content Writer, Researcher, and SEO Analyst around the Content Manager's ownership of content lifecycle decisions.

### When To Use

- a periodic (minimum quarterly) content audit cycle is due
- a published article or cluster shows declining traffic, stale facts, or lost rankings
- competitors or AI answers now cover ground the existing content lacks (information-gain gap)
- legacy content must be brought up to current E-E-A-T and AI-search standards without a full rewrite
- a stakeholder requests a "refresh" and the decision to refresh vs consolidate vs retire must be made on data, not intuition

### Prerequisites

- the audit scope is defined: which URLs, pillar, or cluster is under review
- read access to performance data (GSC/analytics exports, or a Data Analyst who can provide them)
- the content repository, site overlay conventions, and current brand voice guide are known
- the AI content governance policy (human review gate, YMYL rules) is available
- the publisher (user or pipeline) controls deployment — no publish without explicit approval

### Workflow Steps

#### 1. Frame The Audit Scope

Role: **Content Manager**

Use skill: `audit-content`

- define the audit scope: URLs / pillar / cluster under review and the audit cadence
- state the success criteria and the decision the audit supports (recover traffic, close information-gain gap, compliance refresh)
- confirm the AI content governance policy and YMYL rules that apply to any updated content
- do not begin editing any live content before the baseline audit is recorded

#### 2. Baseline Performance And Classify Action

Role: **Content Manager**, **Data Analyst**

Use skill: `analyze-data`

- pull the baseline for each URL: organic traffic trend, engagement, conversions, current rankings, and freshness (publish and last-reviewed dates) — request formal metrics from Data Analyst when raw exports need reproducible analysis (`data-analysis-report.json`)
- flag health issues: broken links, outdated statistics, dead references, and cannibalization with newer URLs
- classify each piece explicitly as one of: keep-as-is, refresh, expand, consolidate (merge), redirect, or retire — with data-backed rationale
- only **refresh** and **expand** continue in this workflow; consolidate, redirect, and retire are strategy decisions the Content Manager escalates or plans separately (technical redirects go to Frontend/DevOps)

#### 3. Read The Content And Inventory Assets

Role: **Content Manager**, **Content Writer**

- read each in-scope piece in full — map thesis, section structure, claims, data points, links, and CTA
- inventory existing E-E-A-T assets (author bio, firsthand accounts, original data, expert quotes) so the refresh preserves them
- list every factual claim with its current source; mark claims that are stale, unsourced, or unverifiable
- record the current pillar–cluster position and internal linking

#### 4. Research The Latest Standards

Role: **Researcher**, **SEO Analyst**

Use skill: `conduct-research`

- verify each stale or flagged claim against current, credible sources; record source and capture date
- research the latest standards for the topic: updated regulations, changed best practices or tooling, and current SERP and AI-answer patterns for the primary keyword
- run an information-gain check against the current top SERP results and AI answers (AI Overviews / AI Mode, Perplexity, ChatGPT) to identify what newer competitors now cover that the piece lacks
- SEO Analyst confirms whether the topical-authority position and target intent still hold; escalate deep or YMYL verification to full research rather than a lightweight pass

#### 5. Update The Content

Role: **Content Writer**

Use skill: `write-article`

- the Content Manager delegates the refresh to the Content Writer (`agent-delegation`) with the audit findings, claim list, and information-gain gaps as input
- correct outdated facts, refresh statistics, replace dead links, and add the missing information-gain sections
- apply current answer-first / GEO-AEO structure where the format now demands it, without gutting the existing narrative or changing the slug/publish date
- preserve and strengthen (never strip) E-E-A-T signals; keep to the brand voice guide
- record a change log: what was updated, corrected, added, and why — the refresh must be reconstructable

#### 6. SEO / GEO-AEO Re-Audit

Role: **SEO Analyst**

Use skill: `optimize-seo`

- re-audit the updated piece against current on-page + GEO/AEO standards; emit `seo-audit-report.json` with findings by severity (Blocking, Important, Follow-Up) and updated `seo-metadata.json`
- verify: title/meta within limits and aligned, clean heading hierarchy, answer-first blocks, fact density, valid schema, intact internal links, and no new cannibalization
- confirm AI bot crawlability and that the last-reviewed date is updated while slug/canonical/publish-date remain unchanged unless a change was explicitly approved
- Blocking findings must be resolved before publish

#### 7. Publish Decision And Record

Role: **Content Manager**

- apply the human editorial review gate; confirm the YMYL/SME and AI-assisted-edit review gates are satisfied before approving republish
- confirm a distribution plan exists for pillar content before shipping the refreshed piece
- the user or publisher controls the actual deployment — do not commit, push, or deploy without explicit user approval
- after publish, update the content inventory: new last-reviewed date, refresh change log reference, and post-refresh performance re-check date

### Checklist

- [ ] audit scope, success criteria, and governance rules framed before any edit
- [ ] baseline recorded per URL (traffic, engagement, rankings, freshness, health flags)
- [ ] action classified per piece (keep / refresh / expand / consolidate / redirect / retire) with data rationale
- [ ] non-refresh actions escalated; only refresh/expand continued
- [ ] full content read; E-E-A-T assets and all factual claims inventoried
- [ ] stale claims verified against current sources with capture dates
- [ ] latest standards researched and information-gain gaps identified
- [ ] content updated within scope; facts corrected, links fixed, gaps closed; E-E-A-T preserved
- [ ] change log recorded — refresh is reconstructable
- [ ] post-update SEO/GEO/AEO audit completed; seo-audit-report.json + seo-metadata.json emitted; Blocking findings resolved
- [ ] YMYL and AI-assisted-edit review gates satisfied; distribution plan confirmed
- [ ] republished with explicit user approval; content inventory and last-reviewed date updated

### Related Workflows

- [content-publishing](content-publishing.md)
- [seo-content-lifecycle](seo-content-lifecycle.md)
- [seo-keyword-brief](seo-keyword-brief.md)

### Related Skills

- **audit-content**: Run the refresh cycle — baseline audit, read, research latest standards, update, re-audit
- **analyze-data**: Provide reproducible performance baselines for the audit classification
- **conduct-research**: Verify claims and research the latest standards and competitor coverage
- **write-article**: Draft the content update and information-gain additions
- **optimize-seo**: Post-update SEO/GEO/AEO audit and metadata

### Failure Modes

- **Audit before baseline**: a content piece is updated before the baseline metrics are recorded. **Mitigation:** record rank, traffic, and conversion rate pre-update; the audit evidence decides the action, not assumption.
- **AI-assisted edit published unedited**: an AI-suggested edit ships without human review. **Mitigation:** enforce the human editorial sign-off before publish; track `reviewed_by` and `reviewed_at`.
- **YMYL refresh without SME**: a finance/health/legal update ships without expert review. **Mitigation:** require human SME sign-off for YMYL-adjacent pages; reject unverified claims.
- **Stale content kept alive**: a redundant or outdated page is refreshed instead of consolidated. **Mitigation:** classify the action explicitly; route redirect/retire to Content Manager.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/seo-audit-report.json`** — capture the four-axis scores (overall, SEO, AEO, readability), the prioritized findings (Blocking, Important, Follow-Up), and the projected post-fix score.
- **`contracts/schemas/seo-metadata.json`** — when the audit closes; capture the updated title, meta, canonical, and schema decisions.

### Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: an AI-suggested audit finding may reframe the page goal through off-target keyword recommendations. **Mitigation:** cross-check the audit against the original page objective; reject reframed goals.
- **ASI06 Memory & Context Poisoning**: retrieved research and prior audits are untrusted inputs; verify every cited claim against the live source before publishing the audit.
- **ASI09 Human-Agent Trust Exploitation**: do not present a refresh as "guaranteed to recover rankings" without evidence; surface the residual risk and the actual metrics honestly.

