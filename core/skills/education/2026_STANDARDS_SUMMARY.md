# 2026 Education Standards & Patterns — Consolidated Research Summary

## Overview
Deep research conducted September 2026 across AI in Education, Adaptive Learning Systems, Bayesian Knowledge Tracing, Cognitive Load Theory, Vygotsky ZPD, Bloom's Taxonomy revision, Growth Mindset, and EU AI Act High-Risk compliance for education AI systems.

---

## 1. Bloom's Taxonomy Revision for AI Age (2026)

### Key Changes (Education Week, April 2026)
- **Traditional hierarchy insufficient**: Lower-order → higher-order climb doesn't match GenAI interaction
- **New Orchestration Level** (above Create):
  - Deciding what to ask, how to structure prompts
  - When to trust/question AI outputs
  - Integrating AI-generated content into original work
  - Balancing human reasoning with AI assistance
- **Fluid cognitive movement**: Learners move among creating, evaluating, refining — not hierarchical
- **Metacognitive regulation**: Planning, monitoring, evaluating own learning with AI tools

### Implications for Skills
- **create-exercises**: Add Orchestration-level items; verify DOK 3/4 survive AI tool access
- **design-learning-plan**: Include human-AI collaboration milestones in learning pathways
- **grade-and-review**: Assess orchestration skills, not just final output

---

## 2. Adaptive Learning Systems & Intelligent Tutoring (2026)

### Effectiveness Evidence
- **ITS effectiveness**: d ≈ 0.35–0.76 over traditional teaching (VanLehn, 2011; Wang et al., 2026)
- **Adaptive platforms** (NexusAI, DreamBox, Lexia, Carnegie Learning Cognitive Tutor): Full adaptive learning, AI content generation, auto-assessment, teacher AI tools
- **Kazakhstan pre-service CS teacher platform**: BKT algorithm for learning trajectory management

### ES-LLMs Architecture (AIED 2026 Paper)
```
Ensemble of Specialized LLMs:
├── Specialized Agents: Tutoring, Assessment, Feedback, Scaffolding, Motivation, Ethics
├── Deterministic Rules-Based Orchestrator: Constraint enforcement (attempt-before-hint, hint caps)
├── BKT Student Model: Per-skill mastery posteriors (N=102 skills)
└── LLM Renderer: Surface realization in natural language
```
- **Reliability**: Constraints as explicit rules, per-turn agent traces, constraint checks logged
- **Modularity**: Swap BKT for Deep Knowledge Tracing without changing orchestration

### Cosynced Platform (2026)
- **RAG pipeline** + fine-tuned Gemini for language coaching
- **Adaptive lesson generation** based on real-time weakness analysis
- **Peer matching**: Social features for asynchronous practice at similar skill levels

---

## 3. Bayesian Knowledge Tracing (BKT) — 2026 Advances

### Standard BKT (4 Parameters)
- p(L0): Initial knowledge probability
- p(T): Learning probability
- p(S): Slip probability
- p(G): Guess probability

### 2026 Innovations
| Innovation | Description | Source |
|------------|-------------|--------|
| **StanBKT** (May 2026) | Bayesian inference in Stan: HMC, variational inference, Pathfinder, optimization; hierarchical models, posterior predictive inference, uncertainty quantification | arXiv:2605.23048 |
| **Individualized BKT** | Student-specific learning speed parameters boost prediction accuracy | Yudelson et al., CMU |
| **BKT R Package** (May 2026) | CRAN: fitting, cross-validation, prediction, parallelization | CRAN BKT 0.1.0 |
| **Forgetting Parameter** | pForget for knowledge decay (standard BKT assumes zero) | Spectral BKT, KT-IDEM |
| **Multi-Skill per Step** | Multiple skills per problem step | Pardos & Heffernan generalizations |

### Integration Patterns
- **Runtime student model** in ES-LLMs: Mastery posteriors drive agent proposals
- **Adaptive spacing**: Review intervals modulated by pForget and mastery decay
- **Scaffolding intensity**: Modulated by mastery probability thresholds
- **Grading confidence**: Bayesian posteriors for score reliability intervals

