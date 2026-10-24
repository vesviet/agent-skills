# design-learning-plan — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### Adaptive Learning Systems & ITS (2026)
- **Intelligent Tutoring Systems (ITS)**: Moderate to high effectiveness (d ≈ 0.35–0.76) over traditional teaching
- **BKT (Bayesian Knowledge Tracing)**: Standard runtime student model for mastery posteriors per skill
- **Individualized BKT**: Student-specific learning speed parameters boost prediction accuracy
- **StanBKT** (May 2026): Bayesian inference in Stan — HMC, variational inference, hierarchical models, uncertainty quantification
- **ES-LLMs Architecture** (AIED 2026): Ensemble of Specialized LLMs with deterministic rules-based orchestrator, BKT student model, constraint enforcement (attempt-before-hint, hint caps)
- **Cosynced Platform** (2026): RAG pipeline + fine-tuned Gemini for language coaching, adaptive lesson generation, social matching for peer learning

### Vygotsky ZPD & Scaffolding (2026 Research)
- **Adaptive scaffolding** improves performance and self-regulation by optimizing cognitive load
- **Cognitive Load Theory integration**: Scaffolding regulates information flow within working memory
- **Multi-tier scaffolding**: Tier 1 (Universal), Tier 2 (Targeted with faded worked examples), Tier 3 (Intensive extension)
- **Fading process**: Gradual removal of scaffolding until internalization and self-regulation
- **ZPD measurement**: Dynamic, individualized — "distance between actual and potential development under guidance"

### Cognitive Load Theory (2026 Advances)
- **Two-dimensional cognitive load concept**: Intrinsic + extraneous (germane critically discussed as third type)
- **Element interactivity limits**: Maximum 3–5 novel interacting elements per study block
- **Cognitive Load Theory + Scaffolding**: Scaffolding reduces extraneous load, manages intrinsic load
- **Validation questionnaires**: Theory-based measurement of different cognitive load types

### Spaced Repetition & Ebbinghaus (2026)
- **Ebbinghaus decay model**: R = e^(-t/S) — retention intervals Days 1, 3, 7, 14, 30
- **BKT integration**: Mastery posteriors update after each assessment, drive adaptive review scheduling
- **Feynman Technique checkpoints**: Jargon-free layperson explanations with physical analogies
- **Socratic Mode**: Zero-direct-answer, 3-level graduated hint ladder (Constraint Focus → Conceptual Prompt → Isomorphic Mini-Problem)

### Bloom 2026 AI-Age Revision
- **Orchestration level** above Create: Human-AI decision making, prompt engineering, output verification, integration
- **Fluid cognitive movement**: Not hierarchical — learners move among creating, evaluating, refining
- **Metacognitive regulation**: Planning, monitoring, evaluating own learning with AI tools

### EU AI Act High-Risk AI in Education (2026)
- **Learning plan generators = High-Risk** (Annex III, 3a): AI systems for admission/assignment to educational institutions
- **AI-enabled pre-assessment tools**: High-risk if used for readiness determination
- **Human oversight required**: HITL/HOTL/HIC models, automation bias mitigation
- **Conformity assessment**: From Dec 2027 for Annex III systems
- **Record-keeping**: Automatic logging throughout lifecycle (Article 12)

### Growth Mindset & AI (2026 Evidence)
- **Dweck's false growth mindset critique**: Posters/language alone insufficient — need specific strategies, metacognition, quality feedback, safe culture
- **Growth mindset + AI**: Positively associated with engagement in AI-mediated writing (β = 0.244, p < 0.001)
- **AI literacy → Growth mindset**: Perceived affordances mediate the relationship
- **Metacognition + self-regulation**: +7 months additional progress (EEF evidence)

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| ZPD Multi-Tier Scaffolding | **Adaptive Scaffolding with BKT Integration**: Dynamic mastery posteriors drive scaffolding intensity, fading based on BKT probability thresholds |
| Cognitive Load Theory (3-5 elements) | **Two-Dimensional Cognitive Load**: Intrinsic + extraneous measurement, scaffolding as load regulation mechanism |
| Spaced Repetition (Days 1,3,7,14,30) | **BKT-Driven Adaptive Spacing**: Review intervals dynamically adjusted by mastery posterior decay rates |
| Bloom 2027 HOTS | **Bloom 2026 AI-Age with Orchestration Level**: Human-AI collaboration skills, metacognitive regulation |
| Feynman + Socratic Gates | **ES-LLMs Orchestrator Pattern**: Deterministic rules-based coordination, specialized agents, constraint enforcement |
| EU AI Act Compliance | **High-Risk Learning Plan Generator**: Conformity assessment, human oversight design, automation bias mitigation, Article 12 logging |

