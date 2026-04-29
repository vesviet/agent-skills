---
name: agent-tool-orchestration
description: Plan and sequence agent tool use by choosing the smallest reliable tool, parallelizing independent reads, avoiding unsafe shell operations, and validating results. Use when a task requires multiple searches, file edits, commands, or external checks.
---

# Agent Tool Orchestration

Use this skill when a task needs disciplined tool selection and sequencing across exploration, editing, validation, and reporting.

## Core Rules

- prefer specialized tools over shell commands when available
- parallelize independent reads and searches
- do not run destructive commands without explicit user approval
- inspect before editing and validate after substantive changes
- keep tool use scoped to the user's request and repo-local conventions

## Suggested Process

### 1. Classify The Work

Decide whether the task is exploration, implementation, debugging, review, validation, or documentation.

### 2. Choose The Smallest Reliable Tool

Prefer:

- file read tools for known files
- search tools for code discovery
- patch tools for focused edits
- shell commands for validation, build, test, and git status

### 3. Batch Independent Work

Run independent reads, globs, searches, or lints in parallel when they do not depend on each other.

### 4. Sequence Risky Actions

Before commands that create files, run builds, or change state:

- verify the working directory
- check relevant parent paths
- avoid duplicating long-running processes
- confirm permissions or user approval when required

### 5. Validate The Result

After edits:

- run targeted validators or lints
- inspect failures before changing more code
- rerun the smallest check that proves the fix

## Checklist

- [ ] task type classified
- [ ] repo constraints checked before action
- [ ] smallest reliable tools selected
- [ ] independent exploration parallelized
- [ ] state-changing commands sequenced safely
- [ ] edits validated with relevant checks

## Related Skills

- **agent-context-management**: Keep goal, evidence, and assumptions aligned
- **agent-quality-gate**: Run the correct completion checks
- **agent-handoff**: Report results and remaining risk clearly
- **troubleshoot-service**: Diagnose failing commands or runtime behavior
- **commit-code**: Prepare approved changes for delivery
