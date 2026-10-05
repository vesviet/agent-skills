# Contributing to Agent Skills

This guide defines the contribution standards and verification protocols for the `agent-skills` engineering pack.

The pack operates at SOTA 2026–2027 standards with **35 Roles**, **138 Skills** (126 portable core + 12 overlays across 19 categories), **25 Workflows**, **54 JSON Contract Schemas**, **19 Dedicated Review Checklists** (in `core/roles/references/`), **15 Packs**, **18 Overlays**, and **17 Core Pack Validators**. It is engineered for autonomous multi-agent swarms, native A2A 1.0 (JSON-RPC 2.0 / SSE) orchestration, and runtime adapters including Google Antigravity (AGY).

Every component has a strict structural standard, non-negotiable architectural guardrail locks, and automated validators. **Changes are not complete until all 17 core validators pass and dual indexes are synchronized with zero drift.**

---

## Quick Reference Matrix

| Component / Target | Authoring Standard & Location | Primary Validator | Key Invariants & Constraints |
|---|---|---|---|
| **Skill (Core)** | `core/skills/README.md` → Skill Authoring Standard | `validate-skills.py` | Strictly `< 200 lines`, `allowed-tools` present, `agents/openai.yaml` manifest, primary role lock |
| **Skill (Overlay)** | `overlays/README.md` → Overlay Authoring Rules | `validate-skills.py` | Isolated under `overlays/<name>/skills/`, mapped in `OVERLAY_SKILL_ROLES` |
| **Role** | `core/roles/role-standard.md` & `core/roles/README.md` | `validate-roles.py` & `validate-2026-compliance.py` | 19 mandatory sections, 4+ `*-LOCK` architectural guardrails, dedicated checklist in `core/roles/references/` |
| **Workflow** | `core/workflows/README.md` → Workflow Authoring Standard | `validate-workflows.py` | Step `Role:` tags match skill ownership, required sections, valid markdown |
| **Contract (Schema)** | `core/contracts/README.md` → When To Create A Schema | `validate-contracts.py` & `validate-contract-coverage.py` | JSON Schema draft 2020-12, bundled validation examples, A2A 1.0 Part compatibility |
| **Pack** | `packs/README.md` → Pack Authoring Rules | `validate-packs.py` | Valid `manifest.yaml`, overlay dependencies, portable skill lists |
| **Overlay** | `overlays/README.md` → Overlay Authoring Rules | `validate-overlays.py` | `README.md` with tech stack, isolated `rules/` and `skills/`, no core pollution |
| **Policy / Boundaries** | `core/policies/action-boundaries.yaml` | `validate-policy-consistency.py` | Zero pre-authorized irreversible actions, complete 35-role classification, tool mapping |
| **A2A / Agent Cards** | `core/a2a/registry/` & `.well-known/` | `validate-a2a-compliance.py` & `validate-agent-cards.py` | A2A 1.0 protocol conformance, agent cards matching role files |
| **Golden Prompt Evals** | `core/prompts/README.md` | `validate-golden-evals.py` | Valid `manifest.yaml`, $\ge 10$ case pairs (`cases/`), rubric-based expected outputs |
| **Platform Challenge** | `tests/test_*_platform_challenge.py` | `python -m unittest tests/test_<name>.py` | Empirical verification of SOTA 2026–2027 invariants, locks, and DoD |

Run all 17 core validators and check index synchronization:

```bash
# Run all 17 core pack validators
python core/scripts/validate-all.py

# Check index synchronization across INDEX.md and role-skill indices
python core/scripts/generate-index.py --check
```

---

## Adding a New Skill

