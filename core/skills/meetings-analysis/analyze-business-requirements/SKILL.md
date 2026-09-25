---
name: analyze-business-requirements
description: Analyze and write business requirements by making actors, business rules, state transitions, exceptions, preserved behavior, and downstream process impact explicit. Use when a feature, policy change, or bug fix needs implementation-ready requirements and testable acceptance criteria.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Analyze Business Requirements

Use this skill when business needs, bug behavior, or process expectations must be turned into clear, testable requirements.

## When to Use

- a feature/policy change needs requirements
- making actors, rules, state transitions explicit
- defining testable acceptance criteria
- capturing preserved behavior + downstream impact
- **AI-assisted requirements with LLM-as-judge validation**
- **Agentic acceptance criteria for AI agent delivery**
- **EU AI Act chain-of-causality traceability**

## Core Rules

- write requirements as observable behavior, not implementation guesses
- make actors, permissions, rules, and exceptions explicit
- define preserved_behavior versus changed_behavior clearly
- identify downstream teams, approvals, or systems affected by the change
- populate `contracts/schemas/feature-ticket.json` when machine handoff is required
- embed `analytics_request` or `seo_content_request` in the ticket when delegating
- do not let ambiguous business intent pass through as an engineering problem
- apply **Layered Requirements Pipeline**: Impact Mapping (Why/Who → actors, KPIs) → Event Storming (What/Flow → domain events) → User Story Mapping (How/Slices → vertical MVP)
- every User Story must trace to Impact Map actor behavior AND Event Storming domain event
- resolve Event Storming hot-spots before sprint backlog finalization
- slice vertically only: each slice spans UI to database with end-to-end user value
- **Epic-Organized Gherkin Pipeline** (arXiv:2607.01980): 4-step async LLM — relevance → requirements → epic/mind-map → Gherkin; JSON-constrained output
- **LLM-as-Judge Validation** (DeepEval, RAGAS): Independent LLM evaluation for clarity, completeness, consistency
- **Living Requirements Traceability**: AI tools (Trace.space, getleo.ai) link requirements → design → code → tests; mandatory for EU AI Act chain-of-causality
- **Agentic AC Format**: Deterministic observable assertions for agent auto-validation
- **Human BA Sign-Off Gate**: Mandatory for AI-assisted AC before sprint commitment

## Suggested Process

### 1. Frame The Business Problem

Clarify: process/rule under analysis, actors, expected outcome, restore vs new behavior.

### 2. Identify Rules And Exceptions

Capture: business rules, approval/permission rules, edge cases, state transitions.

### 3. Trace Process Impact

Name affected: downstream teams/systems, compliance/audit, data/reporting, operational handoffs.

### 4. Delegate Before Locking AC

| Signal | Delegate to | Ticket field |
| ------ | ------------- | ---------------------- |
| Unknown domain, policy, market | Researcher | Research Request → research-report.json |
| Metrics, baselines, funnel counts | Data Analyst | analytics_request → data-analysis-report.json |
| Content discoverability, CTA, linking | SEO Analyst | seo_content_request → seo-content-brief.json |

Do not lock metric/compliance-heavy AC until delegated artifacts return.

### 5. Epic-Organized Gherkin Generation & Validation

