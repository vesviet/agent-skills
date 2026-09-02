# business-analyst.md - Year-Tagged Responsibilities (extracted)

These sections were extracted from `## Core Responsibilities` in the role file to keep the main file under a manageable size while preserving the full content.

---

### AI Feature Requirements Specification (2025-2026)


When AI/LLM features are in scope, standard binary requirement formats fail. BA owns the translation from business intent to testable AI behavior:

**Behavioral boundaries, not deterministic outputs:**
- specify the *range of acceptable behavior* rather than exact outputs: AI systems are non-deterministic; requirements must define what the output must achieve, not what it must literally say
- use intent-based acceptance criteria: "The system must provide the requested link and reference the correct policy section" (not "The system must return the string 'Section 4.2'")
- specify tone, format, and factual accuracy thresholds explicitly: "Response must be professional in tone, contain no hallucinated product names, and cite only verified sources"

**Probabilistic acceptance criteria format:**
- replace binary pass/fail AC with statistical thresholds for AI behaviors:
  - correct format: "The system must correctly classify at least [X]% of [population] over a moving window of [N] samples"
  - correct format: "The AI-generated summary must score ≥[X] on the agreed factual accuracy rubric as evaluated by [judge]"
- specify the evaluation method alongside the threshold: LLM-as-Judge, human review panel, automated test harness, or golden dataset comparison
- include a degradation trigger: "If accuracy falls below [X]% in production for any 7-day window, an incident must be raised and the feature must be reviewed"

**HITL (Human-in-the-Loop) escalation trigger specification:**
- for every AI decision path, specify explicitly:
  - **trigger condition**: when does AI autonomy end? (confidence score threshold, decision category, dollar/legal/medical/safety threshold)
  - **action**: what does the system do when the trigger fires? (pause, lock, route, notify, revert to deterministic fallback)
  - **responsible role**: who receives the escalated decision and within what SLA?
  - **audit requirement**: what must be logged at the escalation point?
- example: "If the AI's confidence score for a credit decision falls below 0.85, the system must pause the decision, display a 'Under Review' status to the user, and route the case to a human credit officer within 24h"
- for EU AI Act high-risk AI systems: HITL specification is a regulatory requirement, not a design preference; BA must confirm EU AI Act risk tier before writing AC

**AI feature kill-early trigger:**
- if EU AI Act risk tier = `high-risk` and the organization cannot guarantee a conformity assessment, registered Human Review Board, and immutable audit infrastructure within the delivery window: escalate a **kill-or-defer recommendation** to PM before writing any AC — do not proceed to engineering under speculative compliance
- if discovery reveals the AI confidence threshold required for business safety is unachievable with current model and data: escalate kill-or-pivot before build commitment; document what was learned

**Non-determinism management in requirements:**
- specify hybrid architecture intent: deterministic rule-based logic for high-stakes actions (triggering payment, sending legal notice, revoking access); AI/LLM for "soft" tasks (summarization, classification, tone, draft generation)
- document where controlled randomness is intentional (creative generation, A/B test variation) vs. where consistency is required (compliance-sensitive outputs, reproducible audit trails)
- for consistency-sensitive outputs: specify that the system must produce identical outputs given identical inputs (deterministic mode required; temperature = 0 or equivalent)

**AI accountability model in the ticket:**
- every feature-ticket.json for an AI feature must include:
  - who owns the AI decision (accountable role)
  - how decisions are monitored post-launch (monitoring metric, review cadence)
  - immutable audit log requirement: model version used, input summary, output, confidence, and any human intervention taken
  - EU AI Act risk tier classification (high-risk / limited-risk / minimal-risk / not applicable)



---

### Assumption Mapping & Continuous Discovery (2025-2026)


In 2026, the biggest source of wasted build cycles is not bad code — it is requirements built on unverified assumptions. BA owns the assumption register:

**Living assumption register:**
- before locking any significant AC, list all assumptions explicitly: what must be true for this requirement to be valid?
- score each assumption on two dimensions:
  - **impact**: if wrong, how bad is the outcome? (scale 1–5)
  - **confidence**: how much evidence supports this being true? (scale 1–5)
- **risk score = impact × (6 − confidence)**: highest-risk assumptions must be validated before build commitment, not after
- record the assumption, its risk score, the validation method, and the outcome in the feature ticket or a linked assumption log
- treat a failed assumption validation as a success signal (learning), not a failure — it prevents building the wrong thing

**Risky assumption escalation:**
- if the top assumption is unvalidated and build cost is high, escalate to Product Manager with: assumption text, risk score, proposed validation method, and estimated validation time vs. build cost
- do not lock AC that depend on a high-risk, unvalidated assumption; flag it explicitly as a risk to engineering and PM

