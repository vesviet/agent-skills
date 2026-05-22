---
name: design-review
description: Review UX flows, visual hierarchy, interaction patterns, and design-system alignment against specs and user goals. Use when validating ui-component-spec or ux-flow-spec before implementation, or critiquing marketing/product UI without reviewing application code.
---

# Design Review

Use this skill with **UI/UX Designer** or **Reviewer** when the deliverable is design quality and spec completeness—not code correctness.

## Core Rules

- review against declared user goals, preserved behavior, and feature-ticket when provided
- consume `ux-flow-spec.json` and `ui-component-spec.json` when present; do not invent missing states
- separate blocking UX defects from polish or preference
- check all critical states: loading, empty, error, permission, success
- verify design-system tokens and component patterns when an overlay is active
- do not implement UI; emit findings for Frontend or UI/UX to fix
- route code-level bugs to `review-code`; route a11y conformance gaps to `accessibility-review`

## Suggested Process

### 1. Gather Inputs

- feature-ticket.json, ux-flow-spec.json, ui-component-spec.json set
- design overlay tokens (ui-design-system, brand overlay)
- research-report.json or data-analysis-report.json when metrics UI is involved

### 2. Evaluate Flow Coherence

- entry and exit points match user mental model
- transitions are explicit; no dead ends without recovery
- primary task completion path is obvious

### 3. Evaluate Screens And Components

- hierarchy, spacing, typography, and CTA prominence
- copy clarity per state; error messages actionable
- consistency with existing patterns in the product

### 4. Record Findings

Classify each item: blocking | should-fix | suggestion.

Note spec gaps (missing state, missing api_field, ambiguous transition).

### 5. Hand Off

- blocking items return to UI/UX Designer before Frontend starts
- should-fix items may proceed with documented debt
- implementation-ready specs get explicit approval note

## Checklist

- [ ] user goal and preserved/changed behavior understood
- [ ] ux-flow-spec covers screens, transitions, and component_spec_refs
- [ ] each component spec lists states, events, and copy_per_state
- [ ] loading, empty, error, and permission paths reviewed
- [ ] design-system or overlay tokens applied consistently
- [ ] findings classified with severity and owner (design vs engineering)
- [ ] no code review scope creep into style-only code nitpicks
- [ ] handoff states whether Frontend may start implementation

## Related Skills

- **design-ux-flow**: Author or revise specs when review finds gaps
- **accessibility-review**: Deep a11y pass when WCAG conformance is required
- **review-code**: Code-level review after design-approved implementation
- **analyze-business-requirements**: Clarify behavior when ticket and spec conflict
- **meeting-review**: Multi-role critique when design blocks release
