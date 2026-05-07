---
name: design-ux-flow
description: Design or refine a UX flow by defining user goals, preserved behavior, screen states, interaction rules, edge cases, and adjacent flow impact. Use when a feature, bug fix, or behavior change needs a UX/UI brief that frontend and QA can implement and validate reliably.
---

# Design UX Flow

Use this skill when user-facing behavior needs to be turned into a clear flow, screen-state model, and interaction brief.

## Core Rules

- design for user understanding, not only visual polish
- make preserved versus changed behavior explicit
- define all important states, transitions, and recovery paths
- identify adjacent flows or reused patterns that could be affected
- do not leave permissions, validation, or feedback behavior implicit

## Suggested Process

### 1. Define The User Journey

Clarify:

- who the user is
- what goal they are trying to complete
- where they enter and exit the flow
- whether the change fixes confusion, adds capability, or changes behavior

### 2. Map States And Transitions

Identify:

- default state
- loading state
- empty state
- error state
- success or recovery state
- permission-limited or validation-blocked state

### 3. Specify Interaction Rules

Write down:

- primary actions
- validation and inline feedback
- navigation behavior
- retry or recovery behavior
- accessibility-sensitive interactions

### 4. Check Impact Radius

Look for:

- reused components or patterns
- adjacent flows that could regress
- affected roles or visibility rules
- responsive or browser-sensitive behavior

### 5. Produce An Implementation-Ready Brief

Leave a brief that downstream roles can use directly:

- Frontend can implement states and rules
- QA can derive flow-sensitive scenarios
- Product can confirm behavior intent

## Output Format

```markdown
# <Flow or Screen> - UX/UI Brief

## User Journey
- User:
- Goal:
- Entry and exit:
- Existing behavior to preserve or change:

## Screen States
- Default:
- Loading:
- Empty:
- Error:
- Disabled or permission-limited:
- Success / recovery:

## Interaction Rules
- Primary actions:
- Validation:
- Feedback:
- Adjacent flows or reused patterns to re-check:

## Handoff
- Components or surfaces affected:
- Accessibility notes:
- QA-sensitive scenarios:
- Open questions:
```

## Checklist

- [ ] user, goal, and entry/exit defined
- [ ] preserved versus changed behavior stated
- [ ] important states and transitions defined
- [ ] validation and feedback behavior made explicit
- [ ] adjacent flows or reused patterns identified
- [ ] handoff is usable for frontend and QA

## Related Skills

- **write-product-brief**: Clarify the value and scope behind the flow
- **analyze-business-requirements**: Supply business rules and exception logic
- **meeting-review**: Pressure-test UX trade-offs and cross-functional impact
- **add-page-route**: Implement the flow at route level
- **frontend-testing**: Validate the designed states and interactions
