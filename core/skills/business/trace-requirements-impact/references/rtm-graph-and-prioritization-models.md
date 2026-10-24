# Requirements Traceability Matrix (RTM) & Prioritization Models

> Authoritative guide for bidirectional requirements traceability, BFS blast-radius analysis, and BABOK v3 prioritization frameworks.

---

## 1. Bidirectional Requirements Traceability Matrix (RTM)

Traceability ensures full accountability across the software engineering lifecycle.

```
[ L1: Business Need ]  ──► "Reduce customer checkout abandonment by 15%"
       │
[ L2: Business Req ]   ──► "Support one-click guest checkout without mandatory password"
       │
[ L3: Functional Spec] ──► "UC-CHK-002: Guest Checkout via Tokenized Apple Pay / Google Pay"
       │
[ L4: Architecture ]   ──► "ADR-014: Idempotent Payment Intent Service via Stripe Webhooks"
       │
[ L5: Test Cases ]     ──► "TC-E2E-CHK-011: Guest completes checkout in < 30 seconds"
```

### RTM Table Schema

| Req ID | Business Goal | Functional Spec | Component / ADR | Test Case ID | Status | Owner |
|---|---|---|---|---|---|---|
| `REQ-CHK-01` | Reduce churn | `UC-CHK-002` | `payment-service` / `ADR-14` | `TC-CHK-011` | Approved | @business-analyst |
| `REQ-CHK-02` | PCI Compliance | `UC-CHK-005` | `token-vault` / `ADR-09` | `TC-SEC-004` | Approved | @security |

---

## 2. BFS Impact Analysis for Change Requests

When a stakeholder requests a change mid-flight, gut-feel approvals cause unexpected regressions. A structured Breadth-First Search (BFS) identifies the true blast radius.

### The 3-Hop Traversal Algorithm
1. **Queue root node**: `queue.push(target_requirement_id)`
2. **Hop 1 (Immediate Scope)**:
   - Identify sibling requirements sharing the same business rule or entity model.
   - Flag acceptance criteria requiring modification.
3. **Hop 2 (Technical & Architectural Scope)**:
   - Traverse to linked API contracts (`contracts/schemas/*.json`), DB tables, and services.
   - Inspect NFR thresholds (Latency, throughput, encryption).
4. **Hop 3 (Verification & Downstream Scope)**:
   - Locate automated unit, integration, and E2E test scripts.
   - Identify external documentation and operational runbooks.

### Change Impact Assessment Report Format

```markdown
# Change Request Impact Assessment: CR-2026-042

## 1. Change Summary
- **Request**: Add real-time carbon footprint calculation during flight selection.
- **Requester**: Commercial Director
- **Anchor Requirement**: REQ-FLIGHT-014 (Flight Search Results Display)

## 2. Blast Radius Summary
- **Direct Requirements Affected**: 4 (REQ-014, REQ-018, REQ-021, REQ-033)
- **Architectural Components Impacted**: 2 (Search Aggregator Service, Pricing Engine)
- **NFR Conflicts Detected**:
  - *CRITICAL CONFLICT*: `NFR-PERF-003` mandates flight search p99 latency <= 350ms. Calling external emission calculator synchronously adds 450-800ms latency.
- **Impacted Test Cases**: 9 automated E2E tests

## 3. Recommendation & Options
- **Option A (Reject Synchronous Execution)**: Rejection of real-time third-party call on search page.
- **Option B (Recommended - Asynchronous Caching)**: Pre-calculate average route emissions offline and store in ClickHouse/Redis; latency impact < 2ms.
- **WSJF Score**: 14.5 (High user value, low duration under Option B).
```

---

## 3. The 4 BABOK v3 Prioritization Models

### Model 1: WSJF (Weighted Shortest Job First)
The industry standard for Agile backlogs to maximize economic value throughput:

$$\text{WSJF} = \frac{\text{Cost of Delay (CoD)}}{\text{Job Size (Duration)}}$$

Where:
$$\text{Cost of Delay} = \text{User-Business Value} + \text{Time Criticality} + \text{Risk Reduction / Opp Enablement}$$

All parameters scored using Fibonacci scale ($1, 2, 3, 5, 8, 13, 20$).

| Feature / Requirement | User Value | Time Crit | Risk Red | CoD | Job Size | WSJF Score | Rank |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Biometric Auth Login** | 8 | 5 | 5 | 18 | 3 | **6.0** | 1 |
| **PDF Invoice Export** | 5 | 3 | 2 | 10 | 2 | **5.0** | 2 |
| **Dark Mode Theming** | 3 | 1 | 1 | 5 | 3 | **1.67** | 3 |

### Model 2: MoSCoW Analysis
Essential for fixed-deadline release gating:
- **Must Have (M)**: Non-negotiable. Without this, the release cannot launch legally or functionally. (Max 60% of total capacity).
- **Should Have (S)**: Important, but a viable manual or temporary workaround exists. (Approx 20% of capacity).
- **Could Have (C)**: Desirable enhancement if time and budget permit. (Approx 20% of capacity).
- **Won't Have (W)**: Explicitly agreed out of scope for this release cycle; recorded in non-goals.

### Model 3: Impact vs Effort 2x2 Matrix
Ideal for visual stakeholder alignment workshops:
- **High Impact, Low Effort (Quick Wins)**: Do these immediately.
- **High Impact, High Effort (Major Projects)**: Plan carefully, decompose into MVPs.
- **Low Impact, Low Effort (Fill-ins)**: Execute during low-capacity periods.
- **Low Impact, High Effort (Thankless Tasks)**: Challenge, deprioritize, or eliminate.

### Model 4: Timeboxing & Capacity-Constrained Pruning
When sprint capacity is strictly capped (e.g. 50 story points) and stakeholders demand 75 points:
1. Rank all requirements strictly by WSJF.
2. Draw the hard cutoff line at cumulative 50 points.
3. Everything below the line is automatically pruned; produce a formal *Capacity Deficit Report* detailing the trade-off costs.
