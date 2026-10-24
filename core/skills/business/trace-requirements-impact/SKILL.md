---
name: trace-requirements-impact
description: Build Requirements Traceability Matrices (RTM), run BFS change-request impact analysis across requirements to test cases, and prioritize backlogs using BABOK v3 models (MoSCoW, WSJF, Impact/Effort, Timeboxing). Use when assessing change requests, evaluating regression blast radiuses, prioritizing sprint scope, or maintaining end-to-end compliance audit trails.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Trace Requirements Impact

Use this skill to maintain bidirectional requirement traceability, perform automated blast-radius impact analysis on Change Requests (CRs), and calculate objective backlog priority scores using BABOK v3 frameworks.

## When to Use

- a stakeholder requests a mid-project change ("can we add feature X?")
- identifying all test cases, components, and contracts affected by a requirement modification
- building and maintaining the Requirements Traceability Matrix (RTM)
- prioritizing competing backlog items when engineering capacity is constrained
- resolving conflicts between functional scope and non-functional requirements (NFRs)
- preparing compliance audit trails proving every requirement has verifying test cases

## Core Rules

- **Enforce Bidirectional Traceability**: maintain unbroken dependency links across all 5 requirement lifecycle layers:
  `Business Need` ──► `Business Requirement` ──► `Functional/Solution Spec` ──► `Architecture/ADR` ──► `Test Cases`
  - *Forward Traceability*: verify that every business need is satisfied by concrete functional specs and test cases
  - *Backward Traceability*: verify that no code or feature exists without tracing to an approved business need (bans gold-plating)
- **Execute BFS Impact Traversal on Change Requests**: when a Change Request (CR) is submitted, traverse the dependency graph breadth-first up to 3 hops:
  - *Hop 1*: Direct requirement children and neighboring business rules
  - *Hop 2*: Architectural components, database schemas, and external API contracts
  - *Hop 3*: Automated test suites, integration fixtures, and compliance documentation
- **Select Context-Appropriate Prioritization Model**:
  - **MoSCoW**: apply for fixed-deadline, fixed-date milestone commitments (Must = non-negotiable core; Should = important workaround exists; Could = nice to have; Won't = deferred)
  - **WSJF (Weighted Shortest Job First)**: apply for Agile backlogs to maximize economic flow: $\text{WSJF} = \frac{\text{Cost of Delay (CoD)}}{\text{Job Size / Duration}}$
  - **Impact vs Effort Matrix**: apply during executive workshops with non-technical leaders (Quick Wins, Major Projects, Fill-ins, Thankless Tasks)
  - **Timeboxing / Capacity Budgeting**: apply when total sprint capacity is fixed; items exceeding capacity ceiling are systematically pruned
- **Detect & Flag NFR Conflicts**: every change impact assessment must cross-check Non-Functional Requirements (latency budgets, security boundaries, concurrent user limits, regulatory retention)
- Detailed algorithms, matrix schemas, and case studies: [`references/rtm-graph-and-prioritization-models.md`](references/rtm-graph-and-prioritization-models.md)

## Suggested Process

### 1. Ingest Change Request & Map Anchor Node
Receive the proposed requirement change or feature request. Locate the anchor node in the Requirements Traceability Matrix (RTM).

### 2. Run Graph Impact Traversal (BFS)
Execute a breadth-first search traversing upstream drivers and downstream dependents. Collect all affected user stories, acceptance criteria, schema contracts, UI components, and test cases.

### 3. Evaluate NFR Trade-Offs & Blast Radius
Cross-reference impacted nodes against the system NFR registry. Identify conflicts (e.g. real-time calculation vs API p99 latency SLA). Formulate mitigation proposals.

### 4. Calculate Prioritization Score
Apply the chosen framework (WSJF score or MoSCoW tier). Compute Cost of Delay based on business value, time criticality, and risk reduction.

### 5. Generate Impact Assessment Report
Produce a structured Change Impact Assessment containing: blast radius summary table, affected artifacts count, cost/delay estimate, and recommendation (Accept, Accept with Conditions, Defer, or Reject).

## Checklist

- [ ] anchor requirement identified and linked to business objective
- [ ] BFS impact traversal executed; all downstream specs and tests cataloged
- [ ] potential NFR violations (performance, security, scalability) checked
- [ ] backlog priority calculated using explicit formula (WSJF or MoSCoW)
- [ ] mitigation options provided for high-impact change requests
- [ ] change impact assessment delivered in structured Markdown table

## Related Skills

- **elicit-requirements**: structured questioning and BABOK v3 requirement quality audits
- **write-use-cases**: structure user interactions into Karl Wiegers 13-field templates
- **analyze-business-requirements**: analyze and write implementation-ready requirements
- **agent-delegation**: delegate tasks across agent swarms with structured handoffs
