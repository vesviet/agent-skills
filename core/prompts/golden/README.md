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

## Example manifest.yaml

```yaml
prompt_id: agent-coordinator-phase-gate
version: "1.0.0"
role: agent-coordinator
min_pass_rate: 0.9
cases_dir: cases/
```
