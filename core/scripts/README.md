# Validation Scripts

These scripts validate the **core** pack structure and references.

Available validators:

- `validate-rules.py`
- `validate-skills.py`
- `validate-roles.py`
- `validate-workflows.py`
- `validate-all.py`

The rules validator also checks root adapter parity against [adapter-parity.md](../adapter-parity.md).

Additional validators (included in `validate-all.py`):

- `validate-2026-compliance.py` — A2A coverage, coordinator wiring, policies in tool orchestration
- `validate-a2a-compliance.py` — full A2A 1.0 + Antigravity artifacts
- `validate-agent-cards.py` — generated registry vs `agent-card.json`
- `validate-contracts.py` — JSON schema metadata and bundled example required-field/discriminator checks
- `validate-standardization.py` — >=90% pack standardization gate
- `validate-version-sync.py` — `VERSION` vs the A2A registry, all agent cards, adapter templates, and the newest CHANGELOG entry
- `validate-indexes.py` — every skill, schema, role, workflow, overlay, and pack is listed in its index, and the declared counts match disk
- `validate-policy-consistency.py` — `action-boundaries.yaml` vs role files: no verb in two tiers, no irreversible action pre-authorized, every role can create its own outputs, tool-map actions all classified
- `validate-skill-ownership.py` — every skill has a Primary owner, no Primary/Supporting conflict, no Primary skill contradicted by the role's own boundaries, workflow steps resolve to their tagged role's toolbox

### Which validator catches which drift

| Symptom | Validator |
| ------- | --------- |
| `VERSION` bumped but registry/cards not regenerated | `validate-version-sync.py` |
| New skill or schema added but index count still old | `validate-indexes.py` |
| Policy profile copy-pasted between roles with wrong tiers | `validate-policy-consistency.py` |
| Role granted a Primary skill its boundaries forbid | `validate-skill-ownership.py` |
| Workflow step names a skill nobody on that step can run | `validate-skill-ownership.py` |

Generate A2A registry after role edits:

```bash
python3 core/scripts/generate-a2a-registry.py
```

Run them from the repository root or by using the paths directly under `core/scripts/`.
