## SDET Review Checklist

This reference checklist provides detailed evaluation harness, benchmark architecture, test automation, and failure triage validation criteria for SDET engineering to meet 2026–2027 Agentic SWE standards.

### 1. Agent Evaluation Harness & Benchmark Dataset Design
- **Stratified Test Dataset Architecture**:
  - benchmark suite incorporates representative golden input/output pairs, edge cases, and adversarial probe cases
  - dataset versioned and immutable; test sets strictly partitioned from training and few-shot prompt exemplars
  - ground-truth assertions clearly specify deterministic invariants alongside qualitative evaluation rubrics
- **Automated Runner Sandboxing**:
  - test runners execute in isolated, ephemeral sandboxes with restricted network and filesystem egress
  - environment state reset between evaluation runs to eliminate cross-test data pollution or state leakage

### 2. Model-Based Evaluator Calibration & Grading Rubrics
- **LLM-as-a-Judge Calibration**:
  - zero-shot judge models configured with temperature 0.0 to ensure deterministic scoring reproducibility
  - evaluation prompts provide explicit, anchored Likert grading scales (1–5) with concrete behavioral criteria for each tier
  - chain-of-thought rationale generation enforced before final numerical score output
- **Deterministic Assertion Pre-Flight**:
  - deterministic validations (exact keyword matching, regex patterns, schema conformance) executed prior to model-based evaluation
  - model-based evaluation dispatched only when preliminary deterministic checks succeed

### 3. Failure Taxonomy Classification & Defect Triage
- **Standard Defect Categorization**:
  - every evaluation failure mapped to an unambiguous defect category:
    - `schema_violation`: output invalid against Draft 2020-12 contract
    - `hallucination`: unsubstantiated factual claims not grounded in provided context
    - `goal_hijack`: model diverted from target objective by prompt injection or adversarial input
    - `trajectory_loop`: agent trapped in repetitive tool invocation loop without progress
    - `tool_breach`: unauthorized or invalid tool parameter usage violating action policies
    - `timeout`: execution exceeded deadline without producing terminal result
- **Regression Tracking & Telemetry**:
  - historical benchmark telemetry maintained across prompt iterations and model releases
  - failure clustering applied to isolate systemic root causes from stochastic variance

### 4. Flakiness Diagnostics & Asynchronous Test Stability
- **Timing & Race Condition Elimination**:
  - arbitrary fixed sleep intervals strictly prohibited; dynamic condition polling with explicit timeouts enforced
  - background servers and dependencies monitored via socket readiness polling (`with_server.py`) before test dispatch
  - asynchronous promises and event handlers bound to lifecycle cancellation tokens to prevent unhandled rejections
- **Deterministic Seed & Replay**:
  - pseudo-random test data generators seeded deterministically; failing seeds logged for exact local reproduction
  - flaky test detection gates run multi-iteration stress tests (e.g. 10x consecutive passes required before un-quarantining)

### 5. Combinatorial & Property-Based Test Engineering
- **Combinatorial Parameter Coverage**:
  - complex business input spaces covered via pairwise/all-pairs orthogonal arrays (e.g. PICT, AllPairs)
  - boundary values tested at $-1$, $0$, $+1$, empty, null, and maximum capacity limits
- **Property-Based Invariant Verification**:
  - serialization/deserialization routines tested for round-trip idempotency across thousands of generated inputs
  - state machine transition matrices verified against illegal state progression attacks

### 6. Continuous Quality Release Gates & Promotion Policies
- **Strict Quantitative Gate Thresholds**:
  - release promotion requires overall evaluation pass rate $\ge 90\%$
  - zero tolerance for critical safety, prompt injection, or security boundary violations
  - composite evaluation score $\ge 0.85$ across all benchmark dimensions
- **Fail-Closed Release Enforcement**:
  - automated CI gates block deployment if evaluation fails or error rates exceed statistical error margins
  - contract regression gate blocks merges if modified code violates consumer-driven contracts or schemas

### 7. Contract Emission & Downstream Reporting
- **Draft 2020-12 Contract Compliance**:
  - evaluation results emitted conformant to `contracts/schemas/agent-eval-report.json`
  - reports contain run metadata, per-evaluator metrics, rubric breakdowns, and granular failure classification records
  - evaluation artifacts uploaded to persistent observability stores for auditability
