---
name: grade-and-review
description: Evaluate learner work and provide constructive feedback on the designated grading scale. Use when grading assignments, reviewing student submissions, or providing improvement guidance at any educational level.
---

# Grade And Review

Use this skill to assess a student's completed exercise, assign scores based on the specified grading scale, and provide constructive, psychologically supportive feedback tailored to the learner's level.

## When to Use

- grading assignments or submissions
- providing improvement feedback
- applying a designated grading scale
- reviewing learner work at any level

## Core Rules

- Always score out of the designated maximum (e.g., 10-point scale, 100-point scale, or letter grades).
- Adjust encouragement tone to the student’s level and context: younger students or those adjusting to a heavier academic load need more supportive framing; advanced students can handle more direct constructive critique.
- Categorize performance internally if needed (e.g., Excellent, Good, Average, Needs Improvement).
- Never just say "Incorrect" without explaining the exact step where the logic failed.
- Utilize a standardized inline rubric template containing criteria, maximum points, and performance descriptors for levels 1 through 4.
- Support LLM-assisted grading flows requiring human verification, recording metadata such as `graded_by_ai`, `reviewed_by`, and `ai_model`.
- Apply growth mindset feedback principles, focusing on effort, strategies, 'not-yet' language, and providing exactly one clear actionable step.

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

## Related Skills

- **create-exercises**: Assign follow-up practice for identified weak points.
- **review-code**: Apply code-review patterns for technical or programming assignments.
