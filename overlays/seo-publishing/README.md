# SEO Publishing — Dual-Site Sprint Overlay (2025–2026)

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
- **GEO/AEO optimization**: answer-first structure, query fan-out, fact density, AI extractability
- **Topical authority mapping**: pillar–cluster assignment, information gain analysis
- **E-E-A-T quality gates**: experience proof, author entity, trust signals, claim policy
- **Schema/structured data**: type recommendations per article for Frontend implementation
- **AI visibility tracking**: weekly citation checks in Google AI Overviews, Perplexity, ChatGPT
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

- `rules/publishing-cadence.md` — Time windows, dual-site runbook, per-post baseline (traditional SEO + GEO/AEO + E-E-A-T + schema)
- `rules/topic-board-template.md` — 7-day board and daily plan sections with GEO/AEO and topical authority fields
- `rules/publish-log-conventions.md` — Post-publish tracking format with AI visibility tracking and pillar–cluster monitoring
- `rules/site-mix-and-cannibalization.md` — Cluster mix, 7-day keyword guardrails, pillar–cluster maps, entity SEO, and AI visibility rules

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
| Keyword + links + GEO/AEO + pillar–cluster per post | SEO Analyst | seo-content-brief.json (with GEO/AEO fields, schema spec, E-E-A-T gates) |
| Draft | Content Writer | MDX under src/data (with answer-first structure, experience proof) |
| Pre-publish audit | SEO Analyst | seo-audit-report.json (with AI extractability check), seo-metadata.json |
| Log | Content Writer (after publish) or SEO Analyst / Task Planner | publish-log.md entry (with GEO ready, pillar, schema, experience proof) |
| Weekly AI visibility check | SEO Analyst | AI citation report in weekly rollup (Google AI Overview, Perplexity, ChatGPT) |
| Schema implementation | Frontend Developer | JSON-LD per SEO Analyst specification |

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-09-01
