# Cognitive Error Analysis & Socratic Feedback

This reference guide establishes the diagnostic taxonomy for classifying student learning errors and outlines the pedagogical protocol for delivering growth-mindset feedback enforcing Carol Dweck's educational psychology and the "Rule of One" in 2026–2027.

---

## 1. The 4-Tier Cognitive Error Taxonomy

When evaluating student work, educators and evaluators must diagnose the root cognitive failure mechanism rather than merely labeling an answer "incorrect."

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Cognitive Error Taxonomy                           │
├─────────────────────────┬─────────────────────────┬─────────────────────────┤
│ Conceptual              │ Procedural              │ Boundary / Edge Case    │
│ Misunderstanding        │ Execution Error         │ Blindspot               │
│                         │                         │                         │
│ - Flawed mental model   │ - Correct mental model  │ - Happy path succeeds   │
│ - Broken domain axioms  │ - Syntax / off-by-one   │ - Fails on null/overflow│
│ - Re-anchor schemas     │ - Linter / unit test    │ - Counter-example test  │
├─────────────────────────┴─────────────────────────┴─────────────────────────┤
│ Cognitive Overload Interference                                             │
│ - High element interactivity (>3–5 elements) saturates working memory       │
│ - Solution: Decompose task into sequenced sub-schemas                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.1 Conceptual Misunderstandings (Flawed Mental Models)
- **Nature**: The learner holds an incorrect theoretical model of how the underlying system operates.
- **Manifestations**:
  - Confusing concurrency with parallelism (e.g., believing that spawning 10,000 goroutines on a single-core CPU provides 10,000x speedup).
  - Assuming HTTP `GET` requests are inherently idempotent and secure because they do not carry request bodies.
  - Misunderstanding variable scoping in closures within asynchronous loops.
- **Pedagogical Remediation**: Do not provide quick syntax fixes. Re-anchor the foundational schema using physical analogies, memory trace diagrams, or formal invariant definitions.

### 1.2 Procedural Execution Errors (Slips & Mechanical Lapses)
- **Nature**: The learner's mental model is correct, but execution slips occurred during translation into code or calculations.
- **Manifestations**:
  - Off-by-one loop indexing (`i <= len(slice)` instead of `i < len(slice)`).
  - Typographical mistakes in variable names or misplaced return statements.
  - Applying addition instead of multiplication in a known formula.
- **Pedagogical Remediation**: Provide Hint Level 1 (Constraint Focus) directing attention to the offending line, or encourage running the compiler/linter. Avoid over-explaining the concept.

### 1.3 Boundary & Edge-Case Blindspots
- **Nature**: The learner successfully implements the core transformation for standard happy-path inputs, but fails to consider boundary conditions or adversarial states.
- **Manifestations**:
  - Function panics when receiving a nil pointer, empty array, or zero capacity.
  - Integer overflow when calculating midpoints (`(low + high) / 2`).
  - Network timeout or connection drop unhandled in distributed RPC calls.
- **Pedagogical Remediation**: Present an adversarial test case or counter-example that exercises the unhandled boundary. Prompt the student to observe the runtime failure and formulate a guard condition.

### 1.4 Cognitive Overload Interference
- **Nature**: The learner exhibits disorganization, fragmented logic, or incomplete implementations because the task's element interactivity exceeded working memory capacity ($> 3\text{--}5$ interacting novel elements).
- **Manifestations**:
  - Abandoning structured design; mixing unrelated concerns in a monolithic function.
  - Attempting to handle caching, authentication, database transactions, and parsing all at once.
- **Pedagogical Remediation**: Pause the assignment. Decompose the challenge into isolated sub-problems. Provide a faded worked example for the initial stage before resuming.

---

## 2. Growth-Mindset Feedback Science (Carol Dweck)

Feedback tone profoundly influences learner persistence and self-efficacy. In accordance with Carol Dweck's growth-mindset research, feedback must praise deliberate process rather than innate ability.

