# IRT Calibration Models & Granular Scoring Matrices

This reference guide establishes the mathematical principles of Item Response Theory (IRT) for adaptive exercise calibration and defines standardized partial-credit scoring barem structures for constructed-response and programming tasks.

---

## 1. Item Response Theory (IRT) Mathematical Formulations

Traditional classical test theory evaluates questions based solely on raw percentage scores. In contrast, Item Response Theory (IRT) models the non-linear interaction between a learner's latent ability ($\theta$) and the item's intrinsic psychometric characteristics.

### 1.1 The Rasch Model (One-Parameter Logistic / 1PL)
The Rasch 1PL model is the standard model for constructed-response, programming exercises, and open-ended design problems where guessing is negligible:

$$P(X_i = 1 \mid \theta, \beta_i) = \frac{e^{\theta - \beta_i}}{1 + e^{\theta - \beta_i}} = \frac{1}{1 + e^{-(\theta - \beta_i)}}$$

Where:
- $\theta \in (-\infty, +\infty)$: Latent learner capability (typically scaled from -3.0 to +3.0 in standard normal distributions).
- $\beta_i \in (-\infty, +\infty)$: Item difficulty parameter for exercise $i$.
- $P(X_i = 1)$: Probability of the learner successfully solving exercise $i$.

**Properties**:
- When $\theta = \beta_i$, the learner has exactly a $50\%$ probability of answering correctly.
- When $\theta - \beta_i = +1.1$, the success probability reaches $\approx 75\%$ (the ideal calibration point).
- When $\theta - \beta_i \ge +2.0$, success probability exceeds $88\%$ (indicating the challenge is too trivial).
- When $\theta - \beta_i \le -1.5$, success probability falls below $18\%$ (indicating cognitive frustration and anxiety).

### 1.2 The Three-Parameter Logistic Model (3PL)
For multiple-choice questions, diagnostic quizzes, or syntax selection tasks where random guessing is possible, the 3PL model accounts for discrimination and guessing asymptotes:

$$P(X_i = 1 \mid \theta, a_i, b_i, c_i) = c_i + (1 - c_i) \frac{e^{a_i(\theta - b_i)}}{1 + e^{a_i(\theta - b_i)}}$$

Where:
- $a_i > 0$: Item discrimination parameter (the steepness of the logistic curve at the inflection point). Items with $a_i \ge 1.2$ effectively distinguish high-ability from low-ability students.
- $b_i$: Item difficulty inflection parameter.
- $c_i \in [0, 1)$: Pseudo-guessing parameter (the lower asymptote). For a 4-option multiple-choice item, $c_i \approx 0.25$.

---

## 2. Dynamic ZPD Calibration Algorithm (70–80% Target Window)

To sustain deep learning and cognitive flow (avoiding both boredom and anxiety), automated curricula and educators must dynamically calibrate task difficulty to maintain a rolling success rate between **70% and 80%**.

### 2.1 Rolling Moving Average Window
Maintain a sliding window of the learner's last $N = 10$ completed exercise items:

$$\bar{S}_{10} = \frac{1}{10} \sum_{k=t-9}^{t} S_k$$

Where $S_k \in [0.0, 1.0]$ is the normalized score achieved on item $k$.

### 2.2 Difficulty Calibration Update Rule
Following the completion of an exercise block, update the target difficulty $\beta_{next}$ for subsequent assignments:

| Observed Moving Average $\bar{S}_{10}$ | Flow State Diagnostic | Difficulty Adjustment ($\Delta \beta$) | Pedagogical Action |
|---|---|---|---|
| **$\bar{S}_{10} > 0.85$** | Trivial Mastery / Boredom Risk | $\Delta \beta = +0.3$ to $+0.5$ | Elevate task tier (e.g., transition from DOK 2 to DOK 3; introduce concurrent race conditions or resource limits). |
| **$0.70 \le \bar{S}_{10} \le 0.80$** | Optimal Flow State (ZPD) | $\Delta \beta = 0.0$ | Maintain current challenge gradient; vary domain context to solidify schema transfer. |
| **$0.50 \le \bar{S}_{10} < 0.70$** | Developing / Mild Friction | $\Delta \beta = -0.2$ | Provide faded worked examples (Tier 2 Scaffolding); keep conceptual difficulty constant while adding guidance. |
| **$\bar{S}_{10} < 0.50$** | High Anxiety / Cognitive Overload | $\Delta \beta = -0.5$ | Decompose problem into sub-schemas; engage Hint Ladder Level 2; review prerequisite mental models. |

