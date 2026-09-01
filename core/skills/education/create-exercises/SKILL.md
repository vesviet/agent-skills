---
name: create-exercises
description: Design educational assignments, practice tests, and quizzes following designated curriculum matrices and cognitive models. Use when generating exercises, mock exams, or exam preparation materials for specific learning objectives.
---

# Create Exercises

Use this skill to generate practical tasks, tests, or mock exams strictly following the educational standards and curriculum matrices specified for the target learners.

## When to Use

- generating practice tests or quizzes
- building exam-prep materials
- mapping exercises to curriculum objectives
- designing assignments for a learning goal

## Core Rules

- strictly adhere to the requested testing format (short quiz, unit test, mid-term, final) and the target grade or proficiency level; never use notations, formulas, or methods not yet taught in the target curriculum
- map every question to a **Bloom's Taxonomy level** (Remember → Understand → Apply → Analyze → Evaluate → Create) and declare the target level explicitly in the exercise matrix before generation
- **AI-generated questions are drafts only**: all AI-generated exercises must pass a qualified educator's review gate before assignment to students — autonomous publish of AI-generated exercise sets is not permitted
- calibrate difficulty dynamically using **Item Response Theory (IRT)** metrics targeting a **70–80% student success rate** — enough challenge to stimulate learning, enough success to sustain motivation
- integrate **spaced repetition triggers** (SM-2 or SM-15 algorithm) in the question scheduler: calculate the next review date from the student's response quality score and easiness factor; never use fixed equal-interval review schedules
- award **partial credit** for correct intermediate steps in constructed-response questions; never score as all-or-nothing when sub-steps are demonstrably correct
- keep a question-level changelog (`question_id`, `bloom_level`, `difficulty_param`, `last_reviewed`) so exercise sets are auditable and adjustable without full regeneration

## Suggested Process

1. **Identify the Objective & Format**: Determine the test type and the specific chapters or modules being tested.
2. **Design the Exam Matrix**: Allocate points across cognitive levels based on the testing goal.
3. **Draft the Questions**: Write age-appropriate questions. Mix multiple-choice and constructed response formats as suitable.
4. **Define the Answer Key & Rubric**: Create a precise grading rubric down to the required partial point steps.
5. **Review for Edge Cases**: Ensure no questions fall outside the defined curriculum scope.

### 2026: Exercise Engineering and Spaced Repetition

To meet modern digital education requirements, three key practices must be implemented in the exercise generation flow:

#### 1. AI-Assisted Exercise Generation Workflow
When using Large Language Models to generate exercises, follow a structured generative pipeline:
- **Bloom's Taxonomy Filtering**: System prompts must specify the target cognitive level (e.g., Remember, Understand, Apply, Analyze, Evaluate, Create). For example, a prompt asking for "Apply" level should generate real-world scenario questions requiring formula usage, not just concept definitions.
- **Taxonomy Level Breakdown**:
  - **Remember**: Recall facts and basic concepts. (Exercise format: Multiple choice, flashcards, definition matching).
  - **Understand**: Explain ideas or concepts. (Exercise format: Summarization, grouping, concept mapping).
  - **Apply**: Use information in new situations. (Exercise format: Calculations, code execution, simulation tasks).
  - **Analyze**: Draw connections among ideas. (Exercise format: Bug identification, architectural comparison, diagram analysis).
  - **Evaluate**: Justify a stand or decision. (Exercise format: Code review reviews, security posture audits, trade-off analyses).
  - **Create**: Produce new or original work. (Exercise format: System design, writing complete modules, project prototyping).
- **Cognitive Complexity Guardrails**: Restrict AI output from generating overly complex or convoluted language that confuses the target grade level.
- **Human Review Gate**: AI-generated questions are treated as drafts. A qualified educator must review, edit, and approve every question before it is compiled into a student quiz or exam database.

#### Cognitive Matrix and Exercise Alignment Table

| Bloom's Level | Cognitive Process | Target Task Type | Assessment Criteria | Example Exercise |
|---|---|---|---|---|
| Remember | Retrieving relevant knowledge | Multiple-choice questions | Accurate recall of facts | "Define the time complexity of binary search." |
| Understand | Constructing meaning | Concept mapping, explanations | Clear explanation of patterns | "Explain how a hash collision is resolved in Java." |
| Apply | Carrying out or using a procedure | Practical calculations, coding | Execution accuracy and output | "Implement a function to reverse a linked list." |
| Analyze | Breaking material into parts | Debugging, parsing log traces | Identification of root cause | "Determine the memory leak source from this pprof output." |
| Evaluate | Making judgments based on criteria | Code reviews, design critique | Structural and safety arguments | "Review this SQL schema design for N+1 vulnerabilities." |
| Create | Putting elements together | System architecture design | Design novelty and integration | "Design a distributed notification system for 10M users." |

#### 2. Adaptive Difficulty Calibration
Exercise sets should adapt dynamically to student performance to optimize engagement and prevent frustration:
- **Item Response Theory (IRT)**: Model student ability and question difficulty as parameters. Questions are selected based on the student's probability of answering correctly, aiming for optimal information gain.
- **Mathematical Calibration (Rasch Model)**:
  - We use the One-Parameter Logistic Model to compute probability:
  - $$P(X_i = 1 | \theta, \beta_i) = \frac{e^{\theta - \beta_i}}{1 + e^{\theta - \beta_i}}$$
  - Where $\theta$ represents student ability and $\beta_i$ represents item difficulty.
