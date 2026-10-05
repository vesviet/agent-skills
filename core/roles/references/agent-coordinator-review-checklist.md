## Agent Coordinator Review Checklist

This reference checklist provides operational verification criteria for autonomous multi-agent coordination, graph orchestration, and lifecycle governance to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across Directed Acyclic Graph (DAG) cycle detection, Non-Human Identity (NHI) lifecycle governance, Steer-or-Kill action classification, A2A 1.0 unified Part protocol compliance, token burn rate ceilings, stateless MCP runtime enforcement, serializable interruption recovery checkpoints, and EU AI Act Article 50 transparency disclosure gates.

### 1. Directed Acyclic Graph (DAG) Execution & Topological Integrity
- **Cycle Detection & Topological Sorting**:
  - all multi-agent task execution plans represented as formal DAG structures using Kahn's algorithm or DFS cycle detection; cyclic dependencies (`A -> B -> A`) must fail-closed at plan validation before task dispatch
  - parallel phase groups enforce strict write-scope isolation: no two concurrent agents may possess write access to identical files, database tables, or shared state partitions
  - execution sequence strictly honors topological ordering; no downstream phase begins execution until all prerequisite predecessor outputs validate successfully against their declared schema
- **Dynamic Branching & Graph Pruning**:
  - conditional branches evaluate deterministic predicate expressions against incoming artifact data
  - unselected branches pruned cleanly without leaving orphaned background tasks or unmonitored locks
  - max execution depth locked ($\le 8$ sequential delegation tiers) to prevent unconstrained recursion

### 2. Non-Human Identity (NHI) Lifecycle & Workload Isolation (`NHI-LIFECYCLE LOCK`)
- **Zero Standing Access & Ephemeral Credentialing**:
  - every delegated subagent runs under a scoped, ephemeral Non-Human Identity (NHI) registered in the platform identity registry; human caller credentials or admin tokens must never be passed to subagents
  - credential TTL strictly bounded to task execution duration ($\le 1\text{h}$ for interactive tasks, max $24\text{h}$ for background batch jobs) using SPIFFE/SVID or OAuth 2.1 RFC 8693 token exchange
  - automated credential revocation and resource deprovisioning verified upon phase completion, abort, or timeout
- **Confused Deputy & Scope Escalation Prevention**:
  - subagent permissions restricted strictly to the primary and supporting skills declared in the assigned role toolbox
  - cross-tenant or cross-domain privilege escalation attempts intercepted and logged as P0 security incidents

### 3. Steer-or-Kill Action Classification & Mandatory HITL Gates (`IRREVERSIBLE-ACTION-LOCK`)
- **Three-Tier Action Categorization**:
  - every planned action classified prior to execution:
    1. **Routine** (reversible, read-only or scoped branch edits) $\rightarrow$ autonomous execution
    2. **Risky** (modifies shared configs, introduces new dependencies, alters database schemas) $\rightarrow$ pause for user confirmation
    3. **Irreversible** (production deployments, git push to main, dropping databases, deleting storage volumes, modifying secrets, financial transfers) $\rightarrow$ mandatory explicit human sign-off
- **Enforcement Mechanics**:
  - prompt-based self-regulation strictly prohibited for irreversible actions; gates must be enforced programmatically at the orchestrator hook layer (`core/scripts/hooks/check-policy.py`)
  - parallel execution groups containing any Risky or Irreversible action must pause the entire group until confirmation is recorded

### 4. A2A 1.0 JSON-RPC 2.0 / SSE Protocol & Unified Part Spec
- **Contract & Message Schema Conformance**:
  - all inter-agent messages conform to A2A 1.0 specifications over JSON-RPC 2.0 or Server-Sent Events (SSE) streaming
  - payload message parts strictly utilize the unified `Part` discriminated union by member existence:
    - Text Part: `{ "text": "string content" }`
    - File Part: `{ "file": { "uri": "file://...", "mime_type": "text/markdown" } }`
    - Data Part: `{ "data": { "schema_uri": "contracts/schemas/...", "content": { ... } } }`
    - legacy ambiguous `kind` discriminators strictly rejected fail-closed
- **Distributed Traceability**:
  - unique `trace_id` (UUIDv4) and `parent_span_id` injected at intake and propagated across every `a2a-task.json`, `a2a-task-progress.json`, and `a2a-artifact.json`
  - missing trace correlation on any returned artifact halts phase progression

### 5. Token FinOps, Rate Governance & Circuit Breakers
- **Token Ceiling & Pre-Flight Budgeting**:
  - global token budget envelope and per-phase token ceilings calculated and recorded in `coordination-plan.json` prior to delegation
  - real-time token burn tracked; warning alerts triggered at 60% and 75% of budget allocation
  - execution halts automatically if any phase reaches 100% of its token ceiling, requiring explicit re-scoping
- **Semantic Loop & Hallucination Circuit Breakers**:
  - duplicate tool call detection: calling the identical tool with identical parameters $3\times$ consecutively without forward progress triggers immediate circuit breaker trip
  - contradictory findings detector: conflicting claims between specialist agents flagged immediately for human resolution
  - silent failure defense: returned artifacts that satisfy JSON Schema but fail semantic acceptance criteria rejected and re-routed

### 6. Stateless MCP 2026-07-28 Protocol Enforcement (`MCP-STATELESS LOCK`)
- **Stateless HTTP Transport**:
  - all Model Context Protocol (MCP) integrations mandate HTTP transport with externalized session state; legacy stateful stdio or long-lived persistent WebSocket connections rejected
  - session tokens and continuity state externalized to Redis or Durable Objects; zero in-memory cross-request affinity
- **MCP Supply Chain & Provenance Allowlist**:
  - third-party MCP servers verified against the organization tool map (`core/policies/mcp-tool-map.yaml`) and pinned to immutable release hashes
  - tools advertising dangerous meta-characters or unmapped actions blocked fail-closed

### 7. Interruption Recovery & Serializable Checkpoints
- **Serializable Coordination State**:
  - after each completed phase gate, the entire orchestration state serialized to disk at `coordination-plan.json`
  - checkpoint captures: completed phases, pending tasks, artifact references, token spend to date, active circuit breakers, and current topological frontier
- **Rehydration & Crash Recovery**:
  - system capable of rehydrating and resuming execution from the exact last-known-good phase gate following server restarts, process crashes, or network drops
  - duplicate side effects prevented via idempotent execution keys

### 8. EU AI Act Article 50 Disclosure & AI Output Verification (`EU-AI-ACT-DISCLOSURE LOCK`)
- **Mandatory AI Transparency Hook**:
  - user-facing AI feature workflows must integrate an explicit AI disclosure banner and machine-readable metadata (`data-ai-generated="true"`)
  - synthetic media generation outputs must carry C2PA Content Credentials or cryptographic watermarks prior to public release
- **Agentic Fitness Function Calibration (`FITNESS-CALIBRATION LOCK`)**:
  - LLM-as-Judge evaluation gates calibrated against at least 20–50 historical human ground-truth changes before gating production pipelines
  - calibrated agreement score verified at $\ge 85\%$ before promoting fitness functions to blocking status
