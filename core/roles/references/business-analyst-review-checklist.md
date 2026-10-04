## Business Analyst Review Checklist

This reference checklist provides detailed requirements engineering, behavioral specification, domain modeling, and governance verification criteria for Business Analysis to meet 2026–2027 SOTA standards. It synthesizes Modern Requirements Engineering across Domain-Driven Design (DDD) Event Storming, Behavioral Acceptance Criteria (BDD / Gherkin), AI/LLM Probabilistic Specifications, Agentic MCP Governance, Vertical Slice Decomposition, Disciplined BABOK v3 Elicitation, Bidirectional Traceability (RTM), and Machine Handoff Contracts (`feature-ticket.json`).

---

### 1. Requirements Quality & BABOK v3 Nine Criteria Compliance
- **Atomicity & Separation of Concerns**:
  - [ ] every requirement statement represents exactly one business need; zero compound clauses conjoined with "and", "or", "as well as", or "in addition to"
  - [ ] functional requirements strictly separated from non-functional constraints, technical implementations, and project management scheduling
- **Completeness & Invariant Specification**:
  - [ ] requirements state all preconditions, triggers, actor roles, normal paths, alternative branches, and postcondition guarantees
  - [ ] zero "happy-path only" specifications; system state explicitly defined for error, timeout, and cancellation states
- **Consistency & Contradiction Elimination**:
  - [ ] zero internal conflicts between functional user stories and adjacent business policies, accounting rules, or regulatory statutes
  - [ ] domain terminology aligned with the organization's standardized Ubiquitous Language; zero synonymous terms used interchangeably for distinct entities
- **Conciseness & Fluff Elimination**:
  - [ ] all passive voice, narrative filler, and marketing buzzwords removed; requirements formulated as declarative, active-voice statements
  - [ ] subjective and non-verifiable adjectives ("fast", "user-friendly", "robust", "scalable", "seamless", "intuitive") strictly banned
- **Feasibility & Architectural Envelopes**:
  - [ ] requirements verified as technically viable within existing infrastructure limits, budget parameters, and latency budgets
  - [ ] technical feasibility vetted with Technical Lead / Architect prior to requirement baseline freeze
- **Unambiguity & Single-Interpretation Standard**:
  - [ ] requirements admit exactly one interpretation by developers, QA automation engineers, and business stakeholders
  - [ ] domain-specific calculations and formulas expressed with explicit mathematical operator precedence and rounding rules
- **Testability & Objective Verifiability**:
  - [ ] every requirement has at least one deterministic or probabilistic verification procedure with unambiguous pass/fail criteria
  - [ ] unverifiable quality goals translated into measurable SLA / SLO metrics (e.g. "p99 latency < 250ms under 5,000 req/sec")
- **Prioritization & Economic Ranking**:
  - [ ] every backlog item assigned an objective prioritization score using WSJF (Weighted Shortest Job First) or MoSCoW under fixed-capacity limits
  - [ ] priority reflects business value, time criticality, and risk reduction—not stakeholder title or political urgency
- **Understandability & Dual-Audience Accessibility**:
  - [ ] requirements clear and comprehensible to both business domain sponsors and software engineering teams without requiring oral translation

---

### 2. Stakeholder Discovery, Funnel Questioning & Tacit Knowledge Elicitation
- **Funnel Questioning Protocol Execution**:
  - [ ] stakeholder interviews structured sequentially through Open-ended (macro context, workflows), Probing (exceptions, volumes, edge cases), and Closed (explicit locks, invariant confirmation) phases
  - [ ] interview questions avoid leading the witness or embedding preconceived architectural solutions
- **Colombo Probing for Tacit Knowledge**:
  - [ ] deliberate structured curiosity applied to uncover unwritten organizational habits, manual batch jobs, and shadow workarounds
  - [ ] "naive" boundary questions asked to challenge "obvious" tribal concepts and implicit operational defaults
