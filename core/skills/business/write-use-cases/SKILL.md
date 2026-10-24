---
name: write-use-cases
description: Scope, structure, and document production-grade Use Cases using Karl Wiegers 13-field template, Alistair Cockburn goal levels and scoping tests, and 20-point quality validation. Use when detailing user interactions, specifying normal and alternative courses, defining system boundaries, or converting high-level business goals into engineering specifications.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Write Use Cases

Use this skill to design, author, and validate structured Use Case specifications adhering to Alistair Cockburn's scoping rules and Karl Wiegers' 13-field template.

## When to Use

- converting business goals into sequential, actor-driven interaction specifications
- scoping complex multi-step workflows with branch conditions and failure states
- distinguishing Elementary Business Processes (EBPs) from business workflows and subfunctions
- establishing clear boundaries between system responsibilities and human actor tasks
- reviewing and refactoring poorly scoped, UI-dependent, or happy-path-only use cases
- generating verifiable test scenario baselines for QA and automated E2E testing

## Core Rules

- **Enforce Cockburn Scoping & Coffee-Break Test**: a valid Use Case represents an Elementary Business Process (EBP) completed by one person in one sitting (typically 2 to 30 minutes), leaving data in a consistent state
  - If it takes days or spans cross-departmental handoffs: declare as a *Summary-level business workflow*, decompose into discrete Use Cases
  - If it takes seconds (e.g. "Validate OTP", "Click Submit"): declare as a *Subfunction*, embed into the calling Use Case's step
- **Apply Cockburn's 3 Goal Levels**:
  - 🌊 *Summary Level (White)*: high-level end-to-end business goal (e.g. "Fulfill Customer Order")
  - 🎯 *User-Goal Level (Blue)*: canonical sweet spot for software Use Cases (e.g. "Submit Loan Application", "Approve Timesheet")
  - 🐟 *Subfunction Level (Black)*: reusable tactical step (e.g. "Authenticate Biometrics")
- **Mandate Karl Wiegers 13-Field Specification Structure**:
  1. `Use Case ID` (e.g. UC-ORD-001) | 2. `Title` (Active Verb + Noun) | 3. `Scope` & `Goal Level`
  4. `Primary Actor` | 5. `Secondary Actors` / Systems | 6. `Preconditions` (Must be true prior to start)
  7. `Trigger` (Event initiating UC) | 8. `Normal Course` (Numbered atomic steps)
  9. `Alternative Courses` (Branching successful paths) | 10. `Exception Courses` (Error/failure handling)
  11. `Postconditions` (Success Guarantee & Minimal/Failure Guarantee)
  12. `Business Rules` (Referenced IDs, not embedded in course steps)
  13. `Assumptions & Open Questions`
- **Eliminate 10 Writing Anti-Patterns**:
  - *No UI/GUI verbs*: ban "clicks button", "selects dropdown", "enters text"; use semantic intent: "submits credentials", "selects delivery tier"
  - *No embedded `if/else` in Normal Course*: the normal course represents the happy path; branch logic belongs strictly in Alternative or Exception courses
  - *No generic 'User' actors*: specify the precise domain role (e.g. "Loan Officer", "Enrolled Student", "Compliance Auditor")
  - *Explicit Failure Guarantees*: always define system state when an exception occurs (e.g. "Cart remains intact, inventory hold released")
- **Pass 20-Point Quality Checklist**: every use case must achieve >= 18/20 on the validation rubric prior to engineering handover
- Detailed template and anti-patterns: [`references/cockburn-scoping-and-13-field-template.md`](references/cockburn-scoping-and-13-field-template.md)

## Suggested Process

### 1. Scope & System Boundary Definition
Determine the subject system boundary. Apply the coffee-break test to ensure the task is an Elementary Business Process. Classify goal level (Summary, User-Goal, Subfunction).

### 2. Identify Actors & Invariants
Identify the Primary Actor who initiates the interaction to achieve a goal. Identify Supporting Actors and external APIs. Formulate strict Preconditions and Postconditions (Success vs Minimal guarantees).

### 3. Draft the Normal Course (Happy Path)
Author 4 to 9 numbered steps alternating between Actor Action and System Response. Keep steps in active voice and present tense.

### 4. Branch Alternative and Exception Courses
Identify all branching decisions, edge cases, system timeouts, validation failures, and user cancellations. Map each branch to the exact step number in the normal course (e.g. `3a. Card authorization fails`).

### 5. Run 20-Point Checklist & System 2 Review
Evaluate the completed specification against the 20-point quality checklist. Verify zero UI micro-mechanics, atomic steps, and complete failure guarantees.

## Checklist

- [ ] Use Case title formatted as Active Verb + Noun phrase (e.g. "Enroll in Course")
- [ ] scoped at User-Goal level (satisfies Cockburn Coffee-Break test)
- [ ] Primary Actor defined by explicit business role (never generic "User")
- [ ] Preconditions contain only verifiable states, zero business rules
- [ ] Normal Course contains only happy-path sequence, zero nested `if/else`
- [ ] all Alternative and Exception courses explicitly anchored to Normal Course step numbers
- [ ] Success and Minimal (Failure) guarantees fully specified in Postconditions
- [ ] 20-point validation checklist executed with passing score (>= 18/20)

## Related Skills

- **elicit-requirements**: structured questioning and BABOK v3 requirement quality audits
- **analyze-business-requirements**: analyze and write implementation-ready requirements
- **trace-requirements-impact**: maintain RTM and evaluate change request blast radius
- **design-ux-flow**: design user interface workflows and wireframes