Skills represent reusable, modular agent capabilities complying with the [Agent Skills open specification](https://agentskills.io/specification).

### 1. File Placement & Line Budget

- **Core portable skills**: place in `core/skills/<category>/<skill-name>/`
  - Active categories (19 total): `agent`, `ai`, `foundation`, `meetings-analysis`, `repo-ops`, `content`, `seo`, `mmo`, `backend`, `frontend`, `platform`, `security-data`, `documentation`, `education`, `ecommerce`, `legal`, `accounting`, `data`, `architecture`.
- **Overlay skills**: place in `overlays/<overlay-name>/skills/<skill-name>/` for stack- or repo-specific capabilities.
- **Strict Size Constraint**: `SKILL.md` must be **strictly under 200 lines** (enforced by `validate-skills.py`, rejected if $\ge 200$). Detailed technical manuals or checklists belong in `references/`.

### 2. Manifest Structure (`SKILL.md`)

```markdown
---
name: skill-name
description: What the skill does and when to use it. Use when <trigger condition 1> or use for <trigger condition 2>.
allowed-tools:
  - run_command
  - view_file
  - replace_file_content
---

# Skill Name In Title Case

Use this skill when...

## Core Rules

- Non-negotiable constraint 1 (fail-safe posture, minimal footprint)
- Non-negotiable constraint 2 (OWASP AST10 / ASI alignment)

## Suggested Process

### 1. Step Name
Step-by-step actionable execution instructions...

### 2. Verification Step
Validate outputs against expected invariants...

## Checklist

- [ ] Actionable completion check 1
- [ ] Actionable completion check 2
- [ ] Actionable completion check 3
- [ ] Actionable completion check 4
- [ ] Actionable completion check 5

## Related Skills

- **other-skill-name**: One-line description of how and when to coordinate.
```

### 3. Frontmatter Requirements

- `name`: Lowercase letters, numbers, and hyphens (max 64 chars, regex `^[a-z0-9-]{1,64}$`). No leading/trailing hyphens, no consecutive hyphens (`--`), no XML tags, no reserved words (`anthropic`, `claude`). Must match directory name.
- `description`: Must be third-person, max 1024 chars, no XML tags. Must contain trigger phrasing: `"Use when "` or `"Use for "`.
- `allowed-tools`: Non-empty list of tools registered in `core/policies/mcp-tool-map.yaml`. Every tool must be permitted by `core/policies/action-boundaries.yaml` for the owning role.

### 4. Required Body Sections

1. `# Title`: Exactly one H1 matching the skill name in title case (do not end with `' Skill'`).
2. Introductory Paragraph: Short "Use this skill when..." trigger definition.
3. `## Core Rules`: Non-negotiable constraints, failure modes, security requirements.
4. `## Suggested Process`: Phased, actionable execution instructions.
5. `## Checklist`: **At least 5 actionable completion items** (`- [ ]`).
6. `## Related Skills`: Related skills using format `- **<skill-name>**: <description>`.
7. Optional Canonical Headings: `## Output Contracts` (for JSON schemas), `## Deliverable Decision`.

### 5. Companion Interface Manifest (`agents/openai.yaml`)

Every skill must provide an interface manifest at `<skill-dir>/agents/openai.yaml`:

```yaml
interface:
  display_name: "Skill Name In Title Case"
  short_description: "Concise summary of skill capabilities and triggers."
  default_prompt: "Use $skill-name to execute <task> in this codebase."
```

### 6. Deep Technical Guides (`references/`)

When technical documentation, code snippets, or framework guides exceed the 200-line budget:
- Create `<skill-dir>/references/<guide-name>.md`.
- Link relatively from `SKILL.md` (e.g., `See [references/production-guide.md](references/production-guide.md) for cluster topology.`).
- Keep `SKILL.md` focused on trigger conditions, core rules, process, and checklist.

### 7. Primary Ownership & Catalog Registration

- Assign the skill as a **Primary Skill** in exactly one owning role (`core/roles/<role>.md` -> `### Primary Skills`).
- May be listed as **Supporting Skill** in other collaborating roles. Never list a skill as both Primary and Supporting in the same role.
- Add the skill to `core/skills/README.md` under the correct taxonomy section and update count.
- Run index synchronization:
  ```bash
  python core/scripts/generate-index.py
  python core/scripts/validate-skills.py
  python core/scripts/validate-skill-ownership.py
  python core/scripts/validate-indexes.py
  ```

---

## Adding a New Role

Roles represent principal-level software delivery personas. Every role must comply with `core/roles/role-standard.md`.

### 1. Mandatory 19-Section Structure

Create `core/roles/<role-name>.md` following the exact 19 sections:

```markdown
# Role Name

Mission: One sentence declaring the principal mission and outcome ownership.
Level: Principal (or Master-Practitioner)

See [role-standard.md](role-standard.md) for mandatory operating standards.

## Principal Expectations
## Use This Role When
## Core Responsibilities
## Inputs Required
## Outputs Produced
## Deliverable Routing
## Decision Boundaries
## Role Boundaries
## Collaboration
## Guardrails
## Skill Toolbox
## Output Template
## Review Checklist
## Anti-Patterns To Reject
## Role Handoff
## Definition Of Done
```

*(Optional `## Optional Overlays` may follow before the trailing footer: `Last updated: YYYY-MM-DD`).*

### 2. Architectural Guardrail Locks (`*-LOCK`)

Every Tier 1 SOTA role must declare explicit, domain-specific architectural locks in `## Guardrails` alongside the universal locks (`BOUNDARY-LOCK`, `MINIMAL-FOOTPRINT-LOCK`, `IRREVERSIBLE-ACTION-LOCK`, etc.).
- Example: `ai-systems-engineer` declares `VLLM-CACHE-LOCK`, `GPU-DRA-LOCK`, `SLM-DISTILLATION-LOCK`, `AI-GOVERNANCE-LOCK`.
- Example: `aws-engineer` declares `OPENTOFU-KMS-LOCK`, `CROSSPLANE-COMPOSITION-LOCK`, `BOTTLEROCKET-LOCK`, `AWS-IAM-ZERO-TRUST-LOCK`.
- Example: `sre` declares `ERROR-BUDGET-LOCK`, `POSTMORTEM-LOCK`, `RUNBOOK-LOCK`, `CHAOS-EXPERIMENT-LOCK`.

### 3. Dedicated Review Checklist (`references/`)

Every role must be paired with an authoritative review checklist in `core/roles/references/<role-name>-review-checklist.md`:
- Must contain comprehensive pre-flight, architectural, implementation, security, and handoff verification gates.
- Link to it from the role's `## Review Checklist` section.

### 4. Policy Profile & Action Boundaries

Register the role in `core/policies/action-boundaries.yaml`:
- Define `allowed:`, `requires_approval:`, and `denied:`.
- **Irreversible Actions Invariant**: Actions in `NEVER_ALLOWED` (`apply_iac`, `drop_database`, `modify_secrets`, `push_to_production`, `rotate_agent_credentials`, `terminate_instance`, etc.) must **never** be under `allowed`.
- Classify `delegate_task` and deny `bypass_ai_guardrail`.

### 5. Registry Generation & Parity

Regenerate agent cards and synchronized indices:
```bash
python core/scripts/generate-a2a-registry.py
python core/scripts/generate-index.py
```
This generates `core/a2a/registry/<role-name>.json` and maintains **100% SHA-256 bitwise parity** between `core/a2a/.well-known/role-skill-index.json` and `adapters/antigravity/role-skill-index.json`.

### 6. Role Challenge Test Suite

Author an empirical challenge test suite in `tests/test_<role_name>_platform_challenge.py`:
- Test role file structure, section completeness, and link resolution.
- Test that all architectural guardrail locks (`*-LOCK`) are present and enforced.
- Test policy profile consistency in `action-boundaries.yaml`.
- Test primary and supporting skill ownership.
- Test review checklist completeness.

---

## Adding a New Workflow

Workflows define end-to-end multi-step procedures orchestrated across roles and skills.

### 1. File Structure (`core/workflows/<workflow-name>.md`)

```markdown
---
description: Concise one-line description of the workflow purpose and outcome.
---

## Workflow Name Workflow

### Prerequisites

- Pre-condition or input artifact 1
- Pre-condition or input artifact 2

### Workflow Steps

#### 1. Phase Name
Role: **Role Name**
Execute phase actions using designated skills...

#### 2. Next Phase Name
Role: **Collaborating Role Name**
Execute downstream actions...

### Checklist

- [ ] Actionable workflow checkpoint 1
- [ ] Actionable workflow checkpoint 2

### Related Workflows

- `/related-workflow-slug`

### Related Skills

- `skill-name`
```

### 2. Skill Ownership Invariant

Every step's `Role: **<Role Name>**` MUST own the skills called in that step within its Primary or Supporting toolbox. `validate-skill-ownership.py` statically enforces this invariant across all workflows.

### 3. Registration & Validation

- Add the workflow to `core/workflows/README.md` and `README.md`.
- Run index generator and validator:
  ```bash
  python core/scripts/generate-index.py
  python core/scripts/validate-workflows.py
  python core/scripts/validate-skill-ownership.py
  ```

---

## Adding a New Contract (JSON Schema)

Contracts enforce structured data exchange between agents, subagents, and tools.

1. **Schema Location & Standard**: Create `core/contracts/schemas/<contract-name>.json` using **JSON Schema Draft 2020-12**.
2. **A2A 1.0 Part Compatibility**: If defining payload structures for agent messaging, follow A2A 1.0 unified Part contracts (discriminator by member: `text`, `file`, `data`; never use legacy `kind`).
3. **Bundled Examples**: Include valid examples under `examples:` in the schema for automated validator checks.
4. **Registration**: Add a row to the contracts table in `core/contracts/README.md`.
5. **Role & Skill Wiring**:
   - Reference in owning role's `## Outputs Produced` as `contracts/schemas/<contract-name>.json` (logical identifier).
   - Reference in emitting skill's `## Output Contracts`.
6. **Validation**:
   ```bash
   python core/scripts/generate-index.py
   python core/scripts/validate-contracts.py
   python core/scripts/validate-contract-coverage.py
   ```

---

## Adding a New Overlay or Pack

### Overlays (`overlays/<overlay-name>/`)

Overlays inject tech-stack or repository-specific capabilities without polluting the core portable pack.
1. Create `overlays/<overlay-name>/README.md` detailing status, tech stack, and dependencies.
2. Add stack-specific rules under `overlays/<overlay-name>/rules/`.
3. Add overlay-specific skills under `overlays/<overlay-name>/skills/<skill-name>/SKILL.md`.
4. Register overlay in `overlays/README.md` and add skill mappings to `OVERLAY_SKILL_ROLES` in `core/scripts/validate-skills.py`.
5. Run `python core/scripts/validate-overlays.py` and `python core/scripts/validate-skills.py`.

### Packs (`packs/<pack-name>/`)

Packs assemble roles, skills, overlays, and workflows into installable configurations.
1. Create `packs/<pack-name>/manifest.yaml`.
2. Register pack in `packs/README.md` and `README.md`.
3. Run `python core/scripts/validate-packs.py`.

---

## Adding Golden Prompt Cases

Golden prompt evaluations ensure agent instructions produce deterministic, high-quality outputs.

1. Create directory `core/prompts/golden/<prompt-asset-id>/`.
2. Create `manifest.yaml`:
   ```yaml
   prompt_id: <prompt-asset-id>
   version: "1.0.0"
   role: <role-slug>
   min_pass_rate: 0.9
   cases_dir: cases/
   ```
3. Add **at least 10 case pairs** under `cases/`:
   - `NNN-input.json`: Input context and parameters.
   - `NNN-expected.json`: Rubric-based assertions with `must_include` and `must_not_include` arrays. Never use brittle exact-string matching.
4. **Zero Secrets**: Never include real credentials, API tokens, or production PII in test cases.
5. Register in `core/prompts/README.md` and validate:
   ```bash
   python core/scripts/validate-golden-evals.py
   ```

---

## The 17 Core Pack Validators

All changes are validated by the centralized test runner `core/scripts/validate-all.py`:

```bash
python core/scripts/validate-all.py [--parallel] [--fail-fast] [--format text|json|sarif]
```

| # | Validator Script | Scope & Rules Enforced |
|---|---|---|
| 1 | `validate-rules.py` | Enforces parity across all 7+ adapter files (`.cursorrules`, `CLAUDE.md`, `AGENTS.md`, Copilot, Kiro, KiloCode) and checks meta-rules. |
| 2 | `validate-skills.py` | Enforces `< 200 lines`, `allowed-tools` correctness, trigger phrases, checklist $\ge 5$ items, and no broken refs. |
| 3 | `validate-roles.py` | Enforces 19 mandatory sections, section order, minimum depth, primary/supporting skills, and handoffs. |
| 4 | `validate-workflows.py` | Enforces step roles, prerequisites, checklists, and valid markdown structure across all 25 workflows. |
| 5 | `validate-packs.py` | Enforces pack manifest integrity, overlays, and skill lists across all 15 packs. |
| 6 | `validate-overlays.py` | Enforces overlay README, rules, skills, and dependencies across all 18 overlays. |
| 7 | `validate-2026-compliance.py` | Enforces A2A/contract coverage, coordinator wiring, full policy coverage, and graph orchestration. |
| 8 | `validate-contracts.py` | Validates all 54 JSON schemas against Draft 2020-12 and tests bundled examples. |
| 9 | `validate-a2a-compliance.py` | Enforces A2A 1.0 JSON-RPC 2.0 / SSE compliance and Antigravity adapter alignment. |
| 10 | `validate-agent-cards.py` | Validates agent cards in `core/a2a/registry/` and `.well-known/agent-registry.json`. |
| 11 | `validate-standardization.py` | Validates $\ge 90\%$ standardization target, adapter mentions, and orphan agent skills check. |
| 12 | `validate-version-sync.py` | Validates consistent semantic version across 7 authoritative repository files. |
| 13 | `validate-indexes.py` | Validates exact count parity between disk and documentation for roles, skills, workflows, schemas, and packs. |
| 14 | `validate-policy-consistency.py` | Validates `action-boundaries.yaml` against role files, MCP tool map, and irreversible-action gates. |
| 15 | `validate-skill-ownership.py` | Validates exactly one Primary owner per core skill, zero duplicate ownership, and workflow step role resolution. |
| 16 | `validate-contract-coverage.py` | Validates that all contracts emitted by roles or skills exist and match schema definitions. |
| 17 | `validate-golden-evals.py` | Validates golden prompt test cases, manifests, and rubric definitions across all prompt assets. |

---

## Releasing a New Version

The pack follows Semantic Versioning (SemVer):
- **MAJOR** — breaking changes to contracts, role/skill interfaces, or validator invariants.
- **MINOR** — new roles, skills, workflows, or standards refreshes (e.g. SOTA modernization sprints).
- **PATCH** — bug fixes, typo corrections, and minor doc refinements.

### Release Checklist

1. Update `VERSION` (the single source of truth for the release number).
2. Update `CHANGELOG.md` under `## [X.Y.Z] - YYYY-MM-DD` with `Added`, `Changed`, and `Fixed` sections. Describe product/engineering improvements only; never include internal process metadata per `core/rules/code.md`.
3. Synchronize the 7 version-carrying files checked by `validate-version-sync.py`:
   - `VERSION`
   - `README.md` (version summary line)
   - `AGENTS.md` (A2A section header)
   - `CLAUDE.md` (Pack version line)
   - `.cursorrules` (A2A section header)
   - `USER_GUIDE_v2.md` (intro text)
   - `core/codex/.a2a-config.json` (`pack_version`)
4. Regenerate registry and indexes:
   ```bash
   python core/scripts/generate-a2a-registry.py
   python core/scripts/generate-index.py
   ```
5. Run full test verification:
   ```bash
   python core/scripts/validate-all.py
   python core/scripts/generate-index.py --check
   python -m unittest discover -s tests -p "test_*.py"
   ```
6. **Commit Gate**: Do not create a git commit, git tag, or push without explicit user approval.

---

## Rules for All Contributions

- **META-RULE (`core/rules/code.md`)**: Never execute `git commit` or `git push` without explicit user instruction.
- **Zero Credentials & Secrets**: Never create or modify `.env`, `.dev.vars`, or commit private keys, credentials, or API tokens.
- **No Core Pollution**: Keep `core/` strictly repo-agnostic and portable. Place stack-specific, domain-specific, or proprietary logic in `overlays/`.
- **Bitwise Index Parity**: Maintain 100% SHA-256 bitwise parity between `core/a2a/.well-known/role-skill-index.json` and `adapters/antigravity/role-skill-index.json`.
- **Adapter Parity**: When updating core agent operating rules, mirror changes across all adapter files enforced by `validate-rules.py` (`.cursorrules`, `.cursor/rules/agent-skills.md`, `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, `.kiro/steering/agent-skills.md`, `.kilocode/rules/agent-skills.md`).
- **OWASP ASI & AST10 Alignment**: All roles and skills must adhere to the OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10) and OWASP Agentic Skills Top 10 (AST10).

---

## Standard 2026–2027 Alignment

This file is part of the `agent-skills` engineering pack. It governs contribution, validation, and release standards across all supported agent platforms.

- **OWASP ASI**: Applied as described in `core/roles/role-standard.md` (ASI01–ASI10) and per-skill `## Core Rules`.
- **OWASP AST10**: Applied to all skill manifests (`SKILL.md`) including tool scoping, sandboxing, and provenance verification.
- **Failure Modes**: Every contribution must account for failure modes, drift, and unexpected downstream dependencies.
- **Output Contracts**: Structured artifacts produced must conform to JSON schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: Role boundaries are enforced by `core/scripts/validate-skill-ownership.py` and `action-boundaries.yaml`.
- **Commit / Publish Gate**: Follows the META-RULE in `core/rules/code.md` — no commit, no push, no publish without explicit user confirmation.

Last updated: 2026-10-05
