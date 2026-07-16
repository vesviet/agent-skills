---
name: accessibility-review
description: Audit UI for keyboard navigation, focus order, screen-reader labels, color contrast, motion preferences, and ARIA correctness against WCAG 2.2 criteria (including Focus Appearance 2.4.11/12, Target Size 2.5.8, Accessible Authentication 3.3.8/9). Use automated CI gates via @axe-core/playwright for regression detection alongside manual screen-reader testing. Use when validating user-facing flows before release, after design specs land, or when fixing reported a11y defects.
---

# Accessibility Review

Use this skill with **QA Engineer**, **Frontend Developer**, or **UI/UX Designer** when accessibility conformance must be verified explicitly.

## When to Use

- validating user-facing flows before release
- after design specs land
- fixing reported a11y defects
- running @axe-core/playwright gates + screen-reader checks

## Core Rules

- target WCAG 2.1 Level AA unless the repo documents a different bar
- target WCAG 2.2 Level AA as the updated baseline (aligning with ISO/IEC 40500:2025, EU EAA June 2025, and US DOJ April 2026 requirements), specifically auditing new Success Criteria:
  - **3.3.8 Accessible Authentication**: Ensure cognitive function tests (such as memorizing passwords/usernames or solving puzzles) are not required for login processes without alternatives.
  - **3.3.7 Redundant Entry**: Avoid requiring users to re-enter information previously entered in the same process; instead, auto-populate or provide selectable choices.
  - **2.4.11 Focus Appearance**: Verify visible focus indicators have a contrast ratio of at least 3:1 against surrounding colors and are sufficiently sized.
  - **2.5.7 Dragging Movements**: Provide a single-pointer alternative (e.g. click/tap controls) for any functionality requiring dragging.
- evaluate Cognitive Accessibility (COGA) requirements:
  - **Plain Language**: Keep instructions and UI labels simple and concise.
  - **Error Prevention**: Provide automatic suggestions, warnings, and clear instructions before submission.
  - **Memory Aids**: Avoid placeholder-only labels; maintain persistent context and visual cues.
- audit ARIA 1.3 semantic roles and attributes on dynamic elements:
  - Use `suggestion`, `comment`, and `mark` roles for editorial markup and user feedback panels.
  - Use `aria-description` for detailed text description, and `aria-braillelabel` / `aria-braillevaluedescription` for braille readers.
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

### 2026: WCAG 2.2 AA Updated Baseline
The following Success Criteria are enforced to meet updated regulatory baselines (ISO/IEC 40500:2025; EU EAA June 2025; US DOJ April 2026):
- **3.3.8 Accessible Authentication**: Do not require cognitive tests (e.g., copy-paste blocks, security questions, puzzles) for authentication without a mechanism that does not require one or provides support.
- **3.3.7 Redundant Entry**: Previously entered data in a single multi-step workflow must be auto-populated or selectable (except for security/re-verification inputs).
- **2.4.11 Focus Appearance**: The focus indicator must have a minimum area and a contrast ratio of at least 3:1 against the surrounding pixels.
- **2.5.7 Dragging Movements**: Provide click or tap alternatives for dragging functions (e.g. sliders, canvas manipulation).

### 2026: Cognitive Accessibility (COGA)
Design and review UIs with COGA guidelines to assist users with cognitive and learning disabilities:
- **Plain Language**: Avoid jargon, keep paragraphs short, and structure text logically.
- **Error Prevention**: Provide contextual help, input format suggestions, and clear error notifications with actionable recovery steps.
- **Memory Aids**: Display persistent labels, ensure context remains visible across steps, and do not rely on short-term memory (e.g. keep instructions visible during input).

### 2026: ARIA 1.3 Specification Updates
Ensure modern assistive technology support by incorporating new ARIA 1.3 semantic roles and attributes:
- **suggestion**: Use to mark up proposed additions or deletions in collaborative text fields.
- **comment**: Use to identify user-submitted commentary, annotations, or discussion threads.
- **mark**: Use to indicate text marked or highlighted for relevance or reference.
- **aria-description**: Provide an explicit descriptive string to assistive devices without needing an ID reference.
- **aria-braillelabel** & **aria-braillevaluedescription**: Provide custom labels and value descriptions optimized specifically for braille displays.

## Checklist

- [ ] scope routes/components listed
- [ ] keyboard path completes primary user task
- [ ] focus order is logical and focus visible
- [ ] interactive elements have accessible names
- [ ] images and icons have alt text or are marked decorative
- [ ] color contrast checked for text and controls
- [ ] motion respects reduced-motion preference when applicable
- [ ] findings tied to files or components with severity
- [ ] WCAG 2.2 AA new SCs verified (Accessible Auth, Redundant Entry, Focus Appearance, Dragging Movements)
- [ ] Cognitive accessibility (COGA) principles (plain language, error prevention, memory aids) reviewed
- [ ] ARIA 1.3 roles (suggestion, comment, mark) and attributes (aria-description, aria-braillelabel) verified

## Related Skills

- **design-ux-flow**: Add a11y notes to specs when gaps found early
- **design-review**: Visual hierarchy and pattern consistency
- **frontend-testing**: Automate regression tests for a11y fixes
- **review-code**: Broader code review including non-a11y risks
- **write-tests**: Add axe or similar checks when repo supports them
