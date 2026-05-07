---
name: agent-tool-orchestration
description: Plan and sequence agent tool use by choosing the smallest reliable tool, controlling work phase by phase, parallelizing independent reads, avoiding unsafe shell operations, and validating results. Use when a task requires multiple searches, file edits, commands, or external checks across a bug, feature, review, or debugging flow.
---

# Agent Tool Orchestration

Use this skill when a task needs disciplined tool selection and sequencing across exploration, triage, editing, validation, and reporting.

## Core Rules

- prefer specialized tools over shell commands when available
- classify the work phase before choosing tools
- parallelize independent reads and searches
- do not run destructive commands without explicit user approval
- inspect before editing and validate after substantive changes
- keep tool use scoped to the user's request and repo-local conventions
- do not let a task move to the next phase without enough evidence for that phase

## Suggested Process

### 1. Classify The Work And Phase

Decide:

- whether the task is a bug, feature, review, validation, or documentation task
- whether the current phase is intake, triage, implementation, validation, review, or handoff
- what output is required before the phase can end

### 2. Choose The Smallest Reliable Tool For The Phase

Prefer:

- file read tools for known files
- search tools for code discovery
- patch tools for focused edits
- shell commands for validation, build, test, and git status

Examples:

- intake or triage: file reads, searches, logs, focused reproduction commands
- implementation: focused reads, targeted edits, nearby-pattern inspection
- validation: narrow tests, validators, build commands, smoke checks
- handoff: diff inspection, changed-file review, validation summary

### 3. Batch Independent Work

Run independent reads, globs, searches, or lints in parallel when they do not depend on each other.

### 4. Sequence Risky Actions And Phase Gates

Before commands that create files, run builds, or change state:

- verify the working directory
- check relevant parent paths
- avoid duplicating long-running processes
- confirm permissions or user approval when required
- confirm the current phase has enough evidence to justify the next action

### 5. Reopen Earlier Phases When Needed

If new evidence appears:

- reopen triage when reproduction or expected behavior changes
- reopen implementation when validation exposes a deeper cause
- reopen review when a late risk invalidates the previous recommendation

### 6. Validate The Result

After edits:

- run targeted validators or lints
- inspect failures before changing more code
- rerun the smallest check that proves the fix

## Output Format

When this skill is driving a multi-step task, maintain a compact internal control frame:

```markdown
## Orchestration Frame

Work type:
- ...

Current phase:
- ...

Exit criteria:
- ...

Tools selected:
- ...

Evidence required before next phase:
- ...
```

## Checklist

- [ ] task type and current phase classified
- [ ] repo constraints checked before action
- [ ] smallest reliable tools selected
- [ ] independent exploration parallelized
- [ ] state-changing commands sequenced safely
- [ ] phase progression justified by evidence
- [ ] edits validated with relevant checks

## Related Skills

- **agent-context-management**: Keep goal, evidence, and assumptions aligned
- **agent-quality-gate**: Run the correct completion checks
- **agent-handoff**: Report results and remaining risk clearly
- **troubleshoot-service**: Diagnose failing commands or runtime behavior
- **commit-code**: Prepare approved changes for delivery
