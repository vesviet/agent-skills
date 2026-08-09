---
name: setup-llm-gateway
description: Configure a centralized LLM proxy gateway for token routing, budgeting, and failover.
---

# Setup LLM Gateway

Use this skill to implement an AI infrastructure gateway (e.g., LiteLLM, Portkey) that sits between internal applications and external LLM providers (OpenAI, Anthropic, Gemini).

## Core Rules
- **Centralized Choke Point**: All LLM traffic MUST route through the gateway. Direct calls to provider APIs using raw keys are prohibited.
- **Failover Routing**: Configure multi-provider fallback logic (e.g., primary: Claude 3.5 Sonnet -> secondary: GPT-4o -> fallback: Llama 3) to guarantee inference uptime.
- **Cost Attribution**: Enforce mandatory metadata tags (e.g., `team_id`, `project_id`) on all requests to track token budgets accurately.
- **Rate Limiting**: Apply token and request rate limits per user/tenant to prevent abusive spikes or accidental infinite loops from autonomous agents.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/deployment-plan.json`** — Required fields: `infrastructure_changes[]`, `config_updates[]`, and `validation_run` output proving the gateway successfully routes a test request and triggers a failover correctly.

## Checklist
- [ ] Gateway service (LiteLLM/Portkey) deployed.
- [ ] Failover routing matrix configured.
- [ ] Cost attribution tagging enforced.
- [ ] Rate limits applied.
- [ ] `deployment-plan.json` emitted.
