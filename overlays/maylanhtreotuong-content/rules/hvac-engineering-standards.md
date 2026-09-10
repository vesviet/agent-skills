# HVAC Engineering & Empirical Testing Standards

This rule establishes technical integrity, measurement protocols, and thermodynamic standards for all air conditioning analysis published on `maylanhtreotuong`.

## 1. Energy Efficiency & CSPF Standards (TCVN 7830:2021)

All efficiency claims must align with National Standard **TCVN 7830:2021** (Air conditioners — Energy efficiency):
- **CSPF (Cooling Seasonal Performance Factor)**:
  $$\text{CSPF} = \frac{\text{CSTL}}{\text{CSEC}}$$
  - $\text{CSTL}$ (Cooling Seasonal Total Load): Total cooling load over 1,800 operating hours under standard Vietnam climate conditions (kWh).
  - $\text{CSEC}$ (Cooling Seasonal Energy Consumption): Total electrical energy consumed across the season (kWh).
- **5-Star Efficiency Tiers (Ministry of Industry and Trade - MOIT)**:
  - Minimum 5-star baseline: $\text{CSPF} \ge 4.20$.
  - Mid-range Inverter: $5.00 \le \text{CSPF} < 6.00$.
  - Flagship Premium Inverter: $\text{CSPF} \ge 6.20$ (e.g., Daikin FTKY/FTKZ, Panasonic XU/XZ).

## 2. Thermal Comfort Standards (ASHRAE 55-2023)

Content analyzing temperature and indoor air quality must ground recommendations in **ASHRAE 55-2023**:
- **Operating Temperature Range**: $25^\circ\text{C} - 27^\circ\text{C}$ for optimal energy-health balance in tropical climates.
- **Relative Humidity (RH)**: Must be maintained between $50\% - 60\%$. Technologies like Daikin Hybrid Cooling, Panasonic iAUTO-X with Humidity Sensor, and Dry dehumidification modes must be evaluated against this threshold.
- **Air Velocity**: Indoor draught velocity must stay within $0.15 - 0.25\text{ m/s}$ (Coanda 3D airflow or WindFree micro-holes) to prevent thermal discomfort.

## 3. Empirical Testing Protocols

Articles claiming real-world performance must specify measuring equipment and test conditions:
- **Power Consumption Measurement**: Continuous 8-hour overnight logging using electronic digital power meters (e.g., Hioki Power Meter, Sonoff/Tuya calibrated CT sensors). Report in **kWh/night** alongside ambient outdoor temperature ($32^\circ\text{C} - 36^\circ\text{C}$ day, $28^\circ\text{C} - 30^\circ\text{C}$ night).
- **Acoustic Noise Testing**: Sound pressure levels in dB(A) measured at 1 meter distance using calibrated sound level meters (e.g., RION NL-52). Quiet/Sleep modes under 20 dB(A) must be explicitly noted.
- **Circuit Protection (Super PCB)**: Voltage surge tolerance tests ($130\text{V} - 440\text{V}$) for grid fluctuations in suburban and coastal regions.
- **Corrosion Resistance**: Condenser coil protection (e.g., Golden Fin, BlueFin, Microchannel) validated against coastal salt-spray conditions.

---

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

Last updated: 2026-09-10
