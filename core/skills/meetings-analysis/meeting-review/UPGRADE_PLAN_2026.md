# meeting-review — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### Agentic ADR Generation from Meetings (2026)
- **GADR (arXiv:2608.17694, SBES 2026)**: Multi-agent, self-correcting workflow extracting architectural decisions from raw meeting transcriptions → Nygard-formatted ADR drafts
- **Feasibility study**: 5 real project meetings, 4 senior architects, 15 students; captures most expert-identified decisions, outperforms zero-shot/few-shot baselines
- **Agentic RAG advantage**: Structural consistency + richer architectural explanations; critique stage reduces overlaps/fragmentation
- **Human-in-the-loop validation**: Every recorded meeting → reviewable ADR draft with human validation

### Architecture Decision Records (ADR) Standards (2026)
- **Nygard Format**: Context → Decision → Rationale → Controls/Safeguards → Consequences → Related Records
- **ADR Lifecycle**: Proposed → Accepted → Superseded (immutable after acceptance, never modified)
- **ADR Ownership**: Explicit owner per ADR; team establishes definition of ownership
- **Supersession Pattern**: Old ADR status = superseded, linked to new ADR; never delete
- **Controls & Safeguards for AI**: Model version control, prompt/output logging, human-in-the-loop validation, egress controls, rollback plan, DevSecOps integration

### Async-First Decision Making (2026)
- **Written RFC/brief + 48-72h async comment window** before any call
- **Decisions in ephemeral chat without ADR = anti-pattern**
- **DACI Framing**: Driver, Approver, Contributors, Informed; EXACTLY ONE Approver per decision
- **Consensus paralysis from committee approval = prohibited**

### AI-Synthesized Review Perspectives (2026)
- **Explicit labeling**: `[AI-synthesized]` for automated reasoning vs human domain knowledge
- **Human sign-off gate MANDATORY** for architectural decisions, breaking changes, release-blocking recommendations
- **AI-synthesized consensus ≠ cross-functional team alignment**
- **Inferred risks marked**: `[INFERRED — requires human validation]` when not grounded in code/docs
- **Prune ungrounded AI perspectives**: Cannot ground in code path, requirement, or stakeholder constraint → remove

### Decision Intelligence & Agentic AI Governance (2026)
- **DecisionCAMP 2026**: Intelligent Decision Services integrated into enterprise architectures
- **Agentic AI in EDA**: Multi-agent systems for autonomous goal-driven decision-making
- **Critical questions**: Who/what is in control? Trust, accountability, explainability, oversight
- **Interoperability standards**: Ontology-driven approaches for agentic AI adoption

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| ADR mentioned as deliverable | **Nygard-formatted ADR lifecycle mandatory**: Proposed → Accepted → Superseded; immutable after acceptance; explicit owner; Controls/Safeguards for AI |
| Async-first mentioned | **Written RFC/brief + 48-72h async window mandatory** before calls; ephemeral chat decisions without ADR = anti-pattern |
| DACI framing mentioned | **Exactly ONE Approver per decision**; consensus paralysis prohibited |
| AI-synthesized labeling | **Mandatory `[AI-synthesized]` label** + `[INFERRED — requires human validation]` for ungrounded risks |
| Human sign-off gate | **MANDATORY for architectural decisions, breaking changes, release-blocking**; AI consensus ≠ team alignment |
| Agentic ADR generation | **GADR multi-agent workflow**: raw transcript → structured ADR draft with human validation |

### 2. New 2026 Patterns to Add
- **GADR Agentic ADR Pipeline**: Multi-agent self-correcting workflow (transcript → critique → structured ADR)
- **Nygard ADR Format with AI Controls**: Context, Decision, Rationale, Controls/Safeguards, Consequences, Related Records
- **ADR Lifecycle Management**: Proposed → Accepted → Superseded; immutable; explicit ownership
- **Async-First Decision Protocol**: RFC + 48-72h comment window → ADR → sync call only if needed
- **DACI Decision Framing**: Single Approver, explicit Contributors/Informed
- **AI Perspective Guardrails**: `[AI-synthesized]` label, `[INFERRED]` marking, prune ungrounded perspectives
- **Agentic AI Governance**: Controls for model version, prompt logging, human-in-loop, egress, rollback, DevSecOps

