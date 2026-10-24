## Project Manager Review Checklist

This reference checklist provides operational delivery coordination, multi-agent capacity planning, FinOps spend governance, and regulatory milestone verification criteria for project management to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across probabilistic delivery estimation, multi-agent DAG governance, token budget envelopes, Specification-Driven Development (SDD) enforcement, review queue dwell-time management, commit provenance tracking, and rollback readiness.

### 1. Probabilistic Delivery Estimation & Monte Carlo Modeling (`PROBABILISTIC-ESTIMATION LOCK`)
- **Statistical Confidence Percentiles (P85 Target)**:
  - delivery milestones involving AI-assisted development or stochastic agentic workflows avoid brittle single-point date commitments
  - schedules model statistical delivery distributions using Monte Carlo simulations ($N=10,000$ iterations) committing to $P_{85}$ confidence envelopes:
    $$P_{85} = \text{Quantile}_{0.85}\left(\sum_{i=1}^M T_{\text{task}, i}\right)$$
  - three-point PERT estimations calculated per work stream:
    $$\mu = \frac{O + 4M + P}{6}, \quad \sigma = \frac{P - O}{6}$$
    where $O$ is optimistic duration, $M$ is most likely duration, and $P$ is pessimistic duration
- **Buffer & Variance Contingency**:
  - explicit schedule buffers inserted between dependent phases to absorb model regression debugging and evaluation cycles
  - critical milestones require a minimum 20% variance contingency buffer before committing delivery dates to external stakeholders

### 2. Multi-Agent DAG Capacity & Orchestration Governance (`AGENT-CAPACITY LOCK` / `DAG-CYCLE-DETECTION-LOCK`)
- **Kahn's Algorithm Cycle Detection ($O(V+E)$)**:
  - all multi-agent task execution plans represented as formal Directed Acyclic Graphs (DAGs) using Kahn's algorithm or DFS cycle detection; cyclic dependencies ($A \rightarrow B \rightarrow A$) must fail-closed at plan validation before task dispatch
  - parallel execution branches enforce strict workspace and write-scope isolation; no two concurrent agents may possess write access to identical files or partitions
- **Blended Human-Agent Capacity Planning**:
  - sprint and release plans account for concurrent agent workload capacity, LLM provider rate limits (TPM / RPM), and token quotas alongside human engineering bandwidth
  - agent delegation graphs reviewed to ensure critical paths do not bottleneck on single rate-limited models or unavailable specialized agents

### 3. Topological Phase Ordering & Workspace Partition Isolation (`PARALLEL-PHASE-ISOLATION-LOCK`)
- **Topological Phase Progression**:
  - downstream execution phases must never initiate until all prerequisite predecessor outputs validate successfully against declared JSON schema contracts:
    ```json
    // POSITIVE: Topological Phase Scheduling in coordination-plan.json
    {
      "phase_id": "phase-2-implementation",
      "prerequisite_phases": ["phase-1-architecture-spec"],
      "prerequisite_artifacts": ["contracts/schemas/technical-delivery-plan.json"],
      "parallel_tasks": [
        {
          "task_id": "task-2a-backend",
          "assigned_role": "backend-developer",
          "write_scope": "internal/service/**"
        },
        {
          "task_id": "task-2b-frontend",
          "assigned_role": "frontend-developer",
          "write_scope": "web/src/**"
        }
      ]
    }
    ```
  - parallel tasks with conflicting write scopes (`write_scope` overlapping on identical directories or files) are rejected at planning time

### 4. Token FinOps, Cost Allocation & Spend Governance (`TOKEN-FINOPS LOCK`)
- **Exponential Burn Rate Monitoring & Circuit Breakers**:
  - every automated agent phase defines an explicit financial ceiling (maximum allowable dollar spend per feature or task)
  - token burn velocity tracked continuously ($B(t) = B_0 \cdot e^{kt}$); automated warning alerts trigger at 60% and 75% of budget allocation, and halt execution at 100% requiring human re-scoping
- **PromQL Operational Spend Alerts**:
  ```promql
  # Alert if project token burn velocity exceeds safety baseline
  rate(llm_project_tokens_total[1h]) > 100000
  
  # Trip circuit breaker if cumulative spend reaches 75% of budget
  (project_token_spend_usd / project_budget_usd) > 0.75
  ```

### 5. Specification-Driven Development (SDD) & Code Churn Defense (`AI-DEBT & SPECIFICATION LOCK`)
- **Contract-First Engineering Gates**:
  - engineering tasks must possess approved specification contracts (`contracts/schemas/technical-delivery-plan.json`, `feature-ticket.json`, or architecture ADR) before implementation begins; "prompt-and-pray" implementation without verified contracts rejected
