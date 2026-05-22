# Topic Board Template — plan/baiviet

Use for rolling 7-day planning and daily execution. Task Planner owns structure; SEO Analyst owns keywords and link targets.

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

- **Topic:**
- **Working title:**
- **Primary keyword:**
- **Secondary keywords:**
- **Search intent:**
- **Content cluster:**
- **Target path:**
- **Meta description (≤160):**
- **Target length:**
- **H2 outline:** (numbered)
- **Internal links (≥3):** path + anchor
- **High-value link:** property/* or product/* (required ≥1/week per site)
- **SEO brief:** path to seo-content-brief.json or inline
- **Status:** Planned / Briefed / Drafted / Audited / Published
```

## 7-Day Board Table (rolling)

```markdown
| Date | Site | Topic | Primary keyword | Cluster | Brief | Draft | Audit | Status |
|------|------|-------|-----------------|---------|-------|-------|-------|--------|
```

SEO Analyst MUST verify no duplicate primary intent per site within the visible 7-day window.

## Handoff To Content Writer

Each row marked **Briefed** MUST have:

- Approved primary keyword and slug direction
- H2 outline and internal link list
- seo-content-brief.json attached or inlined in plan file

## Machine Handoff

When Agent Coordinator or automation needs JSON, emit `contracts/schemas/seo-weekly-board.json` with `week_start`, `timezone: Asia/Ho_Chi_Minh`, and `entries[]` for each planned post.
