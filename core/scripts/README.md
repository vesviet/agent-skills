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

Generate A2A registry after role edits:

```bash
python3 core/scripts/generate-a2a-registry.py
```

Run them from the repository root or by using the paths directly under `core/scripts/`.
