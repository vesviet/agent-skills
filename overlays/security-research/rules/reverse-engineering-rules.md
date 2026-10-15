# Reverse Engineering Rules

Governance standards, ethical boundaries, sandbox containment architecture, and evidence preservation protocols for binary disassembly, decompilation, and firmware security analysis.

## 1. Ethical and Legal Boundaries

1. **Authorized Defensive Scope**: Reverse engineering is strictly restricted to defensive security auditing, vulnerability discovery, malware analysis, supply chain binary verification, and protocol interoperability research.
2. **Prohibited Activities**:
   - Circumventing Digital Rights Management (DRM) or anti-piracy mechanisms.
   - Authoring software cracks, keygens, or license validation bypasses.
   - Developing weaponized exploits or offensive malware payloads.
   - Exfiltrating proprietary intellectual property or personal data.
3. **Source Code Presence Guard**: If original, human-readable source code is available in the repository or local build context, reverse engineering pipelines are bypassed completely. The agent must inspect and audit source files directly using standard code analysis and search tools (`view_file`, `grep_search`, `search_code`).

## 2. Sandbox Confinement Standards (Tier 2 / Tier 3)

Under no circumstances may untrusted binaries, unpacking scripts, or dynamic tracing tools execute on the host development machine. All analysis must execute within isolated sandboxes:

### Tier 2 Confinement (Hardened OCI Container / gVisor)
Standard environment for static disassembly, unpackers, and decompiler triage:
- **Filesystem**: Read-only root filesystem (`--read-only`), ephemeral scratch volume mounted with `noexec, nosuid, nodev` on `/tmp`.
- **Network Posture**: Strict air-gap with zero network access (`--network=none`). Network egress during decompilation is prohibited.
- **Linux Capabilities**: Drop all privileges (`--cap-drop=ALL`). Prohibit `CAP_SYS_PTRACE`, `CAP_NET_RAW`, and `CAP_SYS_ADMIN`.
- **User Identity**: Run strictly as unprivileged non-root user (`--user 10001:10001`).
- **Resource Constraints (cgroups v2)**: Memory ceiling $\le 2\text{GB}$, CPU quota $\le 2.0$ cores, maximum process IDs $\le 64$ (`--pids-limit 64`).

### Tier 3 Confinement (MicroVM / Firecracker)
Mandatory environment for analyzing packed binaries, kernel drivers, self-modifying code, or suspected malware samples:
- Dedicated guest Linux kernel with hardware-assisted KVM virtualization.
- Ephemeral rootfs discarded immediately upon analysis completion.
- Network air-gap enforced at host bridge layer.

## 3. Decompiler Triage Protocol

Reverse engineering tasks must follow a tiered toolchain triage hierarchy:

1. **Electron & Packaged JavaScript Applications**:
   - Extract `.asar` archives using native unpackers (`npx asar extract app.asar source/`).
   - Run static AST parsing and deobfuscation on extracted JavaScript/TypeScript bundles.
   - Audit embedded dependencies (`package.json`) against known CVE databases.
2. **Native Executables (ELF, PE, Mach-O, Firmware)**:
   - **Phase 1: Header Triage**: Inspect binary architecture, bitness, endianness, section entropy, and compiler stamps (`file`, `rabin2 -I`). Flag high entropy ($> 7.2$) as packed/encrypted.
   - **Phase 2: Surface Extraction**: Extract printable strings, imported dynamic libraries, exported APIs, and cryptographic constants (`rabin2 -z`, `rabin2 -i`, `rabin2 -E`).
   - **Phase 3: Control Flow Decompilation**: Coordinate headless Ghidra (`analyzeHeadless`) or radare2 (`r2 -c 'aaa; pdc'`) to recover C pseudo-code for identified entry points and critical subroutines.

## 4. REA Evidence Ledger Standards

Every reverse engineering operation must output a durable, verifiable Reverse Engineering Artifact (REA) evidence ledger containing:

1. **Artifact Identification**: Target filename, exact byte size, cryptographic hashes (SHA-256, MD5), MIME type, CPU architecture, and compiler signature.
2. **Provenance & Execution Environment**: Extraction origin, decompiler toolchain versions, and unique sandbox container execution ID.
3. **Discovered Attack Surface**:
   - Exported symbols and callable entry points.
   - Imported external system calls and dynamic libraries.
   - Extracted IP addresses, URLs, API paths, and hardcoded secrets/tokens.
   - Cryptographic primitives and cipher signatures.
4. **Defect & Vulnerability Matrix**:
   - Vulnerability classification (CWE / OWASP category) and severity score (CVSS v4.0).
   - Memory address offset (`0x...`) and disassembled instruction sequence.
   - Detailed root cause explanation and actionable defense/remediation guidance.

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
