# Adapter Parity Standard

This document defines the minimum behavior that every root-level agent adapter must preserve.

Adapters may differ in syntax and style, but they must not weaken the operating contract of the pack.

## Required Parity Groups

Every adapter must preserve these nine groups:

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

### 7. Environment File Protection

The adapter must preserve all of the following:

- explicit prohibition on committing `.dev.vars` and `.env` (or other local environment files)
- instruction to verify `git status` and keep them in `.gitignore`

### 8. Repo-Local Override

The adapter must state that repo-local rules override these pack defaults when they are explicitly present.

### 9. Comment Hygiene

The adapter must preserve both:

- prefer no comment over comments that merely restate the code
- keep each code comment within 3 lines unless a longer doc comment, file header, or tooling directive is required

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

## Standard 2026 Alignment

This parity document governs every adapter. The 2026 upgrade pass added the
following invariants; adapters that mirror these groups must also mirror
the new failure-mode coverage below.

### Failure Modes

- **Parity drift between adapters**: a core rule changes but the Antigravity / Cursor / Claude / Kiro / Kilo Code / Copilot mirrors do not pick up the change. **Mitigation:** the parity validator (`validate-rules.py`) blocks the change when the mirrors drift; require `python3 core/scripts/validate-rules.py` to pass before merging any rule change.
- **Forbidden wording introduced**: an adapter uses `P0` / `P1` / `P2` labels or exposes thought-process narration in user-visible artifacts. **Mitigation:** the parity validator scans for forbidden wording; the build fails on detection.
- **Comment hygiene violated in an adapter example**: a code example in an adapter is over-commented or restates the code. **Mitigation:** examples must obey the same comment-hygiene rules as the core; review every example block in the adapter diff.
- **Adapters weakening the rule set**: an adapter omits a parity group to fit character limits. **Mitigation:** if a group cannot fit, prefer a reference link to `core/rules/code.md` rather than dropping the rule; the parity validator flags missing groups.
- **Policy reference omitted**: an adapter stops pointing to `action-boundaries.yaml` and `data-classification.yaml`. **Mitigation:** the parity validator confirms both paths are present; reject adapters that lose the policy reference.

### Security Guardrails (OWASP ASI)

- **ASI07 Inter-Agent Communication**: every adapter must preserve the policy-as-code enforcement contract so cross-agent payloads remain schema-validated.
- **ASI09 Human-Agent Trust Exploitation**: every adapter must preserve the explicit commit / push / publish approval requirement so the user is never bypassed.
- **ASI10 Rogue Agents**: every adapter must preserve the meta-rule that halts and asks the user when an action would violate the rules; never let an adapter silently absorb a rule violation.

Last updated: 2026-09-01