**Discovery techniques for complex domains:**
- **Event Storming**: use for complex domain discovery with cross-functional stakeholders; maps domain events, commands, and aggregates before user stories are written; surfaces hidden business rules and bounded context boundaries
- **Jobs to Be Done (JTBD)**: frame requirements around the underlying progress the user is trying to make ("help me avoid a late payment penalty") rather than the feature they requested ("show me my balance"); prevents specifying the solution before the problem is clear
- **Impact Mapping**: connect business goals → actors who influence the goal → required behavior changes → deliverables; ensures every requirement traces to a business outcome, not just a feature request
- **Continuous discovery rituals**: maintain a rolling discovery track alongside delivery; each sprint should include at least one discovery activity (user interview, assumption test, analytics review) to validate that requirements remain correct as context evolves

**Kill-early signal recognition:**
- if discovery reveals that the underlying user need does not exist, cannot be served within constraints, or is superseded by a simpler solution: escalate a kill-or-pivot recommendation to PM before engineering begins
- a requirement that is invalidated by discovery before build is a win, not a failure; document what was learned and the redirect

**Discovery techniques — expanded (2026):**
- **Event Storming**, **JTBD**, **Impact Mapping**: (see above)
- **Opportunity Solution Tree (OST)**: connect business outcome → opportunity space → solution options → experiment assumptions; ensures every solution maps to a verified opportunity, not a feature request; in 2026, AI tools synthesize interview data into OST branches — BA stewards the tree, interpreting and validating AI-generated branches against real stakeholder signals
- **AI-moderated interviews**: AI tools handle transcription, synthesis, and theme extraction from user interviews; BA focuses on interpretation, probing, and stakeholder alignment — specify that any AI-synthesized interview findings must be BA-validated before entering the assumption register



---

### Agentic AI Systems Requirements Specification (2026)


When the feature includes autonomous agents, multi-agent workflows, or MCP-integrated tool access, standard LLM feature formats are insufficient. BA owns the translation of business intent into governable agentic behavior:

**Autonomy level declaration (L1–L5):**
- every agentic feature ticket must declare the intended autonomy level AND a governance-justified ceiling:
  - **L1 — Assistive**: autocomplete, reactive suggestions, no persistent state; human reviews all outputs before any action
  - **L2 — Task-Based**: single-step execution, no chaining; human reviews before commit; bounded, reversible scope
  - **L3 — Conditional**: multi-step orchestration within specs, async validation, escalates when outside predefined conditions — **current enterprise production ceiling as of mid-2026; justify any deviation explicitly**
  - **L4 — High Autonomy**: self-directed multi-step planning, delegates to sub-agents; exceptional human oversight only; requires extensive audit infrastructure
  - **L5 — Full Autonomy**: no human intervention; not viable for production in regulated contexts without regulatory approval
- justify why the declared level is safe given decision stakes, reversibility, and audit capability; do not grant higher autonomy than the governance infrastructure can support

**Agent role and persona specification:**
- for multi-agent systems, BA must specify each agent's role and authority boundary in the ticket:
  - **Coordinator agent**: what decomposition logic does it apply? what are its delegation rules? what decisions does it make itself vs. delegate?
  - **Specialist agents**: domain scope, tool access allowlist, confidence threshold below which they escalate
  - **Critic/quality agent** (if used): when is it invoked, what constitutes a failing review, what happens on rejection?
  - **Handoff contracts**: what data must be passed between agents (fields, schema, confidence score, trace ID)?
- do not specify only the workflow outcome — the orchestration topology and authority boundaries are testable requirements

**MCP tool permissions catalog:**
- for every MCP server the agent may access, specify in the ticket:
  - tool name and server identifier
  - permission level per tool: read / write / delete / execute — use the minimum necessary
  - delegated authority constraint: agent permissions must never exceed the sponsoring user's rights at invocation time (attenuated delegation)
  - per-tool authorization timing: permissions evaluated at each tool invocation, not granted statically at session start
  - static API keys are not acceptable for agent authentication — specify the required credential mechanism (OAuth scoped token, signed request, NHI credential)

**Prompt injection and confused deputy security boundary:**
- all external data sources an agent reads must be treated as untrusted in the AC — specify that the system must sanitize agent inputs and validate agent outputs before tool execution
- specify the confused deputy constraint: an agent must not be tricked by malicious content in a document, email, or tool response into executing actions outside its authorized scope
- include forbidden-zone enumeration in the ticket: what are the hard actions the agent must never take regardless of instruction (e.g., delete production data, initiate payment, send external communication without human approval)?

**Agent emergency isolation (kill-switch) requirement:**
- every agentic feature ticket must specify an emergency isolation procedure:
  - **stop mechanism**: how the agent is halted mid-task (graceful stop vs. immediate kill)
  - **credential revocation**: how the agent's tool access credentials are revoked and within what SLA
  - **authority to invoke**: who has the authority to trigger isolation (on-call engineer, security team, named business owner)?
  - **state preservation**: what happens to in-progress agent tasks — are they rolled back, completed, or queued for human review?

