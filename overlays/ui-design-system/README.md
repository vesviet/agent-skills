# UI Design System Overlay

Composable overlay for the `ui-ux-designer` role when work must follow a **brand or project design system** in addition to core UX rules.

This overlay does not replace `core/roles/ui-ux-designer.md`. Compose it with core and any project overlay (for example overlays/maydiengiaisaigon for Elomus e-commerce).

## Scope

- Flow vs component deliverable conventions
- When to emit ux-flow-spec.json vs ui-component-spec.json
- Pointer to project-specific palette, typography, and component patterns

## Included

- `rules/handoff-conventions.md` — Contract layering and Frontend handoff order

## Activation

```
Role: ui-ux-designer
Overlay: overlays/ui-design-system
```

Add a **project** design overlay when one exists:

```
Overlay: overlays/maydiengiaisaigon
```

Read that project's rules/elomus-design-system.md (or equivalent) before finalizing visual and interaction specs.

## Project Design Overlays (examples)

| Overlay | Use when |
| ------- | -------- |
| overlays/maydiengiaisaigon | Máy Điện Giải Sài Gòn / Elomus Laravel storefront |
| (repo-local rules) | Any app with documented tokens in overlays/ or docs/ |
