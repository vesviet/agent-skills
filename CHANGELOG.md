# Changelog

All notable changes to the agent-skills engineering pack.

## [2.1.0] - 2026-05-13

### Fixed
- `core/scripts/common.py`: `parse_frontmatter` now supports YAML block scalars (`>`, `|`, `>-`, `|-`). Multi-line descriptions no longer trigger false "invalid frontmatter line" errors.
- `core/skills/security-data/data-engineer/SKILL.md`: restored multi-line description now that the parser handles it correctly.

### Added
- `overlays/vesviet-content/rules/content-brand.md`: populated with real voice/tone guidelines, style constraints (meta ≤ 160 chars, Production Failure template, code linting rules), and publishing constraints for Vesviet and Learn sites.
- `overlays/vesviet-content/workflows/publish-series.md`: end-to-end workflow for producing and publishing multi-part technical series across both Hugo sites. Covers planning, drafting, translation, review, and go-live steps.
- `core/contracts/schemas/series-article.json`: JSON Schema contract for series article output, validating frontmatter fields (date timezone, description length, weight ordering) and body structure (prerequisite block, production failure, CTA link).

### Changed
- `VERSION`: bumped from 2.0.0 to 2.1.0.

## [2.0.0] - 2026-05-09

### Added
- `core/contracts/` directory with JSON Schema output contracts for structured agent communication
  - `code-review-finding.json`, `implementation-result.json`, `validation-result.json`
  - `a2a-task.json`, `a2a-artifact.json` for Agent-to-Agent delegation
- `core/policies/` directory with machine-readable governance
  - `action-boundaries.yaml` defining role-based action permissions
  - `data-classification.yaml` defining sensitivity levels (public, internal, confidential, restricted)
- `agent-delegation` skill: A2A protocol-based task delegation between supervisor and worker agents
- `agent-semantic-memory` skill: persistent episodic and semantic memory across conversations
- `agent-observability` skill: session-level tracing, cost attribution, and virtuous evaluation cycle
- `agent-model-routing` skill: cost-aware model selection with tier-based routing strategies

### Changed
- `README.md`: added contracts and policies to Core Structure, expanded Agent Operations to 10 skills
- `core/skills/README.md`: updated Agent taxonomy from 6 to 10 skills
- Pack philosophy now reflects 8 core 2026 standards: Structured Outputs, A2A Protocol, Graph Orchestration, Layered Memory, Observability, Policy-as-Code, Model Routing, and Agentic Engineering Tiers

## [1.1.0] - 2026-05-09

### Added
- `agent-prompt-lifecycle` skill: full PromptOps pipeline with versioning, golden datasets, LLM-as-a-Judge evaluation, environment promotion, and drift detection

### Changed
- `agent-tool-orchestration`: added MCP (Model Context Protocol) section with discovery, contracts, auth, idempotency, and cost awareness guidance
- `agent-context-management`: added Context Engineering section covering dynamic context assembly, RAG validation, relevance filtering, context budgeting, and provenance tracking
- `agent-quality-gate`: added prompt evaluation as a quality gate for prompt asset changes
- `README.md`: updated pack philosophy to reflect 2026 Context Engineering and PromptOps standards
- `core/skills/README.md`: added `agent-prompt-lifecycle` to Agent taxonomy (now 6 agent skills)

## [1.0.0] - 2026-05-07

### Added
- Core pack with 35 skills across 7 taxonomy domains
- 19 principal-level delivery roles with skill toolbox enforcement
- 8 reusable workflows with role ownership per step
- 5 agent adapter files (Cursor, Claude Code, AGENTS, Copilot, OpenAI Codex)
- 5 Python validation scripts with adapter parity checking
- 3 overlays (vesviet-content, lease-content, ecommerce-microservices)
- 3 pack manifests (global-engineering, lease-team, vesviet-team)
- Adapter parity standard with automated checking
- OpenAI Codex skill adapters for all applicable skills
