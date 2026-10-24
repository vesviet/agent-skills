---
description: "Active rules for the r3f-stack overlay after the v4.0.0 migration moved the three R3F skills out of core."
---

# R3F Stack Conventions

- Skills under this overlay assume a React + R3F/Three.js target. Do not load them for vanilla Three.js, Babylon.js, or non-React projects.
- 3D performance budgets (60fps / 1M triangles / 4MB gzipped) are defaults; tighten per project.
- When adding a new R3F skill, keep the naming pattern `<verb>-<noun>` and stick to R3F-idiomatic guidance (declarative scene graph, useFrame, drei helpers).
- Coordinate with `overlays/obj-configurator` for product-configurator specifics.

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
  See `See `core/skills/agent/integrate-webmcp/SKILL.md` and the `implementation-result.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/agent/integrate-webmcp/SKILL.md` and the `implementation-result.json` schema.

Last updated: 2026-09-01
