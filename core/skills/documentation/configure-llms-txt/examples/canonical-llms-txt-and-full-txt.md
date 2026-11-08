# Canonical llms.txt & llms-full.txt Examples

## 1. Canonical `/llms.txt`

```markdown
# Agent Skills Platform

> Agent Skills is an enterprise engineering skill pack and multi-agent coordination
> framework providing deterministic A2A contracts, PromptOps golden benchmarks,
> and Clean Architecture microservice patterns.

## Architecture & Core Documentation

- [Clean Architecture Guide](https://skills.example.com/docs/architecture.md): Kratos layer separation, Wire dependency injection, and zero-leakage biz layers.
- [A2A Delegation Protocol](https://skills.example.com/docs/a2a-protocol.md): JSON-RPC 2.0 task contracts, structured handoffs, and verification gates.
- [Security & Zero Trust](https://skills.example.com/docs/security.md): SPIFFE/SPIRE workload attestation, ephemeral JWT rotation, and OWASP ASI mitigations.

## Machine & Agentic Discovery

- [Agent Registry](https://skills.example.com/.well-known/agent-card.json): A2A 1.0 Agent Card registry.
- [API Catalog](https://skills.example.com/.well-known/api-catalog): RFC 9727 API Linkset endpoints.
- [MCP Server Card](https://skills.example.com/.well-known/mcp/server-card.json): MCP server tools and resource schemas.
- [Commerce Manifest](https://skills.example.com/.well-known/ucp): UCP v2026-08-25 agent checkout capabilities.
```

## 2. Canonical `/llms-full.txt` (Exemplar Extract)

```markdown
# File: docs/architecture.md
# Architecture & Clean Code Standards
The system follows strict Clean Architecture layout:
- `api/`: Protobuf contracts and OpenAPI specifications.
- `internal/service/`: Protocol adapter translating transport to domain usecases.
- `internal/biz/`: Pure business logic; no GORM DB imports.
- `internal/data/`: Persistence layer wrapping GORM and Redis clients.

---

# File: docs/a2a-protocol.md
# Agent-to-Agent (A2A 1.0) Task Lifecycle
All agent handoffs require structured JSON artifacts validating against:
- `contracts/schemas/a2a-task.json`
- `contracts/schemas/a2a-artifact.json`
- `contracts/schemas/a2a-task-status.json`
```
