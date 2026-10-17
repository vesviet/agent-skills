## Agent Coordinator Review Checklist

This reference checklist provides operational verification criteria for autonomous multi-agent coordination, graph orchestration, and lifecycle governance to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across Directed Acyclic Graph (DAG) cycle detection, Non-Human Identity (NHI) lifecycle governance, Steer-or-Kill action classification, A2A 1.0 unified Part protocol compliance, token burn rate ceilings, stateless MCP runtime enforcement, serializable interruption recovery checkpoints, and EU AI Act Article 50 transparency disclosure gates.

### 1. Directed Acyclic Graph (DAG) Execution & Cycle Prevention (`DAG-CYCLE-DETECTION-LOCK`)
- **Mathematical Invariant & Kahn's Algorithm Verification**:
  - all multi-agent execution plans must be formally modeled as a finite directed graph $G = (V, E)$, where vertices $v \in V$ represent atomic tasks and directed edges $(u, v) \in E$ declare that task $u$ must complete before task $v$ can initiate
  - cycle detection and topological ordering must execute prior to task dispatch using Kahn's algorithm operating in deterministic $O(|V| + |E|)$ time and $O(|V| + |E|)$ space:
    1. Compute in-degree for every vertex: $\forall v \in V, \, d_{\text{in}}(v) = |\{u \in V \mid (u, v) \in E\}|$
    2. Initialize zero-indegree queue: $Q \leftarrow \{v \in V \mid d_{\text{in}}(v) = 0\}$
    3. Initialize empty topological schedule list: $L \leftarrow []$
    4. While $Q \neq \emptyset$: pop $u$ from $Q$, append $u$ to $L$; for each outgoing edge $(u, v) \in E$, decrement $d_{\text{in}}(v) \leftarrow d_{\text{in}}(v) - 1$; if $d_{\text{in}}(v) = 0$, push $v$ into $Q$
    5. Invariant assertion: $|L| = |V| \iff G \text{ is a strictly acyclic DAG}$
  - if $|L| < |V|$, an unresolvable cyclic dependency exists in the task graph; orchestrator must immediately trip fail-closed, aborting execution before any subagent is dispatched
- **Positive DAG Specification vs Circular Anti-Pattern**:
  ```json
  // POSITIVE: Valid Acyclic Task Graph (Kahn's algorithm passes: |L| == 3)
  {
    "tasks": [
      {"id": "task_1", "role": "researcher", "dependencies": []},
      {"id": "task_2", "role": "solution-architect", "dependencies": ["task_1"]},
      {"id": "task_3", "role": "backend-developer", "dependencies": ["task_2"]}
    ]
  }
  ```
  ```json
  // NEGATIVE ANTI-PATTERN: Circular Deadlock (REJECT FAIL-CLOSED: |L| < |V|)
  {
    "tasks": [
      {"id": "task_A", "role": "planner", "dependencies": ["task_C"]},
      {"id": "task_B", "role": "implementer", "dependencies": ["task_A"]},
      {"id": "task_C", "role": "reviewer", "dependencies": ["task_B"]}
    ]
  }
  ```
- **Write-Scope Partition Isolation & Frontier Concurrency**:
  - parallel task execution groups within the same topological frontier must enforce strict mutual exclusion on write scopes; no two concurrent agents may possess write access to the same file, directory, or database partition
  - maximum recursion delegation depth is strictly locked to $\le 8$ sequential delegation tiers to prevent unbounded subagent spawning

### 2. Non-Human Identity (NHI) Lifecycle & Workload Isolation (`NHI-LIFECYCLE LOCK`)
- **Zero Standing Access & Ephemeral Credentialing**:
  - every delegated subagent runs under a scoped, ephemeral Non-Human Identity (NHI) registered in the platform identity registry; human caller credentials or admin tokens must never be passed to subagents
  - credential TTL strictly bounded to task execution duration ($\le 1\text{h}$ for interactive tasks, max $24\text{h}$ for background batch jobs) using SPIFFE/SVID X.509 certificates or OAuth 2.1 RFC 8693 token exchange
  - automated credential revocation and resource deprovisioning verified upon phase completion, abort, or timeout
