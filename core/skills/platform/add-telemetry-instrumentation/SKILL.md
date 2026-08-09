---
name: add-telemetry-instrumentation
description: Add or update logging, metrics, and tracing by following the repo's observability patterns and OpenTelemetry (OTel) GenAI Semantic Conventions. Use when a service, feature, endpoint, job, or integration needs operational visibility — including AI/LLM features requiring token-level tracing (gen_ai.usage.input_tokens, gen_ai.request.model), multi-agent workflow correlation, RAG step spans, and tool invocation traces.
---

# Add Telemetry Instrumentation

Use this skill when code changes need matching observability so operators can understand traffic, failures, latency, and dependency behavior.

## When to Use

- a service/endpoint/feature needs visibility
- adding logs, metrics, or traces (OTel)
- tracing AI/LLM token usage and RAG steps
- correlating multi-agent workflow spans

## Core Rules

- follow the repo's existing logging, metrics, and tracing patterns
- instrument important boundaries rather than every line of code
- keep telemetry names, labels, and dimensions stable enough for dashboards and alerts
- avoid high-cardinality labels unless the repo explicitly supports them
- never log secrets, credentials, tokens, or unnecessary sensitive data
- use stable OpenTelemetry GenAI conventions (opt in via `OTEL_SEMCONV_STABILITY_OPT_IN`) for LLM/agent tracking
- design hierarchical trace spans using `create_agent` operation types and step attributes for agent reasoning
- configure Cloudflare Workers native observability using the `observability` block in `wrangler.jsonc` and OTLP push
- capture GPU infrastructure metrics prefixed with `hw.gpu.*` via OTel Collector and DCGM exporter integration

## Suggested Process

### 1. Identify Critical Paths

Determine the key entrypoints, dependency calls, background jobs, and failure domains that need visibility.

### 2. Add Structured Logging

Add logs for meaningful state changes, warnings, and errors.

Prefer repo-local conventions for:

- log levels
- correlation IDs or request IDs
- structured fields
- error wrapping or stack capture

### 3. Add Metrics

Add or update metrics that help answer operational questions:

- request, job, or event counts
- latency or duration distributions
- failure counts by stable reason
- dependency call outcomes

### 4. Add Tracing

Instrument spans across service boundaries, external API calls, database queries, or long-running internal operations when the repo uses tracing.

### 5. Check Operational Usefulness

Verify that the telemetry can support dashboards, alerts, incident triage, and release verification without creating noise.

### 6. Validate Sensitive Data Handling

Confirm that logs, metrics labels, and trace attributes do not expose secrets, credentials, tokens, or unnecessary personal data.

## 2026 Observability Patterns

### 2026: OpenTelemetry GenAI Semantic Conventions

When instrumenting Generative AI and Large Language Model (LLM) operations:
- Opt into stable OpenTelemetry semantic conventions by setting the environment variable `OTEL_SEMCONV_STABILITY_OPT_IN` to enable standardized trace/metric formats.
- Trace and standardize LLM requests using the following specific attributes:
  - `gen_ai.system`: Standardized name of the model provider (e.g., `openai`, `anthropic`, `vertex_ai`).
  - `gen_ai.request.model`: The specific model name requested (e.g., `gpt-4o`, `claude-3-5-sonnet`).
  - `gen_ai.usage.input_tokens`: The count of input/prompt tokens.
  - `session.id`: Correlation ID mapping LLM calls to a specific user session or agent workflow instance.

### 2026: Agent Reasoning Trace Spans

To visualize and debug complex multi-step agent reasoning chains:
- Initiate agent execution using a root span with operation type `create_agent`.
- Structure intermediate steps, tool calls, and planning actions as hierarchical child spans nested under the root agent span.
- Enrich every agent span with the following semantic attributes:
  - `agent.name`: Name or role of the agent executing the work (e.g., `orchestrator`, `explorer`).
  - `agent.step_type`: The type of action or step being run (e.g., `reasoning`, `tool_call`, `planning`, `compaction`).

### 2026: Cloudflare Workers OpenTelemetry Configuration

For edge deployments utilizing Cloudflare Workers:
- Enable native Cloudflare observability by adding the `observability` configuration block to `wrangler.jsonc` (or `wrangler.toml`):
  ```jsonc
  {
    "observability": {
      "enabled": true,
      "head_sampling_rate": 1.0
    }
  }
  ```
- For external trace shipping, configure direct OTLP push over HTTP/HTTPS (using libraries like `@microlabs/otel-cf-workers` or custom exporters) to export telemetry payload directly to downstream collector backends (e.g., Honeycomb, Datadog).

### 2026: GPU Metrics Collection

For model inference and GPU-accelerated computing nodes:
- Expose GPU hardware utilization and performance data using the NVIDIA DCGM (Data Center GPU Manager) exporter.
- Set up an OpenTelemetry Collector to scrape DCGM Prometheus metrics endpoints.
- Standardize GPU metric names with the prefix `hw.gpu.*` (e.g., `hw.gpu.utilization`, `hw.gpu.memory.used`, `hw.gpu.temperature`, `hw.gpu.power`) utilizing the OTel Collector `transform` processor for namespace normalization.

## Checklist

- [ ] existing telemetry pattern reviewed
- [ ] critical paths identified
- [ ] structured logs added or updated
- [ ] metrics added or updated
- [ ] tracing added or updated when the repo uses tracing
- [ ] sensitive data exposure checked
- [ ] dashboards, alerts, or runbooks updated when needed
- [ ] OpenTelemetry GenAI semantic conventions applied and enabled via `OTEL_SEMCONV_STABILITY_OPT_IN`
- [ ] agent reasoning steps traced hierarchically under a root `create_agent` span with `agent.name` and `agent.step_type`
- [ ] Cloudflare Workers telemetry configured with wrangler `observability` block and OTLP push
- [ ] GPU metrics (`hw.gpu.*`) scraped via OTel Collector and DCGM exporter

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Related Skills

- **debug-runtime-platform**: Investigate runtime behavior using telemetry evidence
- **setup-deployment**: Wire telemetry config into runtime source of truth
- **performance-profiling**: Measure latency, throughput, or resource bottlenecks
- **security-audit**: Review sensitive data exposure risk
- **commit-code**: Prepare telemetry changes for delivery
