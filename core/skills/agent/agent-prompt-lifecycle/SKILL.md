---
name: agent-prompt-lifecycle
description: Manage prompt assets through their full lifecycle including versioning, evaluation against golden datasets, drift detection, and controlled promotion across environments. Use when creating, updating, reviewing, or auditing prompt definitions in roles, skills, workflows, or system instructions to ensure measurable quality and safe deployment.
---

# Agent Prompt Lifecycle

Use this skill when prompt changes need structured versioning, automated evaluation, and production observability rather than ad-hoc editing and gut-feel assessment.

## When to Use

- creating or updating a prompt definition
- reviewing/auditing prompts in roles or skills
- evaluating prompts against golden datasets
- detecting prompt drift before promotion

## Core Rules

- treat prompt definitions as versioned assets, not disposable text
- change one element at a time when iterating on a prompt
- never promote a prompt change to production without running it against the relevant eval set
- maintain a golden dataset of representative inputs and expected behaviors for every actively used prompt
- log the rationale for every prompt change
- separate structural changes (adding a block) from behavioral changes (modifying instructions)
- do not claim a prompt improvement without measurable evidence
- optimize prompts programmatically using DSPy framework compilation, signatures, and MIPROv2 optimizers
- integrate prompt tracking platforms including PromptLayer, LangSmith, or Phoenix for production monitoring
- enforce A/B testing validation with statistical significance (p < 0.05) before full promotion
- track prompt drift by calculating the cosine similarity of embedding centroids of prompt outputs
- implement evaluation-driven promotion gates utilizing golden datasets and LLM-as-judge scorers

## Key Concepts

### Context Engineering

In 2026, prompt quality depends more on the context assembled into the model's window than on the phrasing of instructions. When evaluating or designing prompts, consider:

- whether the prompt relies on static text that should be dynamically retrieved (RAG)
- whether tool integrations follow the Model Context Protocol (MCP) standard
- whether the context assembly is reproducible and testable

### PromptOps Pipeline

A production prompt lifecycle follows five stages:

1. **Registry**: prompts stored outside application code, with change tracking
2. **Golden Dataset**: curated input/output pairs representing expected behavior
3. **Automated Eval**: every change scored against the golden dataset before promotion
4. **Environment Promotion**: Development → Staging → Production with rollback capability
5. **Production Observability**: drift detection via sampled output review and quality metrics

### LLM-as-a-Judge

For tasks where output quality is subjective, use a powerful model as an automated evaluator:

- define a scoring rubric (accuracy, completeness, format compliance, hallucination)
- run the judge against sampled outputs on a schedule
- flag scores below threshold for human review

## Suggested Process

### 1. Identify The Prompt Asset

Determine which prompt is changing:

- a role definition (`roles/*.md`)
- a rule file (`rules/*.md`)
- a workflow (`workflows/*.md`)
- a skill (`skills/*/SKILL.md`)
- a system instruction or adapter file

### 2. Document The Change

For every prompt change, record:

- what changed and why
- which block was modified (identity, scope, workflow, output contract, fallback, etc.)
- the expected impact on output behavior

Use a changelog entry format:

```text
v1.3 — 2026-05-09
- narrowed scope: removed financial advice from allowed topics
- added output contract: require JSON with confidence scores
- reason: reduce hallucination rate on financial queries
```

### 3. Build Or Update The Golden Dataset

For the prompt being changed, ensure a golden dataset exists with:

- at least 10 representative test cases
- edge cases that historically caused failures
- adversarial inputs that test guardrails
- expected behavior described as pass/fail criteria, not exact string matches

### 4. Run Evaluation

Before promoting the change:

- run the updated prompt against the golden dataset
- compare scores to the previous version
- if using LLM-as-a-Judge, verify the judge prompt itself has not drifted
- document any regressions and decide whether they are acceptable trade-offs

### 5. Promote Through Environments

- merge the prompt change into the development branch
- validate in staging against the full eval suite
- deploy to production only after staging passes
- set up a rollback trigger if production quality metrics drop

### 6. Monitor In Production

After deployment:

- sample 1–5% of production outputs for quality review
- run sampled outputs through the LLM-as-a-Judge weekly
- track key metrics: format compliance rate, hallucination rate, user correction rate
- trigger re-evaluation if any metric degrades beyond threshold

## 2026 PromptOps Patterns

### 2026: DSPy Automatic Prompt Optimization

Prompt engineering shifts from manual template editing to programmatic optimization using DSPy:
- **Signatures and Modules**: Define model behavior using formal DSPy signatures (specifying input/output roles and types) rather than raw string instructions.
- **Bootstrap Optimizers**: Utilize optimization algorithms (such as `BootstrapFewShotWithRandomSearch` or `MIPROv2`) to automatically compile few-shot examples and instruction variations.
- **Versioned Artifacts**: Save compiled DSPy program state files (JSON configuration and parameters) under version control alongside source code.

### 2026: Prompt Tracking and A/B Testing

Maintain continuous visibility and statistical rigor for prompt updates:
- **Observability Platforms**: Integrate tracking platforms such as PromptLayer, LangSmith, or Phoenix to trace prompts, model configurations, and output histories.
- **A/B Testing**: Run prompt variations in parallel against production traffic splits.
- **Statistical Significance**: Validate performance differences using statistical tests and require a p-value less than 0.05 (p < 0.05) before full deployment.

### 2026: Embedding-Based Prompt Drift Detection

Detect gradual changes in prompt performance or model behavior over time:
- **Centroid Embeddings**: Calculate vector embeddings for sample production prompt outputs on a recurring basis.
- **Cosine Similarity**: Measure the cosine similarity between the current output embedding centroid and the baseline centroid established during initial evaluation.
- **Alerting Thresholds**: Trigger alert notifications and prompt re-evaluation when cosine similarity drops below the acceptable threshold.

## Output Format

When reporting a prompt lifecycle action, use:

```markdown
## Prompt Lifecycle Report

Asset changed:
- ...

Change type:
- Structural | Behavioral | Context | Eval-only

Change summary:
- ...

Eval results:
- Previous score: ...
- Current score: ...
- Regressions: ...

Promotion decision:
- Promote | Hold | Rollback

Monitoring plan:
- ...
```

## Checklist

- [ ] prompt asset and change type identified
- [ ] change rationale documented
- [ ] only one element changed per iteration
- [ ] golden dataset exists with at least 10 cases
- [ ] eval run against golden dataset
- [ ] scores compared to previous version
- [ ] regressions documented and accepted or fixed
- [ ] promotion path followed (dev → staging → production)
- [ ] production monitoring plan in place
- [ ] drift detection schedule established

## Related Skills

- **agent-context-management**: Track prompt evaluation evidence across iterations
- **agent-tool-orchestration**: Sequence eval runs and promotion steps safely
- **agent-quality-gate**: Run prompt eval as part of the broader quality gate
- **agent-handoff**: Report prompt change impact and monitoring plan
- **review-code**: Apply review discipline to prompt changes
