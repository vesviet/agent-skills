---
name: publish-lease-content
description: End-to-end 6-step content production workflow enforcing the 5-Pillar strategy and 7-day mix guardrails for leaseinvietnam.
version: 1.1.0
roles:
  - content-writer
  - seo-analyst
  - content-manager
---

# Publish Lease Content Workflow

This workflow standardizes the weekly sprint cadence for `leaseinvietnam`.

## 7-Day Content Mix Guardrails
Before beginning a sprint, the `Task Planner` or `Content Manager` must ensure:
- **Balance**: Mix of guides, neighborhood comparisons, trust-safety, and market data.
- **Cannibalization**: No repeated primary keyword intent within 7 days.
- **Link Equity**: At least 1 post/week strengthens links to high-value property listing pages.
- **Trust Maintenance**: At least 1 post/week in scam/trust category.

## 6-Step Production Workflow

### Step 1: SEO Briefing (`seo-analyst`)
- Consume target keywords and generate `seo-content-brief.json`.
- Specify Answer-First requirements, Fact Density, and E-E-A-T proof type.

### Step 2: Research & Outline (`content-writer` / `researcher`)
- Consult minimum 2-3 verifiable sources (official government sites, batdongsan, GSO).
- Produce outline matching the selected core template (Radar, Guide, Scam, Neighborhood).

### Step 3: Drafting (`content-writer`)
- Author in `.mdx` using the `<AnswerFirst>` component.
- Maintain minimum length of 1,400+ words.
- Execute anti-slop self-scan (remove fluff and hedge words).

### Step 4: Internal Link Insertion (`content-writer`)
- Insert minimum 3 contextual internal links to existing cluster pages.
- Insert 1+ link to a relevant property listing page.
- (Optional) Insert up to 2 cloaked affiliate links (`/go/partner`) if contextually relevant and NOT a trust-safety article.

### Step 5: Schema & Metadata Verification (`seo-analyst`)
- Verify frontmatter: `title` (≤60 chars), `description` (120-155 chars), `unique_angle`, `anti_slop_gate`.
- Verify JSON-LD Schema (e.g., FAQPage if applicable).
- Emit `seo-audit-report.json`.

### Step 6: Publish & Record (`content-manager`)
- Verify `anti_slop_gate.gate_passed: true`.
- Execute local build (`npm run build`). If exit 0, commit and push to Cloudflare.
- Log entry into weekly publish tracker.

### Failure Modes

- **Cannibalization in the 7-day mix**: two posts in the same week target the same primary keyword intent. **Mitigation:** the 7-Day Content Mix Guardrails section requires a non-repeated intent; reject the plan that violates the guardrail.
- **Brief published without anti-slop gate**: a brief ships without `anti_slop_gate: { gate_passed: true }`. **Mitigation:** Step 5 enforces the gate; reject the brief when the gate flag is missing.
- **Answer-first blockquote used instead of `<AnswerFirst>`**: a draft uses `> **Quick Answer:**` instead of the component. **Mitigation:** the GEO/AEO 2026 standards forbid the blockquote pattern; reject the draft and refactor.
- **Word count below 1,400**: a long-form article ships too short. **Mitigation:** Step 3 requires the 1,400-word minimum; reject the draft when the count is below the threshold.
- **Internal links below 4**: a post ships with fewer than 3 contextual links plus 1 commercial link. **Mitigation:** Step 4 enforces the link count; reject the draft when the count is below.
- **Affiliate link on a trust-safety article**: a cloaked `/go/partner` link lands in a scam/trust post. **Mitigation:** Step 4 forbids cloaked links in trust-safety articles; reject the link.
- **Build failure on publish**: `npm run build` exits non-zero. **Mitigation:** Step 6 requires exit 0; do not commit when the build fails.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/seo-content-brief.json`** from Step 1, capturing the H2 outline, the answer-first guidance, the FAQ, the internal-link targets, the word-count band, the GEO/AEO fields, the schema requirements, and the E-E-A-T gates.
- **`contracts/schemas/seo-audit-report.json`** from Step 5, capturing the four-axis scores (overall, SEO, AEO, readability) and the projected post-fix score.
- **`contracts/schemas/content-handoff.json`** (or markdown frontmatter block) from Step 6, capturing the publish event, the human review status, and the week log entry.