- **Anti-Rationalization & System 2 Reflective Pause**:
  - [ ] BA conducts a reflective self-audit before finalizing tickets: "Did I assume unstated business logic? Are numerical targets verified by data?"
  - [ ] unverified stakeholder statements documented as formal Open Questions with proposed interpretations rather than accepted as facts

---

### 3. Cockburn Scoping & Karl Wiegers 13-Field Use Case Verification
- **Cockburn Scoping & The Coffee-Break Test**:
  - [ ] use cases scoped at the **User-Goal Level (Blue)**: represents an Elementary Business Process (EBP) completed by one person in one sitting (2–30 minutes) leaving data in a consistent state
  - [ ] long-running workflows spanning days or departments classified as **Summary Level (White)** and decomposed into discrete user-goal use cases
  - [ ] tactical micro-actions taking seconds (e.g. "Validate OTP", "Click Submit") classified as **Subfunction Level (Black)** and nested within parent use cases
- **Karl Wiegers 13-Field Production Template Adherence**:
  - [ ] all 13 fields fully articulated: 1. UC ID, 2. Title (Active Verb + Noun), 3. Scope & Goal Level, 4. Primary Actor, 5. Secondary Actors/Systems, 6. Preconditions, 7. Trigger, 8. Normal Course, 9. Alternative Courses, 10. Exception Courses, 11. Postconditions, 12. Business Rules Referenced, 13. Assumptions & Open Questions
  - [ ] Normal Course contains 4–9 numbered happy-path steps alternating between Actor Action and System Response; zero embedded `if/else` logic
  - [ ] all Alternative and Exception courses explicitly anchored to specific Normal Course step numbers (e.g. `4a. Payment authorization rejected`)
- **Explicit Failure Guarantees & Zero GUI Mechanics**:
  - [ ] Postconditions define both the **Success Guarantee** and the **Minimal / Failure Guarantee** (system state when transaction aborts)
  - [ ] UI micro-mechanics ("clicks button", "selects dropdown", "enters text") completely eliminated in favor of domain semantic verbs ("submits credentials", "selects fulfillment method")

---

### 4. Domain-Driven Design (DDD) & Event Storming Invariants
- **Event Storming Timeline Syntax & Semantics**:
  - [ ] **Domain Events** expressed as immutable facts in past tense (e.g. `OrderPlaced`, `AccountDebited`, `ClaimApproved`); zero active verbs
  - [ ] **Commands** expressed in present imperative tense representing user or system intent (e.g. `PlaceOrder`, `DebitAccount`, `ApproveClaim`)
  - [ ] **Aggregates** explicitly identified as transactional consistency boundaries enforcing business invariants
  - [ ] **Business Policies** defined declaratively as `Whenever [Domain Event] Then [Command]`
- **Bounded Context Boundaries & Context Mapping**:
  - [ ] distinct bounded contexts established; zero "Entity Smuggling" (e.g. reusing a monolithic `User` across Auth, Billing, and Shipping)
  - [ ] upstream/downstream integration relationships defined using DDD patterns (Shared Kernel, Customer-Supplier, Conformist, Anti-Corruption Layer - ACL)
  - [ ] Core Domains differentiated from Supporting and Generic Subdomains; core competitive logic receives highest analytical depth

---

### 5. Vertical Slice Decomposition, Walking Skeletons & User Story Mapping
- **Elephant Carpentry & The 8 Slicing Patterns**:
  - [ ] stories decomposed vertically across all architectural tiers (UI, API, Domain, DB) rather than horizontally by technical layer
  - [ ] slicing patterns applied deliberately: By Workflow Step, By Business Rule Variation, By Data Channel, By User Persona, By Major Effort vs Variation, By CRUD Operation, By Non-Functional SLA, or By Reversibility
