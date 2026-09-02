# OBJ 3D Configurator Overlay

Project-specific conventions for the 3D Product Configurator — an interactive WebGL application for customizing apparel products.

**Depends on:** `overlays/astro-cloudflare`

- **Repo:** `D:\regna\cloudflare\obj`
- **Live:** Cloudflare Workers (`obj.sweet-voice-f606.workers.dev`)

## Specifics

- Astro v5 host + React Three Fiber (R3F) interactive islands
- Three.js / R3F for 3D rendering, Redux Toolkit + Zustand for state
- Prisma ORM + SQLite for design persistence (`prisma/schema.prisma`)
- Express.js backend (`server.js`) for local dev API
- Design Hub legacy codebase in `src/design-hub/` (React class → hooks migration)

## Rules

- `rules/obj-project-rules.md` — 3D engine, state management, design-hub architecture

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
