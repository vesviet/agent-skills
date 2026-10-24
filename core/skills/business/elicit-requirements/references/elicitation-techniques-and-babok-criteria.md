# Elicitation Techniques & BABOK v3 Quality Standards

> Authoritative reference guide for structured requirements elicitation, the Colombo Method, and the 9 BABOK v3 requirement quality criteria.

---

## 1. Funnel Questioning Protocol

Funnel questioning prevents two critical failure modes in requirements elicitation: premature convergence on implementation details, and vague, unfalsifiable stakeholder statements.

```
       ▼  Phase 1: Open-Ended Questions (Broad Discovery)
      ▼▼▼  Phase 2: Probing Questions (Exceptions, Volumetrics, Edge Cases)
     ▼▼▼▼▼ Phase 3: Closed Confirmation Questions (Hard Boundaries & SLAs)
```

| Phase | Purpose | Example Question | Stakeholder Response Pattern |
|---|---|---|---|
| **Phase 1: Open** | Understand the operational context and end-to-end intent | *"How does the regional sales team currently process custom discount approvals?"* | Narrative describing daily routine, pain points, and manual handoffs. |
| **Phase 2: Probing** | Uncover frequency, edge cases, exceptions, and dependencies | *"What specific conditions cause a discount request to bypass the regional manager?"* | Reveals hidden rules: enterprise accounts, quarterly deadlines, VIP status. |
| **Phase 3: Closed** | Lock precise numerical limits, SLAs, and unambiguous states | *"Is 15% discount the exact ceiling requiring VP sign-off, or can directors approve up to 20%?"* | Binary confirmation: *"Directors can approve up to 20% only during Q4."* |

---

## 2. The Colombo Method (Tacit Knowledge Elicitation)

Named after TV detective Columbo, this technique uses purposeful faux-naïveté to bypass defensive or assumed knowledge barriers.

### Core Principles
1. **Never pretend to understand an ambiguous term**: When a stakeholder says *"The system must be compliant with standard policies"*, never nod. Ask: *"Forgive my confusion, which specific policy document and section applies here?"*
2. **Explore the "Obvious"**: Ask questions whose answers seem trivial. *"What happens if a user submits twice in one second?"* Often, developers assume frontend throttling while stakeholders expect backend idempotency.
3. **The "Just One More Thing" Probe**: Before concluding an interview, ask: *"If this system fails on day 1, what is the most likely reason why?"* This reliably surfaces political constraints and legacy risks.

---

## 3. The 9 BABOK v3 Requirement Quality Criteria

Every functional and non-functional requirement must satisfy all 9 characteristics:

| Criterion | Violation Pattern (Before) | Compliant Standard (After) | Engineering Rationale |
|---|---|---|---|
| **1. Atomic** | *"The system shall authenticate users and send a welcome SMS and create an onboarding ticket."* | Split into 3 atomic requirements: REQ-01 (authenticate), REQ-02 (send SMS), REQ-03 (create ticket). | Compound requirements cannot be tracked, estimated, or failed independently in CI. |
| **2. Complete** | *"System will notify users when invoice is overdue."* | *"System shall dispatch an email notification within 15 minutes of an invoice exceeding Net-30 status, logging the event in the audit trail."* | Missing trigger, channel, timing SLA, and audit state. |
| **3. Consistent** | REQ-10 states guest checkout is allowed; REQ-45 states all orders require a verified email and password. | Align with product owner: guest checkout creates a lightweight guest account with tokenized email verification. | Conflicting requirements lead to architectural rework. |
| **4. Concise** | *"It is imperative and essential that the modern intuitive dashboard display realtime metrics."* | *"Dashboard shall display active session count updated every 5 seconds."* | Eliminates fluff adjectives and subjective puffery. |
| **5. Feasible** | *"System shall calculate global route optimization across 100,000 nodes in under 100 milliseconds."* | *"System shall calculate regional route optimization across up to 500 nodes within 800ms; global optimization runs asynchronously."* | Mathematically / computationally unrealistic bounds refined to feasible scope. |
| **6. Unambiguous** | *"System should support heavy transaction loads smoothly."* | *"System shall sustain 2,500 requests/second at p99 latency <= 250ms under standard peak profile."* | Exactly one interpretation across QA, DevOps, and Dev. |
| **7. Testable** | *"UI must be aesthetically pleasing and responsive."* | *"UI shall achieve 0 accessibility violations on axe-core WCAG AA, with layout shifts (CLS) <= 0.05 across mobile (390px) and desktop (1440px)."* | Replaces aesthetic opinion with automated test assertions. |
| **8. Prioritized** | All 80 backlog items labeled as "High Priority". | Apply WSJF or MoSCoW: Must (40%), Should (30%), Could (20%), Won't (10%). | Prevents project failure when schedule slips. |
| **9. Understandable** | Overly technical code pseudocode pasted as a requirement. | Plain-language behavioral specification using standard business domain terms defined in the project glossary. | Enables business sponsors to validate acceptance criteria without reading code. |

---

## 4. System 2 Reflective Loop & Anti-Rationalization Guardrails

### The BA Reflective Checklist
Before submitting a requirement artifact for engineering handoff, answer:
1. **Evidence Check**: Does every business rule trace back to an interview quote, policy document, or verified data report?
2. **Failure Mode Check**: Have I specified what happens when external dependencies timeout, inputs are malformed, or users abandon mid-flow?
3. **Rationalization Trap**: Did I write *"System behavior will be determined during implementation"*? If yes, STOP. Document as a formal Open Question with options A/B.
