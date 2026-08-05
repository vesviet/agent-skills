---
name: design-learning-plan
description: Create a structured, curriculum-aligned learning plan or syllabus. Use when planning a study schedule, syllabus, exam preparation roadmap, or grade transition plan for any educational level.
---

# Design Learning Plan

Use this skill to structure a personalized or generalized study plan, ensuring strict alignment with the designated educational standards and curriculum scope for the target learners.

## When to Use

- planning a study schedule or syllabus
- building an exam-prep roadmap
- creating a grade-transition plan
- structuring curriculum-aligned learning

## Core Rules

- Always map the plan to the standard academic calendar or the specific timeframe of the learner.
- Organize study blocks based on realistic standard periods (e.g., 45-minute or 60-minute blocks).
- For grade transition plans, explicitly include time for consolidating foundational habits from the previous level before introducing new abstract or advanced content.
- Do not overwhelm the learner; respect cognitive load limits appropriate to the student’s age and background.
- Schedule milestones following spaced repetition principles (days 1, 3, 7, 14, 30) based on the Ebbinghaus forgetting curve.
- Incorporate Feynman technique checkpoints that require students to explain concepts simply and without jargon.
- Integrate LLM tutoring elements that utilize the Socratic method to guide students toward answers rather than revealing them.

## Suggested Process

1. **Analyze Requirements**: Identify the subject, target grade or proficiency level, time constraints, and specific goals (e.g., summer review, mid-term, final exam prep).
2. **Determine the Scope**: Select the chapters and concepts based on the official textbook or curriculum standards for the target.
3. **Sequence the Learning**: Order topics logically. For transition plans, start by reviewing prior key concepts before introducing new theory.
4. **Allocate Time**: Assign realistic learning blocks. Balance between theory, practice, and review.
5. **Set Milestones**: Define checkpoints (quizzes, unit tests, mid-terms, final exams).

### 2026: Scheduling and LLM Tutoring Integration

To ensure maximum long-term memory retention and deep conceptual understanding, learning plans must integrate cognitive science milestones, simplification exercises, and intelligent AI tutoring scaffolds:

#### 1. Spaced Repetition Scheduling (Ebbinghaus Forgetting Curve)
Humans lose about 50% of new information within 24 hours if no review occurs. To counteract this decay, study milestones must be scheduled at optimal retention intervals:
- **Ebbinghaus Forgetting Curve Model**:
  - Memory retrievability decay is represented by:
  - $$R = e^{-\frac{t}{S}}$$
  - Where $R$ is memory retrievability, $t$ is elapsed time, and $S$ is memory stability.
  - Review milestones at days 1, 3, 7, 14, and 30 reset $t$ to 0 and multiply the stability factor $S$, flattening the decay curve over time.
- **Milestone Day 1**: Initial encoding and immediate post-study review (e.g., write down key takeaways).
- **Milestone Day 3**: First active retrieval checkpoint to interrupt initial forgetting.
- **Milestone Day 7**: Conceptual consolidation through application exercises.
- **Milestone Day 14**: Jargon-free mapping and comparison exercises.
- **Milestone Day 30**: Comprehensive active recall and review of the entire module.

#### Retention Schedule Mapping Table

| Timeline | Study Block / Milestone | Cognitive Goal | Active Recall Activity | Forgetting Curve Status |
|---|---|---|---|---|
| Day 1 | Concept Introduction | Encoding & initial comprehension | Immediate quiz / write summary | High decay risk (R drops to ~50% within 24h) |
| Day 3 | First Review Block | Retrieval pathway strengthening | Explain-it-simply exercise | Stability increased; decay rate slowed |
| Day 7 | Second Review Block | Context generalization | Practical application / debugging | Retrievability stabilized at ~80% |
| Day 14 | Mid-term Checkpoint | Synaptic consolidation | Jargon-free concept mapping | Stability further doubled |
| Day 30 | Long-term Assessment | Multi-concept integration | Mock exam / project demo | Long-term memory transfer achieved |

