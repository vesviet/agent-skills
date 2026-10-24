# analyze-business-requirements — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### AI-Assisted Requirements Engineering (2026)
- **Epic-Organized Gherkin Generation** (arXiv:2607.01980, SEET 2026): 4-step pipeline — relevance classification → requirements update → epic/mind-map generation → Gherkin generation; expert raters prefer epic-organized on Correctness (4.61 vs 4.14), Executability (4.61 vs 4.07), Completeness (4.31 vs 3.50)
- **LLM-as-Judge Validation**: Independent LLM evaluation (DeepEval, RAGAS) for clarity, completeness, internal consistency; AI-generated AC can pass human review while containing subtle contradictions
- **JSON-Constrained Pipeline**: Structurally valid scenarios across all outputs; 99% structural validity for zero-shot baseline
- **Living Requirements Traceability**: AI-assisted tools (Trace.space, getleo.ai) link requirements → design docs → code modules → test cases; critical for EU AI Act compliance and regulated industries requiring chain-of-causality audit trails

### Agentic AC Format (2026)
- **Deterministic Observable Assertions**: When downstream delivery involves AI agents, write AC as deterministic assertions (not prose intent) so agents can auto-validate implementation output
- **Agentic Workflow Integration**: Requirements → Epic → Feature Block → Scenarios (Gherkin) with SSE real-time state updates

### EU AI Act Compliance (2026)
- **High-Risk AI Systems**: Requirements for AI systems in regulated domains require chain-of-causality traceability
- **Human Sign-Off Gate**: Mandatory for AI-assisted AC generation before sprint commitment

### Layered Requirements Pipeline Enhancements
- **Impact Mapping**: Why & Who → actors and KPI targets
- **Event Storming**: What & Flow → past-tense domain events (`OrderPlaced`, `PaymentFailed`)
- **User Story Mapping**: How & Release Slices → vertical MVP slice
- **Traceability**: Every User Story must trace to Impact Map actor behavior AND Event Storming domain event

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| AI-assisted AC generation with LLM-as-judge | **Epic-Organized Gherkin Pipeline**: 4-step (relevance → requirements → epic/mind-map → Gherkin) with JSON-constrained output |
| Living requirements traceability mention | **Mandatory AI-assisted traceability**: Trace.space, getleo.ai for requirements → design → code → test links; EU AI Act chain-of-causality |
| Agentic AC format mention | **Deterministic observable assertions**: Not prose intent; agents auto-validate implementation |
| Human sign-off gate | **EU AI Act compliance gate**: Mandatory human business analyst sign-off for AI-assisted AC |

### 2. New 2026 Patterns to Add
- **Epic-Organized Gherkin Generation Pipeline** with 4 LLM calls and SSE state streaming
- **LLM-as-Judge Validation** using DeepEval/RAGAS for clarity, completeness, consistency
- **Living Requirements Traceability** linking requirements to design, code, tests
- **Agentic AC Format** for deterministic agent auto-validation
- **EU AI Act Chain-of-Causality** audit trail requirements
- **Structured State Management** via SSE for real-time requirements updates

### 3. Checklist Additions
- [ ] Epic-organized Gherkin pipeline: relevance classification → requirements update → epic/mind-map → Gherkin generation
- [ ] JSON-constrained Gherkin output for structural validity (99%+)
- [ ] LLM-as-judge validation (DeepEval/RAGAS) for clarity, completeness, internal consistency
- [ ] Living requirements traceability: requirements → design docs → code modules → test cases
- [ ] AI-assisted traceability tools (Trace.space, getleo.ai) integrated
- [ ] Agentic AC format: deterministic observable assertions for agent auto-validation
- [ ] EU AI Act chain-of-causality audit trail for high-risk features
- [ ] Human business analyst sign-off gate for AI-assisted AC before sprint commitment
- [ ] SSE real-time state updates for requirements/epic/Gherkin changes
- [ ] Every User Story traces to Impact Map actor behavior AND Event Storming domain event
- [ ] Event Storming hot-spots resolved before sprint backlog finalization
- [ ] Vertical slicing only: each slice spans UI to database with end-to-end user value

### 4. Failure Mode Additions
- **Epic-organized vs requirement-aligned coverage gap**: Epic-organized may miss lexical coverage but gains expert preference. Mitigation: Use both TF-IDF and dense embedding coverage metrics.
- **LLM-as-judge false confidence**: Independent LLM may miss domain-specific contradictions. Mitigation: Blind expert assessment alongside automated evaluation.
- **Traceability link rot**: AI-assisted links become stale as code evolves. Mitigation: Automated CI checks for traceability freshness.
- **Agentic AC over-specification**: Deterministic assertions may constrain implementation flexibility. Mitigation: Balance observable outcomes with implementation freedom.
- **EU AI Act compliance gaps**: Missing chain-of-causality for high-risk features. Mitigation: Automated audit trail validation in CI.

### 5. Output Contract Updates
- Add `contracts/schemas/epic-organized-gherkin-spec.json` for pipeline configuration
- Add `contracts/schemas/llm-as-judge-validation-spec.json` for evaluation criteria
- Add `contracts/schemas/living-traceability-spec.json` for requirements→code links
- Add `contracts/schemas/agentic-ac-spec.json` for deterministic assertions
- Update `contracts/schemas/feature-ticket.json` with 2026 traceability fields

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Epic-organized Gherkin pipeline (4-step with SSE) | High |
| P0 | LLM-as-judge validation (DeepEval/RAGAS) | High |
| P0 | Living requirements traceability (Trace.space/getleo.ai) | High |
| P0 | Agentic AC format for deterministic assertions | Medium |
| P1 | EU AI Act chain-of-causality audit trail | High |
| P1 | SSE real-time state updates | Medium |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test epic-organized Gherkin pipeline with PURE dataset requirements
- Validate LLM-as-judge scores against expert blind assessment
- Verify traceability links freshness in CI
- Test agentic AC auto-validation with downstream agent