---
name: add-ui-component
description: Add or evolve a reusable UI component by following the repo's design system, composition patterns, accessibility rules, and state boundaries. Use when building frontend components or shared presentation elements.
---

# Add UI Component

Use this skill when a frontend change needs a new reusable component or a meaningful update to an existing one.

## Core Rules

- follow the repo's existing design system before inventing a new pattern
- prefer composition over one-off duplication
- keep accessibility, semantics, and keyboard behavior explicit
- keep styling and state responsibilities narrow and understandable
- update visual or interaction tests when the component contract changes

## Suggested Process

### 1. Inspect A Similar Component

Find a nearby component that matches:

- visual hierarchy
- state complexity
- prop or input pattern
- styling system
- test approach

### 2. Define The Component Contract

Clarify:

- what the component renders
- what inputs it accepts
- what events or callbacks it emits
- what states it must support
- whether it is presentational, stateful, or compositional

### 3. Build The Smallest Useful Version

Start with:

- semantic structure
- the main visual state
- required interactions
- loading, empty, error, or disabled states if relevant

Avoid prematurely adding variant complexity the first consumer does not need.

### 4. Integrate Styling And Accessibility

Check:

- semantic element choice
- focus behavior
- keyboard support
- aria labels or relationships where needed
- responsive behavior in the repo's style system

### 5. Connect State Carefully

If the component needs state:

- keep transient UI state local when possible
- avoid reaching directly into global state unless the repo expects it
- separate data fetching from pure presentation when the repo uses that pattern

### 6. Add Tests

Use skill: `frontend-testing`

Cover:

- render behavior
- important interaction paths
- accessibility-sensitive states
- prop or slot/children variations that are easy to break

## Checklist

- [ ] similar component pattern reviewed
- [ ] component contract defined
- [ ] accessibility and semantics checked
- [ ] state boundaries kept clear
- [ ] styling follows local system
- [ ] tests added or updated

## Related Skills

- **add-page-route**: Place the new component into a page or route flow
- **integrate-api-client**: Connect UI state to backend data safely
- **frontend-testing**: Add UI and interaction coverage
- **review-code**: Review accessibility and maintainability risk
- **commit-code**: Prepare the component change for delivery