#### 2. Feynman Technique Checkpoints
To confirm deep understanding rather than rote memorization, plans must place "Explain-It-Simply" checkpoints at key milestones. These checkpoints follow four main steps:
- **Feynman Technique Steps**:
  - *Step 1: Identify the Topic*: Write down the concept name at the top of a page.
  - *Step 2: Explain Simply*: Write a description of the concept using language appropriate for a 10-year-old child.
  - *Step 3: Diagnose Gaps*: Highlight areas where the explanation is weak, confusing, or relies too much on technical jargon, then return to the source material to clarify.
  - *Step 4: Simplify and Analogize*: Refine the explanation by removing all jargon and introducing simple real-world analogies.
- **Explain to a Child**: Prompt the student to describe the target concept in writing using the simplified steps.
- **Jargon Elimination**: The response must be audited (either by an LLM or an instructor) to identify technical jargon. If terms like "polymorphism" or "recursion" are used, the student must rewrite the explanation using simple, real-world analogies (e.g., "polymorphism is like a universal remote control that controls different devices").

#### 3. LLM Tutoring Integration
Integrate interactive AI tutoring systems directly into the study blocks:
- **Socratic Method Prompting**: Configure the LLM tutor to act as a Socratic guide. It must never output the code block or direct answer. Instead, it must ask leading questions that nudge the student to identify their own logic errors or fill in missing steps.
- **LLM Socratic Prompt Blueprint**:
  ```markdown
  System Prompt:
  You are an expert Socratic tutor in this subject. Your goal is to guide the student.
  Constraints:
  - Do NOT provide the final code, answer, or solution to the problem.
  - Ask exactly one guiding question at a time to lead the student to the next step.
  - If the student makes an error, point out the logical inconsistency gently.
  - Prompt the student to explain their reasoning if they show confusion.
  ```
- **Socratic Interaction Flow**:
  - The student submits a code attempt or math calculation.
  - The AI tutor checks for syntax or logical errors.
  - Instead of correcting the code, the AI asks a Socratic question about the expected output (e.g., "What value does the loop variable take on the first iteration?").
  - The student responds to the question, and the process repeats.
- **Scaffolded Hints**: When a student gets stuck, the AI tutor should provide hints graded by depth:
  - *Hint Level 1*: Focus student attention on the specific line or rule violated.
  - *Hint Level 2*: State the conceptual rule in simple terms.
  - *Hint Level 3*: Provide a simplified mini-problem showcasing the same pattern.

## Checklist

- [ ] Target grade/level and specific goal are explicitly defined.
- [ ] Timeline matches the school year structure and reasonable period blocks.
- [ ] Plan includes age-appropriate review checkpoints.
- [ ] Curriculum aligns with the designated educational standards.
- [ ] Built-in time for consolidating learning habits or bridging previous gaps is included.
- [ ] Spaced repetition milestones scheduled at days 1, 3, 7, 14, and 30 to mitigate Ebbinghaus forgetting curve decay.
- [ ] Feynman technique checkpoints embedded to test simplification and jargon-free explanation.
- [ ] LLM tutoring modules configured to follow Socratic questioning paths instead of direct answers.
- [ ] `learning-handoff.json` emitted when handing the plan to another teacher or to a parent/administrator consumer (see Output Contracts)

## Output Contracts

When this skill is the producing role for a `learning-handoff.json` artifact (per `core/contracts/schemas/learning-handoff.json`), emit:

- **`contracts/schemas/learning-handoff.json`** — populate `moet_alignment[]` from the curriculum standards referenced, `plan_phases[]` mirroring the timeline blocks above, `exercise_refs[]` pointing at the artifacts produced by `create-exercises`, and `evaluation_rubric_ref` for `grade-and-review` to consume. This ensures downstream teachers or automated tutors ingest a machine-readable plan rather than re-parsing prose.

Skip emission for one-off ad-hoc tutoring sessions with no persistent handoff.

## Related Skills

- **create-exercises**: Design practice materials that match the plan milestones.
- **analyze-business-requirements**: Adapt the plan when broader program goals or constraints apply.
