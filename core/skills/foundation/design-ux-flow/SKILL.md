---
name: design-ux-flow
description: Design or refine a UX flow by defining user goals, preserved behavior, screen states, interaction rules, edge cases, and adjacent flow impact. Use when a feature, bug fix, or behavior change needs a UX/UI brief that frontend and QA can implement and validate reliably.
---

# Design UX Flow

Use this skill with the **UI/UX Designer** role when user-facing behavior must become structured specs for engineering.

## Core Rules

- design for user understanding, not only visual polish
- make preserved versus changed behavior explicit (align with feature-ticket.json when provided)
- define all important states, transitions, and recovery paths
- emit `contracts/schemas/ux-flow-spec.json` for multi-screen work
- emit one `contracts/schemas/ui-component-spec.json` per entry in `component_spec_refs`
- set `flow_id` on every component spec to match the parent flow
- identify adjacent flows or reused patterns that could be affected
- do not implement production UI — hand off specs to Frontend Developer

## Deliverable Decision

| Scope | Emit |
| ----- | ---- |
| Feature spanning 2+ screens or routes | ux-flow-spec.json + N × ui-component-spec.json |
| Single widget / isolated component change | ui-component-spec.json (include flow_id if part of a program) |
| Dashboard or metrics-heavy UI | ux-flow-spec.json; consume data-analysis-report.json for field shapes |
| Marketing blog / SEO landing | Decline — route to SEO Analyst + Content Writer |

## Suggested Process

### 1. Consume Requirements

- feature-ticket.json from Business Analyst (actors, rules, AC, preserved/changed)
- research-report.json or data-analysis-report.json when supplied
- project design overlay tokens (ui-design-system + brand overlay)

### 2. Define The User Journey

Clarify user, goal, entry/exit, and behavior change type (fix vs new capability).

### 3. Map States And Transitions

Build screens[] and transitions[] for ux-flow-spec.json.

### 4. Specify Components

For each surface, write ui-component-spec.json: props, states, events, copy_per_state, api_fields, accessibility.

### 5. Check Impact Radius

Document adjacent flows, permissions, analytics_events, and api_needs.

### 6. Package Handoff

Publish UX handoff manifest (flow path + component paths) for Frontend and QA.

## Output Format

Markdown brief (see `core/roles/ui-ux-designer.md` template) **plus** JSON contracts when machine handoff is required.

## Checklist

- [ ] feature-ticket or PM inputs consumed
- [ ] ux-flow-spec.json valid for multi-screen scope
- [ ] each component_spec_ref has a matching ui-component-spec.json
- [ ] flow_id consistent across flow and component specs
- [ ] api_needs and open_questions captured
- [ ] design system overlay rules respected
- [ ] handoff manifest complete

## Related Skills

- **analyze-business-requirements**: Interpret BA rules before designing states
- **write-product-brief**: Align with PM scope and outcomes
- **meeting-review**: Resolve UX trade-offs with stakeholders
- **add-ui-component**: Frontend implementation — not design delivery
- **add-page-route**: Route-level wiring after specs exist
- **frontend-testing**: QA validation patterns for designed states