---

## 3. Granular Partial-Credit Scoring Barems

Constructed-response tasks, architectural proposals, and programming challenges must never be evaluated on an all-or-nothing (0 or 100%) basis. Doing so penalizes productive struggle and conceals intermediate conceptual mastery.

### 3.1 The 25 / 50 / 25 Universal Scoring Barem
Every constructed task must partition its point allocation across three standardized phases:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Universal 100% Score Allocation                       │
├───────────────────────┬─────────────────────────────┬───────────────────────┤
│    Conceptual Setup   │   Intermediate Execution    │  Edge-Case & Boundary │
│          25%          │             50%             │          25%          │
│                       │                             │                       │
│  - Problem framing    │  - Algorithmic logic        │  - Invariant defense  │
│  - Invariant selection│  - Data transformations     │  - Null/overflow tests│
│  - Interface contracts│  - Core functional steps    │  - Error handling     │
└───────────────────────┴─────────────────────────────┴───────────────────────┘
```

1. **Phase 1: Conceptual Framing & Architecture Setup (25%)**:
   - Correctly models data contracts, chooses appropriate primitives (e.g., buffered channels, mutexes, specific data structures).
   - Establishes valid interface signatures and state variables.
   - Demonstrates understanding of the governing theoretical constraints.
2. **Phase 2: Intermediate Execution & Core Algorithmic Logic (50%)**:
   - Correctly implements the primary transformation, state transition, or computation.
   - Preserves deterministic behavior on happy-path inputs.
   - Points are awarded incrementally for each verifiable intermediate sub-step, even if subsequent steps fail.
3. **Phase 3: Edge-Case & Boundary Defense (25%)**:
   - Correctly defends against boundary conditions: zero-length collections, null pointers, integer overflow, network timeouts, concurrent race conditions.
   - Implements graceful error propagation and non-panicking recovery.

---

## 4. Concrete Scoring Matrix Templates

### Example: Concurrency-Safe Cache Implementation (Total: 20 Points)

| Phase | Evaluation Criterion | Points | Scoring Descriptor & Verifiable Evidence |
|---|---|:---:|---|
| **Phase 1: Setup** | Interface & Mutex Structure | 3 | Struct contains read-write mutex (`sync.RWMutex`), underlying map, and eviction tracking. |
| | Capacity & Parameter Validation | 2 | Constructor validates `maxSize > 0` and returns structured error for invalid arguments. |
| **Phase 2: Execution** | Concurrent Read Lock Acquisition | 3 | `Get()` method acquires `RLock()`, defers `RUnlock()`, and returns cached item if present. |
| | Write Lock & Safe Insertion | 4 | `Set()` method acquires full `Lock()`, updates storage, and updates access metadata. |
| | Eviction Policy Execution | 3 | When capacity exceeded, correctly identifies LRU node and purges it from index. |
| **Phase 3: Boundary** | Double-Check / Concurrency Race | 2 | Avoids race window between upgrade of `RLock` to `Lock` during cache misses. |
| | Nil Key & Zero-Value Defense | 1 | Handles empty string key or nil payload gracefully without panicking. |
| | Concurrent Stress Test Coverage | 2 | Submits unit test executing 100 concurrent readers and writers without data race. |

### Anti-Patterns in Scoring
- **Binary Grading Penalty**: Marking a 20-point task as 0 points because a single unit test failed an off-by-one check, despite flawless thread synchronization logic.
- **Unanchored Point Deductions**: Subtracting points with comments like "Doesn't look idiomatic" without citing specific lines and standard guidelines.
