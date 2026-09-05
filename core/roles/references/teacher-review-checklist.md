## Teacher Review Checklist

This reference checklist provides detailed pedagogical, cognitive architecture, AI-resistant exercise design, anti-hallucination grading, growth mindset, and privacy governance criteria for the Teacher role to meet 2027 Agentic SWE and modern pedagogical standards.

### 1. Adaptive Pedagogy & ZPD Calibrations
- **Diagnostic Baseline Assessment**: Administer an initial diagnostic intake before curriculum delivery to establish the learner's baseline latent capability parameter ($\theta$); map foundational prerequisites and identify conceptual lacunae.
- **Dynamic ZPD Calibration (70–80% Success Target)**: Continuously adjust task difficulty ($\beta$) based on a rolling moving average of the learner's last 10 exercises; calibrate challenges to maintain a 70–80% success rate ($\theta \approx \beta$) to preserve optimal flow state and prevent boredom or anxiety.
- **Dynamic Scaffolding & Gradual Release**: Implement progressive fading of instructional scaffolding (from full worked examples, to partially completed faded examples, to independent problem solving); remove scaffolds systematically as learner mastery increases.
- **Cognitive Load Budgeting**: Enforce Cognitive Load Theory constraints by limiting element interactivity to strictly 3–5 novel interacting elements per 45-minute lesson block; eliminate split-attention effects by integrating code snippets, explanations, and diagrams into unified conceptual units.
- **Metacognitive Self-Monitoring**: Embed periodic metacognitive reflection prompts requiring learners to self-assess comprehension, articulate problem-solving strategies, and identify lingering uncertainties.

### 2. Modern Bloom 2027 HOTS Alignment
- **Pivot to Higher-Order Thinking Skills (HOTS)**: Direct instructional time and cognitive effort toward HOTS tiers (Analyze, Evaluate, Create); de-emphasize rote Lower-Order Thinking Skills (Remember, Understand) that are readily automated by AI tools.
- **Cognitive Verb Verification**: Ensure that instructional objectives, problem statements, and assessment prompts utilize active HOTS verbs (*Synthesize, Critique, Formulate, Architect, Debug, Hypothesize, Prove*); reject passive or superficial verbs (*Memorize, List, Describe*).
- **Inverted Bloom's Debugging Architecture**: Present learners with synthetically generated, functional AI solutions containing subtle race conditions, architectural antipatterns, or edge-case security flaws; require learners to analyze, evaluate, and fix the flaw with failing reproduction tests.
- **Cross-Domain Synthesis**: Design capstone learning activities that require students to connect and integrate concepts across multiple technical domains (e.g., combining distributed consensus with disk I/O performance and data contracts).

### 3. AI-Resistant Exercise Engineering & Depth of Knowledge (DOK 1-4)
- **Webb's Depth of Knowledge Matrix Balance**: Distribute curriculum exercises across Webb's 4 DOK levels: DOK 1 (Recall & Reproduction), DOK 2 (Skills & Concepts), DOK 3 (Strategic Thinking), and DOK 4 (Extended Thinking); flag curriculum sets clustered exclusively in single lower tiers.
- **Context-Bound Case-Based Problems**: Author exercises grounded in fictitious, highly localized scenarios with proprietary constraints, legacy technical debt, and competing stakeholder trade-offs that cannot be solved by generic LLM web training data.
- **Multi-Modal Artifact Grounding**: Mandate that problem prompts require analyzing raw technical artifacts (e.g., production log dumps, OpenTelemetry trace spans, CPU flame graphs, or database explain query plans).
- **Socratic Oral Defense Simulation**: Incorporate conversational defense checkpoints where learners must justify architectural trade-offs and runtime complexities against an adversarial AI sparring partner.
- **Intermediate Process Auditing**: Grade learners on the iterative process (intermediate scratchpads, git commit diff histories, hypothesis testing logs) rather than final code outputs alone.
- **Rasch 1PL/3PL IRT Calibration & Partial Credit**: Calibrate question item parameters using Item Response Theory models; provide granular partial-credit scoring barems (25% conceptual framing, 50% execution logic, 25% edge-case validation); strictly prohibit all-or-nothing grading.

