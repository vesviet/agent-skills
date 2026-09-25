# grade-and-review — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### EU AI Act High-Risk AI Grading Systems (2026)
- **AI-enabled grade calculators = High-Risk** (Annex III, 3a): Process assessment/test grades → determine final grades
- **Human oversight mandatory**: HITL (Human-in-the-loop), HOTL (Human-on-the-loop), or HIC (Human-in-command)
- **Automation bias mitigation** (Article 14(4)(b)): Built-in measures to prevent over-reliance on AI outputs
- **Conformity assessment**: Internal (Annex VI) or third-party (Annex VII) before deployment (from Dec 2027)
- **Record-keeping** (Article 12): Automatic logging of grading events, decisions, human interventions
- **Transparency** (Article 13): Deployers must understand and appropriately use system outputs
- **Accuracy & robustness** (Article 15): Known variations across population groups, foreseeable misuse scenarios
- **Deployer obligations** (Article 26): Assign competent human oversight, monitor operation, report incidents, keep logs ≥6 months

### Anti-Hallucination Grading (2026 Advances)
- **Line Citation Protocol**: Every deduction requires verbatim quote + line number from submission
- **Anti-Superficial Fluency Filter**: Cap eloquent but non-rigorous work at Level 2 (Developing)
- **Executable Proof Verification**: Code must pass tests; prose must have concrete derivations
- **ES-LLMs Grading Architecture**: Specialized agents (assessment, feedback, ethics) + deterministic orchestrator with constraint enforcement
- **StanBKT Uncertainty Quantification**: Bayesian posterior distributions for grading confidence intervals

### Cognitive Error Taxonomy (2026)
- **4-Tier Taxonomy**: Conceptual Misunderstanding, Procedural Execution Error, Boundary Blindspot, Cognitive Overload
- **AI-Mediated Error Patterns**: Hallucination acceptance, automation bias, prompt dependency, verification skipping
- **BKT-Informed Diagnosis**: Mastery posteriors per skill identify specific knowledge gaps vs. performance errors
- **Growth Mindset Integration**: Dweck's "not-yet" framing + metacognitive strategy training (not just effort praise)

### Growth Mindset Evidence (2026)
- **False growth mindset critique** (Dweck, 2015+): Posters/language alone insufficient
- **Effective components**: Metacognitive strategies (+7 months EEF), specific feedback, safe error culture, quality feedback
- **AI-mediated engagement**: Growth mindset → engagement in AI writing (β = 0.244, p < 0.001)
- **AI literacy → Growth mindset**: Perceived affordances mediate relationship
- **Process praise specificity**: "Your argument needs counter-example in paragraph two" > "try harder"

### Rule of One + Socratic Feedback (2026)
- **Exactly one actionable step** per evaluation cycle — prevents cognitive overload
- **Socratic hint ladder**: Level 1 Constraint Focus → Level 2 Conceptual Prompt → Level 3 Isomorphic Mini-Problem
- **AI Tutor Socratic Mode**: Zero direct answers, single guiding question, graduated escalation

### Learning Analytics & Assessment Contracts (2026)
- **Pseudonymous student tokens**: `STU-8f2e-2027` format, no PII
- **Assessment metadata**: `graded_by_ai`, `reviewed_by`, `verification_status`, `conformity_assessment_ref`
- **Cognitive diagnostic output**: Error category, BKT mastery posterior, ZPD progression
- **Cross-agent handoff**: `learning-assessment-report.json` + `learning-handoff.json`

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| 4-Tier Analytic Rubrics | **BKT-Informed Rubrics**: Mastery posteriors per skill inform criterion weighting, dynamic thresholds |
| Anti-Hallucination Line Citation | **Executable Verification + Citation**: Code tests + prose derivations + verbatim line citations |
| Anti-Superficial Fluency Filter | **AI-Mediated Fluency Detection**: Detect LLM-generated patterns (coherence without rigor, hallucinated citations) |
| Cognitive Error Taxonomy (4-tier) | **Extended Taxonomy**: Add AI-mediated errors (hallucination acceptance, automation bias, prompt dependency) |
| Growth Mindset Feedback | **Evidence-Based Growth Mindset**: Metacognitive strategies, specific feedback, safe culture — not posters |
| Rule of One | **Rule of One + Socratic Ladder**: Single step + 3-level hint escalation for AI tutor interactions |
| EU AI Act Compliance | **High-Risk Grading System**: Conformity assessment, HITL/HOTL/HIC oversight, Article 12 logging, Article 26 deployer duties |

### 2. New 2026 Patterns to Add
- **EU AI Act High-Risk Grading Compliance**: Conformity assessment evidence, human oversight model, automation bias mitigation, record-keeping
- **BKT-Informed Grading**: Mastery posteriors per skill provide confidence intervals for score reliability
- **Executable Verification Pipeline**: Sandbox code execution, test suite validation, derivation checking
- **AI Fluency Detection**: Linguistic markers of LLM generation (excessive coherence, missing citations, hallucination patterns)
- **Socratic AI Tutor Integration**: Zero-direct-answer, 3-level hint ladder, attempt-before-hint constraint
- **StanBKT Uncertainty Quantification**: Bayesian posteriors for grading confidence, model comparison
- **Cognitive Diagnostic Dashboard**: Per-skill mastery, error category, ZPD progression, growth mindset indicators
- **Cross-Agent Assessment Contracts**: Schema-validated handoffs with full audit trail

