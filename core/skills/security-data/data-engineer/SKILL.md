---
name: data-engineer
description: "DEPRECATED — use build-data-pipeline instead. This skill redirects to build-data-pipeline, which covers all ETL, pipeline, warehouse, orchestration, and data quality work. Use when migrating references away from this name."
---

# Data Engineer

> **Deprecated.** This skill has been renamed to `build-data-pipeline` to resolve a naming collision with the `data-engineer` role.
> Replace all references to `$data-engineer` with `$build-data-pipeline`.

## Core Rules

- do not use this skill for new work — use `build-data-pipeline` instead
- update any role Skill Toolbox or Related Skills that reference `data-engineer` to use `build-data-pipeline`

## Suggested Process

1. Identify where `data-engineer` skill is referenced (role toolbox, related skills, workflows)
2. Replace each reference with `build-data-pipeline`
3. Verify the replacement with `validate-roles.py` and `validate-skills.py`

## Checklist

- [ ] all references to `data-engineer` skill in role Skill Toolboxes replaced with `build-data-pipeline`
- [ ] all references to `data-engineer` in Related Skills sections replaced with `build-data-pipeline`
- [ ] all references to `data-engineer` in workflows replaced with `build-data-pipeline`
- [ ] validation scripts pass after replacement (`validate-roles.py`, `validate-skills.py`)
- [ ] README Skill Boundaries table updated to reference `build-data-pipeline`

## Related Skills

- **build-data-pipeline**: The canonical replacement for this skill
- **analyze-data**: One-off exploration and reports without pipeline ownership