- **INVEST Quality Verification**:
  - [ ] **I**ndependent: stories can be released and tested in any sequence without hard pipeline coupling
  - [ ] **N**egotiable: captures the essence of what is needed while leaving room for engineering trade-offs
  - [ ] **V**aluable: delivers observable value to an end customer or downstream consumer
  - [ ] **E**stimable: scope and complexity are sufficiently clear for engineering sizing
  - [ ] **S**mall: sized to complete within a fraction of a sprint (typically 1–3 days of engineering effort)
  - [ ] **T**estable: acceptance criteria provide unambiguous, objective pass/fail proof
- **Walking Skeleton & Tracer Bullets**:
  - [ ] the first vertical slice in an epic delivers an ultra-thin end-to-end "walking skeleton" connecting all tiers to validate architecture early
- **Story Mapping & Opportunity Solution Trees**:
  - [ ] backbone user activities mapped horizontally; release slices defined vertically by value threshold
  - [ ] solutions linked to verified customer opportunities via Opportunity Solution Trees (OST); feature requests without verified opportunity trees rejected

---

### 6. Behavioral Acceptance Criteria (BDD / Gherkin) & Equivalence Partitioning
- **Strict BDD Syntactic Invariants**:
  - [ ] scenarios authored in `Given [Precondition State] When [Action] Then [Expected Observable Outcome]` format
  - [ ] **Single-Action Invariant**: the `When` step contains exactly ONE discrete action verb; chained actions conjoined with "and" are refactored
  - [ ] context independence guaranteed: scenarios do not rely on state from previous scenario executions
- **Stateful Invariants & Conservation Laws**:
  - [ ] `Then` assertions verify both the primary business outcome AND system conservation invariants (e.g. $\sum \text{Debits} \equiv \sum \text{Credits}$, inventory balance non-negativity)
  - [ ] failure guarantees specified for negative scenarios (zero database mutations, rollback verified, audit events emitted)
- **Boundary Value Analysis (BVA) & Pairwise Matrices**:
  - [ ] input domains partitioned into valid and invalid equivalence classes; boundary values (Min-1, Min, Min+1, Max-1, Max, Max+1) explicitly tested
  - [ ] multi-variable combinations mapped into combinatorial pairwise decision tables in the ticket body

---

### 7. AI/LLM Probabilistic Acceptance Criteria & Statistical Bounds
- **Probabilistic Behavioral Specifications**:
  - [ ] binary pass/fail AC strictly banned for non-deterministic AI/LLM outputs; requirements define behavioral envelopes and acceptable intent ranges
  - [ ] statistical acceptance thresholds specified over sample windows: e.g. "System must achieve $\ge 95\%$ factual accuracy over rolling window of $N \ge 1,000$ production queries"
- **Evaluation Harness & Ground Truth Benchmarks**:
  - [ ] evaluation method explicitly declared: automated LLM-as-Judge (with named model and rubric), human SME panel, or curated golden dataset
  - [ ] judge identity, scoring rubric, and benchmark dataset location referenced in the ticket
- **Production Degradation Alerting**:
  - [ ] automated degradation trigger specified: concrete threshold (e.g. accuracy $< 90\%$ for 48h) that triggers an automated incident, halts autonomous actions, and reverts to manual or deterministic fallback
- **Hybrid Architecture Demarcation**:
  - [ ] strict boundary declared between deterministic rule-based logic (financial calculation, legal notice dispatch, database mutation) and AI probabilistic inference (summarization, draft generation, classification)

---

### 8. Human-in-the-Loop (HITL) Governance & Escalation Protocols
- **Mandatory HITL Escalation Triggers**:
  - [ ] every AI decision path with financial, legal, medical, safety, or access-control impact has explicit escalation trigger conditions (e.g. confidence score $\theta < 0.85$, loan amount $> 100,000,000\text{ VND}$)
  - [ ] escalation action specified: pause workflow, flag status as `UNDER_REVIEW`, route to human reviewer queue
