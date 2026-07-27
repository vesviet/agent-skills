---
name: write-vesviet-learn-content
description: Draft or update Hugo Markdown for the Vesviet portfolio site or the Learn notes site. Use when creating or editing content under `/home/user/personalized/vesviet/content` or `/home/user/personalized/learn/content`, including posts, series, radar entries, or learn docs.
---

# Write Vesviet Learn Content

Use this skill when new or updated articles must land in one of the two Hugo sites whose content roots are fixed below.

## Content Roots

| Site | Absolute content path | Public site (from `hugo.toml`) |
|------|------------------------|----------------------------------|
| Vesviet (portfolio / blog) | `/home/user/personalized/vesviet/content` | `https://tanhdev.com/` |
| Learn (notes / research) | `/home/user/personalized/learn/content` | `https://learn.tanhdev.com/` |

Both sites use the **PaperMod** theme, Vietnamese or English copy is acceptable when it matches sibling pages in the same folder.

## Core Rules

- **never guess frontmatter**: open two or three recent files in the **same subtree** (`posts/`, `series/<name>/`, `radar/`, `docs/`) and copy delimiter style, keys, and ordering
- **YAML Safety Enforcement**: Both `vesviet` and `learn` require strict inline array syntax for arrays in YAML to prevent parser crash errors:
  - ✅ **CORRECT**: `categories: ["Backend", "Golang"]`
  - ❌ **INCORRECT**: 
    ```yaml
    categories:
      - Backend
      - Golang
    ```
- **Vesviet** content most often uses YAML frontmatter (`---` … `---`) with fields such as `title`, `date`, `draft`, `description`, `tags`, `categories`, and for long pieces `ShowToc` / `TocOpen`; **radar** pages may set `mermaid: true` and `categories: [Tech Radar]`
- **Learn** strictly enforces **YAML** across all new migrations (including `posts/` and `series/`). Ensure parity with the 2026 standardized schemas.
- use **Asia/Ho_Chi_Minh** style offsets in `date` when exemplars do (e.g. `+07:00`)
- internal links follow existing patterns: `/posts/.../`, `/series/.../`, `/radar/.../` (trailing slash when sibling links use it)
- **radar** and long-form **Vesviet** posts are Hugo `content/posts`-style pages under `content/radar/` with their own section; do not invent a new top-level folder without checking `hugo.toml` and nav
- prefer filenames that match established slugs (`kebab-case.md`); for series parts, mirror numbering and naming used in that series

## Suggested Process

### 1. Pick The Site And Subtree

Decide Vesviet vs Learn, then whether the piece is a **post**, **series** chapter, **series index**, **radar** entry (Vesviet only), or **learn doc** (`learn/content/docs/`).

### 2. Clone Local Conventions

Read neighboring files: one `_index.md` if the piece belongs in a series, plus the latest similar article. Align frontmatter delimiter, keys, tone, heading style, and link format.

### 3. Apply The Content Writer Research Rules

When the topic needs net-new evidence, follow the active **Content Writer** role: multiple research passes before drafting. When the user supplied sources or repo notes, synthesize from that material only.

### 4. Draft In Place

Write body Markdown consistent with Goldmark (`unsafe` may be enabled—use HTML only when existing posts do). Use `mermaid` code fences only when `mermaid: true` appears on comparable radar or post frontmatter.

### 5. Wire Navigation

For a new **series** or important **post**, update the relevant `_index.md` or hub page (e.g. series index, `posts/_index.md` on Learn) if that is the established pattern—mirror how prior entries were added.

### 6. Sanity Check

Confirm `draft` flag, `title`/`description` or `summary`, slug vs filename, and that at least one internal link resolves the same way as siblings.

## Checklist

- [ ] correct site root (`vesviet/content` vs `learn/content`) chosen
- [ ] frontmatter uses YAML with strict inline array notation (`categories: ["..."]`)
- [ ] `date`, tags/categories, and optional `ShowToc` / `TocOpen` / `mermaid` align with exemplars
- [ ] slug, filename, and permalinks match Hugo config and existing link style
- [ ] voice and structure match nearby content in that subtree
- [ ] series or radar navigation updated when the repo already does that for new entries

## Related Skills

- **write-documentation**: general doc drafting discipline and clarity patterns
- **write-tech-radar**: concise decision framing for radar-style entries
- **meeting-review**: synthesize stakeholder input before publishing sensitive claims
