## Task Planner Review Checklist

This reference checklist provides operational task decomposition, execution sequencing, agentic autonomy calibration, and delivery planning criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across Directed Acyclic Graph (DAG) task slicing, Critical Path Method (CPM) scheduling, Trust Ladder autonomy tier declarations, contract output alignment (`technical-delivery-plan.json`), background agent UX contracts, Generative UI (GenUI) governance planning, stateless MCP protocol alignment, and blast-radius mitigation.

### 1. Work Breakdown Structure (WBS) & DAG Task Decomposition (`DAG-TASK-DECOMPOSITION-LOCK`)
- **Atomic, Testable Execution Slices**:
  - large feature or refactoring initiatives decomposed into discrete, ordered tasks with explicit preconditions, inputs, deliverables, and definition of done
  - each task step specifies an exact owning role (`Role: **Role Name**`) that possesses the required skills in its declared Primary or Supporting toolbox
  - tasks organized as a valid Directed Acyclic Graph (DAG); circular dependencies eliminated; parallel branches explicitly specify write-scope boundaries
  - Kahn's algorithm validates graph acyclicity in deterministic $O(|V| + |E|)$ time prior to task dispatch:
    1. Compute in-degree $d_{\text{in}}(v) = |\{u \in V \mid (u, v) \in E\}|$
    2. Queue $Q \leftarrow \{v \in V \mid d_{\text{in}}(v) = 0\}$
    3. Assert $|L| = |V| \iff G \text{ is acyclic}$; if $|L| < |V|$ fail-closed
- **Critical Path Method (CPM) Scheduling**:
  - task plans compute the Critical Path Method (CPM) duration:
    $$\text{Critical Path Duration} = \max_{p \in \text{Paths}} \sum_{i \in p} t_i$$
  - slack time (float) calculated for non-critical paths: $\text{Float}_j = \text{Late Start}_j - \text{Early Start}_j$

### 2. Contract Output Alignment & Schema Conformance (`OUTPUT-CONTRACT-ALIGNMENT-LOCK`)
- **Mandatory Output Contracts**:
  - Task Planner must author and emit `contracts/schemas/technical-delivery-plan.json` and `contracts/schemas/coordination-plan.json`
  - authoring contracts owned by other roles (e.g., `contracts/schemas/seo-weekly-board.json` owned by SEO Analyst) is strictly prohibited
- **Delivery Plan Schema Specification**:
  - execution plans produce valid, schema-compliant JSON:
    ```json
    {
      "plan_id": "tdp-2026-auth-upgrade",
      "objective": "Upgrade authentication stack to RFC 8693 token exchange",
      "tasks": [
        {
          "step_id": "step-1",
          "role": "solution-architect",
          "action": "Author OAuth token exchange ADR",
          "inputs": ["docs/architecture/auth-baseline.md"],
          "deliverables": ["docs/adr/0042-rfc8693-exchange.md"],
          "blast_radius_tier": 1
        },
        {
          "step_id": "step-2",
          "role": "security-engineer",
          "action": "Validate SPIFFE SVID down-scoping policies",
          "prerequisites": ["step-1"],
          "deliverables": ["core/policies/token-exchange-rules.yaml"],
          "blast_radius_tier": 2
        }
      ]
    }
    ```

### 3. Trust Ladder Autonomy Tier Calibration (`TRUST-LADDER LOCK`)
- **Explicit Autonomy Tier Declaration**:
  - every agentic or automated feature explicitly declares its operating autonomy tier in planning artifacts:
    1. **Tier 1 (Suggest)**: Agent proposes action/code; human executes
    2. **Tier 2 (Verify)**: Agent drafts implementation; human reviews and confirms before execution
    3. **Tier 3 (Delegate)**: Agent executes routine tasks autonomously; pauses for approval on high-risk boundaries
    4. **Tier 4 (Automate)**: Agent executes full pipeline autonomously within predefined operational envelopes
- **Anti-Autopilot Trap**:
  - unearned autonomy tiers prohibited; new agentic capabilities must demonstrate reliable performance at Suggest/Verify before promoting to Delegate/Automate