---

## 4. Cognitive Load Theory & Vygotsky ZPD (2026)

### Cognitive Load Theory Advances
- **Two-dimensional model**: Intrinsic + Extraneous (Germane critically discussed as third type)
- **Element interactivity limits**: Max 3–5 novel interacting elements per 45-60 min study block
- **Scaffolding as load regulation**: Reduces extraneous load, manages intrinsic load
- **Validation questionnaires**: Theory-based measurement of load types (Kalyuga, 2011; Sweller et al., 2011)

### ZPD & Scaffolding (2026 Research)
- **Adaptive scaffolding** improves performance & self-regulation by optimizing cognitive load
- **Fading process**: Gradual removal until internalization → self-regulated learner
- **Dynamic ZPD**: "Distance between actual and potential development under guidance" — always changing
- **Multi-tier differentiation**:
  - **Tier 1**: Universal Core
  - **Tier 2**: Targeted Scaffolding with faded worked examples
  - **Tier 3**: Intensive Extension challenges

### Integration with BKT
- **Mastery posteriors** drive scaffolding intensity (high mastery → less scaffolding)
- **Fading thresholds**: BKT probability > 0.85 triggers fading
- **Cognitive load budgeting**: Per-block element limits enforced by orchestrator

---

## 5. Spaced Repetition & Memory (2026)

### Ebbinghaus Model
- **Decay formula**: R = e^(-t/S)
- **Standard intervals**: Days 1, 3, 7, 14, 30
- **BKT-driven adaptation**: Intervals modulated by individual pForget and mastery posterior decay rates

### Feynman Technique & Socratic Method
- **Feynman checkpoints**: Jargon-free layperson explanations with physical analogies
- **Socratic Mode**: Zero direct answers, single guiding question
- **3-Level Graduated Hint Ladder**:
  1. **Constraint Focus**: "What happens if you change this parameter?"
  2. **Conceptual Prompt**: "How does this concept relate to the problem?"
  3. **Isomorphic Mini-Problem**: "Try this simpler version first"

---

## 6. Growth Mindset & AI (2026 Evidence)

### Dweck's False Growth Mindset Critique (2015–present)
- **Posters/language alone insufficient** — "The path to a growth mindset is a journey, not a proclamation"
- **Effective components** (EEF +7 months):
  - Metacognitive strategy training (plan, monitor, evaluate)
  - Specific feedback practices ("Your argument needs counter-example in paragraph two")
  - Safe error culture (errors as data, not deficiencies)
  - Quality feedback focused on learning process

### AI-Mediated Growth Mindset (2026 Studies)
- **Growth mindset → Engagement in AI writing**: β = 0.244, p < 0.001 (Frontiers, June 2026)
- **AI literacy → Growth mindset**: Perceived affordances mediate relationship
- **AI as feedback partner**: Timely, specific, constructive feedback → successful experiences → mindset development

---

## 7. EU AI Act High-Risk Education AI (2026)

### Classification (Annex III, 3a)
**High-Risk AI Systems in Education**:
- AI systems for access/admission/assignment to educational/vocational institutions
- AI-enabled grade calculators (determine final grades from assessment data)
- AI-enabled pre-assessment tools (readiness determination)

### Requirements (Articles 8-15)
| Article | Requirement | Education Application |
|---------|-------------|----------------------|
| **Article 9** | Risk Management System | Identify grading bias, hallucination risks, automation bias |
| **Article 10** | Data Governance | Representative training data, student privacy, pseudonymous tokens |
| **Article 11** | Technical Documentation | Model cards, BKT parameters, rubric specifications |
| **Article 12** | **Record-Keeping** | Automatic logging of all grading/plan/exercise events |
| **Article 13** | Transparency | Deployer instructions, limitations, accuracy variations |
| **Article 14** | **Human Oversight** | HITL/HOTL/HIC, automation bias mitigation, stop button |
| **Article 15** | Accuracy & Robustness | Cross-population validation, adversarial testing |