- **Confused Deputy Defense & Scope Attenuation**:
  - RFC 8693 token exchange requests must down-scope permissions to the minimum necessary primary and supporting skills declared in the subagent's role card:
  ```json
  {
    "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
    "subject_token": "eyJhbGciOiJSUzI1NiIs...",
    "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
    "audience": "https://agent-gateway.internal/roles/backend-developer",
    "scope": "role:backend-developer:execute task:write-unit-tests"
  }
  ```
  - cross-tenant or cross-domain privilege escalation attempts intercepted and logged as P0 security incidents

### 3. Steer-or-Kill Action Classification & 4-Tier HITL Approval Gate Matrix (`IRREVERSIBLE-ACTION LOCK`)
- **4-Tier Action Classification Matrix**:
  | Tier | Action Category | Blast Radius | Examples | Execution Mode | Veto Powers & Escalation Path |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | **Tier 1** | Routine / Read-Only | Minimal ($R_0$) | File view, grep search, directory list, syntax linting | Fully Autonomous | Automated tool audit log; zero human interruption |
  | **Tier 2** | Low-Risk Mutation | Contained ($R_1$) | Ephemeral branch commit, local unit test run, temp file generation | Autonomous + Async Notify | Project Manager notify; rollback via git revert |
  | **Tier 3** | High-Risk Mutation | Elevated ($R_2$) | DB migration, IAM change, dependency update, cross-role dispatch | Synchronous Pause for Approval | Technical Lead approval; SLA dwell-time $\le 4\text{h}$ before escalation |
  | **Tier 4** | Critical / Irreversible | Catastrophic ($R_3$) | Git push to main, production deploy, dropping DB tables, secret rotation, financial rails | Mandatory Explicit Human Sign-Off | Dual-key sign-off (Tech Lead + Security Lead); no automated bypass |
- **Enforcement Mechanics & Dwell-Time SLAs**:
  - prompt-based self-regulation strictly prohibited for irreversible actions; gates must be enforced programmatically at the orchestrator hook layer (`core/scripts/hooks/check-policy.py`)
  - parallel execution groups containing any Tier 3 or Tier 4 action must pause the entire group until confirmation is recorded
  - human review queue dwell time tracked; review bottlenecks exceeding 4 hours escalate to engineering leads to prevent stalling autonomous agent fleets

### 4. Token FinOps, Exponential Burn Rate Governance & Circuit Breakers (`FINOPS LOCK`)
- **Exponential Token Burn Rate Equation & Bounds**:
  - real-time token burn velocity modeled via continuous exponential acceleration:
    $$\text{BurnRate}(t) = B_0 \cdot e^{k \cdot t}$$
    where $B_0$ is the initial token burn velocity (tokens/second), $k$ is the token acceleration coefficient ($k = \frac{\ln(B(t_2)/B(t_1))}{t_2 - t_1}$), and cumulative phase token consumption is given by:
    $$B_{\text{cum}}(T) = \int_0^T B(t)\,dt = \frac{B_0}{k}\left(e^{k \cdot T} - 1\right) \le C_{\text{phase}}$$
  - token burn acceleration threshold is clamped at $k \le 0.05\text{ s}^{-1}$; sustained $k > 0.05$ triggers automated rate throttling
- **Real-Time PromQL Circuit Breakers**:
  ```promql
  # Instantaneous token consumption velocity breach
  rate(llm_tokens_consumed_total{env="prod"}[5m]) > 5000
  
  # Phase cumulative token budget saturation (>75%)
  (llm_phase_tokens_used / llm_phase_tokens_limit) > 0.75
  ```
  - alert triggers at $60\%$ and $75\%$ of declared phase ceiling; hard circuit breaker trips at $100\%$, halting phase execution immediately
- **Anti-Ping-Pong Semantic Loop Breaker**:
  - calling the identical tool with identical parameters $3\times$ consecutively without forward state progress trips an emergency circuit breaker
  - state hash evaluated on every invocation: $H_i = \text{SHA256}(\text{tool\_name} \mathbin{\Vert} \text{args} \mathbin{\Vert} \text{workspace\_hash})$; if $H_i = H_{i-1} = H_{i-2}$, abort task with `ERR_SEMANTIC_PING_PONG`

