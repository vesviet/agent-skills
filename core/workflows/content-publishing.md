---
description: Workflow for producing a publish-ready article from an SEO brief — covering Content Writer drafting, SEO Analyst audit, and post-publish logging
---

## Content Publishing Workflow

Use this workflow when an `seo-content-brief.json` is ready and the article must move from brief to published URL. Covers Content Writer drafting, SEO Analyst draft audit, user-controlled deployment, and publish-log recording. Also known as: publish-content workflow.

If the brief doesn't exist yet and the work starts from a bare topic, start at [seo-content-lifecycle](seo-content-lifecycle.md) instead — it prepends the planning and research steps, then hands off to this workflow's step 3.

### When To Use

- an SEO content brief exists and drafting can begin
- a previously drafted article needs an SEO audit before publishing
- a published article needs its record updated in the publish log

### Prerequisites

- `seo-content-brief.json` is available from SEO Analyst (or briefing is inline)
- the target site's content root path and frontmatter schema are known
- the site repo's local overlay is identified (for example: `overlays/lease-content`, `overlays/vesviet-content`)
- the publisher (user or pipeline) has deploy access to the site

### Workflow Steps

#### 1. Confirm The Brief

Role: **Content Writer**, **SEO Analyst**

Before drafting:

- load and review `seo-content-brief.json` — confirm all required fields are present
- verify that the primary keyword, H2 structure, word count target, and internal link targets are populated
- confirm the content freshness type and topical cluster position
- confirm E-E-A-T requirements (experience proof type, author entity, YMYL flag)
- if any required field is missing or ambiguous, request clarification from SEO Analyst before drafting

#### 2. Research And Gather Evidence

Role: **Content Writer**

Use skill: `write-article`

Run the required research passes before drafting:

- if research-report.json was provided by Researcher, synthesize only from that material
- otherwise run **at least 3–4 distinct research passes** (different queries, sources, or angles)
- gather the evidence required for the E-E-A-T experience proof type specified in the brief
- collect at minimum 3 verifiable data points (statistics, expert quotes, specific numbers) per 500 words of planned content
- do not fabricate evidence — if required proof type (original photo, firsthand account) cannot be produced, flag the gap before drafting

#### 3. Draft The Article

Role: **Content Writer**

Use skill: `write-article`

Follow the brief exactly:

- implement answer-first structure: open each H2 section with a direct answer ≤60 words before elaboration
- match H2 headings to natural language queries from the brief ("How to...", "What is...", "Why does...")
- embed all internal links with the anchor text specified in the brief
- include the FAQ block when brief requires it (format as `## FAQ` with `### Question?` subheadings for schema compatibility)
- match the on-page spec: title tag, meta description, slug, word count target
- add the experience proof signal specified in the brief (do not fabricate if unavailable — escalate)
- follow site overlay frontmatter rules (for example: `overlays/lease-content` for leaseinvietnam/maylanhtreotuong)

Do not invent keyword or link strategy that differs from the brief.

#### 4. Self-Check Before Handoff To SEO Analyst

Role: **Content Writer**

Before sending draft to SEO Audit:

- word count meets or exceeds the brief target (default: 1,400+)
- all required internal links are present and resolve to real URLs
- title tag ≤60 chars and meta description ≤160 chars
- FAQ block present if required
- answer-first opening present in each H2 section (≤60 words direct answer before elaboration)
- execute Anti-AI Semantic Audit self-check: run blacklisted clichés scan ("delve", "tapestry", "testament", "unlock", "game-changer", "pinnacle", "foster", "realm", "crucial", "harness", "navigating", "intertwined", "multifaceted", "underpin", "cornerstone", "elevate", "shed light", "ever-evolving" — zero tolerated), verify burstiness variance (sentence length std dev ≥ 6.0 words), and verify active voice percentage (≥85%)
- document Information Gain: verify empirical proof (benchmarks, logs, firsthand case studies) and record net-new value that surpasses the current Top 10 SERP results
- experience proof signal is included or gap is explicitly flagged

#### 5. SEO Audit The Draft

Role: **SEO Analyst**

Use skill: `optimize-seo`

Audit the draft against the brief:

- verify on-page spec compliance: title, meta, slug, H2 structure, word count
- verify keyword density — primary keyword appears naturally in title, first paragraph, and 2–3 H2s
- verify all 3+ internal links are present with correct anchor text
- execute GEO (Generative Engine Optimization) & AEO extractability audit: verify answer-first BLUF structure (≤60 words per H2), target entity salience in lead paragraphs, markdown comparison tables / quantitative lists, quotable fact density (≥3 verifiable data points per 500 words), Schema.org @graph (TechArticle, Person E-E-A-T, FAQPage), and llms.txt compatibility
- execute competitive Information Gain audit against live Top 10 SERP competitors: rate differentiation ("exceptional", "strong", "moderate", "low", "zero"); require "exceptional" or "strong" to clear the gate
- verify E-E-A-T signals: experience proof, author reference, trust signals
- check robots.txt allows AI bots if GEO/AEO is a brief requirement
- flag any Blocking issues (must fix before publish), Important issues (should fix), and Follow-Up items

Emit `seo-audit-report.json` containing `anti_ai_semantic_audit`, `information_gain_audit`, and `geo_readiness_checklist` categorized by severity.

Emit `seo-metadata.json` with final title tag, meta description, slug, schema type recommendations.

#### 6. Revise If Needed

Role: **Content Writer**, **Content Manager**

