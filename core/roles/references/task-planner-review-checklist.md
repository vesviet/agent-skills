## Task Planner Review Checklist

This reference checklist provides operational task decomposition, execution sequencing, agentic autonomy calibration, and delivery planning criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across Directed Acyclic Graph (DAG) task slicing, Trust Ladder autonomy tier declarations, background agent UX contracts, Generative UI (GenUI) governance planning, stateless MCP protocol alignment, EU AI Act regulatory milestone tracking, CI evaluation gates, and blast-radius mitigation.

### 1. Work Breakdown Structure (WBS) & DAG Task Decomposition
- **Atomic, Testable Execution Slices**:
  - large feature or refactoring initiatives decomposed into discrete, ordered tasks with explicit preconditions, inputs, deliverables, and definition of done
  - each task step specifies an exact owning role (`Role: **Role Name**`) that possesses the required skills in its declared Primary or Supporting toolbox
  - tasks organized as a valid Directed Acyclic Graph (DAG); circular dependencies eliminated; parallel branches explicitly specify write-scope boundaries
- **Separation of Exploration and Commitment**:
  - architectural spikes, proof-of-concept tests, and technical discovery separated from implementation tasks; discovery exit criteria defined before commit phases begin

### 2. Trust Ladder Autonomy Tier Calibration (`TRUST-LADDER LOCK`)
- **Explicit Autonomy Tier Declaration**:
  - every agentic or automated feature explicitly declares its operating autonomy tier in planning artifacts:
    1. **Tier 1 (Suggest)**: Agent proposes action/code; human executes
    2. **Tier 2 (Verify)**: Agent drafts implementation; human reviews and confirms before execution
    3. **Tier 3 (Delegate)**: Agent executes routine tasks autonomously; pauses for approval on high-risk boundaries
    4. **Tier 4 (Automate)**: Agent executes full pipeline autonomously within predefined operational envelopes
- **Anti-Autopilot Trap**:
  - unearned autonomy tiers prohibited; new agentic capabilities must demonstrate reliable performance at Suggest/Verify before promoting to Delegate/Automate

### 3. Background Agent UX & Async Interruption Contracts (`BACKGROUND-AGENT-UX LOCK`)
- **Status Surfaces & Progress Notification**:
  - long-running background agent workflows include explicit UX specifications for real-time progress surfaces, status indicators, and notification contracts
  - notifications define trigger events, severity tiers, and clear call-to-action responses
- **Asynchronous Interruptibility & Cancellation**:
  - background tasks must support non-destructive pause, redirect, and cancellation controls without leaving corrupted state or orphaned resources
  - task completion handoff specifies what summary data is presented to the user for review

### 4. Generative UI (GenUI) Governance Planning (`GENUI-GOVERNANCE LOCK`)
- **Component Palette & Assembly Constraints**:
  - dynamically assembled or AI-generated user interfaces mandate an explicit component allowlist from the design system
  - forbidden component combinations and brand-safety boundaries specified
- **Drift Detection & Safe Fallback**:
  - automated runtime checks verify assembled UI against layout and accessibility rules
  - graceful fallback rendering defined for instances where generative UI assembly violates rules or encounters rendering errors

### 5. Stateless MCP 2026-07-28 Integration Planning (`MCP-STATELESS LOCK`)
- **Stateless HTTP Transport Architecture**:
  - Model Context Protocol (MCP) integrations planned using stateless HTTP transport complying with the MCP 2026-07-28 specification
  - session state persistence assigned to external data stores (Redis, Durable Objects, D1) rather than in-memory process state
- **Tool Catalog Mapping**:
  - required agent tools mapped against registered MCP servers and verified against `core/policies/mcp-tool-map.yaml`

### 6. EU AI Act Article 50 & Regulatory Deadline Planning (`EU-AI-ACT-DISCLOSURE LOCK`)
- **Mandatory Disclosure Component Scheduling**:
  - user-facing AI interaction plans include Article 50 transparency disclosure components rendered prior to first user engagement
  - synthetic media generation plans incorporate C2PA Content Credentials and machine-readable metadata marking
- **Regulatory Timeline Alignment**:
  - delivery milestones align with live EU AI Act deadlines: Article 50 transparency enforcement and GPAI governance live as of August 2026

### 7. Automated Continuous Evaluation Gates (`EVAL-GATE LOCK`)
- **Golden Dataset & Benchmark Gating**:
  - prompt modifications, LLM model migrations, or tool additions plan automated CI evaluation gates
  - evaluations test against versioned golden prompt/response datasets with calibrated judge scoring ($\ge 85\%$ human agreement threshold)
- **Regression Detection**:
  - accuracy, hallucination, and latency regression thresholds established before deployment

### 8. Blast Radius Control, Checkpoints & Rollback Strategy
- **Risk Blast Radius Containment**:
  - tasks that touch shared data, production configuration, or external payment rails define explicit blast-radius boundaries
  - checkpoints inserted before irreversible steps; rollback steps and recovery playbooks documented for each delivery slice
