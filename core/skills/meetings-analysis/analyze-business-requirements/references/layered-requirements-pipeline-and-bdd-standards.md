# Layered Requirements Pipeline & BDD Specification Standards

> Authoritative reference guide for the 4-tier Layered Requirements Pipeline (Impact Mapping → Event Storming → Story Mapping → BDD Gherkin), stateful invariants, and machine handoff via `core/contracts/schemas/feature-ticket.json`.

---

## 1. The 4-Tier Layered Requirements Pipeline

Modern requirements engineering prevents scope creep and architectural misalignment through a progressive 4-tier refinement funnel:

```
[ Tier 1: Impact Mapping ]     ──► WHY & WHO: Strategic goals, actors, KPI metrics
        │
        ▼
[ Tier 2: Event Storming ]     ──► WHAT & FLOW: Domain Events (past tense), Commands, Aggregates
        │
        ▼
[ Tier 3: Story Mapping ]      ──► HOW & SLICES: Backbone, Walking Skeleton, vertical slices
        │
        ▼
[ Tier 4: Executable BDD ]     ──► VERIFICATION: Given/When/Then, stateful invariants, failure guarantees
```

### Tier Mapping Matrix:
| Pipeline Tier | Core Question | Primary Artifact | Key Invariants | Downstream Consumer |
| :--- | :--- | :--- | :--- | :--- |
| **1. Impact Mapping** | Why & Who? | Goal $\to$ Actor $\to$ Impact $\to$ Deliverable tree | Every feature traces to a business metric; bans vanity features | Product Manager, Business Sponsor |
| **2. Event Storming** | What & Flow? | Timeline of Domain Events, Commands, Aggregates | Events strictly past tense; bounded contexts mapped; no entity smuggling | Solution Architect, Technical Architect |
| **3. Story Mapping** | How & Slices? | 2D User Story Map (Patton Backbone + Slices) | Walking skeleton connects all layers end-to-end; INVEST criteria | Technical Lead, Scrum Team |
| **4. BDD Specifications**| How to Verify?| Given/When/Then scenarios with BVA matrices | Single-Action Invariant; stateful conservation laws; failure guarantees | QA Automation Engineer, Developers |

---

## 2. BDD Gherkin Syntactic Precision & Invariants

### 2.1 The Single-Action Invariant
In production-grade BDD, the `When` clause must represent exactly ONE discrete state transition:
- **Violating Pattern**: `When user enters PIN and clicks Submit and authorizes transfer`
- **Compliant Pattern**: `When the customer confirms the wire transfer`

### 2.2 Stateful System Invariants
Acceptance criteria must assert that system conservation laws are never violated:
- **Financial Balance Conservation**:
  $$\sum \text{Debits} \equiv \sum \text{Credits}$$
- **Inventory Non-Negativity**:
  $$\text{StockAvailable} = \text{StockOnHand} - \text{StockAllocated} \ge 0$$
- **Audit Immutability**:
  Every state transition must emit an immutable Domain Event with UUIDv7 timestamp.

### 2.3 Explicit Failure Guarantees
Negative scenarios must specify the postcondition state when an exception or timeout occurs:
```gherkin
@negative @boundary
Scenario: Insufficient funds rejects transfer atomically
  Given customer account has available balance of 50.00 USD
  When customer requests transfer of 100.00 USD
  Then transfer request is rejected with error code "ERR_INSUFFICIENT_FUNDS"
  And customer account available balance remains exactly 50.00 USD
  And zero journal legs are committed to the ledger
  And failure guarantee: zero partial state mutations, zero funds deducted
```

---

## 3. Boundary Value Analysis (BVA) & Pairwise Decision Tables

Input domains must be partitioned into equivalence classes with explicit boundary testing:

```
Boundary Range: [-∞, Min-1] | [Min] | [Min+1, Max-1] | [Max] | [Max+1, +∞]
Partitions:     [ Invalid ]  [ BVA ]     [ Valid ]     [ BVA ]  [ Invalid ]
```

### Production Decision Table Schema:
| Vector ID | Amount ($) | Account Tier | KYC Status | Result | State Transition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-BVA-01` | $0.00 | Standard | Verified | Reject: `INVALID_AMOUNT` | None |
| `TC-BVA-02` | $0.01 (Min) | Standard | Verified | Approved (Base Fee) | State: `PROCESSED` |
| `TC-BVA-03` | $9,999.99 | Standard | Verified | Approved (Tier 1 Fee)| State: `PROCESSED` |
| `TC-BVA-04` | $10,000.00 | Standard | Verified | Escalate: `AML_REVIEW` | State: `PENDING_AML` |
| `TC-BVA-05` | $50,000.01 | Standard | Verified | Reject: `LIMIT_EXCEEDED`| None |

---

## 4. Probabilistic Acceptance Criteria & AI Governance

For non-deterministic AI and LLM features, binary pass/fail criteria are strictly replaced by statistical confidence envelopes:

$$\mathbb{P}\left(\text{Metric}(Y_{\text{generated}}, Y_{\text{ground\_truth}}) \ge \tau\right) \ge 1 - \alpha \quad \text{over } N \ge 500 \text{ evaluation samples}$$

### The 4-Part AI AC Spec:
1. **Behavioral Envelope**: Range of acceptable responses, tone, factual accuracy bounds, forbidden topics.
2. **Statistical Threshold**: Minimum accuracy / precision / recall percentage over moving window of $N$ samples.
3. **Evaluation Judge & Benchmark**: LLM-as-Judge (DeepEval, RAGAS with named model/rubric) or curated Golden Benchmark dataset.
4. **Degradation Alert**: Automated trigger halting autonomous actions and notifying on-call SME if accuracy drops below threshold in production.

---

## 5. Machine Handoff via `feature-ticket.json`

All analyzed requirements must be serialized into the canonical `core/contracts/schemas/feature-ticket.json` format:
- `vertical_slice_metadata`: Pattern (workflow step, rule variation), INVEST checklist, walking skeleton flag.
- `event_storming_context`: Bounded context, aggregate root, past-tense domain events, commands, read models.
- `ai_feature_spec`: Behavioral boundaries, probabilistic AC, HITL escalation triggers, EU AI Act risk tier.
- `agentic_feature_spec`: Autonomy level (L1–L5), MCP per-invocation permissions, forbidden zones, kill-switch.
- `responsible_ai_spec`: Four-Fifths Rule ($\text{DIR} \ge 0.80$), subgroup error bounds, XAI four pillars.
- `nfr_envelope`: Latency p99 budgets, error ceilings, GDPR Article 6 legal basis, Right to Erasure cascade SLAs.
