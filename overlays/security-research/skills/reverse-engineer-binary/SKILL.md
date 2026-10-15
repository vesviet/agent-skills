---
name: reverse-engineer-binary
description: Use when deconstructing compiled binaries, Electron bundles, and firmware images in air-gapped sandboxes to produce structured REA evidence ledgers.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, execute_command, run_tests]
---

# Reverse Engineer Binary

Deconstruct compiled executables, Electron packages, and firmware images in air-gapped sandboxes using Ghidra, radare2, and unpacking toolchains to generate verifiable REA evidence ledgers.

## When to Use

- Auditing third-party compiled binaries or closed-source dependencies for security vulnerabilities
- Unpacking Electron desktop bundles (`.asar`) to inspect embedded JavaScript application logic
- Extracting hardcoded API tokens, cryptographic credentials, and network endpoints from executables
- Triage of suspicious binaries, malicious firmware blobs, or supply-chain drop-in libraries
- Producing defensible Reverse Engineering Artifact (REA) evidence reports for security audits

## Core Rules

- **Defensive Ethics Invariant**: Reverse engineering is restricted strictly to vulnerability discovery, defensive auditing, malware analysis, and interoperability research. DRM circumvention, license key generation, and exploit authoring are strictly prohibited.
- **Source Code Presence Guard**: If readable source code is present in the repository, bypass this reverse engineering skill entirely and audit source code directly using standard code analysis tools.
- **Mandatory Sandbox Confinement**: Never execute or decompile untrusted binaries directly on the host machine. All analysis must execute inside Tier 2 (hardened OCI/gVisor container with `--read-only`, `--network=none`, `CAP_DROP=ALL`) or Tier 3 (Firecracker microVM).
- **Network Air-Gap**: The analysis environment must have `--network=none` active at all times. Network egress during binary inspection is strictly forbidden.
- **Triage Toolchain Hierarchy**:
  - Electron / JS packages: Unpack using `asar` and run static AST analysis
  - Native binaries: Run static header triage, strings extraction (`rabin2 -z`), symbol recovery (`rabin2 -i`), followed by headless Ghidra or radare2 decompilation
- **Verifiable REA Ledger**: Every analysis must produce a structured REA evidence ledger recording artifact hashes, decompiler tool versions, discovered entry points, and vulnerability findings.

## Suggested Process

### 1. Ingest Artifact and Verify Boundaries
- Compute cryptographic checksums: SHA-256 and MD5 hashes of target binary artifact.
- Check repository context for human-readable source code; if source exists, abort reverse engineering and switch to source code review.
- Confirm target scope aligns with defensive audit, vulnerability research, or supply chain verification.

### 2. Initialize Air-Gapped Sandbox Environment
- Launch Tier 2 hardened OCI container with read-only root (`--read-only`), dropped capabilities (`--cap-drop=ALL`), non-root UID (`10001:10001`), and network air-gap (`--network=none`).
- Mount target binary into sandboxed scratch workspace with `noexec` flags when performing static disassembly.
- Set process limits (memory $\le 2\text{GB}$, CPU $\le 2.0$, PIDs $\le 64$).

### 3. Conduct Decompiler Triage
- **For Electron / Node packages**:
  - Execute `npx asar extract <file>.asar <dest_dir>` to recover source tree.
  - Review `package.json` dependencies and scan JS code for dynamic `eval` or remote script loaders.
- **For Native Binaries (ELF, PE, Mach-O)**:
  - Run binary header classification (`file`, `rabin2 -I`) to determine architecture, bitness, and section entropy.
  - Extract ASCII and UTF-16 strings (`rabin2 -z`, `rabin2 -zz`) to locate URLs, IPs, file paths, and credentials.
  - Map external imports (`rabin2 -i`) and exported symbols (`rabin2 -E`) to understand system call surfaces.
  - Launch headless Ghidra script or radare2 (`r2 -c 'aaa; pdc'`) on target function addresses.

### 4. Synthesize REA Evidence Ledger
- Record binary metadata: filename, byte size, SHA-256 hash, architecture, compiler signature, and packing status.
- Document discovered entry points, API call sequences, and cryptographic constants.
- Detail identified vulnerabilities with memory offset addresses, assembly snippets, and CWE/CVSS classifications.
- Formulate actionable defensive mitigations and patch recommendations.

