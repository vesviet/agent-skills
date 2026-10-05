## Technical Writer Review Checklist

This reference checklist provides operational documentation architecture, Markdown AST linting, schema-driven API documentation, and dual-audience AI readability criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across zero-warning Markdown AST validation, dual-audience (human and LLM) readability, automated OpenAPI/AsyncAPI sync, live MCP tool definition parity, agent runbook operational envelopes, EU AI Act Annex IV technical documentation, and Generative Engine Optimization (GEO).

### 1. Markdown AST Validation & Prose Quality (`MARKDOWN-AST-LINT LOCK`)
- **Zero-Warning Markdown AST Linting**:
  - all markdown documentation passes `markdownlint-cli2` with zero errors or warnings
  - strict heading hierarchy enforced: exactly one top-level H1 per document; no skipped heading levels (e.g. H2 $\rightarrow$ H4 prohibited)
  - all internal relative file links and external URLs validated via automated link-checker; zero dead links (HTTP 404) allowed
- **Prose Style & Terminology Consistency (Vale Linter)**:
  - prose validated against style rules (Google Developer Style Guide / Vale linter) ensuring concise, active-voice, and second-person or imperative phrasing
  - internal process jargon, subagent IDs, or ephemeral run metadata excluded from public-facing documentation

### 2. Dual-Audience Documentation Architecture (`DUAL-AUDIENCE LOCK`)
- **Optimized for Humans and LLM Agents**:
  - documentation designed for dual consumption: human engineers seeking actionable guides and autonomous AI agents ingesting context windows
  - key concepts lead with compact, self-contained summary blocks ($\le 400$ tokens) to minimize RAG context-window bloat
  - step-by-step procedures end with checkable, observable completion criteria rather than open-ended bounds

### 3. Schema-Driven API Documentation Synchronization (`SCHEMA-SYNC LOCK`)
- **Automated Generation from OpenAPI / AsyncAPI**:
  - API reference documentation generated directly from version-controlled OpenAPI 3.1 or AsyncAPI schemas (via Redocly, Mintlify, or Fern) in CI/CD pipelines
  - manual authoring of API parameter tables or endpoint payloads strictly prohibited to eliminate hallucination vectors and drift

### 4. Live Tool Definition & MCP Registry Parity (`TOOL-DEFINITION LOCK`)
- **Synchronized MCP Tool Manifests**:
  - documentation for Model Context Protocol (MCP) tools verified against the active server registry (`/.well-known/mcp/server-card.json` or live FastMCP endpoints)
  - documented tool names, input parameter schemas, and return formats must match production code with zero divergence

### 5. Agent Runbooks & Operational Envelopes (`AGENT-RUNBOOK-ENVELOPE LOCK` / `AGENT-HANDOFF LOCK`)
- **Actionable Multi-Agent Runbooks**:
  - operational runbooks for autonomous agent workflows document decision triggers, parameter boundaries, timeout limits, and failure recovery paths
  - procedures specify step-by-step instructions for human operators to inspect active state, pause execution, inject manual corrections, and trigger clean rollbacks
- **Inter-Agent Handoff Documentation**:
  - handoff points between specialist agents documented with required input contracts, expected return schemas, and validation checks

### 6. EU AI Act Technical Documentation File (`EU-AI-ACT-DOC-COMPLIANCE LOCK`)
- **Annex IV Technical Documentation Conformance**:
  - systems classified as high-risk AI or GPAI maintain a comprehensive Technical Documentation File complying with EU AI Act Annex IV (covering system architecture, training data provenance, risk management, human oversight measures, and cybersecurity protections)
  - documentation retained and versioned with a mandated 10-year retention schedule

### 7. Generative Engine Optimization (GEO/AEO) & Answer-First Architecture (`GEO-ACCURACY LOCK`)
- **Answer-First Structure**:
  - documentation pages lead with concise, fact-dense direct answers ($\le 200$ words) to common technical inquiries before branching into detailed implementation steps
  - JSON-LD structured data (Schema.org `TechArticle`, `HowTo`) embedded where appropriate for machine search indexing

### 8. `llms.txt` Deployment & Realistic Scoping
- **Standardized `llms.txt` File Structure**:
  - developer-facing documentation repositories provide root-level `/llms.txt` and `/llms-full.txt` files summarizing project architecture, documentation entry points, and CLI commands
  - `llms.txt` positioned accurately as an agent navigation map; not misrepresented as a search engine ranking factor

### 9. Version Control & Release Documentation Standards (`DOC-RELEASE LOCK`)
- **SemVer Changelog Governance**:
  - every user-facing release includes a structured CHANGELOG entry following Keep a Changelog standards
  - breaking changes, deprecation schedules, and migration guides documented with reproducible code examples
- **Contract Deliverable Conformance**:
  - documentation handoffs produce valid, schema-compliant `contracts/schemas/documentation-handoff.json`

### 10. Operational Failure Modes & Escalation Protocols
- **API Drift Escalation**:
  - discrepancies between documented endpoints and live OpenAPI specifications block release pipelines until rectified
- **Broken Example Traps**:
  - code samples and curl commands tested in automated test pipelines to prevent publishing obsolete syntax
