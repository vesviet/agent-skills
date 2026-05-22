# Publish Log Conventions — plan/baiviet/publish-log.md

Append-only log for planned vs actual publishing. SEO Analyst or Task Planner updates after each publish or carry-over.

## Location

Default: `plan/baiviet/publish-log.md` (workspace root; set `PLAN_BAIVIET_ROOT` if different).

## Entry Format

Newest dates first. One section per calendar day:

```markdown
## YYYY-MM-DD
- Lease:
  - Topic:
  - Primary keyword:
  - Slug:
  - Internal links:
  - Status: Drafted | Draft Ready | Published | Carry-over
- May lanh:
  - Topic:
  - Primary keyword:
  - Slug:
  - Internal links:
  - Status: Drafted | Draft Ready | Published | Carry-over
```

## Field Rules

| Field | Rule |
| ----- | ---- |
| Topic | Working headline or plan topic line |
| Primary keyword | Exact phrase targeted in title/H1/meta |
| Slug | Repo-relative path under src/data (e.g. post/guides/slug.mdx) |
| Internal links | Comma-separated paths or slugs (minimum 3 when published) |
| Status | Use Carry-over when draft missed publish window |

## After Publish

- Set Status to **Published** only after live URL or repo merge confirmed by user
- Cross-check slug matches deployed route
- If audit changed metadata, note "meta updated per seo-audit-report" in Topic line or a Note bullet

## Weekly Rollup

Every 7 days, Task Planner adds a short summary block at top of publish-log or in plan file:

```markdown
## Week YYYY-MM-DD — YYYY-MM-DD rollup
- Lease published: N / planned: M
- May lanh published: N / planned: M
- Carry-overs:
- GSC notes (from SEO/Data Analyst):
- Next week focus clusters:
```

## Link To Contracts

When machine-readable tracking is required, mirror published rows into `seo-weekly-board.json` `entries[].status` = `published`.
