---
name: agent-model-routing
description: Select the most cost-effective model for each task or sub-task based on complexity, risk tier, and budget constraints. Use when orchestrating multi-step workflows, delegating tasks, or when token costs need active management.
---

# Agent Model Routing

Use this skill when the choice of model matters for cost, quality, or latency and the default model may not be the best fit for every sub-task.

## When Agent Coordinator Enables This

Enable **`agent-model-routing`** (Supporting skill) when:

- the coordination plan has **three or more phases** with different complexity (e.g., triage → implement → review)
- token budget is tight and premium models must be reserved for security, architecture, or incident steps
- cascade routing can start phases on mid-tier models and escalate only on validation failure
- parallel A2A delegations mix low-risk formatting work with high-risk engineering steps

Skip explicit routing when the task is a **single-phase** handoff to one specialist, or when the user pinned a model for the whole session.

## When to Use

- orchestrating multi-step workflows with mixed complexity
- delegating sub-tasks to cheaper or stronger models
- token costs need active budget management
- a sub-task's risk tier changes the model choice

## Core Rules

- match model capability to task complexity — do not use premium models for routine work
- default to mid-tier models and escalate only when quality requires it
- track and report token costs per model tier
- never compromise safety-critical tasks for cost savings
- respect the risk tier assigned to each task or workflow step

## Model Tiers

### Lightweight (Routine)

Best for: autocomplete, formatting, simple extraction, template filling, boilerplate generation.

Characteristics: fast, cheap ($0.10-$2/M tokens), may lack deep reasoning.

### Mid-Tier (Standard)

Best for: feature implementation, code review, CRUD operations, documentation, most day-to-day development work.

Characteristics: balanced cost and capability ($2-$15/M tokens), reliable structured output.

### Premium (Complex)

Best for: architectural decisions, security audits, complex debugging, multi-file refactoring, production incident response.

Characteristics: highest capability ($15-$60/M tokens), strongest reasoning, highest latency.

## Routing Strategies

### Rule-Based Routing

Assign model tier based on the task type or risk tier:

| Risk Tier | Default Model Tier | Escalation Trigger |
|:----------|:-------------------|:-------------------|
| Vibe | Lightweight | Output quality below threshold |
| Agentic | Mid-Tier | Complex reasoning required |
| Engineering | Premium | Always (safety-critical) |

### Cascade Routing

Start with a cheaper model. Escalate only if:

- the output fails schema validation
- the output fails quality checks
- the task requires reasoning beyond the model's capability
- confidence scores are below threshold

### Cost-Aware Planning

Before starting a multi-step workflow:

- estimate total token budget
- assign model tiers to each step
- reserve premium budget for the most critical steps
- track actual usage against budget

## Suggested Process

### 1. Classify The Task

Determine:

- task type (implementation, review, debugging, documentation, etc.)
- risk tier (vibe, agentic, engineering)
- expected output complexity
- whether structured output is required

### 2. Select The Model Tier

Apply the routing strategy:

- match risk tier to default model tier
- check budget constraints
- consider cascade routing for uncertain complexity

### 3. Execute And Monitor

During execution:

- track tokens consumed per step
- monitor output quality
- escalate to a higher tier if quality is insufficient

### 4. Report Costs

After completion:

- report tokens used per model tier
- compare actual cost to budget
- flag steps where escalation occurred
- identify opportunities for future cost optimization

## Checklist

- [ ] task classified by type, risk tier, and complexity
- [ ] model tier selected based on routing strategy
- [ ] budget constraints checked before execution
- [ ] token usage tracked per step
- [ ] output quality monitored for escalation triggers
- [ ] escalation justified and documented when used
- [ ] final cost reported with breakdown by model tier
- [ ] optimization opportunities identified for future tasks

## Related Skills

- **agent-tool-orchestration**: Integrate model selection into the orchestration frame
- **agent-delegation**: Specify model tier requirements in A2A task contracts
- **agent-observability**: Record routing decisions and costs for analysis
- **agent-quality-gate**: Use output quality as an escalation trigger
