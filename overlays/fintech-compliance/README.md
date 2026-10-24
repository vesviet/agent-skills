# Fintech Compliance Overlay

Composable overlay for the `data-analyst` and financial risk modeling roles when developing regulatory-grade retail credit scorecards, probability of default (PD) engines, and financial compliance audits.

This overlay codifies Basel II/III Internal Ratings-Based (IRB) standards, Fair Lending explainability requirements, monotonic Weight of Evidence (WOE) transformations, Information Value (IV) variable filtering, Points to Double Odds (PDO) scorecard calibration, and Population Stability Index (PSI) drift monitoring.

## Scope

- Binary default target modeling and credit risk feature engineering
- Strictly monotonic Weight of Evidence (WOE) continuous and categorical binning
- Information Value (IV) predictive power screening ($0.02 \le \text{IV} \le 0.50$)
- Logistic regression scorecard scaling with Points to Double Odds (PDO) calibration
- Population Stability Index (PSI) and Characteristic Stability Index (CSI) drift detection
- Model explainability, adverse action code generation, and Basel governance compliance

## Included

- `rules/credit-scorecard-rules.md` — Regulatory rules for monotonic WOE binning, IV thresholds, PDO scaling, and PSI drift
- `skills/build-credit-scorecard/SKILL.md` — Regulatory credit risk scorecard modeling and calibration skill

## Activation

```
Role: data-analyst
Overlay: overlays/fintech-compliance
```

Compose with `overlays/data-analyst-stack` when executing SQL/DuckDB feature extraction or Metabase risk monitoring dashboards.

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

Last updated: 2026-10-15
