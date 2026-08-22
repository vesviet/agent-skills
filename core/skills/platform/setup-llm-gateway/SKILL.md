---
name: setup-llm-gateway
description: Configure a centralized LLM proxy gateway for token routing, budgeting, and failover. Use when deploying multi-model routing, enforcing token rate limits, managing provider credentials, or centralizing AI observability.
---

# Setup LLM Gateway

Use this skill to implement an AI infrastructure gateway (e.g., LiteLLM, Portkey) that sits between internal applications and external LLM providers (OpenAI, Anthropic, Gemini).

## Core Rules

- **Centralized Choke Point**: All LLM traffic MUST route through the gateway. Direct calls to provider APIs using raw keys are prohibited.
- **Failover Routing**: Configure multi-provider fallback logic (e.g., primary: Claude 3.5 Sonnet → secondary: GPT-4o → fallback: Llama 3) to guarantee inference uptime.
- **Cost Attribution**: Enforce mandatory metadata tags (e.g., `team_id`, `project_id`) on all requests to track token budgets accurately.
- **Rate Limiting**: Apply token and request rate limits per user/tenant to prevent abusive spikes or accidental infinite loops from autonomous agents.
- **Credential Vaulting**: Secure provider master API keys in a dedicated secrets manager; never expose upstream keys to client applications.
- **LLM-SLO-TARGETS**: Define measurable SLOs for each virtual model tier: TTFT (Time-to-First-Token) p95 < 800ms for interactive, < 3s for batch; TBT (Time-Between-Tokens) p95 < 25ms; alert on SLO breaches per model, not globally.
- **PROMPTOPS-TOKEN-BUDGET**: Track token usage per `(team_id, model, prompt_template_version)` tuple — prompt template version changes must be reflected in metadata tagging so cost attribution remains accurate after prompt engineering changes.
- **AGENTIC-CIRCUIT-BREAKER**: Configure a hard circuit breaker (max total tokens per agent invocation session) to prevent autonomous agent loops from exhausting daily budgets — set per-session token cap ≤ 10% of daily budget.

## Suggested Process

### 1. Select Gateway Architecture & Engine

Evaluate and select the LLM gateway engine based on technical requirements:
- LiteLLM Proxy for Python/Kubernetes native environments supporting 100+ LLM providers.
- Portkey or Cloudflare AI Gateway for edge-deployed, managed caching and routing pipelines.
- Verify support for streaming responses, function/tool calling passthrough, and structured JSON output constraints.

### 2. Deploy Gateway Infrastructure & Vault Credentials

Provision the gateway runtime:
- Deploy the gateway service as a high-availability deployment behind a load balancer.
- Store upstream provider API keys (OpenAI, Anthropic, Google Vertex AI) in AWS Secrets Manager or HashiCorp Vault.
- Configure internal API key generation for downstream applications with role-based permissions and spending limits.

### 3. Configure Model Routing Matrix & Failover Fallbacks

Define routing rules and resilience strategies:
- Define virtual model aliases (e.g., `fast-model`, `reasoning-model`) mapping to concrete upstream endpoints.
- Configure automated failover fallbacks triggered by HTTP 429 (rate limits), 5xx server errors, or timeout thresholds.
- Set up latency-based and cost-optimized routing rules where appropriate.

### 4. Enforce Token Budgets, Rate Limits & Metadata Tagging

Implement traffic controls and governance:
- Require client requests to include metadata headers (`x-team-id`, `x-project-id`, `x-user-id`).
- Configure token-bucket rate limits (requests per minute and tokens per minute) per client key.
- Set hard monthly budget caps per project with automated request rejection when budgets are exhausted.

### 5. Instrument Observability & Tracing

Use skill: `add-telemetry-instrumentation`
- Configure OpenTelemetry trace export following OpenTelemetry GenAI semantic conventions (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`).
- Forward gateway access logs to centralized logging backends.
- Set up monitoring dashboards for token consumption, latency percentiles (p50, p95, p99), and provider error rates.

### 6. Validate Routing, Failover & Load Resilience

Use skill: `troubleshoot-service`
- Execute end-to-end integration tests routing test prompts across all configured virtual models.
- Simulate provider outages by injecting HTTP 500/429 responses and assert that fallback models respond without client disruption.
- Verify that rate limiting correctly throttles traffic when request ceilings are exceeded.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/deployment-plan.json`** — Required fields: `infrastructure_changes[]`, `config_updates[]`, and `validation_run` output proving the gateway successfully routes a test request and triggers a failover correctly.

## Checklist

- [ ] LLM gateway service deployed in high-availability configuration.
- [ ] Upstream provider API keys vaulted in secrets management.
- [ ] Virtual model aliases and multi-provider failover routing configured.
- [ ] Client authentication, rate limits, and token budgets enforced per tenant.
- [ ] Mandatory cost attribution metadata tagging validated on incoming requests.
- [ ] OpenTelemetry GenAI semantic tracing and latency metrics enabled.
- [ ] Failover and throttling behaviors verified via integration tests.
- [ ] `deployment-plan.json` emitted.

## Related Skills

- **agent-model-routing**: Select cost-effective models dynamically before dispatching to the gateway
- **setup-gpu-finops**: Track token spend and GPU compute costs across infrastructure layers
- **implement-structured-outputs**: Ensure gateway preserves JSON Schema constrained decoding across routed models
- **add-telemetry-instrumentation**: Wire OpenTelemetry GenAI semantic conventions and trace propagation
- **manage-secrets**: Securely store and rotate provider API keys and gateway authentication tokens
- **system-design**: Architect high-availability LLM proxy clusters and failover topologies
