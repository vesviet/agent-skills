# Golden Prompt Evaluation Fixtures (PromptOps Standard 2026/2027)

This directory houses curated, versioned evaluation datasets (**Golden Fixtures**) used to benchmark, validate, and gate the promotion of prompt assets in the `agent-skills` pack.

---

## 1. Directory Structure

```
golden/
  README.md
  <prompt-asset-id>/
    manifest.yaml      # Asset metadata, governance thresholds, contract references
    cases/
      001-input.json   # Test scenario: role, request, inputs, context
      001-expected.json # Evaluation rubric: required tokens, forbidden tokens, schema validation
      ...
      010-input.json
      010-expected.json
```

---

## 2. Manifest Specification (`manifest.yaml`)

Each prompt asset must provide a valid `manifest.yaml` adhering to the late-2026 Agent Skills Specification:

```yaml
schema_version: "2026.1"
prompt_id: a2a-coordination
name: "Agent-to-Agent (A2A) Coordination & Delegation Lifecycle"
domain: a2a
role: agent-coordinator
target_role: agent-coordinator
skill: agent-a2a-protocol
target_skill: agent-a2a-protocol
version: "1.0.0"
description: >
  Evaluates whether the agent-coordinator properly orchestrates multi-agent tasks
  under the A2A 1.0 protocol with strict schema contracts and DAG phasing.
min_pass_rate: 0.95
governance:
  min_pass_rate: 0.95
  contract_schema: core/contracts/schemas/coordination-plan.json
cases_dir: cases/
```

### Required Fields:
- `prompt_id`: Kebab-case identifier matching the directory name.
- `version`: Semantic version string (`1.0.0`).
- `role` or `target_role`: Canonical role slug declared in `core/roles/`.
- `skill` or `target_skill`: Canonical skill slug declared in `core/skills/`.
- `min_pass_rate`: Float between `0.0` and `1.0` (typically `0.90` or `0.95`).
- `cases_dir`: Relative path to test cases directory (must be `cases/`).

---

## 3. Test Case Specification

Every test case consists of a strictly paired `NNN-input.json` and `NNN-expected.json`:

### A. Input Fixture (`NNN-input.json`)
```json
{
  "case_id": "A2A-001",
  "name": "Multi-Agent DAG Task Decomposition for Full-Stack Feature Delivery",
  "work_type": "coordination",
  "role": "agent-coordinator",
  "skill": "agent-a2a-protocol",
  "user_request": "Coordinate end-to-end implementation of multi-factor authentication.",
  "target": "tasks/user-authentication-flow",
  "context": {
    "roles_involved": ["backend-developer", "frontend-developer", "qa-engineer"],
    "protocol": "A2A 1.0 DAG coordination"
  }
}
```

### B. Expected Rubric (`NNN-expected.json`)
```json
{
  "must_include": [
    "coordination-plan",
    "phases",
    "backend-developer",
    "frontend-developer",
    "qa-engineer",
    "DAG"
  ],
  "must_not_include": [
    "single monolithic agent",
    "execute all roles unilaterally"
  ],
  "required_tokens": [
    "coordination-plan",
    "phases",
    "backend-developer",
    "frontend-developer",
    "qa-engineer",
    "DAG"
  ],
  "forbidden_tokens": [
    "single monolithic agent",
    "execute all roles unilaterally"
  ],
  "schema_validation": {
    "enabled": true,
    "schema_ref": "core/contracts/schemas/coordination-plan.json",
    "contract_type": "coordination-plan"
  }
}
```

---

## 4. Promoted Datasets Index (58 Total Cases)

| Asset ID | Target Role | Target Skill | Output Contract | Min Pass Rate | Cases |
|----------|-------------|--------------|-----------------|---------------|-------|
| [`a2a-coordination`](a2a-coordination/manifest.yaml) | `agent-coordinator` | `agent-a2a-protocol` | `coordination-plan.json` | 95% | 10 |
| [`agent-coordinator-phase-gate`](agent-coordinator-phase-gate/manifest.yaml) | `agent-coordinator` | `agent-a2a-protocol` | `coordination-plan.json` | 90% | 18 |
| [`security-audit`](security-audit/manifest.yaml) | `security-engineer` | `security-audit` | `security-audit.json` | 95% | 10 |
| [`payment-integration`](payment-integration/manifest.yaml) | `ecommerce-engineer` | `integrate-payment-gateway` | `api-contract-spec.json` | 95% | 10 |
| [`code-refactoring`](code-refactoring/manifest.yaml) | `technical-lead` | `review-code` | `implementation-result.json` | 90% | 10 |

---

## 5. Authoring Rules & Quality Standards

1. **Volume Minimum**: Each promoted prompt asset must maintain $\ge 10$ test case pairs.
2. **Data Hygiene**: Never include secrets, API tokens, passwords, or customer PII in input or expected fixtures.
3. **Rubric-Based Assertions**: Use token assertions and schema validations rather than brittle exact-string matching to accommodate natural language variance across LLMs.
4. **Adversarial & Edge Cases**: Include adversarial prompts that test guardrails (e.g. prompt injection, unauthorized privilege escalation, out-of-scope requests).
5. **Contract Enforcement**: Enable `schema_validation` whenever the evaluated skill produces a structured handoff contract.

---

## 6. Verification Command

Run the automated evaluation validator:

```bash
python3 core/scripts/validate-golden-evals.py
```

---

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-09-10
