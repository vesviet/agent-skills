# create-exercises — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### Bloom's Taxonomy Update for AI Age (2026)
- **Traditional hierarchy challenged**: Moving from lower-order to higher-order thinking doesn't align with GenAI interaction
- **New cognitive demands**: Deciding what to ask, how to structure questions, when to trust/question AI outputs, integrating AI content into original work
- **Fluid movement**: Learners move fluidly among creating, evaluating, refining — not hierarchical climb
- **Orchestration skills**: Human-AI collaboration requires active decision-making, balancing human reasoning with AI assistance

### AI-Resistant Exercise Design (2026 Standards)
- **Cognitive resilience framework** (Westerbeek, 2026): Design against erosion of attention, language construction, working memory rehearsal, early meaning-generation
- **Deliberate friction**: Bounded AI use inside platforms architecturally optimized for frictionless engagement
- **Developmental window protection**: AI support must scaffold the zone rather than replace child's operation within it
- **Adolescent regulatory support**: Environment must supply friction and verification steps that developing cognitive control cannot yet reliably supply

### Item Response Theory (IRT) Advances (2026)
- **StanBKT** (May 2026): Bayesian inference in Stan for BKT — Hamiltonian Monte Carlo, variational inference, Pathfinder, optimization
- **Hierarchical BKT models**: Flexible prior specification, posterior predictive inference, uncertainty quantification
- **Individualized BKT**: Student-specific learning speed parameters boost prediction accuracy
- **BKT R package** (May 2026): CRAN package for fitting, cross-validating, predicting with BKT models
- **Deep Knowledge Tracing alternatives**: Neural approaches but lack transparency for real-time safety orchestration

### EU AI Act High-Risk AI Compliance (2026)
- **Education AI = High-Risk** (Annex III, 3a): AI systems for access/admission/assignment to educational institutions
- **AI-enabled grade calculators**: High-risk — require human oversight, conformity assessment (from Dec 2027)
- **Human oversight models**: Human-in-the-loop (HITL), Human-on-the-loop (HOTL), Human-in-command (HIC)
- **Automation bias mitigation**: Built-in measures to prevent over-reliance on AI outputs
- **Record-keeping**: Automatic logging of events throughout lifecycle (Article 12)
- **Conformity assessment**: Internal (Annex VI) or third-party (Annex VII) before market placement

### Webb's DOK & AI Integration (2026)
- **DOK 1-4 mapping** must account for AI tool availability
- **DOK 3/4 verification**: Require multi-step reasoning, context-bound problems, synthetic flaw detection
- **AI-shortcut resistance archetypes** (5 types): Context-bound, synthetic flaw injection, raw telemetry, oral defense, proprietary context

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| Bloom 2027 HOTS tiers | **Bloom 2026 AI-Age Revision**: Orchestration skills, fluid cognitive movement, human-AI decision balance |
| AI-Shortcut Resistance (5 archetypes) | **Cognitive Resilience Framework**: Deliberate friction, developmental window protection, regulatory scaffolding |
| IRT Calibration (Rasch 1PL/3PL) | **StanBKT Bayesian Inference**: Hierarchical models, HMC/variational inference, uncertainty quantification, posterior predictive checks |
| Human Educator Review Gate | **EU AI Act Compliance**: High-risk AI classification, conformity assessment, human oversight design (HITL/HOTL/HIC), automation bias mitigation, Article 12 record-keeping |
| DOK 1-4 Matrix | **DOK-AI Alignment**: Verify cognitive depth survives AI tool access; reject rote questions at DOK 3/4 |

### 2. New 2026 Patterns to Add
- **Bloom 2026 AI-Age Taxonomy** with orchestration level above Create
- **Cognitive Resilience Exercise Design** with deliberate friction patterns
- **StanBKT Integration** for Bayesian IRT with uncertainty quantification
- **EU AI Act High-Risk Compliance** metadata in exercise contracts
- **Adaptive Exercise Generation** using BKT mastery posteriors
- **Multi-Modal Exercise Formats**: Code, diagram, oral defense, artifact debugging
- **Synthetic Flaw Injection** with known hallucination patterns for debugging practice