### Human Oversight Models (Article 14)
1. **Human-in-the-loop (HITL)**: AI cannot act without human decision at each step
2. **Human-on-the-loop (HOTL)**: AI acts autonomously, human monitors real-time, can intervene
3. **Human-in-command (HIC)**: Human sets boundaries, AI operates within them

### Automation Bias Mitigation (Article 14(4))
- Awareness of over-reliance tendency
- Correct interpretation tools/methods
- Ability to disregard/override/reverse AI output
- Stop button / safe halt procedure

### Conformity Assessment (Article 43)
- **Internal (Annex VI)**: Most systems — provider self-assessment with QMS
- **Third-party (Annex VII)**: Biometric, critical infrastructure — notified body
- **Deadlines**: Dec 2027 (Annex III), Aug 2028 (Annex I)
- **CE Marking + EU Declaration of Conformity + EU Database Registration**

### Deployer Obligations (Article 26)
- Use per instructions, assign competent human oversight
- Monitor operation, report incidents, suspend on risk
- Keep logs ≥6 months, inform workers, data protection assessment

---

## 8. Cross-Skill Integration Patterns

### Exercise → Plan → Grading Flow
```
1. create-exercises
   ├── Bloom 2026 Orchestration level items
   ├── Cognitive resilience: deliberate friction, bounded AI
   ├── StanBKT IRT: hierarchical, HMC, uncertainty quantification
   ├── EU AI Act compliance metadata
   ├── Synthetic flaw injection (hallucination patterns)
   ├── Multi-modal formats (code, diagram, oral, artifact)
   └── Adaptive selection via BKT mastery posteriors
       ↓
2. design-learning-plan
   ├── BKT-powered adaptive sequencing
   ├── ES-LLMs orchestrator + specialized agents
   ├── Two-dimensional cognitive load budgeting
   ├── BKT-driven spaced repetition (pForget modulation)
   ├── Bloom 2026 Orchestration milestones
   ├── Growth mindset: metacognition, specific feedback, safe culture
   ├── Peer matching via BKT similarity
   ├── RAG-enhanced content retrieval
   └── EU AI Act High-Risk compliance
       ↓
3. grade-and-review
   ├── EU AI Act grading compliance (conformity, oversight, logging)
   ├── BKT-informed rubrics (mastery-weighted criteria)
   ├── Executable verification (sandbox + tests + derivations)
   ├── AI fluency detection (LLM pattern markers)
   ├── Extended error taxonomy (+ AI-mediated errors)
   ├── Evidence-based growth mindset (metacognition + strategy)
   ├── Rule of One + Socratic Ladder (3-level hints)
   ├── StanBKT uncertainty (Bayesian confidence intervals)
   └── Cognitive diagnostic dashboard (per-skill mastery)
```

---

## 9. Required Contract Schemas (2026)

### New Schemas to Create
| Schema | Owner Skill | Purpose |
|--------|-------------|---------|
| `bloom-2026-taxonomy.json` | create-exercises | AI-age cognitive levels including Orchestration |
| `cognitive-resilience-exercise-spec.json` | create-exercises | Deliberate friction, bounded AI patterns |
| `stanbkt-irt-spec.json` | create-exercises | Bayesian IRT parameters, posteriors, uncertainty |
| `eu-ai-act-compliance-spec.json` | create-exercises | High-risk AI metadata for exercise generators |
| `adaptive-exercise-selection-spec.json` | create-exercises | BKT-driven exercise selection |
| `bkt-learning-plan-spec.json` | design-learning-plan | Mastery-driven plan adaptation |
| `es-llms-orchestrator-spec.json` | design-learning-plan | Agent coordination, constraint enforcement |
| `cognitive-load-budget-spec.json` | design-learning-plan | Per-block intrinsic/extraneous load planning |
| `adaptive-spaced-repetition-spec.json` | design-learning-plan | BKT-driven review intervals |
| `growth-mindset-integration-spec.json` | design-learning-plan | Metacognitive strategies, feedback, safe culture |
| `peer-matching-spec.json` | design-learning-plan | Social learning, BKT similarity matching |
| `eu-ai-act-learning-plan-spec.json` | design-learning-plan | High-risk plan generator compliance |
| `eu-ai-act-grading-spec.json` | grade-and-review | High-risk grading system compliance |
| `bkt-grading-spec.json` | grade-and-review | Mastery-informed assessment |
| `executable-verification-spec.json` | grade-and-review | Code/prose validation pipeline |
| `ai-fluency-detection-spec.json` | grade-and-review | LLM pattern markers |
| `socratic-tutor-spec.json` | grade-and-review | Hint ladder, attempt-before-hint constraints |
| `stanbkt-uncertainty-spec.json` | grade-and-review | Bayesian grading confidence intervals |
| `cognitive-diagnostic-dashboard-spec.json` | grade-and-review | Per-skill mastery, error category, ZPD |

