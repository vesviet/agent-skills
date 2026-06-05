# Topic Board Template — plan/baiviet

Use for rolling 7-day planning and daily execution. Task Planner owns structure; SEO Analyst owns keywords, link targets, GEO/AEO optimization, and topical authority mapping. Updated for 2025–2026 SEO standards.

## File Naming

| File | Purpose |
| ---- | ------- |
| `plan/baiviet/plan-YYYY-MM-DD.md` | Daily plan + 7-day context |
| `plan/baiviet/publish-log.md` | Cumulative publish history |
| `plan/baiviet/seo-weekly-board-YYYY-MM-DD.json` | Optional machine handoff (seo-weekly-board.json schema) |

## Daily Plan Header

```markdown
# Publishing Plan — YYYY-MM-DD

> **Roles:** Task Planner, SEO Analyst, Content Writer
> **Draft window:** 08:00–11:00 (UTC+7) | **Publish:** 11:30–14:00 (UTC+7)
```

## Section 1 — Last 7 Days Inventory

Per site, list recent posts with:

- Path or slug
- Status: Published / Draft Ready / Carry-over
- Primary keyword
- Content cluster (see site-mix-and-cannibalization.md)

State **keyword guardrail**: intents to avoid duplicating in the next 7 days.

## Section 2 — Today's Posts (dual-site)

Repeat for each site:

```markdown
### Site: leaseinvietnam | maylanhtreotuong

#### Traditional SEO
- **Topic:**
- **Working title:**
- **Primary keyword:**
- **Secondary keywords:**
- **Search intent:** [informational | commercial | navigational | transactional]
- **Content cluster:**
- **Target path:**
- **Meta description (≤160):**
- **Target length:**
- **H2 outline:** (numbered)
- **Internal links (≥3):** path + anchor
- **High-value link:** property/* or product/* (required ≥1/week per site)

#### GEO / AEO
- **Answer-first block:** [≤60 words opening for main H2]
- **Query fan-out:** [3–5 sub-questions from PAA + LLM]
- **Answer format per section:** [definition | comparison table | numbered steps | bullet list]
- **Fact density target:** [minimum verifiable data points]

#### Topical Authority
- **Pillar page URL:**
- **Cluster position:** [pillar | supporting | supplementary]
- **Information gain:** [what makes this unique vs top SERP results]
- **Content freshness type:** [new_topic | evergreen_refresh | data_update | experience_addition]

#### E-E-A-T
- **Experience proof:** [original_photo | firsthand_account | documented_test | expert_interview]
- **Author entity:** [author name + profile URL]
- **YMYL-adjacent:** [yes/no]

#### Schema
- **Required schema types:** [Article | FAQPage | HowTo | Product]

#### Status
- **SEO brief:** path to seo-content-brief.json or inline
- **Status:** Planned | Briefed | Drafted | Audited | Published
```

## 7-Day Board Table (rolling)

```markdown
| Date | Site | Topic | Primary keyword | Cluster | Pillar page | GEO ready | Brief | Draft | Audit | Status |
|------|------|-------|-----------------|---------|-------------|-----------|-------|-------|-------|--------|
```

- **Pillar page**: URL of the pillar page this article supports
- **GEO ready**: ✅ when answer-first + query fan-out + schema specified in brief; ❌ otherwise

SEO Analyst MUST verify:
- no duplicate primary intent per site within the visible 7-day window
- pillar–cluster balance: each pillar has ≥3 supporting articles
- GEO/AEO fields complete before marking Briefed

## Handoff To Content Writer

Each row marked **Briefed** MUST have:

- Approved primary keyword and slug direction
- H2 outline and internal link list
- seo-content-brief.json attached or inlined in plan file
- Answer-first guidance for each H2 section
- Query fan-out list (3–5 sub-questions)
- Experience proof type specified
- Schema types recommended

## Machine Handoff

When Agent Coordinator or automation needs JSON, emit `contracts/schemas/seo-weekly-board.json` with `week_start`, `timezone: Asia/Ho_Chi_Minh`, and `entries[]` for each planned post.