- **Operational SLA & Responsible Roles**:
  - [ ] designated responsible role named for review (e.g. "Senior Credit Officer"); maximum response SLA defined (e.g. "within 4 hours")
  - [ ] secondary escalation path specified if primary reviewer fails to action ticket within SLA window
- **Immutable Audit Logging Schema**:
  - [ ] mandatory audit log fields specified: model version, prompt hash, input feature vector, output confidence score, human reviewer ID, final decision token, override reason, and millisecond timestamps

---

### 9. Agentic AI Autonomy (L1–L5), MCP Least-Privilege & Kill-Switch Safeguards
- **Autonomy Level Declaration & Governance Ceiling**:
  - [ ] agentic feature tickets explicitly declare intended autonomy level (L1 Assistive, L2 Task-Based, L3 Conditional Orchestration, L4 High Autonomy, L5 Unbounded)
  - [ ] L3 (Conditional) enforced as enterprise production ceiling; any L4 proposal requires documented executive risk sign-off
- **MCP Tool Permissions & Attenuated Authority**:
  - [ ] per-tool permissions cataloged: read, write, delete, execute; granted strictly under least-privilege principles
  - [ ] **Attenuated Authority Invariant**: agent permissions must NEVER exceed the sponsoring user's rights at invocation time
  - [ ] authorization evaluated dynamically at each tool invocation; persistent static API credentials strictly prohibited
- **Forbidden-Zone Enumeration**:
  - [ ] hard boundary actions cataloged that the agent must NEVER execute under any circumstances (e.g. drop database tables, initiate unreviewed bank transfers, send unapproved external communications)
- **Emergency Kill-Switch Specification**:
  - [ ] hardware/software stop mechanism specified: procedure to halt executing agents, revoke tool credentials within $\le 60$ seconds, and preserve or rollback in-flight state
- **Agent Registry Launch Gate**:
  - [ ] ticket mandates that the agent must be registered in the enterprise agent inventory (ID, human owner, tool allowlist, autonomy ceiling) prior to deployment

---

### 10. Responsible AI, Bias Prevention (Four-Fifths Rule) & Explainability (XAI)
- **Four-Fifths Rule & Disparate Impact Ratio (DIR)**:
  - [ ] automated scoring or classification affecting protected groups specifies a Disparate Impact Ratio threshold: $\text{DIR} \ge 0.80$ across all protected classes
  - [ ] disaggregated error rates: False Negative Rate (FNR) and False Positive Rate (FPR) for any protected subgroup must not exceed $\pm 5\%$ of aggregate mean
  - [ ] intersectional bias testing required across multiple attributes (e.g. age $\times$ gender)
- **Explainability (XAI) Four-Pillar Verification**:
  - [ ] explanation type specified: contrastive ("Why X instead of Y?"), feature-attribution (SHAP/LIME scores), or counterfactual ("What must change to achieve Y?")
  - [ ] four verifiable criteria enforced in AC:
    - *Intelligibility*: explanation readable at an 8th-grade reading level by non-technical users
    - *Faithfulness*: explanation mathematically reflects actual model feature weights
    - *Actionability*: provides at least one concrete action the user can take to alter the outcome
    - *Accessibility*: rendered inline at the decision point, not buried in secondary documentation
- **Post-Market Fairness Monitoring**:
  - [ ] post-launch automated monitoring plan specified with alerts for statistical parity drift

---

### 11. Data Governance, GDPR Compliance & Privacy Lineage
- **GDPR Article 6 Legal Basis & Consent Management**:
  - [ ] lawful basis for data processing declared (Consent, Contract, Legal Obligation, Vital Interests, Public Task, Legitimate Interests)
  - [ ] consent capture mechanisms require explicit affirmative action; withdrawal parity enforced (withdrawing consent as easy as granting)
  - [ ] immutable consent audit log required for every grant and withdrawal event
- **Data Lineage & Provenance Mapping**:
  - [ ] data flow diagrams required tracing personal data across collection $\to$ ingestion $\to$ processing $\to$ storage $\to$ deletion
  - [ ] training data provenance documented for AI models ingesting user data; opt-out propagation verified
