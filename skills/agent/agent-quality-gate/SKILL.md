---
name: agent-quality-gate
description: Run and interpret repository quality gates for agent-delivered changes, including validators, lint, tests, build checks, and diff sanity checks. Use when reporting completion, preparing commits, or declaring a pack, role, workflow, or code change ready.
---

# Agent Quality Gate

Use this skill when changes need evidence that they are complete, valid, and aligned with repo-local checks.

## Core Rules

- run the repo's own validators before declaring completion
- choose targeted checks first, then broader checks when risk justifies them
- do not hide skipped checks or failing validation
- fix introduced issues when the cause is clear and local
- never treat a clean diff or passing lint as proof of full behavioral safety

## Suggested Process

### 1. Identify Required Gates

Inspect the repo for applicable checks:

- validation scripts
- lint or static analysis
- tests
- build commands
- formatting or documentation checks
- diff whitespace checks

### 2. Match Gates To Change Risk

Run narrow checks for small documentation or single-file changes. Run broader checks when behavior, shared contracts, scripts, or release paths changed.

### 3. Run Checks Safely

Use repo-local commands and avoid inventing workflows. If a command is expensive or environment-dependent, explain the trade-off before skipping it.

### 4. Interpret Failures

When a check fails:

- identify whether the failure was introduced by the current change
- fix local, clear failures
- avoid masking unrelated pre-existing failures
- rerun the failing check after a fix

### 5. Report Evidence

Summarize exact checks run, pass/fail status, skipped checks, and residual risk.

## Checklist

- [ ] required repo-local gates identified
- [ ] check scope matched to change risk
- [ ] relevant validators, lints, tests, or builds run
- [ ] failures investigated and fixed when local
- [ ] skipped checks explained
- [ ] final status reported with residual risk

## Related Skills

- **agent-tool-orchestration**: Run checks in the right order
- **agent-context-management**: Track validation evidence across long tasks
- **agent-handoff**: Communicate validation results clearly
- **write-tests**: Add coverage when risk is not protected
- **commit-code**: Validate changes before approved commit creation
