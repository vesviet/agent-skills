---
name: accessibility-review
description: Audit UI for keyboard navigation, focus order, screen-reader labels, color contrast, motion preferences, and ARIA correctness against WCAG-oriented criteria. Use when validating user-facing flows before release, after design specs land, or when fixing reported a11y defects.
---

# Accessibility Review

Use this skill with **QA Engineer**, **Frontend Developer**, or **UI/UX Designer** when accessibility conformance must be verified explicitly.

## Core Rules

- target WCAG 2.1 Level AA unless the repo documents a different bar
- test keyboard-only paths for every primary task in scope
- verify visible focus indicators and logical tab order
- ensure images, icons, and controls have accessible names (text or aria-label)
- check color contrast for text and interactive states; do not rely on color alone
- respect `prefers-reduced-motion` when animations are present
- cite concrete selectors, routes, or component names for every finding
- route visual/IA issues without a11y impact to `design-review`; route logic bugs to `review-code`

## Suggested Process

### 1. Define Scope

- routes, components, or ux-flow-spec screens in scope
- supported browsers and assistive tech assumptions from repo docs
- whether design specs already document a11y behavior

### 2. Static Spec Review

When specs exist:

- copy_per_state includes announcements for dynamic updates
- focus trap and escape behavior documented for modals
- error messages associated with fields (aria-describedby pattern)

### 3. Implementation Review

- semantic HTML landmarks (main, nav, heading order)
- form labels, grouping, and error association
- custom widgets: roles, states, keyboard handlers
- live regions for toasts and async status

### 4. Manual Checks

- tab through primary flow without mouse
- activate controls with Enter/Space where expected
- screen reader spot-check on critical path (if tooling available)

### 5. Report

List violations by severity: critical (blocks task) | serious | moderate | minor.

Recommend fix pattern, not only failure description.

## Checklist

- [ ] scope routes/components listed
- [ ] keyboard path completes primary user task
- [ ] focus order is logical and focus visible
- [ ] interactive elements have accessible names
- [ ] images and icons have alt text or are marked decorative
- [ ] color contrast checked for text and controls
- [ ] motion respects reduced-motion preference when applicable
- [ ] findings tied to files or components with severity

## Related Skills

- **design-ux-flow**: Add a11y notes to specs when gaps found early
- **design-review**: Visual hierarchy and pattern consistency
- **frontend-testing**: Automate regression tests for a11y fixes
- **review-code**: Broader code review including non-a11y risks
- **write-tests**: Add axe or similar checks when repo supports them
