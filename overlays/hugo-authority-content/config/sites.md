# Authority Blog Content Sites

Site roots, corpus inventory, and cross-site authority rules for the two Hugo twins.
Snapshot: 2026-09-13. Canonical indexes: `learn/plan/CONTENT_INDEX.md` and
`authority-blog/reports/CONTENT_INDEX.md` — regenerate those before updating this file.

## Site Roots

| Site | Repo path (workspace-relative) | Public host | Language | Role |
|---|---|---|---|---|
| Authority Blog (portfolio flagship) | `authority-blog/` | `https://authority-blog.example.com/` | `en` | Authority site: expanded English masterclasses, tech radar, consulting conversion (`hire.md`) |
| Learn (notes / research) | `learn/` | `https://learn.authority-blog.example.com/` | `vi` | Vietnamese twin: research notes, series library, deep-research batch reports |

Both sites use Hugo + PaperMod. `learn` additionally runs a Hugo Book layout under `content/docs/`.

## Corpus Inventory (2026-09-13)

| Corpus | Authority Blog | Learn |
|---|---|---|
| Posts | 66 | 86 (7 internal reports `draft: true`) |
| Series dirs | 25 | 25 |
| Series files | 251 (225 chapters) | 251 (225 chapters) |
| Radar editions | 27 (2026-04 → 2026-09) | 63 (2026-04 → 2026-09) |
| Docs | — | 3 (Hugo Book) |
| Categories | 16 | 15 |
| Root pages | 7 | 8 |
| Total content files | 374 | 433 |

## Masterclass Twin Model

- Each flagship topic ships as a Vietnamese twin on `learn` (canonical notes) and an
  expanded English masterclass on `authority-blog` (authority).
- Batch 1–5 deep research (5 × 100 rounds) has upgraded 70 posts on `learn` and the
  mirrored flagships on `authority-blog` to masterclass standard: >20 KB, >2,500 words,
  production-grade code, standardized Mermaid, quantitative tables.
- Deep-research reports live only on `learn` as `draft: true` posts
  (`deep-research-100-rounds-report.md`, batches 3/4/5) — never publish on `authority-blog`.

## Cross-Site Authority Flow (one-way)

- `learn` → `authority-blog` only. 90 learn files link up to the English flagship via the
  `> 🇬🇧 Read the English version...` callout.
- `authority-blog` → `learn` links are FORBIDDEN (0 occurrences as of snapshot; keep it that way).
- `canonicalURL` frontmatter always points at the file's own host — learn posts
  canonicalize to `learn.authority-blog.example.com`, authority-blog posts to `authority-blog.example.com`.

## Publishing Notes

- Keep site roots and publishing notes here instead of in the global core.
- Answer-first coverage targets: authority-blog 61/66 posts, learn 69/86 posts (drafts exempt).
- Radar is authority-blog-only (`content/radar/YYYY-MM/`), monthly editions.
