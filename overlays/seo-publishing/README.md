# SEO Publishing — Dual-Site Sprint Overlay

Publishing overlay for recurring SEO content on **Lease in Vietnam** and **May Lanh Treo Tuong**. Composes on top of:

- `core/roles/seo-analyst.md` (briefs, audits, keyword discipline)
- `core/roles/task-planner.md` (7-day board and cadence)
- `core/roles/content-writer.md` (drafting after brief)

Also pair with site overlays when editing content files:

- overlays/lease-content
- overlays/vesviet-content (not required for these two Astro sites; lease-content covers lease + maylanh skill)

## Scope

- Dual-site sprint: up to **2 posts/day** (1 Lease + 1 May lanh) when active
- Rolling **7-day topic board** and daily **publish log** under the workspace plan folder
- Per-post SEO baseline, content-mix guardrails, and cannibalization checks
- Handoff contracts: seo-content-brief.json, seo-audit-report.json, seo-metadata.json, seo-weekly-board.json

## Workspace Paths (default)

Set `PLAN_BAIVIET_ROOT` to the active plan folder (default in personalized workspace):

| Artifact | Default path |
| -------- | ------------ |
| 7-day board | `plan/baiviet/plan-YYYY-MM-DD.md` |
| Publish log | `plan/baiviet/publish-log.md` |
| Daily checklist | `plan/baiviet/publishing-cadence-defaults-checklist.md` |
| Lease content | `leaseinvietnam/src/data/` |
| May lanh content | `maylanhtreotuong/src/data/` |

## Included

- `rules/publishing-cadence.md` — Time windows, dual-site runbook, per-post baseline
- `rules/topic-board-template.md` — 7-day board and daily plan sections
- `rules/publish-log-conventions.md` — Post-publish tracking format
- `rules/site-mix-and-cannibalization.md` — Cluster mix and 7-day keyword guardrails

## Activation

```
Role: seo-analyst
Overlay: overlays/seo-publishing
```

For full publish pipeline on a sprint day:

```
Role: task-planner
Overlay: overlays/seo-publishing
```

Then hand off briefs to SEO Analyst and drafts to Content Writer with overlays/lease-content as needed.

## Role Responsibilities Under This Overlay

| Step | Owner | Output |
| ---- | ----- | ------ |
| Update 7-day board | Task Planner + SEO Analyst | plan-YYYY-MM-DD.md or seo-weekly-board.json |
| Keyword + links per post | SEO Analyst | seo-content-brief.json |
| Draft | Content Writer | MDX under src/data |
| Pre-publish audit | SEO Analyst | seo-audit-report.json, seo-metadata.json |
| Log | Content Writer (after publish) or SEO Analyst / Task Planner | publish-log.md entry |
