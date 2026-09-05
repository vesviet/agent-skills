---
name: design-learning-plan
description: Create a structured, curriculum-aligned learning plan or syllabus following ZPD pathways, SMART objectives, and spaced repetition. Use when planning a study schedule, syllabus, exam preparation roadmap, or grade transition plan for any educational level.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# Design Learning Plan

Use this skill to structure personalized, adaptive study plans adhering to Vygotsky's Zone of Proximal Development (ZPD), Cognitive Load Theory, quantitative SMART learning objectives, and Ebbinghaus spaced retention schedules.

## When to Use

- structuring curriculum-aligned syllabi and personalized study roadmaps
- designing multi-tier ZPD pathways (Tier 1 Universal, Tier 2 Targeted, Tier 3 Intensive)
- formulating quantitatively verifiable SMART learning objectives
- scheduling spaced repetition intervals (Days 1, 3, 7, 14, 30) and Feynman checkpoints
- planning grade-transition roadmaps with 15% consolidation buffers

## Core Rules

- always map learning plans to explicit academic calendars; budget study blocks into realistic units (45–60 min) with strict cognitive load limits ($3\text{--}5$ novel interacting elements per unit)
- formulate all milestone goals as **SMART Quantitative Learning Objectives** using active Bloom 2027 HOTS verbs, specific operational constraints, and numerical pass criteria (see [`references/zpd-pathways-and-smart-objectives.md`](references/zpd-pathways-and-smart-objectives.md))
- implement **Vygotsky ZPD Multi-Tier Scaffolding**: differentiate instructional delivery across Tier 1 (Universal Core), Tier 2 (Targeted Scaffolding with faded worked examples), and Tier 3 (Intensive Extension challenges)
- schedule review milestones at **Days 1, 3, 7, 14, and 30** per the Ebbinghaus forgetting curve decay model ($R = e^{-t/S}$) to systematically flatten forgetting rates (see [`references/spaced-scheduling-and-socratic-scaffolding.md`](references/spaced-scheduling-and-socratic-scaffolding.md))
- allocate a **minimum 15% dedicated consolidation buffer** for grade-transition or prerequisite remediation plans
- embed **Feynman Technique checkpoints** at review milestones: require jargon-free, layperson explanations with physical analogies to expose hidden mental model gaps
- configure automated tutoring interactions in **Strict Socratic Mode**: AI tutors must ask one guiding question at a time, never output direct solutions or full code, and escalate strictly through the **3-level graduated hint ladder** (Level 1: Constraint Focus $\to$ Level 2: Conceptual Prompt $\to$ Level 3: Isomorphic Mini-Problem)

## Suggested Process

1. **Intake & Diagnostic Assessment**: Determine target subject, curriculum standards, and learner baseline ability ($\theta$).
2. **Formulate SMART Objectives**: Construct quantitative, verifiable learning targets for each milestone.
3. **Architect ZPD Scaffolding Tiers**: Design Tier 1 universal materials, Tier 2 faded worked examples, and Tier 3 extension katas.
4. **Sequence Spaced Review Milestones**: Map study blocks across Ebbinghaus retention intervals (Days 1, 3, 7, 14, 30).
5. **Embed Feynman & Socratic Gates**: Define simplification checkpoints and configure Socratic hint ladders.
6. **Emit Machine-Readable Contract**: Serialize plan parameters into `learning-handoff.json`.

### In-Depth Reference Guides
- **ZPD Pathways & SMART Objectives**: [`references/zpd-pathways-and-smart-objectives.md`](references/zpd-pathways-and-smart-objectives.md) — Multi-tier scaffolding, Cognitive Load Theory, and SMART formulas.
- **Spaced Scheduling & Socratic Scaffolding**: [`references/spaced-scheduling-and-socratic-scaffolding.md`](references/spaced-scheduling-and-socratic-scaffolding.md) — Ebbinghaus decay math, 15% buffer rules, Feynman audits, and 3-level hint ladders.

## Checklist

- [ ] Target grade, proficiency tier, and curriculum standards are explicitly verified.
- [ ] Cognitive load is budgeted: maximum 3–5 novel interacting elements per 45-minute study block.
- [ ] All learning milestones contain quantitative SMART objectives with measurable benchmarks.
- [ ] Differentiated pathways provide Tier 1 universal, Tier 2 targeted scaffolding, and Tier 3 extension tasks.
- [ ] Review milestones are scheduled at Days 1, 3, 7, 14, and 30 per the Ebbinghaus model.
- [ ] Minimum 15% dedicated consolidation buffer is allocated for grade transitions or prerequisite gaps.
- [ ] Feynman simplification checkpoints are embedded at key milestones with jargon-free criteria.
- [ ] Socratic tutoring modules enforce zero-direct-answer constraints and the 3-level graduated hint ladder.
- [ ] Structured contract `contracts/schemas/learning-handoff.json` is emitted for cross-role handoffs.

## Output Contracts

When the learning plan is handed off to an educator, automated tutor, or LMS, emit:

- **`contracts/schemas/learning-handoff.json`** — populating `artifact_type: "learning_plan"`, `zpd_assessment`, `smart_objectives`, `formative_scaffolding_tiers`, and `spaced_repetition_schedule`.
- For human-readable reports, emit markdown learning plan documents featuring timeline tables, Feynman checkpoints, and graduated hint prompts.

## Failure Modes

- **Vague qualitative objectives**: goals phrased as "understand concurrency." Mitigation: enforce SMART formula with verifiable passing thresholds.
- **Cognitive overload stacking**: introducing > 5 novel concepts in a single block. Mitigation: enforce element interactivity limits; decompose into sequenced sub-schemas.
- **Omission of consolidation buffer**: grade-transition plan skips review buffer, triggering cascading failure. Mitigation: mandate 15% dedicated buffer.
- **Spaced repetition skipping**: omitting Days 1, 3, 7, 14, or 30 review blocks. Mitigation: enforce Ebbinghaus schedule validation.
- **Socratic bypass**: AI tutor emits complete code solutions. Mitigation: lock tutor prompts to single-question Socratic inquiry and graduated hint escalation.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: anonymize student identifiers; store learner cognitive profiles securely.
- **ASI04 Supply Chain**: validate automated scheduling tools and curriculum data sources against trusted manifests.
- **ASI05 RCE Guard**: never construct plan schemas or tutor instructions from unvalidated external inputs.
- **ASI07 Inter-Agent Communication**: serialize learning plans into schema-validated JSON contracts.
- **ASI09 Human-Agent Trust Exploitation**: transparently communicate AI tutor boundaries and require educator sign-off.

## Related Skills

- **create-exercises**: Generate DOK 1–4 assignments and AI-resistant problem sets matching plan milestones.
- **grade-and-review**: Assess student work using 4-tier analytic rubrics and diagnose cognitive errors.