---

## 10. Implementation Priority Matrix

| Priority | create-exercises | design-learning-plan | grade-and-review |
|----------|------------------|---------------------|------------------|
| **P0** | Bloom 2026 Orchestration level | BKT adaptive sequencing | EU AI Act grading compliance |
| **P0** | Cognitive resilience framework | ES-LLMs orchestrator | BKT-informed grading |
| **P0** | StanBKT Bayesian IRT | EU AI Act plan compliance | Executable verification |
| **P0** | EU AI Act exercise compliance | | AI fluency detection |
| **P1** | Adaptive BKT exercise selection | Cognitive load budgeting | Extended error taxonomy |
| **P1** | Synthetic flaw injection | BKT spaced repetition | Growth mindset (evidence-based) |
| **P1** | Multi-modal formats | Bloom 2026 Orchestration | Socratic tutor + hint ladder |
| **P1** | | Growth mindset integration | StanBKT uncertainty |
| **P1** | | Peer matching | Cognitive dashboard |
| **P1** | | RAG content retrieval | |
| **P2** | Failure modes | Failure modes | Failure modes |
| **P2** | Contract schemas | Contract schemas | Contract schemas |

---

## 11. Validation Gates (All Skills)

1. **Pack validation**: `python3 core/scripts/validate-all.py` from agent-skills root
2. **INDEX.md regeneration**: `python3 core/scripts/generate-index.py` if VERSION bumped
3. **Adapter parity**: `validate-rules.py` (9 parity groups)
4. **Skill-specific tests**:
   - StanBKT integration with ASSISTments 2017 (N=942,816) / 2020 datasets
   - ES-LLMs orchestrator constraint enforcement (attempt-before-hint, hint caps)
   - EU AI Act compliance metadata + conformity assessment evidence
   - BKT adaptive spacing with pForget parameter validation
   - Cognitive load budgeting with element interactivity measurement
   - AI fluency detection false positive/negative rates
   - Socratic tutor zero-direct-answer enforcement
   - Article 12 automatic logging, Article 26 deployer obligations
   - Cognitive resilience exercises with AI tool access attempts

---

## 12. Key References

- **Bloom 2026**: Education Week "Bloom's Taxonomy Needs an Update for the AI Age" (Apr 2026)
- **AI in Education**: IES 2026 review (20 causal studies), Penn GSE Adaptive Learning Systems course
- **BKT Advances**: StanBKT (arXiv:2605.23048), Individualized BKT (CMU), BKT R Package (CRAN 2026)
- **ES-LLMs**: AIED 2026 "From Untamed Black Box to Interpretable Pedagogical Orchestration"
- **Cognitive Load**: Kalyuga (2011), Sweller et al. (2011), Educational Psychology Review 2026
- **ZPD/Scaffolding**: Vygotsky (1978), Adaptive scaffolding studies (2026)
- **Growth Mindset**: Dweck (2015+ false mindset critique), Structural Learning (2026), Frontiers (2026)
- **EU AI Act**: Regulation (EU) 2026/1744, Article 14 Human Oversight, Annex III 3a Education
- **Cosynced**: Katz School M.S. Data Analytics platform (Jun 2026)