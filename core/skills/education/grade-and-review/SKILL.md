---
name: grade-and-review
description: Evaluate learner work and provide constructive feedback on the designated grading scale. Use when grading assignments, reviewing student submissions, or providing improvement guidance at any educational level.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Grade And Review

Use this skill to evaluate student submissions against 4-tier criterion-referenced rubrics, eliminate AI grading hallucinations via verifiable line citations, diagnose cognitive error categories, and deliver growth-mindset feedback enforcing the Rule of One.

## When to Use

- evaluating student exercises, code repositories, or open-ended design submissions
- grading against standardized 4-tier analytic rubrics (Beginning, Developing, Proficient, Advanced)
- diagnosing cognitive failure modes (conceptual vs procedural vs boundary vs overload)
- authoring growth-mindset feedback using "not-yet" framing and strictly one actionable remediation step
- emitting verified machine-readable assessment contracts under EU AI Act High-Risk AI governance

## Core Rules

- score submissions using **Standardized 4-Tier Criterion-Referenced Rubrics** (Beginning 0–49%, Developing 50–69%, Proficient 70–89%, Advanced 90–100%) with observable behavioral descriptors; never assign holistic single-number grades (see [`references/analytic-rubrics-and-grading-hallucination-defense.md`](references/analytic-rubrics-and-grading-hallucination-defense.md))
- enforce the **Anti-Hallucination Line Citation Protocol**: every point deduction must explicitly quote the student's submission line number and verbatim text/code snippet; unanchored critiques or fabricated errors are strictly prohibited
- apply the **Anti-Superficial Fluency Filter**: penalize eloquent, AI-synthesized prose that lacks technical rigor, concrete derivations, or unit tests; cap fluency-only work at Level 2 (Developing)
- diagnose underlying cognitive failure modes using the **4-Tier Cognitive Error Taxonomy** (Conceptual Misunderstanding, Procedural Execution Error, Boundary Blindspot, Cognitive Overload) (see [`references/cognitive-error-analysis-and-socratic-feedback.md`](references/cognitive-error-analysis-and-socratic-feedback.md))
- deliver **Carol Dweck Growth-Mindset Feedback**: praise persistence and strategic debugging over innate ability; frame gaps using "not-yet" language
- strictly enforce the **Rule of One**: restrict corrective remediation in each evaluation cycle to **exactly one high-impact actionable step** to prevent cognitive overload and decision fatigue
- comply with **EU AI Act High-Risk AI Governance**: AI grading outputs are advisory recommendations; release to student gradebooks requires verified sign-off by a qualified human educator (`reviewed_by`, `verification_status: "verified_and_approved"`)

## Suggested Process

1. **Submission Inspection & Line-by-Line Review**: Compare student code/work step-by-step against rubric criteria.
2. **Score Against 4-Tier Descriptors**: Assign points across criteria; record mandatory verbatim quotes and line numbers for deductions.
3. **Diagnose Cognitive Error Category**: Classify any logic failures as conceptual, procedural, boundary, or overload.
4. **Draft Growth-Mindset Feedback**: Formulate process praise, "not-yet" framing, and isolate the single highest-impact action step.
5. **Human Educator Verification Gate**: Verify citations against raw source and approve assessment metadata.
6. **Emit Assessment Contracts**: Serialize results to `learning-assessment-report.json` and `learning-handoff.json`.

### In-Depth Reference Guides
- **Rubrics & Hallucination Defense**: [`references/analytic-rubrics-and-grading-hallucination-defense.md`](references/analytic-rubrics-and-grading-hallucination-defense.md) — 4-tier rubric matrices, line citation protocol, fluency filters, and EU AI Act compliance.
- **Cognitive Error Analysis & Socratic Feedback**: [`references/cognitive-error-analysis-and-socratic-feedback.md`](references/cognitive-error-analysis-and-socratic-feedback.md) — Error taxonomy, Dweck growth mindset praise, not-yet framing, and the Rule of One.

## Checklist

- [ ] Submissions are evaluated against explicit 4-tier analytic rubrics with observable behavioral criteria.
- [ ] Every score deduction includes a verified submission line reference and verbatim quote.
- [ ] Anti-superficial fluency filter is applied: ungrounded eloquent text capped at Developing (Level 2).
- [ ] Primary cognitive error category is diagnosed (conceptual, procedural, boundary, overload, or none).
- [ ] Feedback praises effort and strategic debugging rather than innate intelligence or talent.
- [ ] Deficiencies are phrased using constructive "not-yet" developmental language.
- [ ] Actionable remediation guidance is strictly limited to exactly one improvement step (Rule of One).
- [ ] Mandatory EU AI Act audit metadata is populated (`graded_by_ai`, `reviewed_by`, `verification_status`).
- [ ] Student personal data is anonymized using pseudonymous tokens (`student_token`, e.g., `STU-8f2e-2027`).

## Output Contracts

When the assessment result is handed off to a gradebook, LMS, student, or cross-agent workflow, emit:

- **`contracts/schemas/learning-assessment-report.json`** — primary contract populating `student_token`, `overall_score`, `rubric_breakdown` (with line citations), `cognitive_error_diagnosis`, `growth_mindset_feedback`, `zpd_progression`, and `audit_metadata`.
- **`contracts/schemas/learning-handoff.json`** — secondary contract when transmitting multi-agent educational state, learning plan progression, or curriculum handoffs.
- For human-readable reports, emit markdown assessment summaries matching the standard role template.

## Failure Modes

- **Grading hallucination**: AI deducts points for non-existent mistakes. Mitigation: enforce line citation verification gate; reject unanchored deductions.
- **Superficial fluency trap**: awarding advanced grades for articulate but non-working code. Mitigation: enforce anti-fluency filter; verify executable proofs.
- **Feedback avalanche**: overwhelming learner with 5–10 simultaneous critiques. Mitigation: strictly enforce the Rule of One.
- **Fixed-mindset praise**: telling students "you are a natural genius." Mitigation: enforce process and effort praise.
- **Autonomous high-stakes release**: AI grade published without human educator sign-off. Mitigation: enforce EU AI Act human verification gate.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: never include real student PII; enforce pseudonymous student tokens (`STU-...`).
- **ASI04 Supply Chain**: validate automated grading scripts and test runners against trusted manifests.
- **ASI05 RCE Guard**: execute student code only in isolated sandbox containers with resource limits.
- **ASI07 Inter-Agent Communication**: emit structured, schema-valid JSON assessment contracts.
- **ASI09 Human-Agent Trust Exploitation**: surface AI assistance honestly; require educator sign-off.

## Related Skills

- **create-exercises**: Generate targeted follow-up practice addressing diagnosed cognitive errors.
- **design-learning-plan**: Update learner ZPD progression and spaced repetition intervals based on evaluation data.
