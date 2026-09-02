# Golf ICM — Project Rules

Project-specific conventions for the Golf ICM niche catalog site.

## 2026 Astro Migration Notes

- **Astro 6**: `Astro.locals.runtime.env` → direct `env` parameter access.
- **TailwindCSS v4**: replace `tailwind.config.js` with `@theme {}` CSS blocks.
- **Content Layer**: if adding content collections, use `src/content.config.ts` with `glob()` loader.
- Run `npx @tailwindcss/upgrade` for automated Tailwind migration.

## Site Architecture

- Primary content in `src/pages/index.astro` — single-page catalog with sections.
- Additional pages for 404, API endpoints, blog articles (MDX).
- Components in `src/components/` — Astro-only (no React islands needed).
- Styles in `src/styles/` — TailwindCSS v4 base + custom `@theme` tokens.

## Product Galleries

- Gallery data auto-generated to `generated_galleries.json` via build scripts.
- `generate_galleries.mjs` — scans `public/` media for product images, outputs JSON.
- `clone_raw.mjs` — clones raw product images from source.
- `apply_updates.mjs` — applies batch updates to gallery metadata.
- Image assets in `public/` — served as-is through Cloudflare CDN.

## Brand Positioning

- Niche: Golf apparel, polo shirts, resort wear, country club uniforms.
- Tone: Premium, sophisticated, performance-focused.
- Target: Golf clubs, resorts, corporate events, tournament organizers.
- Keywords: custom golf apparel, polo shirts manufacturer, resort wear OEM.
- **2026 GEO/AI**: Add Q&A structured data to product sections for AI search citations.

## Content (MDX)

- Blog articles use MDX format with reading-time estimation.
- Typography plugin enabled (`@tailwindcss/typography` — import via CSS in v4).
- Frontmatter: `title`, `date`, `description`, `image`, `tags`.

## Deploy

- `npm run deploy` → `astro build && wrangler pages deploy dist`.
- GitHub Actions on `main` branch.
- Secrets via `.dev.vars` (local) / Cloudflare Dashboard (prod).

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
  See `See `core/skills/foundation/setup-design-system/SKILL.md` and the `edge-deployment-spec.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/foundation/setup-design-system/SKILL.md` and the `edge-deployment-spec.json` schema.

Last updated: 2026-09-01