### 3. Checklist Additions
- [ ] GADR agentic ADR pipeline available for meeting transcription → ADR draft
- [ ] Nygard ADR format: Context, Decision, Rationale, Controls/Safeguards, Consequences, Related Records
- [ ] ADR lifecycle: Proposed → Accepted → Superseded; immutable after acceptance
- [ ] Explicit ADR owner assigned; team ownership definition established
- [ ] AI Controls & Safeguards documented: model version control, prompt/output logging, human-in-loop, egress controls, rollback plan, DevSecOps integration
- [ ] Async-first protocol: written RFC/brief + 48-72h async comment window before scheduling calls
- [ ] DACI framing: exactly ONE Approver per decision; consensus paralysis prohibited
- [ ] All AI-synthesized perspectives labeled `[AI-synthesized]`
- [ ] Inferred risks marked `[INFERRED — requires human validation]`
- [ ] Ungrounded AI perspectives pruned (no code path, requirement, or stakeholder constraint)
- [ ] Human sign-off gate enforced for architectural/breaking/release-blocking decisions
- [ ] Decision owner OR escalation owner named for every decision
- [ ] Residual risk and unverified assumptions explicitly listed in conclusion
- [ ] Superseded ADRs linked to replacements; never deleted
- [ ] Code-review-finding.json with severity (blocking/important/follow-up), owner, category
- [ ] coordination-plan.json when review spawns follow-up phases with owners/dependencies

### 4. Failure Mode Additions
- **GADR hallucinated decisions**: Agent extracts decisions not actually made. Mitigation: Critique stage, expert review ground truth, human validation gate.
- **ADR mutation after acceptance**: Team modifies accepted ADR instead of superseding. Mitigation: Immutable ADR enforcement, CI check for modifications.
- **Async window bypass**: Decision made in call without prior RFC. Mitigation: Enforce RFC-first policy, reject decisions without async trail.
- **Multiple Approvers**: Committee approval causing paralysis. Mitigation: DACI enforcement — exactly one Approver, escalation path defined.
- **AI consensus mistaken for alignment**: Team assumes AI agreement = human agreement. Mitigation: Mandatory human sign-off, surface splits honestly.
- **Ungrounded AI perspective pollution**: Synthetic disagreement manufacturing. Mitigation: Prune perspectives without code/requirement/stakeholder grounding.
- **Agentic AI control ambiguity**: Who owns autonomous agent decisions? Mitigation: ADR Controls/Safeguards for AI, explicit ownership, audit trail.
- **Missing residual risk**: Known caveats omitted from conclusion. Mitigation: Enforce residual risk section in every review output.

### 5. Output Contract Updates
- Add `contracts/schemas/gadr-adr-pipeline-spec.json` for agentic ADR generation
- Add `contracts/schemas/nygard-adr-ai-controls-spec.json` for ADR format with AI safeguards
- Add `contracts/schemas/async-decision-protocol-spec.json` for RFC + comment window
- Add `contracts/schemas/daci-decision-spec.json` for single-approver framing
- Add `contracts/schemas/ai-perspective-guardrails-spec.json` for labeling/pruning rules
- Update `contracts/schemas/code-review-finding.json` with 2026 severity/category fields
- Update `contracts/schemas/coordination-plan.json` for follow-up phase dependencies

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | GADR agentic ADR pipeline (transcript → critique → ADR) | High |
| P0 | Nygard ADR format with AI Controls/Safeguards | High |
| P0 | Async-first RFC + 48-72h comment window enforcement | Medium |
| P0 | DACI single-approver framing | Medium |
| P1 | AI perspective guardrails (`[AI-synthesized]`, `[INFERRED]`, pruning) | Medium |
| P1 | ADR lifecycle management (immutable, supersession, ownership) | Medium |
| P1 | Human sign-off gate for architectural/breaking/release decisions | High |
| P2 | Agentic AI governance controls (model version, logging, rollback) | Medium |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test GADR pipeline on real meeting transcripts with expert ground truth
- Verify ADR immutability enforcement in CI
- Validate async-first protocol compliance (RFC before call)
- Test DACI single-approver enforcement
- Verify AI perspective labeling and pruning logic
- Test human sign-off gate blocks AI-only consensus