# OpenTelemetry Semantic Conventions & GenAI Observability Standards (2026)

## 1. W3C TraceContext & Distributed Propagation

### 1.1 Trace Context Headers
Distributed tracing requires unbroken propagation of context across all process boundaries, asynchronous message queues (Kafka, Dapr, RabbitMQ), and network hops:
- **`traceparent`**: `00-{trace_id}-{parent_id}-{trace_flags}` (e.g. `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`).
- **`tracestate`**: Preserves vendor-specific telemetry attributes across multi-cloud boundaries.

---

## 2. OpenTelemetry GenAI Semantic Conventions (v1.30+)

When instrumenting LLM agent operations, opt-in via `OTEL_SEMCONV_STABILITY_OPT_IN=genai` and emit standardized attributes:
- `gen_ai.system`: Provider identifier (`openai`, `anthropic`, `vllm`).
- `gen_ai.request.model` & `gen_ai.response.model`: Model IDs (e.g. `gpt-4o`, `deepseek-r1`).
- `gen_ai.usage.input_tokens`: Count of prompt/context tokens.
- `gen_ai.usage.output_tokens`: Count of generated tokens.
- `gen_ai.usage.tokens`: Total aggregated token consumption.
- `gen_ai.response.finish_reasons`: Array of termination causes (`stop`, `length`, `tool_calls`).
- `gen_ai.server.time_to_first_token`: Duration from request initiation to arrival of the first streaming chunk (TTFT).

---

## 3. Multi-Window Multi-Burn-Rate (MWMBR) SLI Alerting

Alerting on simple error rates causes false positives during off-peak hours and delayed notification during catastrophic regressions:
- **Dual Window Evaluation**: Evaluate error budget consumption across short windows (5m, 30m, 2h) paired with long windows (1h, 6h, 3d).
- **Empty-Vector Coalescing**: Guard against alert flapping when traffic drops to zero:
  ```promql
  (
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    /
    sum(rate(http_requests_total[5m]))
  ) > (14.4 * (1 - 0.999))
  or on() vector(0)
  ```