### 5. A2A 1.0 JSON-RPC 2.0 / SSE Protocol & Unified Part Spec (`A2A-PROTOCOL LOCK`)
- **Discriminated Union by Structural Member Existence**:
  - all inter-agent messages conform to A2A 1.0 specifications over JSON-RPC 2.0 or Server-Sent Events (SSE) streaming
  - payload message parts strictly utilize the unified `Part` model discriminated by structural property existence:
  ```json
  // POSITIVE: A2A 1.0 Unified Part Specification (Draft 2020-12)
  {
    "jsonrpc": "2.0",
    "method": "a2a.deliverArtifact",
    "params": {
      "task_id": "4b7b2521-7f8e-4a88-8254-8e1f592e3894",
      "parts": [
        {"text": "Execution completed successfully with zero lint warnings."},
        {
          "file": {
            "uri": "file:///workspace/build/reports/audit.json",
            "mime_type": "application/json",
            "size_bytes": 4096
          }
        },
        {
          "data": {
            "schema_uri": "contracts/schemas/validation-result.json",
            "content": {"status": "PASSED", "checks_run": 42, "violations": 0}
          }
        }
      ]
    }
  }
  ```
  ```json
  // NEGATIVE ANTI-PATTERN: Ambiguous Legacy Discriminators (REJECT FAIL-CLOSED)
  {
    "parts": [
      {"kind": "text", "body": "Deprecated discriminator string"},
      {"type": "data", "payload": {"foo": "bar"}}
    ]
  }
  ```
- **Distributed Traceability & Correlation**:
  - unique `trace_id` (UUIDv4) and `parent_span_id` injected at orchestration intake and propagated across every `a2a-task.json`, `a2a-task-progress.json`, and `a2a-artifact.json`
  - missing trace correlation on any returned artifact halts phase progression

### 6. Stateless MCP 2026-07-28 Protocol Enforcement (`MCP-STATELESS LOCK`)
- **Stateless HTTP Transport & Session Externalization**:
  - all Model Context Protocol (MCP) integrations mandate stateless HTTP transport complying with the MCP 2026-07-28 specification
  - long-lived stateful stdio or persistent WebSocket connections prohibited in production orchestrators; session continuity externalized to Redis or Durable Objects
- **Tool Allowlist & Supply Chain Gate**:
  - third-party MCP servers verified against the organization tool map (`core/policies/mcp-tool-map.yaml`) and pinned to immutable release hashes
  - tools advertising unmapped mutations or dangerous shell escapes blocked fail-closed

### 7. Interruption Recovery & Serializable Checkpoints (`CHECKPOINT-RESTORE LOCK`)
- **Deterministic Coordination State Serialization**:
  - after each completed phase gate, the entire orchestration state serialized to disk at `coordination-plan.json`
  - checkpoint captures: completed phases, pending tasks, artifact references, token spend to date, active circuit breakers, and current topological frontier
- **Rehydration & Crash Recovery**:
  - system capable of rehydrating and resuming execution from the exact last-known-good phase gate following server restarts, process crashes, or network drops
  - duplicate side effects prevented via idempotent execution keys

### 8. EU AI Act Article 50 Disclosure & Calibrated Quality Verification (`EU-AI-ACT-DISCLOSURE LOCK`)
- **Mandatory AI Transparency Hook**:
  - user-facing AI feature workflows must integrate an explicit AI disclosure banner and machine-readable metadata (`data-ai-generated="true"`)
  - synthetic media generation outputs must carry C2PA Content Credentials or cryptographic watermarks prior to public release
- **Agentic Fitness Function Calibration (`FITNESS-CALIBRATION LOCK`)**:
  - LLM-as-Judge evaluation gates calibrated against at least 20–50 historical human ground-truth changes before gating production pipelines
  - calibrated agreement score verified at $\ge 85\%$ before promoting fitness functions to blocking status

### 9. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **DAG Cycle Check** | $|L| = |V|$ | `python3 core/scripts/validate-graph.py` | 0 cycles detected; deterministic ordering |
| **Token FinOps Ceiling** | $B_{\text{cum}} \le C_{\text{phase}}$ | Prometheus `llm_phase_tokens_used` | Token consumption within envelope |
| **A2A Part Validation** | Structural discrimination | `python3 core/scripts/validate-contracts.py` | 100% conforming to unified Part model |
| **HITL Tier 4 Sign-Off** | Cryptographic approval | `python3 core/scripts/hooks/check-policy.py` | Dual signature present for Tier 4 |
| **Checkpoints Saved** | Serializable state | `test -f coordination-plan.json` | Valid schema and hash verified |