- **GIST Technical Debt Ceilings**:
  - monitor Generated, Implicit, Systemic, and Tacit (GIST) code debt in repositories
  - 14-day code churn percentage bounded by:
    $$\text{Churn}_{14d} = \frac{\text{Lines Deleted}}{\text{Lines Added} + \text{Lines Deleted}} \times 100\% \le 8\%$$
  - AST code duplication percentage bounded by:
    $$\text{Duplication}_{\text{AST}} = \frac{\text{Cloned Tokens}}{\text{Total Tokens}} \times 100\% \le 15\%$$
  - exceeding debt ceilings immediately freezes new feature dispatch and mandates refactoring sprints

### 6. Reviewer Fatigue Mitigation & Approval Queue Dwell Time (`ANTI-FATIGUE & DWELL-TIME LOCK`)
- **Approval Optimization**:
  - human approval gates placed strictly on high-impact, risky, or irreversible actions (Tier 3/4); low-risk read-only steps run autonomously to prevent human reviewer burnout
- **Dwell-Time SLA Tracking**:
  - human review queue dwell time tracked; review bottlenecks exceeding 4 business hours escalated to prevent stalling downstream agent execution graphs:
    $$\text{DwellTime}_{\text{median}} \le 4.0\text{ hours}$$

### 7. Commit Provenance Tracking & Regulatory Governance (`COMMIT-PROVENANCE LOCK`)
- **Git Commit Provenance Tagging**:
  - commits generated by AI agents must record machine-readable provenance metadata in commit trailers:
    ```git
    commit 9b1deb4d3b7d4bad9bdd2b0d7b3dcb6d
    Author: Autonomous Implementer <agent@internal>
    Date:   2026-10-17 07:00:00 +0000

        feat: implement atomic lua inventory fencing

        Co-authored-by: AgentCoordinator <coordinator@internal>
        X-Agent-Model: anthropic/claude-3-5-sonnet-20241022
        X-Agent-Task-ID: 4b7b2521-7f8e-4a88-8254-8e1f592e3894
    ```
- **Regulatory Timeline Compliance (`AI-COMPLIANCE LOCK`)**:
  - project plans track live EU AI Act milestones: August 2026 transparency (Article 50) and GPAI governance gates enforced prior to release; Annex III high-risk compliance scheduled against December 2027 deadlines

### 8. Critical Path Dependencies & Rollout Playbooks
- **Critical Path Method (CPM) Chain Identification**:
  - coordination plans compute the project Critical Path:
    $$\text{Total Duration} = \max_{p \in \text{Paths}} \sum_{i \in p} t_i$$
  - all external dependencies (APIs, shared services, DB migrations) committed with named owners before sprint freeze
- **Rollback Playbooks & Staging Windows**:
  - release schedules include dedicated staging verification windows and automated canary evaluation periods prior to full traffic cutover
  - comprehensive rollback playbooks with verified recovery time objectives (RTO $\le 15\text{min}$) documented for every release

### 9. Operational Incident & Stalled Agent Escalation Protocols
- **Heartbeat & Liveness Monitoring**:
  - automated subagent tasks monitored via `progress.md` heartbeat timestamps; absence of heartbeat updates for $> 15\text{min}$ triggers a liveness alert
  - idling or circular looping tasks without forward progress for $> 30\text{min}$ cancelled via `manage_task(kill)` and escalated to Project Manager

### 10. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Monte Carlo P85** | P85 SLA committed | `python3 scripts/monte_carlo_sim.py` | 85% probability buffer included |
| **DAG Cycle Check** | $|L| = |V|$ | `python3 core/scripts/validate-graph.py` | 0 cycles; deterministic topological sort |
| **Token Budget Cap** | Spend $\le 100\%$ budget | Prometheus `project_token_spend_usd` | Zero unauthorized budget overruns |
| **GIST Debt Ceiling** | Churn $\le 8\%$, Dup $\le 15\%$ | `jscpd src/ && git log --numstat` | Churn and duplication within limits |
| **Dwell-Time SLA** | Dwell $\le 4\text{h}$ median | Jira / Linear review queue analytics | Median queue dwell $\le 4.0\text{h}$ |
| **Commit Lineage** | Trailers present | `git log -n 5 --format="%(trailers)"` | `Co-authored-by` and `X-Agent-Model` valid |
| **Delivery Contract**| Valid `coordination-plan.json` | `python3 core/scripts/validate-contracts.py` | 100% schema compliant |
| **Heartbeat SLA**   | Progress update $\le 15\text{min}$| Heartbeat daemon check | 0 stale/hung subagents |
