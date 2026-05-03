# Skills Inventory

This directory contains the skill inventory for the full global engineering pack.

## Taxonomy

### Agent

These cover agent operating discipline:

- `agent-context-management`
- `agent-memory-compaction`
- `agent-tool-orchestration`
- `agent-quality-gate`
- `agent-handoff`

### Foundation

These are the default portable skills:

- `analyze-business-requirements`
- `commit-code`
- `create-migration`
- `design-ux-flow`
- `meeting-review`
- `navigate-service`
- `performance-profiling`
- `review-code`
- `review-service`
- `troubleshoot-service`
- `write-product-brief`
- `write-tests`

### Backend

These cover service implementation:

- `add-api-endpoint`
- `add-event-handler`
- `add-service-client`
- `scaffold-new-service`

### Frontend

Implemented in this batch:

- `add-ui-component`
- `add-page-route`
- `debug-3d-scene`
- `integrate-r3f-three-legacy`
- `integrate-api-client`
- `optimize-3d-assets`
- `frontend-testing`

### Platform

These cover delivery and runtime:

- `setup-deployment`
- `debug-runtime-platform`
- `add-telemetry-instrumentation`

### Security And Data

Implemented in this batch:

- `manage-secrets`
- `database-maintenance`
- `security-audit`

### Documentation

Implemented in this batch:

- `write-documentation`
- `write-tech-radar`

## Priority Plan

### Priority 1 Implemented In This Batch

- `add-api-endpoint`
- `add-event-handler`
- `add-service-client`
- `scaffold-new-service`
- `setup-deployment`
- `debug-runtime-platform`

### Priority 2 Recommended Next

- `design-review`
- `3d-material-pipeline`
- `incident-report`
- `release-notes`
- `product-discovery`

### Priority 3 Nice To Add

- `accessibility-review`
- `frontend-state-management`
- `data-pipeline-review`

## Naming Rules

- prefer generic names over stack-specific names
- categorize skills under their respective taxonomy folders (agent, foundation, backend, frontend, platform, security-data, documentation)
- move stack-specific or org-specific variants into separate packs later if needed

## Skill Authoring Standard

Every `SKILL.md` should use this baseline structure unless a skill has a clear reason to be shorter:

1. YAML frontmatter with `name` and `description`.
2. H1 title matching the skill name in title case.
3. One short "Use this skill..." paragraph.
4. `## Core Rules` for non-negotiable constraints.
5. `## Suggested Process` for the normal execution path.
6. `## Checklist` for completion checks.
7. `## Related Skills` with one-line descriptions.

Optional sections such as `## Output Format`, `## Adaptation Notes`, `## Quick Reference`, or domain-specific guidance are fine when they make the skill easier to execute.

Descriptions should include both what the skill does and when to use it. Keep skills repo-agnostic by default; put stack-specific assumptions in adapters or examples rather than the main trigger text.

## Validation Gate

Run this before treating skill changes as complete:

```bash
python3 scripts/validate-skills.py
```

The validator checks:

- every skill has valid `name` and `description` frontmatter
- descriptions include both capability and trigger language
- skill names match directory names
- every skill has the baseline sections
- checklists contain enough actionable completion checks
- related skill references point to existing skills
- role and workflow skill references resolve

Skill changes are not done until this check passes.
