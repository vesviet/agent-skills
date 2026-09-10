# Máy Lạnh Treo Tường Content Overlay

This overlay provides domain-specific engineering rules, HVAC technical schemas, and publishing workflows for the `maylanhtreotuong` Astro v5 site (deployed on Cloudflare Pages/Workers).

## Tech Stack & Dependencies

- **Framework**: Astro v5 (`astro: ^5.12.9`) with `@astrojs/cloudflare` v12.
- **Stack Dependency**: Depends on `overlays/astro-cloudflare` for Wrangler deployment, bindings, and Cloudflare Pages architecture.
- **Sprint Dependency**: Works alongside `overlays/seo-publishing` for 7-day topic clustering, cannibalization guardrails, and cadence tracking.

## Included Components

### Rules
- `rules/content-schema.md`: Strict Astro Content Collection frontmatter specifications for both `post` (300 articles across 7 category folders) and `product` (72 models). Mandates `unique_angle`, `substance_requirement`, `anti_slop_gate`, and Answer-First BLUF block.
- `rules/hvac-engineering-standards.md`: Thermal engineering and HVAC testing standards. Enforces TCVN 7830:2021 CSPF energy efficiency calculations, ASHRAE 55-2023 thermal comfort vi khí hậu, Hioki Power Meter electricity logs (kWh/night), RION NL-52 acoustic testing (dB(A)), Super PCB 440V surge tolerances, and inverter compressor physics.
- `rules/silo-linking.md`: Silo link topology routing equity from 300 technical articles to 72 commercial product landing pages. Mandates anchor text distributions and `<PostCallToAction />` integration.

### Skills
- `skills/write-maylanhtreotuong-content`: Specialized drafting skill for Vietnamese HVAC content across 4 archetypes: Product Review & Teardown, Buying & Sizing Guide, Electricity & Operating Cost, and Technology Comparison.

### Workflows
- `workflows/publish-maylanhtreotuong-content.md`: 6-step publishing workflow covering technical SEO briefing, empirical data verification, Answer-First drafting, anti-slop verification, Silo link insertion, and Cloudflare build verification.

### Config
- `config/collections.md`: Comprehensive corpus inventory (300 posts across 7 category folders, 72 products, Astro glob loaders, Zod schemas, E-E-A-T engineering personas).

## Corpus Metrics (Snapshot 2026-09-10)

- Total Posts: 300 MDX articles across 7 categories: `gia-ca` (25), `huong-dan` (63), `kien-thuc` (71), `kinh-nghiem` (30), `mua-sam` (33), `review` (33), `so-sanh` (45).
- Total Products: 72 MD specification files under `src/data/product/`.
- AnswerFirst Coverage: 100% (300/300 posts).
- Anti-Slop Gate Coverage: 100% verified.

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

Last updated: 2026-09-10
