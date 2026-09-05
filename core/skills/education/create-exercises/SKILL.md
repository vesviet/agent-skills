---
name: create-exercises
description: Design educational assignments, practice tests, and quizzes following designated curriculum matrices, Webb's DOK 1-4, and cognitive models. Use when generating exercises, mock exams, or exam preparation materials for specific learning objectives.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Create Exercises

Use this skill to generate practical tasks, problem sets, and exams strictly following the educational standards, Depth of Knowledge (DOK) levels, and curriculum matrices specified for the target learners.

## When to Use

- generating practice tests, coding katas, or diagnostic quizzes
- engineering AI-resistant case studies and flawed artifacts for student debugging
- calibrating exercise sets to learner ZPD using Item Response Theory (IRT)
- mapping exercises to curriculum objectives and Bloom 2027 HOTS tiers
- structuring granular partial-credit scoring matrices and answer keys

## Core Rules

- strictly adhere to the requested testing format (short quiz, unit test, mid-term, final) and target proficiency level; never use notations, formulas, or methods not yet taught in the target curriculum
- map every question to **Webb's Depth of Knowledge (DOK 1 to 4)** and **Bloom's Taxonomy 2027**; declare target cognitive levels explicitly before generation (see [`references/dok-and-ai-resistant-exercise-design.md`](references/dok-and-ai-resistant-exercise-design.md))
- implement **AI-Shortcut Resistance**: embed proprietary context, synthetic flaws/hallucinations for student debugging, raw artifact telemetry, or oral defense prompts to prevent copy-paste solving
- calibrate difficulty dynamically using **Item Response Theory (IRT)** (Rasch 1PL / 3PL models) targeting a **70–80% student success moving average** across a rolling 10-item window (see [`references/irt-calibration-and-scoring-matrices.md`](references/irt-calibration-and-scoring-matrices.md))
- award **granular partial credit** across conceptual setup (25%), execution logic (50%), and edge-case boundary verification (25%); strictly prohibit all-or-nothing scoring for constructed responses
- **AI-generated questions are drafts only**: all AI-generated exercises must pass a qualified human educator's review gate before assignment to students
- keep a question-level changelog (`question_id`, `dok_level`, `difficulty_param`, `last_reviewed`, `human_review_status`) for auditability

## Suggested Process

1. **Intake & Diagnostic Assessment**: Determine target subject, curriculum standards, and learner latent ability ($\theta$).
2. **Design Exercise Matrix**: Allocate items across Webb's DOK 1–4 and Bloom HOTS (Analyze, Evaluate, Create).
3. **Draft Context-Bound Problems**: Engineer exercises embedding real-world constraints, synthetic flaws, or artifact telemetry.
4. **Calibrate IRT Parameters**: Model item difficulty ($\beta$) to sustain a 70–80% success moving average in the learner's ZPD.
5. **Construct Scoring Barems**: Author granular partial-credit answer matrices (25% setup / 50% execution / 25% edge cases).
6. **Human Educator Verification Gate**: Route drafted exercises for educator review and sign-off prior to student release.

### In-Depth Reference Guides
- **DOK & AI Resistance**: [`references/dok-and-ai-resistant-exercise-design.md`](references/dok-and-ai-resistant-exercise-design.md) — DOK 1–4 matrix, cognitive verb distribution, and 5 AI-shortcut resistance archetypes.
- **IRT Calibration & Scoring**: [`references/irt-calibration-and-scoring-matrices.md`](references/irt-calibration-and-scoring-matrices.md) — Rasch 1PL/3PL formulas, rolling moving average calibration, and partial-credit barems.

## Checklist

- [ ] Target grade, subject domain, and curriculum standards are verified before generation.
- [ ] Questions are distributed according to Webb's DOK 1–4 matrix and Bloom 2027 HOTS alignment.
- [ ] Problem prompts incorporate at least one AI-shortcut resistance archetype (context-bound, synthetic flaw, raw telemetry).
- [ ] Difficulty parameter ($\beta$) is calibrated via IRT to target a 70–80% rolling success rate in the learner's ZPD.
- [ ] Constructed-response items have granular partial-credit scoring barems (25% setup / 50% execution / 25% boundary).
- [ ] No constructed-response items use all-or-nothing scoring.
- [ ] AI-generated exercise sets contain explicit human review gate metadata (`reviewed_by`, `verification_status`).
- [ ] Question-level changelog tracks `question_id`, `dok_level`, `difficulty_param`, and `last_reviewed`.

## Output Contracts

When the exercise set crosses a role boundary or is handed off to an LMS, tutoring engine, or teacher, emit:

- **`contracts/schemas/learning-handoff.json`** — populating `artifact_type: "exercises"`, `dok_level`, `bloom_taxonomy_tier`, `ai_resistance_mechanisms`, and `content_paths`.
- For human-readable formats, emit an exercise matrix markdown file detailing questions, DOK tags, IRT parameters, and partial-credit barems.
- Every AI-generated question set must record human review metadata before student assignment.

## Failure Modes

- **DOK level drift**: a question's cognitive depth does not match the declared DOK tier. Mitigation: verify active verbs and multi-step reasoning requirements; reject rote questions labeled as DOK 3/4.
- **Trivial LLM copy-paste vulnerability**: an exercise is solved instantly by generic AI without critical thinking. Mitigation: apply Archetype 1 (context-bound) or Archetype 2 (synthetic flaw injection).
- **Difficulty calibration drift**: student success rate diverges from the 70–80% target window. Mitigation: recalibrate difficulty parameter $\beta$ via Rasch 1PL model using rolling moving average.
- **All-or-nothing scoring**: intermediate correct logic receives 0 points due to final step slip. Mitigation: enforce the 25/50/25 partial-credit barem.
- **Unreviewed exercise release**: AI-drafted questions assigned directly to learners without educator sign-off. Mitigation: enforce the EU AI Act human review gate.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: never include student personal identifiers or institutional credentials in exercise sets.
- **ASI04 Supply Chain**: validate automated test harnesses and IRT calculation modules against approved manifests.
- **ASI05 RCE Guard**: sanitize test execution environments when executing student-submitted code or tests.
- **ASI07 Inter-Agent Communication**: emit structured `learning-handoff.json` payloads for reliable multi-agent processing.
- **ASI09 Human-Agent Trust Exploitation**: transparently declare AI provenance and require human educator sign-off.

## Related Skills

- **grade-and-review**: Evaluate completed exercises against 4-tier analytic rubrics and diagnose cognitive errors.
- **design-learning-plan**: Sequence exercises within broader adaptive ZPD pathways and spaced repetition schedules.
