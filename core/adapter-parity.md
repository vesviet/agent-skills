# Adapter Parity Standard

This document defines the minimum behavior that every root-level agent adapter must preserve.

Adapters may differ in syntax and style, but they must not weaken the operating contract of the pack.

## Required Parity Groups

Every adapter must preserve these six groups:

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

### 6. Policy-As-Code Enforcement

The adapter must reference the machine-readable policy layer that governs state-changing actions:

- `core/policies/action-boundaries.yaml`
- `core/policies/data-classification.yaml`

It must make clear that action boundaries and data classification are checked before state-changing actions. Adapters that also cover MCP tool mapping should reference `core/policies/mcp-tool-map.yaml`, but the two files above are the required minimum.

## Enforcement

Parity is machine-checked by `core/scripts/validate-rules.py`, which validates these adapter files against the parity groups above:

- `.cursorrules`
- `.cursor/rules/agent-skills.md`
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `.kiro/steering/agent-skills.md` (Kiro-native always-on steering)
- `.kilocode/rules/agent-skills.md` (Kilo Code native rules)

A change to `core/rules/code.md` or to any parity group must be mirrored across all of these adapters, and `validate-rules.py` must pass before the change is considered done. Codex, Windsurf, and VS Code Copilot read the root `AGENTS.md` (the shared open standard) rather than a dedicated mirror.

### Forbidden Wording

Adapters (and the source rules) must not contain:

- exposed "thought process" narration in user-visible artifacts
- `P0`/`P1`/`P2` severity labels — use `Blocking`, `Important`, and `Follow-Up` instead

## Notes

- Adapters may be shorter than the full source documentation.
- Adapters may rephrase wording when the target platform needs different phrasing.
- Adapters must not weaken any parity group even if the wording changes.
