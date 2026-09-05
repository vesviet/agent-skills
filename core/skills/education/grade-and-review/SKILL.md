---
name: grade-and-review
description: Evaluate learner work and provide constructive feedback on the designated grading scale. Use when grading assignments, reviewing student submissions, or providing improvement guidance at any educational level.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Grade And Review

Use this skill to assess a student's completed exercise, assign scores based on the specified grading scale, and provide constructive, psychologically supportive feedback tailored to the learner's level.

## When to Use

- grading assignments or submissions
- providing improvement feedback
- applying a designated grading scale
- reviewing learner work at any level

## Core Rules

- always score out of the designated maximum and calibrate encouragement tone to the learner's level — younger or struggling students need supportive framing; advanced learners can absorb direct critique
- **AI is a grading assistant, not the decision-maker** (EU AI Act High-Risk AI classification, effective August 2026): AI grading outputs are recommendations; a qualified human educator MUST review, adjust, and approve before any grade is communicated to the student or used for progression decisions
- **Four-tier criterion-referenced rubric**: every assessment must decompose into specific criteria with observable behavioral descriptors across 4 tiers (Beginning 0–49% / Developing 50–69% / Proficient 70–89% / Advanced 90–100%) — never grade on a holistic single-number scale without criterion breakdowns
- award **partial credit** for correct intermediate steps; never score as all-or-nothing; explain the exact step where logic failed when marking incorrect — never just say "Incorrect"
- **Growth Mindset feedback protocol**: praise effort and strategy, not innate ability; use "not-yet" framing for gaps ("You haven't mastered X yet, but..."); limit critical feedback to **exactly one major actionable step** per review session to prevent cognitive overload
- **mandatory audit metadata** on every AI-assisted grading record: `graded_by_ai: true`, `reviewed_by: "<name> (ID)"`, `ai_model: "<model-id>"`, `verification_status: "verified"`, `verification_timestamp` — records without this block are not submission-ready
- **anti-superficial-fluency guardrail**: do not award high rubric marks for articulate phrasing alone (AI easily produces fluency); prioritize analytical rigor, reasoning evidence, and factual accuracy in scoring

## Suggested Process

1. **Review the Submission**: Compare the student's work step-by-step against the rubric or answer key.
2. **Score the Work**: Award partial points for correct intermediate steps, even if the final answer is wrong. Calculate the final score.
3. **Draft Student Feedback**: Address the student directly. Highlight what they did well before pointing out mistakes.
4. **Draft Parent/Sponsor Feedback (Optional)**: Summarize the student's current proficiency and suggest home support if requested.
5. **Provide a Correction Guide**: Offer detailed, step-by-step hints so the student can arrive at the correct answer themselves.

### 2026: Rubrics, AI Grading, and Feedback Science

To standardize grading quality, increase grading efficiency, and reinforce student motivation, the evaluation process incorporates the following 2026 standards:

#### 1. Standardized Inline Rubric Template
All assessments must use a structured four-level rubric. For each criterion, the grader evaluates the student against specific performance descriptors:

#### Rubric Performance Levels Table

| Performance Level | Descriptor | Percentage Range | Core Focus |
|---|---|---|---|
| Level 1: Beginning | Lacks basic understanding, cannot write compiling/correct structures | 0% - 49% | Critical foundational gaps |
| Level 2: Developing | Approaches standards; code compiles but fails primary logical checks | 50% - 69% | Syntax correct; logic errors present |
| Level 3: Proficient | Meets standards; solution is correct and passes all primary test cases | 70% - 89% | Logic correct; needs style or minor speed adjustments |
| Level 4: Advanced | Exceeds standards; handles all extreme edge cases and optimizes complexity | 90% - 100% | Flawless execution and design patterns |

- **Sample Rubric Structure**:
  ```yaml
  criterion: "Logic and Correctness"
  max_points: 10
  level_descriptors:
    level_1: "Code does not execute or outputs unrelated results (0-4 points)."
    level_2: "Code executes but fails key functional requirements (5-6 points)."
    level_3: "Code compiles and correctly solves the main problem (7-8 points)."
    level_4: "Code is fully correct, optimized, and free of logical flaws (9-10 points)."
  ```

#### 2. LLM-Assisted Grading and Verification
To speed up the evaluation process, utilize an AI model to perform the initial assessment, which must then be audited by a human instructor:
- **AI Evaluation**: The LLM analyzes the submission against the rubric, marks the syntax, calculates initial scores, and drafts a feedback report.
- **Verification Requirement**: A human instructor must review the AI-generated assessment, adjust points where nuance was missed, and approve the submission.
- **Mandatory Schema Metadata**: The resulting grade entry must include the following verification audit block:
  ```yaml
  graded_by_ai: true
  reviewed_by: "Jane Doe (ID: 4091)"
  ai_model: "gpt-4o-mini-2024-07-18"
  verification_status: "Verified and Approved"
  ```