- **Right to Erasure (Article 17) & Retention Limits**:
  - [ ] erasure flow specified in AC: list of all downstream datastores, caches, and third-party processors that must receive deletion cascades
  - [ ] erasure propagation SLA defined (default $\le 30$ days; internal SLA target $\le 72$ hours) with automated verification tests
- **DPIA Triggers & ROPA Updates**:
  - [ ] Data Protection Impact Assessment (DPIA) trigger assessed; flagged as a blocking dependency if processing sensitive or profiling data
  - [ ] Records of Processing Activities (ROPA) update action item included for new data categories

---

### 12. Bidirectional Traceability (RTM) & Change Request Impact Analysis (BFS)
- **Bidirectional Traceability Chain**:
  - [ ] unbroken links maintained across all 5 layers: Business Need $\to$ Business Requirement $\to$ Functional Spec $\to$ Architecture ADR $\to$ Automated Test Cases
  - [ ] Forward Traceability: every business goal has verifying test cases
  - [ ] Backward Traceability: zero code or feature elements exist without tracing to an approved business need (bans gold-plating)
- **BFS Blast Radius Analysis on Change Requests**:
  - [ ] Breadth-First Search graph traversal executed on Change Requests (CRs) up to 3 hops:
    - *Hop 1*: Sibling requirements and immediate parent user stories
    - *Hop 2*: Architectural components, database schemas, and API contracts
    - *Hop 3*: Automated test suites, integration fixtures, and compliance audits
  - [ ] Change Impact Assessment delivered with affected artifacts count, cost/delay estimate, and recommendation (Accept, Defer, Reject)
- **Quantitative WSJF Prioritization**:
  - [ ] Backlog priority calculated using economic flow: $\text{WSJF} = \frac{\text{Cost of Delay}}{\text{Job Size}}$
  - [ ] Cost of Delay derived from User-Business Value, Time Criticality, and Risk Reduction

---

### 13. Non-Functional Requirements (NFR) & Architectural Envelopes
- **Quantitative Performance & Latency Budgets**:
  - [ ] p95 and p99 latency ceilings specified in milliseconds under defined concurrent load (e.g. "p99 < 350ms at 2,000 RPS")
  - [ ] throughput capacity targets specified in requests/sec or transactions/sec with peak burst multipliers
- **Availability, Reliability & Recovery Objectives**:
  - [ ] service availability SLA defined (e.g. 99.9% or 99.95%); error budget burn rate triggers specified
  - [ ] Recovery Time Objective (RTO) and Recovery Point Objective (RPO) defined for disaster recovery
- **Scalability, Storage & Retention Horizons**:
  - [ ] data growth models documented with projected 1-year and 3-year volumetric projections
  - [ ] data retention policies specified with automated purging or cold-storage archiving rules

---

### 14. Executable Contract Machine Handoff (`feature-ticket.json`) & Living Documentation
- **JSON Schema Draft 2020-12 Compliance**:
  - [ ] deliverable formatted as a valid `feature-ticket.json` artifact passing all JSON Schema Draft 2020-12 validations
  - [ ] machine discriminators (`contract_type: "feature-ticket"`) and required fields strictly populated
- **Living Assumption Register**:
  - [ ] all underlying beliefs and hypotheses cataloged in the assumption register
  - [ ] assumptions scored using Risk Score formula: $\text{Risk Score} = \text{Impact} \times (6 - \text{Confidence})$
  - [ ] assumptions with Risk Score $\ge 15$ flagged as blocking risks; validation experiments executed prior to engineering commitment
- **Zero Pseudo-Requirements Mandate**:
  - [ ] zero placeholder markers (`TBD`, `TODO: implement`, `magic happens here`, `handled by dev`) in acceptance criteria
  - [ ] tickets represent production-grade, authoritative sources of truth ready for architectural design and test automation
