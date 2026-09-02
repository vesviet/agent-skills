# Golf ICM Overlay

Project-specific conventions for the Golf ICM niche website — golf apparel and resort wear catalog.

**Depends on:** `overlays/astro-cloudflare`

- **Live:** Cloudflare Pages (`golf-icm.sweet-voice-f606.workers.dev`)

## 2026 Stack Status

| Component | Current | Target |
|-----------|---------|--------|
| Astro | v5 | **v6/v7** — Content Layer API, direct `env` binding access |
| TailwindCSS | v3 | **v4** — CSS-first, no `tailwind.config.js` |
| Node.js | 18/20 | **22+** (required by Astro 6) |

## Specifics

- Single-page catalog site (`src/pages/index.astro` — primary content inline)
- MDX support for blog/article content (`@astrojs/mdx`)
- Gallery generation scripts (`generate_galleries.mjs`, `clone_raw.mjs`, `apply_updates.mjs`)
- Product gallery data in `generated_galleries.json`
- Tailwind + Tabler icons (`@iconify-json/tabler`)
- Contact form via Resend API + Turnstile

## Rules

- `rules/golf-project-rules.md` — Catalog structure, gallery management, brand positioning

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