### 4. INVEST Work Slicing & Blast Radius Governance (`INVEST-SLICING-CRITERIA-LOCK`)
- **INVEST Criteria Compliance**:
  - each delivery slice must satisfy INVEST principles:
    - **Independent**: loose coupling between adjacent slices
    - **Negotiable**: scope can be adjusted without invalidating the architecture
    - **Valuable**: delivers testable, incremental progress
    - **Estimable**: clear boundaries allow realistic duration bounds
    - **Small**: execution bounded to $\le 2\text{ hours}$ of agent compute
    - **Testable**: explicit verification oracle provided for each step
- **Blast Radius Scoring & Rollback Readiness**:
  - every task slice assigned a blast radius score (Tiers 1–4) with documented rollback playbooks before work begins

### 5. Plan Checkpoint-Restore & State Serialization (`PLAN-CHECKPOINT-RESTORE-LOCK`)
- **Serializable Checkpoint States**:
  - task plans exceeding 3 sequential steps must declare serializable checkpoint states to allow resume-from-checkpoint after interrupts or crashes
  - checkpoint snapshots record completed step outputs, pending tasks, and token expenditure to date
  - idempotency keys attached to each step prevent duplicate side-effect execution during recovery

### 6. Three-Point Statistical Estimation & Confidence Intervals
- **Probabilistic Duration Envelopes**:
  - duration estimates provide three-point estimations:
    $$\mu = \frac{O + 4M + P}{6}, \quad \sigma = \frac{P - O}{6}$$
  - $95\%$ statistical confidence intervals calculated:
    $$\text{CI}_{95\%} = [\mu - 1.96\sigma, \, \mu + 1.96\sigma]$$
  - plans incorporate confidence bounds to feed downstream Monte Carlo project simulations

### 7. Background Agent UX & Async Interruption Contracts (`BACKGROUND-AGENT-UX LOCK`)
- **Status Surfaces & Progress Notification**:
  - long-running background agent workflows include explicit UX specifications for real-time progress surfaces, status indicators, and notification contracts
  - notifications define trigger events, severity tiers, and clear call-to-action responses
- **Asynchronous Interruptibility & Cancellation**:
  - background tasks must support non-destructive pause, redirect, and cancellation controls without leaving corrupted state or orphaned resources

### 8. Generative UI (GenUI) Governance Planning (`GENUI-GOVERNANCE LOCK`)
- **Component Palette & Assembly Constraints**:
  - dynamically assembled or AI-generated user interfaces mandate an explicit component allowlist from the design system
  - automated runtime checks verify assembled UI against layout and accessibility rules
  - graceful fallback rendering defined for instances where generative UI assembly violates rules or encounters rendering errors

### 9. Stateless MCP 2026-07-28 Integration Planning (`MCP-STATELESS LOCK`)
- **Stateless HTTP Transport Architecture**:
  - Model Context Protocol (MCP) integrations planned using stateless HTTP transport complying with the MCP 2026-07-28 specification
  - session state persistence assigned to external data stores (Redis, Durable Objects, D1) rather than in-memory process state
  - required agent tools mapped against registered MCP servers and verified against `core/policies/mcp-tool-map.yaml` using `python3 core/scripts/validate-policy-consistency.py`

### 10. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **DAG Cycle Check** | $|L| = |V|$ | `python3 core/scripts/validate-graph.py` | 0 cycles; deterministic topological order |
| **Output Schema Gate** | Emits `technical-delivery-plan` | `python3 core/scripts/validate-contracts.py` | Valid schema; no SEO contracts |
| **INVEST Slice Cap** | Duration $\le 2\text{h}$ | Task estimate review | All tasks sized $\le 2\text{ hours}$ |
| **Autonomy Tier Gate** | Declared in Tiers 1–4 | Plan inspection | Valid Trust Ladder tier assigned |
| **Checkpoints Defined**| For plans $> 3$ steps | `grep -i "checkpoint" plan.json` | Checkpoint serialized at each phase |
| **Critical Path CPM** | Critical chain computed | CPM calculation script | Identified zero-float path |
| **MCP Stateless Gate** | Stateless HTTP SSE | Architecture inspection | 0 persistent WebSocket/stdio |
