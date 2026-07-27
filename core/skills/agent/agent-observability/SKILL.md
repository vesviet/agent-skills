---
name: agent-observability
description: Trace agent reasoning chains, tool call sequences, context injections, and token costs to enable debugging, cost attribution, and continuous evaluation improvement. Use when deploying agents to production, diagnosing unexpected outputs, tracking costs across tenants, or building evaluation datasets from real-world failures.
---

# Agent Observability

Use this skill when agent behavior needs to be traceable, debuggable, and measurable beyond simple pass/fail checks.

## When to Use

- deploying agents to production
- diagnosing unexpected or wrong agent outputs
- attributing token/cost across tenants
- building evaluation datasets from real failures

## Core Rules

- trace every tool call, reasoning decision, and context injection at session level
- track token usage (input and output) per step and per session
- never log secrets, credentials, or PII in traces
- feed production failures back into evaluation golden datasets
- use tail-based sampling in high-volume environments to manage cost
- attribute costs to the appropriate tenant, feature, or workflow

## Key Concepts

### Session-Level Tracing

Individual LLM call tracing is insufficient. Agent failures are causal chains — a mistake at step 3 may not manifest until step 7. Capture the full session:

- system prompt and context injected at each step
- tool calls with inputs and outputs
- reasoning decisions and branching logic
- memory reads and writes
- final output and user feedback

### The Virtuous Cycle

The most mature teams feed production failures back into their evaluation loop:

1. agent produces unexpected output in production
2. the trace is flagged (manually or by drift detection)
3. the input/output pair is added to the golden dataset
4. the prompt or skill is updated
5. the eval suite runs against the expanded dataset
6. regression is prevented permanently

### OpenTelemetry For GenAI

Use OpenTelemetry GenAI semantic conventions (Development status) to ensure portability. See `core/observability/otel-genai.md` for the full mapping. Core attributes:

- `gen_ai.operation.name`: operation type — use a spec enum value (`chat`, `generate_content`, `execute_tool`, `invoke_agent`, `plan`, ...), never invented names
- `gen_ai.provider.name`: provider flavor (`anthropic`, `openai`, `gcp.vertex_ai`, ...) — replaces the deprecated `gen_ai.system`
- `gen_ai.request.model` / `gen_ai.response.model`: requested and responding model
- `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens`: tokens consumed and generated (plus `gen_ai.usage.reasoning.output_tokens` for reasoning models)
- `gen_ai.response.finish_reasons`: why generation stopped (plural array)
- `gen_ai.conversation.id`: session/thread correlation (use the standard OTel `trace_id` for span correlation)

### Cost Attribution

Track costs at multiple dimensions:

- per-user or per-tenant
- per-feature or per-workflow
- per-model tier (lightweight vs premium)
- per-session

## Suggested Process

### 1. Instrument The Session

At session start:

- assign a unique session/trace ID
- record the initial context (role, rules, skills loaded)
- record the model and routing decision

### 2. Trace Each Step

For every action:

- log the tool or operation name
- log inputs (sanitized of secrets)
- log outputs and status
- log token usage
- log elapsed time
- log any context injected from memory or RAG

### 3. Detect Anomalies

Flag sessions where:

- total token usage exceeds expected budget by 2x
- the agent called the same tool more than 3 times in a loop
- the agent changed its plan mid-execution more than twice
- the final output contradicts intermediate reasoning
- user required a re-prompt or correction

### 4. Sample For Review

In production:

- keep 100% of failed or anomalous traces
- sample 1-5% of successful traces
- use tail-based sampling: decide whether to keep after the session completes, based on outcome

### 5. Close The Loop

Weekly:

- review flagged traces
- extract input/output pairs for the golden dataset
- update prompts or skills if patterns emerge
- track metrics over time: format compliance, hallucination rate, user correction rate, average cost

## Checklist

- [ ] session trace ID assigned
- [ ] model and routing decision recorded
- [ ] every tool call traced with inputs, outputs, and token usage
- [ ] context injections (RAG, memory) traced
- [ ] secrets and PII excluded from traces
- [ ] anomalous sessions flagged
- [ ] sampling strategy applied (tail-based for production)
- [ ] production failures fed back to golden dataset
- [ ] cost attributed to appropriate dimensions
- [ ] weekly review cycle established

## Related Skills

- **agent-tool-orchestration**: Provide trace data for every tool call
- **agent-quality-gate**: Use trajectory review as a quality gate
- **agent-prompt-lifecycle**: Feed production insights into prompt evaluation
- **agent-model-routing**: Record routing decisions for cost analysis
- **agent-context-management**: Trace what context was injected and from which source