### 2. New 2026 Patterns to Add
- **BKT-Powered Adaptive Learning Plans**: Mastery posteriors per skill drive content sequencing, review scheduling, scaffolding intensity
- **ES-LLMs Tutoring Architecture**: Specialized agents (tutoring, assessment, feedback, scaffolding, motivation, ethics) + deterministic orchestrator
- **Cognitive Load Budgeting**: Per-block element interactivity limits with load type measurement
- **Adaptive Spaced Repetition**: Ebbinghaus intervals modulated by BKT forgetting parameters (pForget)
- **Growth Mindset Integration**: Metacognitive strategy training, specific feedback practices, safe error culture
- **Peer Learning Matching**: Social features matching learners at similar skill levels (Cosynced pattern)
- **RAG-Enhanced Content Retrieval**: Accurate contextual information for adaptive content generation
- **Multi-Modal Learning Pathways**: Code, diagram, text, oral, peer-collaborative formats

### 3. Checklist Additions
- [ ] BKT student model integrated: per-skill mastery posteriors drive plan adaptation
- [ ] ES-LLMs architecture: specialized agents + deterministic orchestrator with constraint enforcement
- [ ] Adaptive scaffolding: intensity modulated by BKT mastery probability, fading at threshold
- [ ] Two-dimensional cognitive load budgeting: intrinsic + extraneous per study block
- [ ] BKT-driven spaced repetition: review intervals adapted by mastery posterior decay
- [ ] Bloom 2026 Orchestration level: human-AI collaboration milestones in plan
- [ ] Growth mindset integration: metacognitive strategy training, specific feedback, safe culture
- [ ] Peer learning matching: social features for asynchronous practice at similar skill levels
- [ ] RAG-enhanced content: accurate contextual retrieval for adaptive content generation
- [ ] Multi-modal pathways: code/diagram/text/oral/peer formats per learning objective
- [ ] EU AI Act High-Risk compliance: conformity assessment evidence, human oversight model (HITL/HOTL/HIC)
- [ ] Automation bias mitigation: explicit verification steps, override/stop mechanisms in tutor interactions
- [ ] Article 12 record-keeping: automatic logging of plan generation, adaptation events, tutor interactions
- [ ] Conformity assessment: internal (Annex VI) or third-party (Annex VII) before deployment
- [ ] Feynman checkpoints: jargon-free explanations with physical analogies at milestones
- [ ] Socratic tutor mode: zero-direct-answer, 3-level hint ladder enforced

### 4. Failure Mode Additions
- **BKT model drift**: Mastery posteriors become inaccurate over time → Mitigation: StanBKT posterior predictive checks, periodic recalibration with new data
- **Orchestrator constraint violation**: Specialized agent bypasses safety rules → Mitigation: Deterministic rules-based orchestrator with attempt-before-hint, hint caps
- **Cognitive load miscalibration**: Exceeding 3-5 element limit → Mitigation: Real-time load measurement, automatic block decomposition
- **Spaced repetition rigidity**: Fixed intervals ignore individual forgetting rates → Mitigation: BKT pForget parameter drives adaptive intervals
- **Growth mindset superficiality**: Posters without strategy training → Mitigation: Metacognitive strategy integration, specific feedback, error-safe culture
- **EU AI Act deployment gap**: Plan generator used without conformity assessment → Mitigation: Compliance gate in deployment pipeline, CE marking verification
- **Peer matching failure**: Mismatched skill levels → Mitigation: BKT-based similarity matching, async practice design
- **RAG hallucination in content**: Inaccurate contextual retrieval → Mitigation: Verified knowledge base, citation requirements, human review gate

### 5. Output Contract Updates
- Add `contracts/schemas/bkt-learning-plan-spec.json` for mastery-driven adaptation
- Add `contracts/schemas/es-llms-orchestrator-spec.json` for agent coordination
- Add `contracts/schemas/cognitive-load-budget-spec.json` for per-block load planning
- Add `contracts/schemas/adaptive-spaced-repetition-spec.json` for BKT-driven intervals
- Add `contracts/schemas/growth-mindset-integration-spec.json` for metacognitive strategies
- Add `contracts/schemas/peer-matching-spec.json` for social learning features
- Add `contracts/schemas/eu-ai-act-learning-plan-spec.json` for high-risk compliance
- Update `contracts/schemas/learning-handoff.json` with 2026 fields

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Integrate BKT student model for adaptive plan sequencing | High |
| P0 | Add ES-LLMs orchestrator architecture with constraint enforcement | High |
| P0 | Add EU AI Act High-Risk compliance (conformity assessment, human oversight) | High |
| P1 | Add two-dimensional cognitive load budgeting per study block | Medium |
| P1 | Add BKT-driven adaptive spaced repetition (pForget modulation) | Medium |
| P1 | Add Bloom 2026 Orchestration level for human-AI collaboration | Medium |
| P1 | Add growth mindset integration with metacognitive strategies | Medium |
| P1 | Add peer learning matching with BKT similarity | Medium |
| P1 | Add RAG-enhanced adaptive content retrieval | Medium |
| P2 | Expand failure modes with 2026-specific scenarios | Low |
| P2 | Update output contracts for new schemas | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root after edits
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test BKT integration with ASSISTments 2017 dataset (N=942,816)
- Validate ES-LLMs orchestrator constraint enforcement (attempt-before-hint, hint caps)
- Verify EU AI Act compliance metadata and conformity assessment evidence
- Test adaptive spaced repetition with BKT forgetting parameters
- Validate cognitive load budgeting with element interactivity measurement