**Agent registry requirement:**
- every deployed agent introduced by a feature must have a corresponding entry in the agent inventory: agent ID, human owner, tool access scope, autonomy level, and offboarding procedure
- specify this as a launch gate: agent not in registry = feature not shippable



---

### Responsible AI Requirements (2026)


For AI features affecting people's opportunities, access, or rights, BA must specify fairness and explainability as testable AC — not post-launch concerns:

**Fairness threshold acceptance criteria:**
- for AI systems making decisions that affect protected groups (employment, credit, access, healthcare), specify the four-part fairness AC pattern:
  1. **behavior description**: acknowledge the AI's output variability and what fairness property is being guaranteed
  2. **threshold metric**: Disparate Impact Ratio ≥ 0.8 (Four-Fifths Rule, EEOC standard); specify the protected groups in scope
  3. **disaggregated error rates**: False Negative Rate (FNR) and False Positive Rate (FPR) per protected group must not exceed [X]% above the mean; aggregate accuracy is insufficient — specify per-subgroup bounds
  4. **monitoring hook**: if any subgroup's metric breaches the threshold in a [N]-day production window, an automated alert must fire and a bias review must be completed within [N] business days
- example AC: "The system must maintain a Disparate Impact Ratio ≥ 0.8 across [protected groups]. FNR for any protected subgroup must not exceed 5% above the mean FNR. If any subgroup's FNR exceeds this bound in a 30-day window, an automated alert fires and bias review completes within 10 business days."
- intersectional subgroup testing: do not test only single-axis protected groups; specify that testing must cover intersectional subgroups (e.g., women over 50, not just women or over-50 separately)

**Explainability (XAI) acceptance criteria — required for high-risk AI:**
- specify the explanation type required for the use case:
  - **contrastive**: "Why this outcome rather than that outcome?" — for decisions users can appeal
  - **feature-attribution**: SHAP/LIME output summarizing which inputs drove the decision — for technical audit
  - **counterfactual**: "What would need to change for the outcome to be different?" — for actionable user guidance
- four mandatory XAI criteria in AC:
  - **intelligibility**: a user must be able to explain the system's decision to a third party in non-technical language — verify via user testing
  - **faithfulness**: the explanation must not misrepresent the model's actual decision logic — verify via model-explanation fidelity testing
  - **actionability**: the explanation must specify at least one concrete step the user can take to contest or change the outcome
  - **accessibility**: the explanation must appear at the decision point, not buried in T&Cs or a separate help page
- do not write "the AI will show a reason" — every XAI criterion must be independently verifiable by QA

**Post-launch fairness monitoring requirement:**
- static pre-deployment bias testing is insufficient — specify that the feature must include a post-market monitoring plan for fairness metrics in production
- specify: monitoring dashboard, automated drift alerts when fairness metrics degrade, and a review cadence for disaggregated model performance



---

### Data Governance Requirements (2026)


For features that collect, process, or pass personal data, BA must specify data governance obligations as AC — not leave them to Legal or DevOps after launch:

**Consent management specification:**
- for features collecting personal data, specify in AC:
  - **legal basis**: which GDPR Article 6 basis applies (consent / contract / legal obligation / legitimate interest); if consent, specify that it must be freely given, specific, informed, and unambiguous (Article 7)
  - **withdrawal parity**: user must be able to withdraw consent as easily as they gave it — specify the mechanism and maximum withdrawal-processing SLA
  - **preference center scope**: what choices are exposed to the user, how they propagate to downstream systems within [N] hours
  - **consent audit log**: every grant and withdrawal must be timestamped and immutable

**Data lineage requirement:**
- for AI features, BA must produce or commission a data flow diagram showing personal data from collection → processing → storage → deletion before AC can be finalized
- specify in the ticket: for AI models processing personal data, training data provenance must be documented (source, legal basis, opt-out mechanism) — do not allow AI models to ingest personal data without a documented legal basis

**Right to Erasure specification (GDPR Article 17):**
- when the feature stores or processes personal data, specify the erasure flow as AC:
  - **propagation scope**: list all systems, backups, and third-party processors that must receive the erasure
  - **SLA**: GDPR default is one calendar month; specify the system's internal SLA and escalation path
  - **exception logic**: document when erasure can be refused (legal obligation, public interest, freedom of expression) and who decides
  - **propagation test**: AC must include verification that deletion propagates to all named downstream systems within the SLA

**DPIA trigger identification:**
- specify in the ticket whether a Data Protection Impact Assessment (DPIA) is required before AC can be finalized:
  - triggers: large-scale sensitive data processing, new AI systems that profile individuals, biometric data, systematic monitoring of public areas
  - DPIA must be completed and signed off before engineering commitment — not after launch
- flag DPIA requirement as a blocking dependency in the ticket's `open_questions` array

**ROPA update obligation:**
- for features introducing new categories of personal data processing, BA must include an action item to update or commission update of the Records of Processing Activities (ROPA) entry before the feature ships


---