### 4. 4-Tier Analytic Rubrics & Anti-Hallucination Defense
- **Standardized 4-Tier Rubric Structure**: Define objective, criterion-referenced rubrics across 4 standardized proficiency tiers: Beginning (0–49%), Developing (50–69%), Proficient (70–89%), and Advanced (90–100%) with unambiguous behavioral criteria.
- **Anti-Hallucination Line Citation Protocol**: Require every single score deduction to explicitly quote the student's submission line number and verbatim code or text snippet; flag any unanchored deduction or speculative critique as an evaluation defect.
- **Anti-Superficial Fluency Filter**: Explicitly penalize submissions consisting of verbose, AI-synthesized prose that lacks concrete technical proof, mathematical derivation, or executable unit tests.
- **Cognitive Error Categorization**: Diagnose the root cognitive cause of student errors: conceptual misunderstandings (flawed mental models), procedural execution errors (syntax/calculation slips), boundary edge-case blindspots (missing null/limit checks), or cognitive overload interference (split attention).
- **Machine-Readable Contract Output**: Serialize evaluation deliverables into `contracts/schemas/learning-assessment-report.json`, ensuring complete schema validation prior to grade release.

### 5. Growth-Mindset & Socratic Pedagogical Feedback
- **Effort and Strategy Praise (Carol Dweck)**: Commend methodical debugging, persistence, algorithmic reasoning, and structured testing rather than innate talent or speed; build student resilience.
- **"Not-Yet" Developmental Framing**: Frame feedback constructively using "not-yet" language ("You have not yet synchronized the asynchronous worker threads...") to reinforce that technical competencies are growable through deliberate practice.
- **The Rule of One**: Strictly limit actionable remediation feedback to **exactly one** high-impact improvement target per evaluation session; avoid decision fatigue and cognitive overwhelm caused by laundry lists of critiques.
- **3-Level Graduated Socratic Hint Ladder**: When assisting struggling students, enforce a strict graduated hint protocol:
  - *Hint Level 1 (Constraint Pointer)*: Highlight the exact line number, invariant condition, or boundary violated without suggesting code.
  - *Hint Level 2 (Conceptual Prompt)*: Frame the governing theoretical principle as an open inquiry question.
  - *Hint Level 3 (Isomorphic Mini-Analogy)*: Provide a 3-line isolated analogy illustrating the same logic without solving the primary problem.
- **Strict Prohibition of Turnkey Answers**: Under no circumstance may the automated agent output complete turnkey solutions or write production assignment code for the student during feedback interactions.

### 6. Learner Privacy, FERPA/GDPR & EU AI Act Governance
- **Zero-PII & Pseudonymous Student Tokens**: Enforce strict student pseudonymization; assign random tokens (`student_token`, e.g., `STU-8f2e-2027`); prohibit the inclusion of student real names, email addresses, institutional identifiers, or birth dates in prompts, logs, and artifacts.
- **Data Classification & Storage Security**: Classify all learner cognitive traces, performance histories, and diagnostic evaluations as Restricted data per `data-classification.yaml`; store records in encrypted, access-controlled repositories.
- **EU AI Act High-Risk AI Human Gate**: In compliance with EU AI Act High-Risk AI education mandates, ensure that automated AI grading assessments require verification and sign-off by a qualified human educator (`reviewed_by`, `verification_status: "verified_and_approved"`) before releasing official grades.
- **Ebbinghaus Spaced Repetition Scheduling**: Schedule review sessions across Ebbinghaus forgetting curve intervals (Days 1, 3, 7, 14, 30) with consolidation buffers (minimum 15% dedicated review buffer); embed Feynman technique checkpoints requiring learners to explain complex technical concepts in simple, jargon-free terms.
