# Adapter Parity Standard

This document defines the minimum behavior that every root-level agent adapter must preserve.

Adapters may differ in syntax and style, but they must not weaken the operating contract of the pack.

## Required Parity Groups

Every adapter must preserve these five groups:

### 1. Rule Source Of Truth

The adapter must point to:

- `core/rules/code.md`

It must make clear that the adapter mirrors or derives from the core rules rather than inventing separate policy.

### 2. Safety And Approval Gates

The adapter must preserve all of the following:

- explicit commit approval requirement
- explicit push, tag, publish, or release approval requirement
- explicit local validation requirement before commit
- explicit secret handling prohibition
- explicit prohibition on internal AI or workflow metadata in user-visible artifacts

### 3. Meta-Rule

The adapter must state a meta-rule equivalent to:

- verify actions against `core/rules/code.md` before finalizing or executing
- halt and ask the user when an action would violate the rules

### 4. Role And Skill Enforcement

The adapter must preserve all of the following:

- role standard must be read first
- role-specific file must be read second
- skill toolbox lock must be respected
- boundary lock must be respected

### 5. Workflow Discipline

The adapter must preserve all of the following:

- output a markdown checklist for all workflow steps
- process one workflow step at a time
- mark completion before moving on
- respect the `Role:` ownership line in workflow steps

## Notes

- Adapters may be shorter than the full source documentation.
- Adapters may rephrase wording when the target platform needs different phrasing.
- Adapters must not weaken any parity group even if the wording changes.
