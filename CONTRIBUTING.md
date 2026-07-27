# Contributing to Agent Skills

This guide covers how to add or modify skills, roles, overlays, workflows, and contracts. Each component type has a required structure and a validator — changes are not done until the validator passes.

## Quick Reference

| Adding... | Authoring standard | Validator |
|-----------|-------------------|-----------|
| A skill | `core/skills/README.md` → Skill Authoring Standard | `validate-skills.py` |
| A role | `core/roles/README.md` → Role Authoring Standard | `validate-roles.py` |
| A workflow | `core/workflows/README.md` → Workflow Authoring Standard | `validate-workflows.py` |
| A contract | `core/contracts/README.md` → When To Create A New Schema | `validate-contracts.py` |
| An overlay | `overlays/README.md` → Overlay Authoring Rules | `validate-skills.py` |
| A pack | `packs/README.md` → Pack Authoring Rules | `validate-packs.py` |

Run all validators at once:

```bash
python3 core/scripts/validate-all.py
```

---

## Adding a New Skill

1. Create a directory: `core/skills/<taxonomy>/<skill-name>/`
2. Create `SKILL.md` with this structure:

```markdown
---
name: skill-name
description: What it does and when to use it (both required for validator).
---

# Skill Name In Title Case

Use this skill when...

## Core Rules

- non-negotiable constraint 1
- non-negotiable constraint 2

## Suggested Process

### 1. Step Name
...

## Checklist

- [ ] actionable check 1
- [ ] actionable check 2

## Related Skills

- **other-skill**: one-line description
```

3. Add the skill name to `core/skills/README.md` under the correct taxonomy section.
4. Add the skill to any role toolboxes where it belongs (`core/roles/<role>.md` → `## Skill Toolbox`).
5. Run `python3 core/scripts/validate-skills.py` — must pass before merging.

For overlay-specific skills (stack or project-specific): put them under `overlays/<overlay-name>/skills/<skill-name>/SKILL.md` instead of `core/skills/`.

---

## Adding a New Role

1. Create `core/roles/<role-name>.md`.
2. Follow the 18-section structure defined in `core/roles/role-standard.md` exactly:

```
H1 title → Mission → Level → role-standard link →
Principal Expectations → Use This Role When → Core Responsibilities →
Inputs Required → Outputs Produced → Decision Boundaries →
Collaboration → Guardrails → Skill Toolbox → Output Template →
Review Checklist → Anti-Patterns To Reject → Role Handoff →
Definition Of Done
```

3. Reference only skills that exist in `core/skills/` or loaded overlays.
4. Add a policy entry to `core/policies/action-boundaries.yaml`.
5. Run `python3 core/scripts/generate-a2a-registry.py` to generate the agent card.
6. Run `python3 core/scripts/validate-roles.py` and `validate-2026-compliance.py` — both must pass.

---

## Adding a New Workflow

1. Create `core/workflows/<workflow-name>.md`.
2. Required structure:

```markdown
---
description: concise one-line description
---

## Workflow Name Workflow

### Prerequisites

### Workflow Steps

#### 1. Step Name
Role: **Role Name**
...

### Checklist

### Related Workflows

### Related Skills
```

3. Every step must have a `Role:` line.
4. Add the workflow to `core/workflows/README.md`.
5. Run `python3 core/scripts/validate-workflows.py` — must pass.

---

## Adding a New Contract (JSON Schema)

1. Create `core/contracts/schemas/<contract-name>.json` using JSON Schema draft 2020-12.
2. Add a row to the contracts table in `core/contracts/README.md`.
3. Reference the contract in the relevant skill's `## Output Schema` or role's `## Outputs Produced`.
4. Run `python3 core/scripts/validate-contracts.py` — must pass.

---

## Adding a New Overlay

1. Create `overlays/<overlay-name>/README.md` — include `status`, `tech stack`, what it adds, and dependency on other overlays or `core`.
2. Add rules under `overlays/<overlay-name>/rules/`.
3. Add overlay-specific skills under `overlays/<overlay-name>/skills/` (same SKILL.md format).
4. Add the overlay to `overlays/README.md` under the correct group (Stack / Project / Content & Domain).
5. If a new pack uses it, create `packs/<pack-name>/manifest.yaml` and add it to `packs/README.md`.
6. Run `python3 core/scripts/validate-skills.py` and `validate-packs.py`.

---

## Adding Golden Prompt Cases

1. Create a directory: `core/prompts/golden/<prompt-asset-id>/`
2. Add `manifest.yaml`:

```yaml
prompt_id: <prompt-asset-id>
version: "1.0.0"
role: <role-slug>
min_pass_rate: 0.9
cases_dir: cases/
```

3. Add at least **10 case pairs** under `cases/`:
   - `NNN-input.json` — input context
   - `NNN-expected.json` — rubric with `must_include` and `must_not_include` arrays
4. Never include secrets or production customer data in cases.
5. Use rubric-based expected output — not brittle exact-string match.
6. Add the asset to the table in `core/prompts/README.md`.

---

## Releasing a New Version

The pack uses semantic versioning. Bump the version when a set of changes is ready to publish:

- **MAJOR** — breaking changes to contracts, role/skill structure, or validator expectations.
- **MINOR** — new skills, roles, or workflows; broad standards refreshes; additive capability.
- **PATCH** — fixes, wording, and defect cleanup with no new capability.

When releasing:

1. Update `VERSION` (single source of the number).
2. Add a dated section to `CHANGELOG.md` (`## [X.Y.Z] - YYYY-MM-DD`) with `Added` / `Changed` / `Fixed` groups. Describe product/content changes only — no internal process metadata per `core/rules/code.md`.
3. Sync the version-carrying docs so they match `VERSION`: `README.md` (version summary line), `AGENTS.md` (A2A section header), `CLAUDE.md` (Pack version line), `.cursorrules` (A2A section header), `USER_GUIDE_v2.md` (intro), and `core/codex/.a2a-config.json` (`pack_version`).
4. Run `python3 core/scripts/validate-all.py` — must pass before the release is considered done.
5. Do not create a commit, tag, or release until the user explicitly confirms.

## Rules for All Contributions

- do not touch `.env`, `.dev.vars`, or credential files
- do not weaken any parity group defined in `core/adapter-parity.md`
- do not add repo-specific paths, brand content, or org-local conventions to `core/` — use overlays
- adapter files mirror `core/rules/code.md` — when rules change, update every adapter enforced by `core/scripts/validate-rules.py` and listed in `core/adapter-parity.md` (currently `.cursorrules`, `.cursor/rules/agent-skills.md`, `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, `.kiro/steering/agent-skills.md`, `.kilocode/rules/agent-skills.md`). Codex/Windsurf/VS Code Copilot read `AGENTS.md` directly.
- run `validate-all.py` before considering any change complete
- do not create a commit until explicitly confirmed per `core/rules/code.md`
