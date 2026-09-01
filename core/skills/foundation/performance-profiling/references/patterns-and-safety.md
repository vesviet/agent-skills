# Performance Profiling — Reference

Deep material extracted from `SKILL.md` to keep the main file under 200 lines.
Load this file when triaging an unfamiliar bottleneck or when authoring a
postmortem for a performance incident.

## Common Performance Patterns

### Request Path Bottlenecks

- repeated downstream calls
- repeated serialization
- oversized payloads
- synchronous work that could be deferred

### Data Bottlenecks

- N+1 reads
- missing indexes
- large scans
- long transactions

### Memory Bottlenecks

- repeated allocations
- retained references
- goroutine or worker leaks
- unbounded buffers or caches

### Concurrency Bottlenecks

- coarse locks
- queue buildup
- insufficient backpressure
- too much parallelism on a shared dependency

## AI Inference-Specific Profiling

When the hot path includes LLM calls, embedding lookups, or GPU inference:

- Measure and baseline model latency p50/p95/p99 separately from service latency — LLM calls are often the dominant latency source.
- For GPU services (vLLM, Ollama, ONNX Runtime): profile GPU utilization, VRAM usage, KV cache hit rate, and time-to-first-token (TTFT) using `nvitop` or PyTorch Profiler.
- For batch inference services: profile queue depth and batch fill efficiency — under-batching wastes GPU; over-batching increases tail latency.
- For RAG / semantic search: measure embedding cache hit rate — redundant embedding calls are the most common preventable AI cost spike.
- Report AI inference cost per request alongside latency so optimization decisions weigh both UX and cost impact.
- Correlate profiling data with distributed traces via `trace_id` using OTel Profiles OTLP format to avoid vendor lock-in.

## Production Safety Checklist

If profiling a shared or production environment:

- get explicit approval first
- use the least invasive method that answers the question
- keep profiling duration short
- make sure profiling endpoints or admin tooling are access-controlled
- coordinate with owners if the workload is customer-facing
- continuous profilers must stay under 1.5% CPU overhead with bounded memory limits
