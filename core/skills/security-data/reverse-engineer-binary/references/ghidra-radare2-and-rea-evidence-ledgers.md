# Headless Ghidra, Radare2, and REA Evidence Ledger Methodology (2026)

## 1. Air-Gapped Triage & Entropy Profiling

### 1.1 Safe Sandbox Environment
Binary reverse engineering must never occur directly on the developer host workstation:
- **Tier 2 Hardened OCI Container**:
  ```bash
  docker run --rm -v $(pwd)/samples:/samples:ro --network=none \
    --cap-drop=ALL --security-opt=no-new-privileges \
    mcr.microsoft.com/cbl-mariner/base/core:2.0 \
    sha256sum /samples/target_binary
  ```
- **Shannon Entropy Analysis**:
  Measure section entropy $H(X) = -\sum p(x) \log_2 p(x)$. Sections where $H(X) \ge 7.2$ indicate encrypted payloads or packed compression (UPX, Themida, VMProtect).

---

## 2. Headless Decompilation Protocols

### 2.1 Radare2 Non-Interactive Batch Analysis
Execute deterministic disassembly and function enumeration:
```bash
r2 -q -c "aaa; afl; pdf @ sym.main; q" target_binary
```

### 2.2 Headless Ghidra Scripting
Automate function boundary recovery and C-pseudocode emission:
```bash
analyzeHeadless /tmp/ghidra_project GhidraProject \
  -import target_binary \
  -postScript ExportDecompiledC.java /tmp/decompiled_output/
```

---

## 3. Reverse Engineering Artifact (REA) Evidence Ledger

Every finding documented in an audit deliverable must provide mathematical and architectural proofs:
1. **Target Identification**: SHA-256 digest, SSDEEP fuzzy hash, compiler toolchain signature.
2. **Virtual Memory Offset**: Explicit hexadecimal address (e.g. `0x004018F0`).
3. **Decompiled Pseudocode Snippet**: Exact routine highlighting buffer bounds, integer overflow, or format string vulnerability.
4. **Remediation Specification**: Defensible C/Rust patch preventing exploitability.
