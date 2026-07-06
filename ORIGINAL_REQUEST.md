# Original User Request

## Initial Request — 2026-07-06T14:01:50Z

# Teamwork Project Prompt

Audit all skills in the `agent-skills` repository (`core/skills/`) case by case to ensure quality and compliance. Check that each skill follows the standard format (e.g., contains a valid `SKILL.md`) and adheres to core rules. Produce a detailed Markdown report summarizing the findings.

Working directory: D:\myproject\agent-skills\audit
Integrity mode: benchmark

## Requirements

### R1. Complete Skill Coverage
The team must inspect every skill subdirectory within `D:\myproject\agent-skills\core\skills\`.

### R2. Compliance Audit
For each skill, evaluate whether it contains a properly formatted `SKILL.md` file (including YAML frontmatter with "name" and "description") and adheres to the baseline rules in `core/rules/code.md`.

### R3. Output Report
Generate a detailed Markdown report (`audit_report.md`) that documents the audit results for each skill, clearly highlighting any missing files, formatting errors, or rule violations.

### R4. Verification Script
Write a Python verification script (`verify_audit.py`) that lists all skill directories in `core/skills/` and asserts that every single one is explicitly mentioned and analyzed in `audit_report.md`.

## Acceptance Criteria

### Audit Verification
- [ ] `verify_audit.py` successfully runs and passes, confirming 100% coverage of all skills.
- [ ] `audit_report.md` contains specific pass/fail details for each audited skill.

## Follow-up — 2026-07-06T14:04:00Z

# Teamwork Project Prompt — Roles Audit

Audit all roles in the `agent-skills` repository (`core/roles/`) case by case to ensure they adhere to standard conventions, provide clear responsibilities, and reference valid skills.

Working directory: D:\myproject\agent-skills\audit
Integrity mode: benchmark

## Requirements

### R1. Complete Role Coverage
The team must inspect every role definition file (Markdown) within `D:\myproject\agent-skills\core\roles\`.

### R2. Compliance & Content Audit
For each role, verify compliance with `role-standard.md` by ensuring mandatory sections like "Skill Toolbox" and "Boundary Lock" are present. Also, review the clarity and completeness of the role descriptions and responsibilities.

### R3. Skill Cross-referencing
Ensure that all skills mentioned in a role's "Skill Toolbox" actually exist in the `core/skills/` directory structure. Flag any missing or hallucinated skills.

### R4. Output Report
Generate a detailed Markdown report (`roles_audit_report.md`) that documents the audit results for each role, clearly highlighting any missing sections, broken skill references, or quality issues.

### R5. Verification Script
Write a Python verification script (`verify_roles_audit.py`) that lists all Markdown files in `core/roles/` (excluding `README.md` if appropriate) and asserts that every single role is explicitly mentioned and analyzed in `roles_audit_report.md`.

## Acceptance Criteria

### Audit Verification
- [ ] `verify_roles_audit.py` successfully runs and passes, confirming 100% coverage of all roles.
- [ ] `roles_audit_report.md` contains specific findings (compliance, content quality, and cross-referencing results) for each audited role.
