# Golden Prompt Datasets (PromptOps)

Store versioned prompt evaluation fixtures here. Used with `agent-prompt-lifecycle` skill.

## Layout

```
golden/
  README.md
  <prompt-asset-id>/
    manifest.yaml      # version, role, skill, eval threshold
    cases/
      001-input.json   # input context
      001-expected.json # expected behavior rubric (not exact match)
```

## Rules

- minimum 10 cases per actively promoted prompt asset
- never store secrets or production customer data in cases
- rubric-based expected output — not brittle exact-string match unless stable
- run eval before promoting prompt changes (see agent-prompt-lifecycle checklist)

## Promoted Datasets

| Asset ID | Role | Skill | Contract | Min Pass Rate | Cases |
|----------|------|-------|----------|---------------|-------|
| [agent-coordinator-phase-gate](agent-coordinator-phase-gate/manifest.yaml) | `agent-coordinator` | `agent-a2a-protocol` | `coordination-plan.json` | 90% | 18 |
| [security-audit](security-audit/manifest.yaml) | `security-engineer` | `security-audit` | `security-audit.json` | 95% | 10 |
| [payment-integration](payment-integration/manifest.yaml) | `ecommerce-engineer` | `integrate-payment-gateway` | `api-contract-spec.json` | 95% | 10 |
| [code-refactoring](code-refactoring/manifest.yaml) | `technical-lead` | `review-code` | `implementation-result.json` | 90% | 10 |
| [a2a-coordination](a2a-coordination/manifest.yaml) | `agent-coordinator` | `agent-a2a-protocol` | `coordination-plan.json` | 95% | 10 |

## Example manifest.yaml

```yaml
prompt_id: agent-coordinator-phase-gate
version: "1.0.0"
role: agent-coordinator
min_pass_rate: 0.9
cases_dir: cases/
```
