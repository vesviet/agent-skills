# UX Handoff Conventions — Flow And Component Specs

Apply when the ui-ux-designer role uses overlays/ui-design-system.

## Deliverable Layers

| Layer | Contract | When |
| ----- | -------- | ---- |
| Flow | contracts/schemas/ux-flow-spec.json | Multi-screen journey, navigation, transitions, API needs |
| Component | contracts/schemas/ui-component-spec.json | Each reusable or page-level UI building block |
| Requirements | feature-ticket.json (from BA) | Input only — do not duplicate business rules in UX specs |

## Order Of Work

1. Consume feature-ticket.json (or PM brief) for actors, preserved/changed behavior, AC.
2. Emit **ux-flow-spec.json** for the end-to-end journey.
3. Emit one **ui-component-spec.json** per component listed in `component_spec_refs`.
4. Set `flow_id` on each component spec to match the parent flow.
5. Hand Frontend a manifest: flow path + list of component spec paths.

## Frontend Handoff Manifest (markdown)

```markdown
## UX Handoff Manifest
- Flow spec: <path>/ux-flow-spec.json
- Components:
  - <path>/ProductCard.ui-component-spec.json
  - <path>/CartDrawer.ui-component-spec.json
- Feature ticket: <path>/feature-ticket.json (if any)
- Design system: <project overlay README>
```

## QA Handoff

- Derive scenarios from ux-flow-spec transitions and each component state's enum list.
- Include permission-limited and error recovery paths from the flow spec.

## Brand Overlay

When a project overlay defines colors, typography, or motion (e.g. Elomus Deep Navy + Teal), reference those tokens in component spec descriptions — do not invent conflicting palettes.

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
  See `See `core/skills/foundation/design-ux-flow/SKILL.md` and the `ux-flow-spec.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/foundation/design-ux-flow/SKILL.md` and the `ux-flow-spec.json` schema.

Last updated: 2026-09-01
