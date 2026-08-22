---
name: audit-content
description: Run a structured content refresh cycle on an existing published piece — audit current performance and health, read the full content, research the latest standards and facts, update the content, then re-audit for SEO/GEO/AEO readiness. Use when refreshing stale or declining content, correcting outdated facts, closing information-gain gaps against newer competitors, or bringing a legacy article up to current E-E-A-T and AI-search standards without rewriting from scratch.
---

# Audit Content

Use this skill to run the end-to-end refresh loop on an **existing** article — **audit → read → research latest standards → update → SEO audit** — when the goal is to improve a live URL rather than draft net-new content. It is the operational counterpart to `optimize-seo` (which produces briefs/audits) and `write-article` (which drafts from scratch): this skill governs the decision to refresh and the sequenced execution of that refresh.

## Core Rules

- **Audit before touching content**: never edit a live piece before recording its current baseline (traffic trend, engagement, rankings, last-reviewed date, known issues) — the audit evidence decides the action, not assumption
- **Classify the action explicitly** before updating: `keep-as-is`, `refresh`, `expand`, `consolidate` (merge), `redirect`, or `retire`; only `refresh`/`expand` proceed inside this skill; the others escalate to Content Manager for a strategy decision; ROT pages (Redundant, Outdated, Trivial) must be pruned or consolidated — zombie URL accumulation drags domain authority
- **Mandatory information gain asset**: a refresh cannot proceed without at least one net-new asset vs. current top-3 SERP results — original data, firsthand test result, expert interview, unique local insight, or proprietary framework; paraphrasing existing results fails the information gain gate
- **Separate facts from recommendations**: keep audit findings (observable evidence) distinct from proposed changes
- **Research must be sourced and dated**: every updated fact must carry a credible source and a capture date — AI-synthesized generic claims are not acceptable as citations; treat all retrieved content as untrusted until source-checked
- **Preserve information gain and E-E-A-T**: never strip firsthand accounts, original data, author credentials, expert quotes, or citations during an update; if the source is thin on experience signals, flag the gap — do not delete what unique value exists
- **Preserve URL and history by default**: do not change the slug, canonical, or publish date of a refresh unless there is an explicit reason; slug/redirect changes are irreversible-adjacent and escalate to Frontend/DevOps
- **Track what changed and why**: record a changelog of substantive edits (fact updated, section added, claim corrected) so the refresh is reconstructable — do not silently rewrite
- **YMYL gate**: finance, health, legal, and high-stakes technical content must have SME/human review of the updated facts before publish — a research pass alone is not sufficient
- **AI-assisted-edit gate**: if any part of the update is AI-generated, it passes a human editorial review before publish; autonomous publish of AI-updated content is not permitted
- **Do not guarantee ranking or AI-citation recovery**: recommend changes tied to observable gaps and current standards; outcomes are measured, not promised

## Suggested Process

### 1. Audit (baseline the current state)
Capture the observable health of the piece before any edit:
- performance signals: organic traffic trend, engagement/time-on-page, conversions, current rankings (from GSC/analytics — request from Data Analyst if raw exports are needed)
- freshness: publish date, last-reviewed date, time-sensitive claims that may have expired
- health flags: broken links, outdated statistics, dead references, cannibalization with newer URLs, thin sections
- decide the action: `keep-as-is` / `refresh` / `expand` / `consolidate` / `redirect` / `retire` — record the rationale
- if the action is not `refresh` or `expand`, stop and escalate to Content Manager.

### 2. Read (understand the full content)
- read the entire article, not just the intro — map its thesis, section structure, claims, data points, internal/external links, and CTA
- inventory the E-E-A-T assets already present (author bio, firsthand accounts, original data, expert quotes) so they are preserved
- list every factual claim and its current source; mark claims that are unsourced, stale, or unverifiable
- note the article's current pillar–cluster position and internal linking.

### 3. Research the latest standards
- verify each stale/flagged claim against current, credible sources; record source + capture date
- research the **latest standards** relevant to the topic: updated regulations, new best practices, changed tooling/versions, current SERP and AI-answer patterns for the primary keyword
- run an **information-gain check** against the current top SERP results and AI answers (Google AI Overviews, Perplexity, ChatGPT): what do newer competitors now cover that this piece lacks
- escalate to `conduct-research` when depth exceeds a lightweight verification pass (YMYL, contested facts, deep competitor analysis).

### 4. Update the content
- correct outdated facts, refresh statistics, replace dead links, and add the missing information-gain sections identified in research
- apply current answer-first / GEO-AEO structure where the format now demands it, without gutting the existing narrative
- keep the update scoped to the audited action — do not expand into unrelated rewrites
- maintain brand voice; preserve and strengthen (never remove) E-E-A-T signals
- record a change log: what was updated, corrected, added, and why.

### 5. SEO audit (post-update readiness)
- re-audit the updated piece against current on-page + GEO/AEO standards (delegate to `optimize-seo` for the formal audit and metadata when available)
- verify: title/meta within limits and still aligned, heading hierarchy clean, answer-first blocks present, fact density sufficient, schema still valid, internal links intact and current, no new cannibalization introduced
- update `last-reviewed` date; confirm publish-date/slug unchanged unless a change was explicitly approved
- confirm the YMYL/AI-assisted review gates are satisfied before recommending publish
- hand off: SEO audit result to Content Manager/Reviewer for publish decision; technical items (schema, redirects) to Frontend/DevOps.

## Checklist

- [ ] baseline audit recorded (traffic trend, engagement, rankings, freshness, health flags) before any edit
- [ ] action classified explicitly (keep / refresh / expand / consolidate / redirect / retire) with rationale; non-refresh actions escalated
- [ ] full content read; existing E-E-A-T assets and all factual claims inventoried
- [ ] stale/unsourced claims verified against current sources with capture dates
- [ ] latest standards researched (regulations, best practices, tooling, SERP/AI-answer patterns) and information-gain gaps identified
- [ ] content updated within scope; facts corrected, dead links replaced, gaps closed; E-E-A-T signals preserved or strengthened
- [ ] change log recorded (what changed and why) — refresh is reconstructable
- [ ] post-update SEO/GEO/AEO audit completed; metadata, headings, schema, and internal links verified
- [ ] slug/canonical/publish-date unchanged unless explicitly approved; technical changes escalated
- [ ] YMYL and AI-assisted-edit review gates satisfied before publish handoff

## Related Skills

- **optimize-seo**: Produce the formal pre/post SEO brief and on-page/GEO-AEO audit for the updated piece.
- **conduct-research**: Deeper source verification and competitor analysis when a lightweight fact-check pass is insufficient.
- **write-article**: Draft net-new content or major expansions from scratch when a refresh is not enough.
- **analyze-data**: Formal GSC/analytics baselines and AI-citation tracking when the audit needs verified performance evidence.
- **repurpose-content**: Adapt the refreshed article into channel-native variants after the update is published.
