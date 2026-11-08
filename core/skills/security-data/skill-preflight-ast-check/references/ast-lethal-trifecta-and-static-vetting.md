# Static AST Preflight Vetting & Lethal Trifecta Governance (2026)

## 1. Zero-Execution Static AST Security Vetting

### 1.1 Static Analysis Mandate
Third-party agent skills and external MCP tool definitions must never be evaluated in dynamic runtimes without preflight static analysis. The scanner parses Python abstract syntax trees (`ast.parse`) and TypeScript ASTs without executing any script:
- **AST01 Prohibited Builtins**: Any AST call node matching `eval()`, `exec()`, `compile()`, or `__import__()` triggers immediate rejection.
- **AST02 Subprocess & Shell Traversal**: Calls to `os.system()`, `subprocess.Popen()`, `subprocess.run()`, or shell redirection (`shell=True`) trigger fail-closed denial.
- **AST03 Secret & Environment Harvesting**: Dynamic inspection of `os.environ` keys without declared policy justification is blocked.
- **AST05 Prompt Injection Delimiters**: Raw markdown files are vetted against delimiter hijacking tokens (`<|im_start|>`, `<|im_end|>`, `[SYSTEM]`, `Ignore previous instructions`).

---

## 2. Mathematical Formulation of the Lethal Trifecta

An agent skill $\mathcal{S}$ is evaluated across three orthogonal risk dimensions:
1. $\mathcal{D}_{\text{priv}}(\mathcal{S}) \in \{0, 1\}$: Access to confidential host files, private credentials, or internal databases.
2. $\mathcal{C}_{\text{untrusted}}(\mathcal{S}) \in \{0, 1\}$: Ingestion of untrusted external content (web scraping, user prompts, RSS feeds).
3. $\mathcal{E}_{\text{net}}(\mathcal{S}) \in \{0, 1\}$: Outbound network egress via raw sockets or external HTTP APIs.

The Lethal Trifecta Invariant $\mathcal{T}_{\text{lethal}}(\mathcal{S})$ is defined as:
$$\mathcal{T}_{\text{lethal}}(\mathcal{S}) = \mathcal{D}_{\text{priv}}(\mathcal{S}) \wedge \mathcal{C}_{\text{untrusted}}(\mathcal{S}) \wedge \mathcal{E}_{\text{net}}(\mathcal{S})$$

$$\mathcal{T}_{\text{lethal}}(\mathcal{S}) = 1 \implies \text{Disposition}(\mathcal{S}) = \text{FAIL-CLOSED REJECTION}$$

If private data access ($\mathcal{D}_{\text{priv}} = 1$) and untrusted content ($\mathcal{C}_{\text{untrusted}} = 1$) are both active, outbound network egress must be forcefully revoked:
$$\mathcal{E}_{\text{net}}(\text{Runtime}) \longleftarrow 0 \quad (\text{Air-Gapped Level 0})$$

---

## 3. Physical 4-Tier Sandbox Execution Hierarchy

| Tier | Technology | Startup Latency | Memory Limit | Primary Use Case |
|---|---|---|---|---|
| **Tier 1** | WebAssembly (WASI) | $< 5\text{ms}$ | 64 MB | Algorithmic transforms, regex, pure AST analysis |
| **Tier 2** | Hardened OCI / gVisor | $500\text{ms} - 2\text{s}$ | 512 MB | Local builds, unit tests, linters (`--read-only`) |
| **Tier 3** | Firecracker MicroVM | $5\text{ms} - 150\text{ms}$ | 2048 MB | Untrusted 3rd-party code execution |
| **Tier 4** | Cloud Sandbox SDK | $100\text{ms} - 1.5\text{s}$ | Dynamic | Ephemeral edge agent swarms & browser automation |
