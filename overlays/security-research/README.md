# Security Research Overlay

Composable overlay for the `security-engineer` role when conducting binary disassembly, decompilation triage, malware analysis, firmware auditing, and reverse engineering governance.

This overlay establishes strict ethical and legal boundaries, Tier 2/3 sandbox confinement architecture, multi-toolchain coordination (Ghidra, radare2, Electron asar unpackers), and formal Reverse Engineering Artifact (REA) evidence ledgers.

## Scope

- Binary disassembly, control-flow recovery, and decompilation triage
- Defensive security auditing, vulnerability research, and supply chain binary verification
- Mandatory air-gapped Tier 2 (hardened OCI/gVisor) and Tier 3 (microVM) sandbox containment
- Source code presence guard (automatic bypass of decompilation when source code exists)
- Comprehensive REA evidence ledger tracking (hashes, imports, strings, CVEs, remediation)
- Strict ethical prohibition on malware authoring, DRM circumvention, and license cracking

## Included

- `rules/reverse-engineering-rules.md` — Ethical boundaries, sandbox containment, and evidence logging rules
- `skills/reverse-engineer-binary/SKILL.md` — Binary disassembly, decompilation, and REA ledger skill

## Activation

```
Role: security-engineer
Overlay: overlays/security-research
```

Compose with `core/skills/security-data/security-audit` and `core/skills/security-data/skill-preflight-ast-check` for comprehensive defensive security workflows.

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