#### 3. Growth Mindset Feedback Science
Feedback should be written in accordance with educational psychology, focusing on building long-term resilience:
- **Effort and Strategy Focus**: Praise the student's process and planning rather than their innate intelligence. Use phrases like "Your approach to dividing the helper functions shows strong strategic planning" instead of "You are very smart at programming".
- **"Not-Yet" Language**: Frame areas of improvement as ongoing learning paths. Write "You haven't mastered complex edge-case handling *yet*, but you can get there by practicing..." instead of "You failed edge-case testing".
- **One Actionable Step Limit**: To prevent cognitive overload and discouragement, limit critical feedback to exactly one major improvement action.

#### 4. Graded Assessment Example
Below is an example of an AI-generated assessment record that has been approved by an educator:
```yaml
student_id: "STUDENT_98412"
exercise_id: "EX_ALG_502"
raw_score: 8.5
max_points: 10.0
grade_tier: "Level 3: Proficient"
rubric_breakdown:
  logic_correctness:
    score: 8.0
    max: 10.0
    level: 3
    notes: "Algorithm correctly handles normal cases but has O(N^2) complexity where O(N log N) is possible."
growth_mindset_feedback:
  effort_strategy_praise: "I appreciate the detailed comments you wrote to map out the sorting steps before implementing the logic. This systematic approach is very helpful for debugging."
  not_yet_phrasing: "You have not optimized the time complexity to O(N log N) yet, but you are very close. Consider using a divide-and-conquer strategy."
  one_actionable_step: "For your next attempt, rewrite the partition step using a two-pointer approach to eliminate the nested iteration."
metadata:
  graded_by_ai: true
  reviewed_by: "Jane Doe (Educator ID: 4091)"
  ai_model: "gpt-4o-mini-2024-07-18"
  verification_timestamp: "2026-06-21T09:38:12Z"
```

## Checklist

- [ ] Final score uses the correct standard scale.
- [ ] Partial credit is awarded for constructed-response questions.
- [ ] Feedback tone is appropriate for the student's level.
- [ ] Specific corrections are provided for every mistake.
- [ ] Terminology strictly aligns with the relevant educational standards.
- [ ] Inline rubric is populated with criteria and level 1-4 descriptors.
- [ ] Metadata fields (`graded_by_ai`, `reviewed_by`, and `ai_model`) are recorded correctly.
- [ ] Feedback focuses on effort, uses 'not-yet' phrasing, and specifies exactly one actionable step.

## Output Contracts

When the grading result is consumed by a gradebook, a parent report, or
a cross-role handoff, emit:

- **`contracts/schemas/learning-handoff.json`** (or, when a stable schema is not yet available, a markdown frontmatter block listing `student_id`, `exercise_id`, `raw_score`, `max_points`, `grade_tier`, `rubric_breakdown`, and `metadata`). The frontmatter block is the minimum-viable contract.
- For human-readable reports, the markdown feedback already documented is the canonical format; emit JSON only when crossing a role boundary.
- Every AI-assisted grading record must include the mandatory audit metadata block (`graded_by_ai`, `reviewed_by`, `ai_model`, `verification_status`, `verification_timestamp`); records without this block are not submission-ready.

Skip emission for inline explanatory feedback that does not produce a grade record.

## Failure Modes

- **AI grading without review**: an AI-generated grade ships to the student without a qualified educator's review. Mitigation: enforce the EU AI Act High-Risk AI classification; require human review and approval.
- **Single-number grade**: a holistic single-number score is given without criterion breakdowns. Mitigation: enforce the four-tier criterion-referenced rubric; reject single-number scores.
- **All-or-nothing scoring**: a correct intermediate step receives no credit. Mitigation: award partial credit for demonstrably correct sub-steps; explain the exact step where logic failed.
- **Superficial fluency rewarded**: a high rubric mark is awarded for articulate phrasing alone. Mitigation: prioritize analytical rigor, reasoning evidence, and factual accuracy; reject fluency-only scores.
- **More than one actionable step**: critical feedback lists multiple major actions. Mitigation: limit to exactly one major actionable step per review session; reject over-stuffed feedback.
- **Effort vs ability praise**: feedback praises innate ability instead of effort and strategy. Mitigation: enforce the growth mindset protocol; use "not-yet" framing for gaps.
- **Audit metadata missing**: a grading record lacks `graded_by_ai`, `reviewed_by`, or `ai_model`. Mitigation: enforce the mandatory audit metadata block; reject records without it.
- **Tone mismatch**: feedback tone is harsh for a young or struggling student. Mitigation: calibrate encouragement tone to the learner's level.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: never include student identifiers, instructor names, or institutional tokens in shared grading records beyond what is required.
- **ASI04 Supply Chain**: AI grading libraries and rubric validators must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct grading prompts, rubric scores, or feedback text from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the grading record is consumed by gradebook and parent-report systems; emit a structured contract so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present an AI-generated grade as the final grade; surface the AI provenance and the human reviewer honestly.

## Related Skills

- **create-exercises**: Assign follow-up practice for identified weak points.
- **review-code**: Apply code-review patterns for technical or programming assignments.
