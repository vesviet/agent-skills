## Reverse Engineer Review Checklist

This reference checklist provides technical verification gates, sandbox containment criteria, decompiler accuracy metrics, and defensive ethics standards for Reverse Engineer (Role #39) deliverables to satisfy SOTA 2026–2027 Agentic SWE standards.

### 1. Air-Gapped Sandbox Confinement & Isolation Integrity (`SANDBOX-ISOLATION LOCK`)
- **Containerized Isolation Verification**:
  - target binary executed strictly within an ephemeral Tier 2 hardened OCI/gVisor sandbox or Tier 3 Firecracker microVM
  - root filesystem configured read-only (`--read-only`); capabilities dropped completely (`CAP_DROP=ALL`); user pinned to non-root UID (10001:10001)
  - zero host-level execution: binaries never executed on bare-metal workstations or CI runner host environments
- **Network Air-Gap Enforcement**:
  - container network mode strictly set to `--network=none`; zero outbound network interface sockets active
  - DNS resolution and raw packet socket creation blocked fail-closed; local IPC channels isolated via dedicated UTS/IPC namespaces
- **Blast Radius & Resource Limits**:
  - memory bounded to $\le 2\text{GB}$; CPU quota capped at $\le 2.0$ cores; PID limits enforced ($\le 64$)
  - sandbox blast radius guaranteed at zero:
    $$\text{Blast Radius} = \text{Sandbox Tier (1--3)} \times \text{Network Exposure Score } (0 \text{ if air-gapped}, 1 \text{ if network enabled}) = 0$$

### 2. Multi-Architecture Binary Triage & Static Decompilation (`STATIC-TRIAGE LOCK`)
- **Cryptographic Provenance**:
  - SHA-256 and MD5 checksums computed and verified against external manifests
  - SSDEEP fuzzy hash and TLSH locality-sensitive hash generated to identify binary variants and code reuse
- **Multi-Architecture Coverage**:
  - binary headers validated across target architecture (x86, x86_64, ARMv7, AArch64, RISC-V RV64GC, WebAssembly)
  - calling conventions (System V AMD64, Microsoft x64, ARM AAPCS) and stack frame alignments correctly recognized
- **Decompiler Protocol Fidelity**:
  - headless Ghidra scripts, IDA Pro microcode API, Binary Ninja MLIL/HLIL, or radare2/rizin pipelines produce structured control flow graphs (CFG)
  - decompiled pseudocode cross-checked against raw disassembled assembly; virtual addresses verified for every entry point
- **Entropy & Packer Detection**:
  - Shannon entropy computed across all sections; sections with $H(X) \ge 7.2$ flagged as packed or encrypted:
    $$\text{Shannon Entropy: } H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$

### 3. Dynamic Binary Instrumentation & Non-Invasive Kernel Tracing (`DBI-TRACING LOCK`)
- **Frida Hooking & Runtime Inspection**:
  - Frida v16+ runtime scripts attached inside guest using `Interceptor.attach` and `Memory.protect`
  - in-memory decrypted buffers, symmetric key schedules, and dynamic function parameters dumped without binary tampering
  - anti-debugging techniques (timing checks, `ptrace(PTRACE_TRACEME)`, hardware breakpoint scans) neutralized in-memory
- **Non-Invasive eBPF User Tracing**:
  - `uprobes` and `uretprobes` via bpftrace monitor userspace function boundaries and syscall arguments without attaching debuggers
  - kernel ring buffers sized $\ge 32\text{MB}$; BTF (BPF Type Format) metadata loaded on Linux kernel $\ge 5.15$
- **Instrumentation Overhead Verification**:
  - dynamic instrumentation overhead constrained within operational limits:
    $$\text{DBI Overhead Factor} = \frac{T_{\text{instrumented}}}{T_{\text{baseline}}} \le 5.0$$

### 4. Protocol Reverse Engineering & Wire Format Reconstruction (`PROTOCOL-DISSECTION LOCK`)
- **Network Capture Dissection**:
  - packet captures inspected with Wireshark/TShark; TCP streams reassembled; UDP framing parsed
  - TLS decryption accomplished via `SSLKEYLOGFILE` injection or dynamic BoringSSL/OpenSSL master secret hooking into mitmproxy
- **Wire Format Serialization Recovery**:
  - Tag-Length-Value (TLV), Protocol Buffers (`protoc --decode_raw`), FlatBuffers, and MessagePack framing disassembled
  - message structures, field tags, and scalar types recovered into reproducible `.proto` or schema definitions
- **Contract Conformance**:
  - reconstructed API and RPC endpoints formalized in `contracts/schemas/api-contract-spec.json`
  - protocol finite state machine (FSM) validated:
    $$\text{Protocol State Coverage} = \frac{|\text{Observed State Transitions}|}{|\text{Total Discovered FSM States}|} \ge 0.85$$

### 5. Control Flow Deobfuscation & Symbolic Program Analysis (`DEOBFUSCATION LOCK`)
- **Control Flow Flattening (CFF) Unscrambling**:
  - dispatcher loops and state variables resolved using symbolic execution engines (angr, Z3)
  - basic blocks reordered into structured topological control flow; artificial trampoline jumps removed
- **Opaque Predicate & MBA Simplification**:
  - opaque predicates evaluated symbolically and pruned to eliminate dead branches
  - Mixed Boolean-Arithmetic (MBA) expressions simplified into canonical algebraic identities via microcode AST passes
- **Memory Unpacking & Reconstruction**:
  - dynamic unpacking triggers hooked at memory allocation checkpoints (`VirtualAlloc`, `mprotect`)
  - resident decrypted memory dumped using `pe-sieve`/`moneta`; Import Address Table (IAT) rebuilt
  - cyclomatic complexity reduction ratio verified:
    $$\text{Deobfuscation Ratio} = \frac{V(G)_{\text{flattened}} - V(G)_{\text{recovered}}}{V(G)_{\text{flattened}}} \ge 0.60$$

### 6. Defect Classification, REA Evidence Ledger & Defensive Ethics (`ETHICS-DEFENSE LOCK`)
- **Defensive Ethics Invariant**:
  - zero weaponized exploit payloads, shellcode generators, or bypass scripts produced
  - DRM circumvention, license key generation, and unauthorized access mechanisms strictly barred; requests fail closed
- **REA Evidence Ledger Standards**:
  - every finding documented with exact virtual memory offset, disassembled assembly sequence, and decompiler pseudocode snippet
  - root-cause analysis describes underlying structural bug (e.g. integer truncation, out-of-bounds index, unvalidated length)
- **Vulnerability Schema Compliance**:
  - vulnerabilities emitted conformant to `contracts/schemas/security-audit.json` with CWE identifier and CVSS v3.1/v4.0 scoring
  - OWASP ASI05 (Unexpected Code Execution) and ASI06 (Memory & Context Poisoning) guardrails strictly enforced
- **Verification Gate Conformance Table**:
  | Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
  | :--- | :--- | :--- | :--- |
  | **Air-Gap Verification** | Zero network egress | `docker inspect --format '{{.HostConfig.NetworkMode}}' <id>` | Exactly `none` |
  | **Entropy Check** | Packer identification | `rabin2 -S <binary> \| grep entropy` | Calculated $H(X)$ value |
  | **Decompiler Proof** | Exact instruction offset | Ghidra headless / `r2 -c 'pdc' <addr>` | Verifiable disassembly snippet |
  | **Contract Schema** | Valid `security-audit.json` | `python3 core/scripts/validate-contracts.py` | 100% schema compliant |
  | **Defensive Ethics** | Zero exploit code | Static AST audit of REA report | 0 weaponized shellcode/payloads |
