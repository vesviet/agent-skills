## Review Checklist

### Requirements & Specification
- actors, triggers, and outcomes are clear
- preserved_behavior and changed_behavior are explicit for fixes or policy changes
- business_rules and edge cases are captured (ticket or brief)
- requirements are testable and not hidden as assumptions
- acceptance criteria map to observable behavior
- dependencies and impacted roles or systems are named
- open_questions are listed before implementation starts
- Research Request issued when domain/compliance uncertainty blocks AC
- Analytics Request or verified data-analysis-report cited when AC uses metrics
- SEO Content Request issued when discoverability/conversion outcomes are in scope
- feature-ticket.json populated when machine handoff is required

### AI Feature Requirements (when AI/LLM in scope)
- behavioral boundary specified (not exact output): range of acceptable intent-based behavior defined
- probabilistic AC format used: statistical threshold + evaluation method + judge specified
- degradation trigger defined: what happens when accuracy falls below threshold in production
- HITL trigger fully specified: condition + action + responsible role + SLA + audit log requirement
- non-determinism documented: where deterministic behavior is required vs. where variation is acceptable
- hybrid architecture intent stated: which components are deterministic, which are AI/LLM
- AI accountability model in ticket: who owns decisions, how monitored, audit log requirements
- EU AI Act risk tier classified (Annex III standalone / Annex I embedded product / limited-risk / minimal-risk) and documented in ticket
- Article 50 disclosure AC specified: user-facing disclosure + machine-readable marking (C2PA) + deepfake labeling if applicable
- Article 53 GPAI obligations assessed: model card / training data summary / adversarial testing required if organization is GPAI provider

### Agentic Feature Requirements (when autonomous agents or MCP in scope)
- autonomy level declared (L1–L5) with governance-justified ceiling documented
- each agent's role and authority boundary specified (Coordinator / Specialist / Critic + handoff contracts)
- MCP tool permissions catalog specified per tool: read / write / delete / execute + credential mechanism
- delegated authority constraint: agent cannot exceed sponsoring user's rights at invocation
- forbidden-zone enumeration included: hard actions agent must never take
- kill-switch procedure specified: stop mechanism + credential revocation SLA + authority + state preservation
- agent registry entry required as launch gate
- prompt injection boundary specified: input sanitization + output validation requirements

### Responsible AI Requirements (when protected groups affected)
- fairness AC specified: Disparate Impact Ratio threshold + disaggregated FNR/FPR per subgroup + intersectional testing
- post-launch fairness monitoring specified: automated alerts + review cadence for degraded subgroup metrics
- XAI AC specified (high-risk): explanation type + intelligibility + faithfulness + actionability + accessibility criteria

### Data Governance (when personal data collected or processed)
- legal basis for processing specified (GDPR Article 6)
- consent capture and withdrawal mechanism specified; consent audit log required
- data lineage diagram commissioned or produced before AC finalized
- Right to Erasure AC specified: propagation scope + SLA + exception logic + propagation test
- DPIA trigger assessed: flagged as blocking dependency in open_questions if required
- ROPA update action item included when new personal data processing introduced

### Assumption Register (for significant bets)
- all major assumptions listed before AC is locked
- each assumption scored: impact × (6 − confidence) risk score
- top-risk assumptions have a validation method and target date
- high-risk unvalidated assumptions escalated to PM with build-cost comparison
- kill-or-pivot recommendation issued when discovery invalidates the underlying user need