1. Relevance Classification (LLM #1): Detect requirement-relevant content
2. Requirements Update (LLM #2): Add/revise living requirements list
3. Epic & Mind Map (LLM #3): Group into 3–6 epics with relationships
4. Gherkin Generation (LLM #4): Feature blocks + Scenarios (JSON-constrained)
5. LLM-as-Judge Validation: DeepEval/RAGAS for clarity, completeness, consistency
6. Human BA Sign-Off: Verify against expert blind assessment before sprint

### 6. Write Testable Acceptance Criteria

Express: primary success scenarios, negative/exception cases, observable outputs, preserved constraints, **Agentic AC** (deterministic assertions for agent auto-validation).

### 7. Package For Delivery

Produce: feature-ticket.json, epic-organized-gherkin-spec.json, llm-as-judge-validation-spec.json, living-traceability-spec.json, agentic-ac-spec.json; markdown brief mirroring ticket sections.

## Output Format

```markdown
# <Topic> - Business Analysis Brief

## Business Context
- Problem: - Actors: - Outcome: - Preserved behavior: - Changed behavior:

## Requirements
- Functional requirements: - Business rules: - Permissions / approvals: - Non-goals:

## Acceptance Criteria
- Primary scenarios: - Negative or exception cases: - Observable outputs: - Agentic assertions (if AI agent delivery):

## Process Impact
- Current flow: - Target flow: - Affected downstream teams or systems:

## Traceability
- Impact Map actors → KPI targets: - Event Storming domain events:
- User Story → Epic → Feature Block → Gherkin Scenario:
- Design doc → Code module → Test case links:

## Open Questions
- ...

## Research Request (optional)
## Analytics Request (optional)
## SEO Content Request (optional)
```

See `core/roles/business-analyst.md` for handoff rules for Researcher, Data Analyst, SEO Analyst.

## Checklist

- [ ] problem, actors, expected outcome defined
- [ ] preserved vs changed behavior stated
- [ ] business rules and exceptions captured
- [ ] downstream process impact identified
- [ ] acceptance criteria made observable
- [ ] open_questions listed
- [ ] Research / Analytics / SEO requests issued when triggers apply
- [ ] feature-ticket.json valid when JSON handoff required
- [ ] Epic-organized Gherkin pipeline: relevance → requirements → epic/mind-map → Gherkin
- [ ] JSON-constrained Gherkin output for structural validity (99%+)
- [ ] LLM-as-judge validation (DeepEval/RAGAS) for clarity, completeness, consistency
- [ ] Living traceability: requirements → design docs → code modules → test cases
- [ ] AI traceability tools (Trace.space, getleo.ai) integrated
- [ ] Agentic AC format: deterministic observable assertions for agent auto-validation
- [ ] EU AI Act chain-of-causality audit trail for high-risk features
- [ ] Human BA sign-off gate for AI-assisted AC before sprint commitment
- [ ] SSE real-time state updates for requirements/epic/Gherkin changes
- [ ] Every User Story traces to Impact Map actor behavior AND Event Storming domain event
- [ ] Event Storming hot-spots resolved before sprint backlog finalization
- [ ] Vertical slicing only: each slice spans UI to database with end-to-end user value

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: requirement may reframe user goal through expanded scope. Cross-check against original request.
- **ASI04 Supply Chain**: AI-generated requirements schema-validated against feature ticket; unknown templates untrusted.
- **ASI07 Inter-Agent Communication**: requirement consumed by Solution Architect and downstream; emit structured contract.
- **ASI09 Human-Agent Trust Exploitation**: do not present AI-assisted requirement as "reviewed" without human sign-off; surface AI provenance.

## Failure Modes

- **AC from solution, not user outcome**: AC describes implementation not user behavior. Mitigation: rewrite in user-observable terms.
- **Hidden stakeholder**: downstream role not in recipient list. Mitigation: enumerate affected stakeholders; surface missing before lock.
- **YMYL without expert sign-off**: YMYL feature ships without SME sign-off. Mitigation: require YMYL gate before AC approval.
- **Requirement drift after approval**: ticket approved then expands. Mitigation: freeze AC at ticket creation; new requirements re-scoped.
- **Epic vs requirement coverage gap**: Epic-organized misses lexical coverage but gains expert preference. Mitigation: TF-IDF + dense embedding metrics.
- **LLM-as-judge false confidence**: Independent LLM misses domain contradictions. Mitigation: blind expert assessment alongside automated eval.
- **Traceability link rot**: AI links become stale. Mitigation: automated CI checks for traceability freshness.
- **Agentic AC over-specification**: Deterministic assertions constrain flexibility. Mitigation: balance observable outcomes with implementation freedom.
- **EU AI Act compliance gaps**: Missing chain-of-causality for high-risk. Mitigation: automated audit trail validation in CI.

## Output Contracts

- `contracts/schemas/feature-ticket.json`
- `contracts/schemas/epic-organized-gherkin-spec.json`
- `contracts/schemas/llm-as-judge-validation-spec.json`
- `contracts/schemas/living-traceability-spec.json`
- `contracts/schemas/agentic-ac-spec.json`

## Related Skills

- **write-product-brief**: Product intent and scope boundaries from PM
- **conduct-research**: Light discovery; deep work with Researcher role
- **design-ux-flow**: Requirements → user-facing interaction flow
- **meeting-review**: Resolve conflicting assumptions or policies
- **write-documentation**: Finalized terminology or process guidance
- **review-service**: Validate implementation matches intended process

Last updated: 2026-09-25