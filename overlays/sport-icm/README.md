# Sport ICM Overlay

Project-specific conventions for the Sport ICM niche catalog — custom sportswear, athletic uniforms, and performance activewear.

**Depends on:** `overlays/astro-cloudflare`

- **Live:** Cloudflare Pages (sport-icm workers.dev subdomain)

## 2026 Stack Status

| Component | Current | Target |
|-----------|---------|--------|
| Astro | v5 | **v6/v7** — Content Layer API, direct `env` binding access |
| TailwindCSS | v3 | **v4** — CSS-first, no `tailwind.config.js` |
| Node.js | 18/20 | **22+** (required by Astro 6) |

## Specifics

- Niche catalog site built on Astro + Cloudflare Pages
- Product and category data in `src/data/` (TypeScript or JSON)
- Tailwind v4 + sport/athletic theme overrides (`@theme {}` CSS blocks)
- Contact form via Resend API + Turnstile anti-spam
- Static pages with optional dynamic category routes

## Brand

- Niche: Custom sportswear, athletic uniforms, team jersey OEM
- Audience: Sports clubs, schools, corporate teams, tournament organizers
- Tone: Energetic, performance-focused, professional

## Rules

- `rules/sport-project-rules.md` — Catalog structure, brand positioning, deploy conventions

## Relationship to Other ICM Overlays

| Overlay | Brand | Niche |
|---------|-------|-------|
| [icm-main](../icm-main/README.md) | ICM Factory Direct | B2B corporate, master brand |
| [golf-icm](../golf-icm/README.md) | Golf ICM | Golf apparel, resort wear |
| sport-icm | Sport ICM | Sportswear, athletic uniforms |
| [obj-configurator](../obj-configurator/README.md) | OBJ 3D | WebGL/WebGPU product configurator |

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