### 3. Checklist Additions
- [ ] Bloom 2026 AI-Age taxonomy applied (Orchestration level for human-AI decision making)
- [ ] Cognitive resilience framework: deliberate friction, bounded AI use, developmental window protection
- [ ] StanBKT Bayesian IRT: hierarchical models, HMC/variational inference, posterior uncertainty
- [ ] EU AI Act High-Risk metadata: `ai_system_classification`, `conformity_assessment_type`, `human_oversight_model`, `automation_bias_mitigation`, `record_keeping_enabled`
- [ ] Human oversight design: HITL/HOTL/HIC specified per exercise type
- [ ] DOK-AI alignment verified: questions survive AI tool access, multi-step reasoning required
- [ ] Synthetic flaw injection with known LLM hallucination patterns (factual, reasoning, code)
- [ ] Adaptive exercise selection using BKT mastery posteriors per skill
- [ ] Multi-modal formats: code execution, diagram analysis, oral defense prompts, artifact debugging
- [ ] Question-level changelog includes `irt_model_version`, `bayesian_posterior_samples`, `human_oversight_verified`
- [ ] Conformity assessment evidence linked for high-risk exercise generators
- [ ] Automation bias mitigation: exercises require verification steps before accepting AI output

### 4. Failure Mode Additions
- **AI orchestration gap**: Students cannot effectively direct AI tools → Mitigation: Explicit orchestration exercises at Bloom 2026 Create/Evaluate level
- **Cognitive atrophy**: Over-reliance on AI erodes foundational skills → Mitigation: Deliberate friction exercises with AI disabled/bounded
- **IRT model misspecification**: Wrong IRT model (1PL vs 2PL vs 3PL) → Mitigation: StanBKT model comparison with posterior predictive checks
- **EU AI Act non-compliance**: Exercise generator deployed without conformity assessment → Mitigation: Compliance metadata gate, CE marking verification
- **Automation bias in grading**: Educators over-trust AI exercise recommendations → Mitigation: HITL design, explicit override/stop mechanisms
- **DOK inflation**: Questions labeled DOK 3/4 but solvable by AI → Mitigation: AI-solving attempt verification before release

### 5. Output Contract Updates
- Add `contracts/schemas/bloom-2026-taxonomy.json` for AI-age cognitive levels
- Add `contracts/schemas/cognitive-resilience-exercise-spec.json` for friction patterns
- Add `contracts/schemas/stanbkt-irt-spec.json` for Bayesian IRT parameters and posteriors
- Add `contracts/schemas/eu-ai-act-compliance-spec.json` for high-risk AI metadata
- Add `contracts/schemas/adaptive-exercise-selection-spec.json` for BKT-driven selection
- Update `contracts/schemas/learning-handoff.json` with new 2026 fields

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Add Bloom 2026 AI-Age Taxonomy (Orchestration level) | Medium |
| P0 | Add Cognitive Resilience Framework (deliberate friction, bounded AI) | High |
| P0 | Integrate StanBKT Bayesian IRT with uncertainty quantification | High |
| P0 | Add EU AI Act High-Risk compliance metadata and conformity assessment | High |
| P1 | Add adaptive exercise selection using BKT mastery posteriors | Medium |
| P1 | Add synthetic flaw injection with known hallucination patterns | Medium |
| P1 | Add multi-modal exercise formats (oral defense, artifact debugging) | Medium |
| P1 | Update DOK-AI alignment verification process | Low |
| P2 | Expand failure modes with 2026-specific scenarios | Low |
| P2 | Update output contracts for new schemas | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root after edits
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test StanBKT integration with ASSISTments dataset
- Verify EU AI Act compliance metadata completeness
- Test cognitive resilience exercises with AI tool access
- Validate DOK-AI alignment with LLM solving attempts