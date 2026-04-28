---
name: write-documentation
description: Draft or update technical documentation by following the repo's existing doc structure, audience needs, and source-of-truth boundaries. Use for README updates, service docs, runbooks, integration notes, or change explanations.
---

# Write Documentation

Use this skill when a change needs clear technical documentation or when existing docs are outdated or incomplete.

## Core Rules

- write for the intended audience, not for the author
- keep docs aligned with the actual source of truth
- prefer concrete steps and examples over vague explanation
- do not duplicate large chunks of information that already live elsewhere
- avoid internal workflow wording in user-visible docs unless the repo explicitly expects it

## Suggested Process

### 1. Identify The Documentation Need

Clarify:

- who will read it
- what problem it should solve
- whether it is setup, architecture, operations, usage, or release-oriented documentation

### 2. Inspect Existing Documentation Patterns

Look for:

- local doc location and naming conventions
- section structure
- voice and depth
- whether docs are colocated with code or live elsewhere

### 3. Gather The Minimum Correct Facts

Collect:

- commands or workflows that actually work
- key architecture or integration points
- configuration requirements
- known limitations or risks worth noting

### 4. Draft For Fast Usefulness

Prefer:

- short purpose statement
- prerequisites
- exact steps or examples
- troubleshooting notes when relevant
- links to deeper references instead of repeating them

### 5. Verify The Documentation

Check:

- examples match the code or repo structure
- commands are plausible for the target environment
- ownership and source-of-truth references are clear
- stale or conflicting guidance is removed

## Checklist

- [ ] audience and doc purpose identified
- [ ] local doc pattern reviewed
- [ ] facts gathered from current source of truth
- [ ] examples and steps written clearly
- [ ] stale or conflicting guidance removed

## Related Skills

- **navigate-service**: Gather context before documenting a service
- **review-service**: Capture readiness or release notes after review
- **troubleshoot-service**: Turn learned recovery steps into runbook updates
- **write-tech-radar**: Draft higher-level technology assessments
- **commit-code**: Prepare doc updates for delivery
