---
name: repurpose-content
description: Extract and format micro-content variants (social threads, newsletters, short video scripts) from a core long-form article or asset. Use when creating derivative content for omnichannel distribution.
---

# Repurpose Content

Modern content distribution requires a single narrative to be adapted into multiple native formats. Use this skill when a core piece of content (blog post, whitepaper, case study) needs to be extracted into high-value micro-content variants for omnichannel distribution without losing core message, tone, or E-E-A-T signals.

## When to Use

- a published long-form article needs social/newsletter/video variants
- distributing one narrative across LinkedIn, X, newsletter, and short video
- the source already exists and you only need derivative formats
- you must preserve E-E-A-T and fact density for GEO/AEO citability
- AI-generated variants need a human editorial gate before publish

## Core Rules

- **Native Format Alignment:** adapt to channel conventions — LinkedIn posts need a hook and spaced lines; Twitter/X threads need numbered segments and tight word counts; video scripts need `[Visual/Hook]` markers and ≤150 words for 60-second formats.
- **No Fact Invention:** do not introduce claims, statistics, or examples not present in the source article; flag gaps and note they need original sourcing.
- **Preserve E-E-A-T / Information Gain:** the unique insight, firsthand evidence, and source attribution from the main article must survive in the short-form variant — do not strip credentials, citations, or expert quotes when adapting.
- **Channel Ownership:** handoff labeled variants clearly; do not choose distribution channels unless explicitly requested.
- **Source Must Exist:** do not generate repurposed content from a non-existent source — request or write the primary article first using `write-article`.

### 2025-2026: AI-Assisted Repurposing Governance

- **Human editorial gate is mandatory** when AI generates channel variants: treat AI output as a first draft requiring human review before publish — do not ship AI-repurposed content directly.
- **AI content labeling:** follow the platform's native AI content disclosure requirements (Meta, LinkedIn, and TikTok each have their own mandatory AI label policies as of 2025) — apply the appropriate label or flag for manual application.
- **GEO/AEO-safe adaptation:** when the source article is indexed for Google AI Overviews or Perplexity citation, preserve fact density and structured statements in newsletter and social variants — stripping factual depth reduces AI citability of the core article.
- **Do not repurpose AI-generated source material without verifying its accuracy first** — repurposing amplifies errors; validate the source article's claims before distributing variants.

## Suggested Process

### 1. Analyze Source
Read the primary article. Identify: core thesis, top 3 most impactful statistics or facts, E-E-A-T proof elements (author credentials, firsthand account, citations), and the primary CTA.

### 2. Select Channels and Variants
Based on the requested distribution channels:
- **Twitter/X Thread:** 5-7 tweets — Hook → Problem → Insight 1 → Insight 2 → Conclusion/CTA
- **LinkedIn Post:** 150-300 words — question hook, bulleted insights, community question closing; text-only or carousel script
- **Newsletter Snippet:** 80-120 words — answer-first summary + link back to full article
- **Short Video Script (TikTok/Reels/Shorts):** 30-60 second read (~75-150 words) — `[Visual/Hook]`, `[Body]`, `[Outro/CTA]`
- **Email Subject + Preview:** ≤60 chars subject, ≤90 chars preview text

### 3. Draft Each Variant
- preserve the source's unique insight in each variant
- use native channel vocabulary and formatting
- do not shorten by removing factual claims — shorten by removing context the channel audience already has

### 4. Review Against Constraints
- are variants within channel length limits?
- do they preserve the core E-E-A-T signal?
- do they pass a "would a human write this?" check — not formulaic AI fill?
- is every statistic present in the source?

### 5. Handoff
Output variants clearly labeled by channel. Flag any fact or credential that was omitted for length and needs reinstatement if the audience is more expert.

## Output Format

```
## Repurposed Variants — <Article Title>

Source: <URL or file path>
Channels requested: <list>

---

### Twitter/X Thread
Tweet 1: <hook>
Tweet 2: <insight>
...

### LinkedIn Post
<post body>

### Newsletter Snippet
Subject: <subject line>
Preview: <preview text>
Body: <80-120 word snippet>

### Short Video Script
[Visual/Hook]: ...
[Body]: ...
[Outro/CTA]: ...

---
AI governance: [ ] human editorial review completed before publish
AI label applied: [ ] yes / [ ] not required for this channel
```

## Anti-Patterns To Reject

- repurposing before verifying the source article's factual accuracy
- stripping firsthand proof (photos, credentials, case study data) to hit word count
- generating variants with invented examples or statistics not in the source
- publishing AI-generated social variants without human editorial review
- applying the same word count and tone across all channels — each must be native

## Checklist

- [ ] source article's core thesis and key facts identified
- [ ] E-E-A-T signals (credentials, citations, firsthand proof) mapped from source
- [ ] variants drafted using channel-native formatting (spacing, hooks, threads)
- [ ] no facts invented or imported from outside the source
- [ ] CTA is present and context-appropriate in each variant
- [ ] visual cues or multimedia prompts formatted for video scripts
- [ ] AI content label policy checked for each target platform (2025 requirements)
- [ ] human editorial review gate confirmed before publish

## Related Skills

- **write-article**: Use when drafting the core content from scratch before repurposing.
- **optimize-seo**: Use when ensuring the core content is GEO/AEO-optimized before repurposing for AI-cited surfaces.
- **conduct-research**: Use when source material lacks sufficient factual depth to repurpose credibly.
