## Technical Writer Review Checklist

This reference checklist provides operational documentation architecture, Markdown AST linting, schema-driven API documentation, readability scoring, and dual-audience AI readability criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across zero-warning Markdown AST validation, dual-audience (human and LLM) readability, automated OpenAPI/AsyncAPI sync, live MCP tool definition parity, agent runbook operational envelopes, EU AI Act Annex IV technical documentation, and Generative Engine Optimization (GEO).

### 1. Markdown AST Validation & Prose Quality (`MARKDOWN-AST-LINT LOCK`)
- **Zero-Warning Markdown AST Linting**:
  - all markdown documentation passes `markdownlint-cli2` with zero errors or warnings
  - strict heading hierarchy enforced: exactly one top-level H1 per document; no skipped heading levels (e.g. H2 $\rightarrow$ H4 prohibited)
  - all internal relative file links and external URLs validated via automated link-checker; zero dead links (HTTP 404) allowed:
    ```jsonc
    // .markdownlint.jsonc configuration
    {
      "default": true,
      "MD013": false, // Line length handled by editor wrap
      "MD024": { "siblings_only": true }, // Allow identical headings across different parent sections
      "MD025": { "level": 1 }, // Strictly enforce single H1
      "MD029": { "style": "ordered" } // Consistent ordered list numbering
    }
    ```
- **Vale Prose Style Linting Configuration**:
  - prose validated against style rules (Google Developer Documentation Style Guide / Microsoft Style Guide) ensuring concise, active-voice, and second-person or imperative phrasing:
    ```ini
    # .vale.ini configuration
    StylesPath = styles
    MinAlertLevel = warning
    
    [*.md]
    BasedOnStyles = Vale, Google
    Google.Passive = error
    Google.We = warning
    Google.WordList = error
    ```
  - internal process jargon, subagent IDs, or ephemeral run metadata excluded from public-facing documentation

### 2. Quantitative Readability & Information Density Metrics
- **Mathematical Readability Formulations**:
  - documentation must be quantitatively scored to ensure clarity and accessibility:
    - **Flesch-Kincaid Grade Level** ($FKGL \le 10.0$):
      $$FKGL = 0.39 \left(\frac{\text{total words}}{\text{total sentences}}\right) + 11.8 \left(\frac{\text{total syllables}}{\text{total words}}\right) - 15.59$$
    - **Flesch Reading Ease** ($RE \ge 60.0$):
      $$RE = 206.835 - 1.015 \left(\frac{\text{total words}}{\text{total sentences}}\right) - 84.6 \left(\frac{\text{total syllables}}{\text{total words}}\right)$$
    - **Information Density Ratio** ($ID \ge 0.12$):
      $$ID = \frac{N_{\text{named entities}} + N_{\text{quantified metrics}}}{N_{\text{total words}}} \ge 0.12$$
  - prose failing these readability thresholds must be edited to simplify sentence structure and prune redundant passive phrasing

### 3. Dual-Audience Documentation Architecture (`DUAL-AUDIENCE LOCK`)
- **Optimized for Humans and LLM Agents**:
  - documentation designed for dual consumption: human engineers seeking actionable guides and autonomous AI agents ingesting context windows
  - key concepts lead with compact, self-contained summary blocks ($\le 400$ tokens) to minimize RAG context-window bloat
  - step-by-step procedures end with checkable, observable completion criteria rather than open-ended bounds

### 4. Schema-Driven API Documentation Synchronization (`SCHEMA-SYNC LOCK`)
- **Automated Generation from OpenAPI / AsyncAPI**:
  - API reference documentation generated directly from version-controlled OpenAPI 3.1 or AsyncAPI schemas (via Redocly, Mintlify, or Fern) in CI/CD pipelines
  - manual authoring of API parameter tables or endpoint payloads strictly prohibited to eliminate hallucination vectors and drift
  - breaking changes detected via `oasdiff` before merge:
    ```bash
    spectral lint contracts/openapi.yaml --ruleset spectral:oas --fail-severity=error
    oasdiff breaking original.yaml new.yaml --fail-on ERR
    ```