### 3. Checklist Additions
- [ ] EU AI Act High-Risk classification confirmed for grading system
- [ ] Conformity assessment completed (internal Annex VI or third-party Annex VII)
- [ ] Human oversight model specified: HITL / HOTL / HIC with competent personnel
- [ ] Automation bias mitigation: verification steps, override/stop mechanisms, bias awareness training
- [ ] Article 12 record-keeping: automatic logging of all grading events, human interventions, decisions
- [ ] Article 13 transparency: Deployer instructions for use, known limitations, accuracy variations
- [ ] Article 26 deployer compliance: Human oversight assignment, monitoring, incident reporting, 6-month log retention
- [ ] BKT-informed rubrics: Mastery posteriors weight criteria, dynamic thresholds per skill
- [ ] Executable verification: Code sandbox execution, test suite pass/fail, derivation validation
- [ ] AI fluency detection: LLM pattern markers (coherence without rigor, hallucinated citations, missing derivations)
- [ ] Extended cognitive error taxonomy: + AI-mediated errors (hallucination acceptance, automation bias, prompt dependency, verification skipping)
- [ ] Evidence-based growth mindset: Metacognitive strategy training, specific feedback, safe error culture
- [ ] Rule of One + Socratic Ladder: Single actionable step + 3-level hint escalation
- [ ] StanBKT uncertainty: Bayesian posteriors for score confidence intervals
- [ ] Pseudonymous student tokens: `STU-...` format, no PII in assessment outputs
- [ ] Conformity assessment reference: CE marking, EU Declaration of Conformity, technical documentation
- [ ] Human educator verification gate: `reviewed_by`, `verification_status: "verified_and_approved"` mandatory
- [ ] Cross-agent contracts: `learning-assessment-report.json` + `learning-handoff.json` schema-validated

### 4. Failure Mode Additions
- **EU AI Act deployment violation**: Grading system used without conformity assessment → Mitigation: Deployment gate, CE marking check, technical documentation validation
- **Automation bias in human review**: Educator over-trusts AI grading → Mitigation: HITL design, explicit disagreement workflow, bias awareness training
- **BKT grading miscalibration**: Mastery posteriors don't match actual performance → Mitigation: StanBKT posterior predictive checks, periodic recalibration
- **AI fluency false positive**: Human work flagged as AI-generated → Mitigation: Multi-marker detection, human review override, false positive rate monitoring
- **Executable verification gap**: Code passes tests but has conceptual errors → Mitigation: Hybrid verification (tests + conceptual rubric + derivation check)
- **Record-keeping failure**: Missing logs for audit → Mitigation: Automatic immutable logging, tamper-evident storage, Article 12 compliance
- **Growth mindset superficiality**: "Not yet" language without strategy training → Mitigation: Metacognitive strategy integration, specific feedback templates
- **Socratic ladder bypass**: AI tutor gives direct answers → Mitigation: Prompt locking, single-question enforcement, escalation monitoring

### 5. Output Contract Updates
- Add `contracts/schemas/eu-ai-act-grading-spec.json` for high-risk compliance metadata
- Add `contracts/schemas/bkt-grading-spec.json` for mastery-informed assessment
- Add `contracts/schemas/executable-verification-spec.json` for code/prose validation
- Add `contracts/schemas/ai-fluency-detection-spec.json` for LLM pattern markers
- Add `contracts/schemas/socratic-tutor-spec.json` for hint ladder and constraints
- Add `contracts/schemas/stanbkt-uncertainty-spec.json` for Bayesian confidence intervals
- Add `contracts/schemas/cognitive-diagnostic-dashboard-spec.json` for per-skill diagnostics
- Update `contracts/schemas/learning-assessment-report.json` with 2026 fields
- Update `contracts/schemas/learning-handoff.json` with 2026 fields

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | EU AI Act High-Risk compliance (conformity assessment, human oversight, logging) | High |
| P0 | BKT-informed grading with mastery posteriors and dynamic thresholds | High |
| P0 | Executable verification pipeline (sandbox + tests + derivations) | High |
| P0 | AI fluency detection for LLM-generated content | High |
| P1 | Extended cognitive error taxonomy (+ AI-mediated errors) | Medium |
| P1 | Evidence-based growth mindset integration (metacognition, specific feedback) | Medium |
| P1 | Socratic AI tutor with 3-level hint ladder and attempt-before-hint | Medium |
| P1 | StanBKT uncertainty quantification for grading confidence | Medium |
| P1 | Cognitive diagnostic dashboard with per-skill mastery | Medium |
| P2 | Expand failure modes with 2026-specific scenarios | Low |
| P2 | Update output contracts for new schemas | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root after edits
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test EU AI Act compliance metadata completeness and conformity assessment evidence
- Validate BKT grading with StanBKT posterior predictive checks
- Test executable verification pipeline with sandboxed code execution
- Validate AI fluency detection false positive/negative rates
- Test Socratic tutor constraint enforcement (zero direct answers, hint ladder)
- Verify Article 12 automatic logging and Article 26 deployer obligations