### 2.1 Process Praise vs Ability Praise

| Category | Ineffective / Harmful Praise (Fixed Mindset) | Effective Growth-Mindset Praise (Process & Strategy) |
|---|---|---|
| **High Achievement** | "You are a natural genius at distributed systems!" | "Your methodical approach to diagramming the Raft election state machine before writing code produced exceptionally clean synchronization logic." |
| **Effort & Grit** | "At least you tried your best." | "I appreciate how systematically you isolated the race condition by adding deterministic logging before attempting a fix." |
| **Debugging** | "You are so smart for figuring that out so quickly." | "Your persistence in authoring an automated reproduction test allowed you to catch the subtle race condition on line 42." |

*Why Fixed Praise Fails*: Telling students they are "smart" creates anxiety around maintaining that perception, causing them to avoid challenging DOK 3/4 tasks where failure is possible.

### 2.2 The "Not-Yet" Constructive Framing
Deficiencies and failing tests must never be framed as permanent limitations. Always employ "not-yet" framing:
- *Harmful*: "You failed the thread-safety requirement."
- *Constructive*: "You have **not yet** synchronized the shared order map across concurrent client threads. With proper mutex guards, your logic will hold."

---

## 3. The "Rule of One" (Strict Cognitive Scaffolding Limit)

A major failure mode in automated grading and teacher feedback is the *feedback avalanche*: presenting a struggling student with 5 to 10 distinct corrections across syntax, architecture, formatting, and performance in a single review session.

### 3.1 The Cognitive Overwhelm Mechanism
When learners receive more than two critical corrections simultaneously:
- Working memory becomes saturated.
- Emotional defensiveness and decision fatigue trigger disengagement.
- Learners fix the easiest cosmetic items (e.g., indentation) while ignoring critical architectural blockers.

### 3.2 The Rule of One Protocol
Every feedback deliverable must restrict its critical action guidance to **strictly one high-impact remediation step**:
1. **Identify the Highest-Severity Blocker**: Evaluate all detected errors against the hierarchy:
   $$\text{Conceptual Flaw} > \text{Concurrency/Data Race} > \text{Algorithmic Correctness} > \text{Boundary Blindspot} > \text{Style/Optimization}$$
2. **Isolate That Single Item**: Craft a single, concrete, actionable directive for the learner's immediate next iteration.
3. **Queue Secondary Feedback**: Store minor style improvements, linting suggestions, or secondary optimizations in the diagnostic log for subsequent review cycles.
4. **Pair with a Socratic Question**: Conclude the feedback with an open inquiry question guiding the student to solve that single step.

---

## 4. Concrete Socratic Feedback Case Study

### Context
Student submission implements a concurrent banking ledger in Go.
- *Submission*: Lines 30–45 contain an unlocked map write causing a data race under concurrent transfers. In addition, variable names are brief (`a`, `b`), and comments are missing.

### Compliant Feedback Report (Rule of One Applied)

```markdown
### Evaluation & Feedback for Student STU-8f2e-2027

#### 1. Strategy & Effort Praise
Your structured breakdown of debit and credit transaction stages in `Transfer()` shows strong procedural planning! The validation of non-negative account balances before transfer is executed cleanly.

#### 2. "Not-Yet" Framing
You have not yet synchronized access to the shared `accounts` map across concurrent transfer threads, which triggers a data race when two clients transfer simultaneously.

#### 3. Single Actionable Next Step (The Rule of One)
Focus exclusively on protecting the `accounts` map mutation by acquiring your struct's `sync.Mutex` before line 34 and deferring its unlock. (Do not worry about variable renaming or comments right now).

#### 4. Socratic Probing Question
What happens to memory consistency in the Go runtime if client thread A writes to `accounts["user1"]` at the exact same nanosecond that client thread B reads `accounts["user1"]`?
```