### 5. Live Tool Definition & MCP Registry Parity (`TOOL-DEFINITION LOCK`)
- **Synchronized MCP Tool Manifests**:
  - documentation for Model Context Protocol (MCP) tools verified against the active server registry (`/.well-known/mcp/server-card.json` or live FastMCP endpoints)
  - documented tool names, input parameter schemas, and return formats must match production code with zero divergence

### 6. Agent Runbooks & Operational Envelopes (`AGENT-RUNBOOK-ENVELOPE LOCK` / `AGENT-HANDOFF LOCK`)
- **Actionable Multi-Agent Runbooks**:
  - operational runbooks for autonomous agent workflows document decision triggers, parameter boundaries, timeout limits, and failure recovery paths
  - procedures specify step-by-step instructions for human operators to inspect active state, pause execution, inject manual corrections, and trigger clean rollbacks
- **Inter-Agent Handoff Documentation**:
  - handoff points between specialist agents documented with required input contracts, expected return schemas, and validation checks

### 7. EU AI Act Technical Documentation File (`EU-AI-ACT-DOC-COMPLIANCE LOCK`)
- **Annex IV Technical Documentation Conformance**:
  - systems classified as high-risk AI or GPAI maintain a comprehensive Technical Documentation File complying with EU AI Act Annex IV (covering system architecture, training data provenance, risk management, human oversight measures, and cybersecurity protections)
  - documentation retained and versioned with a mandated 10-year retention schedule

### 8. `llms.txt` and `llms-full.txt` Context Optimization
- **Standardized `llms.txt` File Structure**:
  - developer-facing repositories provide root-level `/llms.txt` ($\le 2,000$ tokens) and `/llms-full.txt` ($\le 32,000$ tokens) files:
    ```markdown
    # Project Title
    > Concise 1-line architecture summary.
    
    ## Core Endpoints
    - [Architecture Docs](docs/architecture.md): High-level system overview
    - [API Reference](docs/api.md): OpenAPI 3.1 specification
    - [Runbooks](docs/runbooks.md): Operational multi-agent incident procedures
    ```
  - token counts audited using `tiktoken` to prevent context buffer overflow during agent retrieval

### 9. Version Control & Release Documentation Standards (`DOC-RELEASE LOCK`)
- **SemVer Changelog Governance**:
  - every user-facing release includes a structured CHANGELOG entry following Keep a Changelog standards:
    ```markdown
    ## [5.1.0] - 2026-10-17
    ### Added
    - Automated Lua inventory fencing tokens in ecommerce service.
    ### Changed
    - Upgraded vLLM serving engine to v1 standalone C++ core.
    ```
  - breaking changes, deprecation schedules, and migration guides documented with reproducible code examples

### 10. Operational Failure Modes & Escalation Protocols
- **API Drift Escalation**:
  - discrepancies between documented endpoints and live OpenAPI specifications block release pipelines until rectified
- **Broken Example Traps**:
  - code samples and curl commands tested in automated test pipelines to prevent publishing obsolete syntax

### 11. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Markdown AST Lint** | 0 errors, 0 warnings | `markdownlint-cli2 "**/*.md"` | Exit code 0; clean AST |
| **Vale Style Linter** | 0 error-level alerts | `vale docs/` | 0 style/passive errors |
| **Reading Ease Score** | $RE \ge 60.0, FKGL \le 10$ | Textstat Python CLI | Reading ease $\ge 60$ |
| **Spectral API Lint** | 0 OAS breaking errors | `spectral lint openapi.yaml` | 0 errors |
| **Link Integrity** | 0 dead URLs (HTTP 404) | `lychee "**/*.md"` | 100% links valid |
| **llms.txt Budget** | $\le 2000$ tokens | `python3 scripts/count-tokens.py llms.txt` | Token count $\le 2000$ |
| **Handoff Schema** | Valid `doc-handoff.json`| `python3 core/scripts/validate-contracts.py` | 100% schema compliant |