Content Manager executes the mandatory **Anti-AI Semantic Audit & Information Gain Approval Gate**:

- `ai_semantic_flaw_score <= 15` (composite penalty score), 0 blacklisted clichés, and active voice ≥ 85% required to pass
- `information_gain_rating` must be "exceptional" or "strong" (evaluated against Top 10 SERP competitors); paraphrased rewrites fail the gate
- Content Manager dual quality gate sign-off is a hard blocker: if `ai_semantic_flaw_score > 15` or `information_gain_rating` < "strong", publication is strictly blocked per the AI SLOP APPROVE LOCK and revisions are mandatory

If the audit returned Blocking findings:

- address all Blocking findings before proceeding to publish
- do not publish with open Blocking issues
- Important findings may be published with explicit stakeholder acknowledgment

If all quality gates and Blocking findings are cleared, proceed to step 7.

#### 7. Prepare For Publish

Role: **Content Writer**, **SEO Analyst**

Emit `content-handoff.json` confirming:

- all required frontmatter fields populated (per site overlay schema)
- `seo_brief_followed: true`
- `seo_audit_passed: true` (or `seo_audit_findings` listing acknowledged Important items)
- `ai_semantic_flaw_score` fully evaluated and passing (`gate_passed: true`, `flaw_score <= 15`, `cliche_count: 0`, `active_voice_percentage >= 85%`)
- `information_gain_rating` set to "exceptional" or "strong"
- `geo_readiness_checklist` verified (`all_gates_cleared: true`)
- `publish_log_updated: false` (set to `true` after step 8)

The user or publisher controls the actual deployment — do not commit, push, or deploy without explicit user approval.

#### 8. Publish And Record

Role: **Technical Lead**, **Content Writer**

The user or publisher controls the actual deployment and must explicitly approve the publish action.

After confirmation of publish:

- append `publish-log.md` with:
  - publish date and time
  - article title and target URL slug
  - primary keyword
  - 3+ internal links used (anchor text + destination)
  - publish status: published / scheduled / carry-over
- update `content-handoff.json`: set `publish_log_updated: true`

If the article is delayed, mark it as `carry-over` in the log and carry the topic to the next sprint day.

### Checklist

- [ ] seo-content-brief.json confirmed — all required fields present
- [ ] research evidence gathered (3–4 passes or from research-report.json)
- [ ] E-E-A-T experience proof available or gap flagged
- [ ] draft written following brief — answer-first, internal links, FAQ, spec
- [ ] self-check passed: word count, links, title, meta, answer-first format
- [ ] Anti-AI Semantic Audit self-check cleared (zero banned clichés, burstiness std dev ≥ 6.0, active voice ≥ 85%)
- [ ] SEO & GEO/AEO audit completed — seo-audit-report.json emitted with Anti-AI, Info Gain, and GEO checklists
- [ ] seo-metadata.json emitted with final title, meta, slug, schema types
- [ ] Content Manager Quality Gate cleared (ai_semantic_flaw_score ≤ 15, information_gain_rating ≥ strong)
- [ ] Blocking findings resolved before publish
- [ ] content-handoff.json emitted with new quality metrics
- [ ] article deployed by user with explicit approval
- [ ] publish-log.md appended — keyword, URL, internal links, status recorded
- [ ] content-handoff.json `publish_log_updated` set to true

### Related Workflows

- [seo-keyword-brief](seo-keyword-brief.md)
- [seo-content-lifecycle](seo-content-lifecycle.md)
- [content-audit](content-audit.md)
- [add-new-feature](add-new-feature.md)
- [troubleshooting](troubleshooting.md)

### Related Skills

- **write-article**: Plan, research, and draft long-form content from the SEO brief
- **optimize-seo**: Audit draft against SEO brief and produce audit report and metadata
- **conduct-research**: Gather evidence when research is insufficient for E-E-A-T requirements

### Failure Modes

- **Draft published without anti-slop gate**: a draft ships without the editorial gate passing. **Mitigation:** enforce the gate at the publish step; block releases where `anti_slop_gate.gate_passed` is `no` or undocumented.
- **Hallucinated fact published**: a statistic or quote appears in the article that is not in the source. **Mitigation:** every claim traces to a primary source; flag unsourced claims as drafts; require Chain-of-Verification for YMYL.
- **E-E-A-T proof absent on YMYL**: a YMYL-adjacent article ships without experience proof, author entity, or trust signals. **Mitigation:** require the E-E-A-T gate for YMYL; require human expert review.
- **Cross-channel format ignored**: identical copy is posted across channels without native reformatting. **Mitigation:** enforce channel-native format alignment (LinkedIn 150-300 words, X 5-7 posts, etc.).

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/content-handoff.json`** (or markdown frontmatter) — capture `source_url`, `channels[]`, `ai_label_required[]`, `human_review_status`, and `fact_density_check`.
- **`contracts/schemas/seo-metadata.json`** — when the published piece has updated SEO metadata; capture the title, meta, canonical, and schema decisions.

### Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: an AI-drafted article may reframe the user goal through off-brand copy. **Mitigation:** cross-check the article's core claim against the source brief; reject reframed goals.
- **ASI03 Identity & Privilege Abuse**: editorial roles must own the publish gate; never let a non-editorial role auto-publish without the human editorial sign-off.
- **ASI09 Human-Agent Trust Exploitation**: do not present AI-generated content as fully verified without the human editorial sign-off; surface the AI provenance and the reviewer honestly.