- **Three-Parameter Logistic Model (3PL)**:
  - For multiple-choice questions with guessing factors:
  - $$P(X_i = 1 | \theta, a_i, b_i, c_i) = c_i + (1 - c_i) \frac{e^{a_i(\theta - b_i)}}{1 + e^{a_i(\theta - b_i)}}$$
  - Where $a_i$ is discrimination, $b_i$ is difficulty, and $c_i$ is the pseudo-guessing probability.
- **Moving Average Baseline**: Track the student's recent performance using a rolling moving average (e.g., the last 10 exercises).
- **Target Success Rate**: Calibrate the difficulty of the next question block to maintain a 70-80% student success rate. This level of challenge is high enough to stimulate learning but low enough to build confidence.

#### 3. Spaced Repetition Triggers
Retention-optimized courses must trigger reviews at calculated intervals using cognitive science models:
- **SM-2 Algorithm Integration**: Schedule reviews based on the SuperMemo-2 algorithm. Calculate intervals ($I$) using response quality ($q$ from 0 to 5) and easiness factor ($EF$):
  - $I(1) = 1$ day
  - $I(2) = 6$ days
  - For $n > 2$: $I(n) = I(n-1) \times EF$
  - Adjust $EF$ based on performance: $EF' = EF + (0.1 - (5 - q) \times (0.08 + (5 - q) \times 0.02))$
- **SM-15 Algorithm Integration**: For fine-grained adaptive systems, use the SuperMemo-15 algorithm, which models memory retention based on three variables: difficulty, stability, and retrievability.
- **Retrievability Math**:
  - $$R = e^{-\ln(2) \cdot \frac{t}{S}}$$
  - Where $t$ is elapsed time since last review and $S$ is memory stability.
- **Scheduler Integration**: Connect the exercise engine to a background scheduling worker. When a student completes a review, calculate the next review date and queue the notification or study block accordingly.
- **Database Schema Schema**:
  - `card_id` - Identifier for the flashcard or exercise.
  - `repetitions` - Number of successful consecutive reviews.
  - `easiness_factor` - The difficulty multiplier.
  - `next_review_due` - Timestamp of next scheduled review.

## Checklist

- [ ] Test format and duration are clearly stated.
- [ ] Target grade or proficiency level is confirmed before setting difficulty.
- [ ] Questions are distributed according to a clear cognitive matrix.
- [ ] Difficulty ratio reflects the educational goal (foundational vs advanced prep).
- [ ] Answer key provides granular point breakdowns.
- [ ] Language and terminology match official textbooks or standards for that level.
- [ ] AI-assisted generation workflow filters by Bloom's Taxonomy level.
- [ ] Human review gate is defined and implemented before student assignment.
- [ ] Difficulty calibration maps against Item Response Theory (IRT) model.
- [ ] Student success metrics are tracked using a moving average aiming at a 70-80% target rate.
- [ ] Spaced repetition schedules are triggered and integrated with SM-2 or SM-15 schedulers.

## Output Contracts

When the exercise set is consumed by an LMS, a tutoring system, or a
cross-role handoff, emit:

- **`contracts/schemas/learning-handoff.json`** (or, when a stable schema is not yet available, a markdown frontmatter block listing `exercise_id`, `bloom_level`, `difficulty_param`, `last_reviewed`, and `human_review_status`). The frontmatter block is the minimum-viable contract.
- For human-readable reports, the markdown exercise matrix already documented is the canonical format.
- Every AI-generated question must be flagged with the human review status; never assign to students without explicit sign-off.

Skip emission for single-question experiments that do not cross a role boundary.

## Failure Modes

- **Bloom level drift**: a question's cognitive level does not match the declared target. Mitigation: enforce the Bloom's Taxonomy filter; reject questions outside the declared level.
- **AI question published unreviewed**: an AI-generated question ships without a qualified educator's review. Mitigation: enforce the human review gate; reject unreviewed questions.
- **Difficulty calibration off**: the IRT-calibrated difficulty drifts from the 70-80% target success rate. Mitigation: re-calibrate using the rolling moving average; reject question blocks outside the target range.
- **Spaced repetition not triggered**: a review is missed because the scheduler did not compute the next review date. Mitigation: integrate SM-2 or SM-15; assert the next review date is set on every response.
- **Constructed response scored all-or-nothing**: a correct intermediate step receives no credit. Mitigation: award partial credit for demonstrably correct sub-steps; explain the exact step where logic failed.
- **Question outside curriculum**: a question uses notation or a method not yet taught. Mitigation: enforce the curriculum scope; reject out-of-scope questions.
- **Changelog missing**: a question's revision history is not tracked. Mitigation: maintain the question-level changelog (`question_id`, `bloom_level`, `difficulty_param`, `last_reviewed`).

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: never include student identifiers, instructor names, or institutional tokens in the exercise matrix.
- **ASI04 Supply Chain**: AI generation libraries and IRT calibration tools must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct exercise prompts, answer keys, or rubric descriptors from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the exercise handoff is consumed by LMS and tutoring systems; emit a structured contract so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present an AI-generated exercise as "ready to assign" without the educator's review sign-off; surface the AI provenance honestly.

## Related Skills

- **grade-and-review**: Evaluate completed exercises against the rubric.
- **design-learning-plan**: Align exercises with the broader curriculum sequence.