### 5. Review Findings and Secure Cleanup
- Validate that all findings are accompanied by exact binary offsets and decompiled evidence snippets.
- Ensure the ephemeral sandbox container is terminated and temporary scratch volumes are purged.

## Output Format

Outputs must format the analysis results into a structured REA evidence ledger:

```markdown
# <Artifact Name> - Reverse Engineering Evidence Ledger

## Artifact Identification
- Filename: <binary_name> | Byte Size: <bytes>
- SHA-256: <64-character-hex-hash>
- Architecture: <e.g. x86_64, ARM64, WebAssembly>
- Compiler / Packer: <detected toolchain or "Unpacked">

## Environment & Provenance
- Sandbox Tier: Tier 2 (OCI / gVisor) | Network: Air-gapped (--network=none)
- Toolchain: Ghidra Headless <version> / radare2 <version>

## Attack Surface Inventory
- Imported Libraries: <list of DLLs or shared objects>
- Sensitive Strings / Endpoints: <extracted URLs, IPs, paths>
- Exported API Surface: <callable functions>

## Vulnerability & Defect Matrix
| Offset | Category | Severity | Root Cause | Remediation |
| :--- | :--- | :--- | :--- | :--- |
| `0x004012A0` | CWE-120 Buffer Overflow | High (CVSS 7.8) | Unbounded `strcpy` | Replace with bounded copy |
```

## Failure Modes

- **Host execution leak**: Running an untrusted binary or dynamic tracer outside a sandbox risks host compromise. **Mitigation**: Strictly mandate Tier 2/3 container isolation with dropped capabilities and noexec mounts.
- **Decompiling existing source code**: Spending agent compute reverse engineering binaries when source code is already present. **Mitigation**: Enforce Source Code Presence Guard in step 1.
- **Network egress during analysis**: Decompilation toolchains phoning home or triggering network beacons embedded in malware. **Mitigation**: Enforce `--network=none` air-gap at the container runtime level.
- **Unverified assembly assertions**: Stating a binary is vulnerable without providing exact offset addresses and instruction disassembly. **Mitigation**: Require proof offsets in the REA evidence ledger.

## Output Contracts

When completing binary analysis or decompilation triage, emit:

- Structured REA evidence ledger markdown document following the Output Format template.
- If reporting security vulnerabilities, companion artifact must adhere to `contracts/schemas/security-audit.json`.

## Security Guardrails (OWASP ASI)

- **ASI05 Sandbox Escape Guard**: Never enable Docker socket forwarding or privileged container flags (`--privileged`) during reverse engineering tasks.
- **ASI06 Binary Data Guard**: Do not output raw unescaped binary bytes or shellcode sequences into user-facing chat logs.

## Checklist

- [ ] Defensive audit or vulnerability research authorization confirmed.
- [ ] Source code presence checked; skipped reverse engineering if source code is present.
- [ ] Cryptographic hashes (SHA-256 and MD5) calculated and recorded.
- [ ] Tier 2/3 sandbox container initialized with `--read-only` and `CAP_DROP=ALL`.
- [ ] Network air-gap verified active (`--network=none`).
- [ ] Binary architecture, compiler signature, and entropy evaluated.
- [ ] Sensitive strings, URLs, IPs, and API keys extracted and cataloged.
- [ ] Dynamic library imports and exported symbol tables mapped.
- [ ] Critical functions decompiled using headless Ghidra or radare2.
- [ ] REA evidence ledger populated with exact memory offsets and remediation advice.
- [ ] Ephemeral sandbox container destroyed upon completion.

## Related Skills

- **security-audit**: Conduct end-to-end vulnerability assessments and CVSS scoring
- **supply-chain-security**: Verify dependencies, signatures, and package hashes
- **manage-secrets**: Isolate, rotate, and secure leaked API keys or credentials found in binaries
- **systematic-debugging**: Formulate testable hypotheses when tracing control flow defects
- **review-code**: Audit decompiled C/C++ pseudo-code or unpacked JavaScript for security flaws
