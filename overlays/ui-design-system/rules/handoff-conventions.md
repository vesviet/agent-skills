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
