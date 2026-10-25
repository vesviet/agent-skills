# Changelog

All notable changes to the agent-skills engineering pack.

## [5.7.0] - 2026-10-25

Modernization of five roles and eleven skills to the verified 2026-10 platform, data, and compliance baseline, with regression-proof challenge tests for every change.

### Data Engineering (ratified-spec correctness)

- `data-engineer` and the `security-data` skills now standardize on the **ratified Apache Iceberg v3 spec** (1.11+/1.12 line); the unratified v4 spec is tracked strictly as roadmap and must never appear in production table configs. Variant is correctly attributed to Iceberg v3 per the official spec.
- Engine pins verified against upstream releases: Delta Lake 4.4, Spark 4.2+, dbt Core 2.0 (1.12 floor, active support to 2027-07), DuckDB 1.5+ / 2.0 LTS (GA 2026-10-21), ODCS v3.2.0, Flink 2.3 (confirmed current).
- Relational maintenance runbooks target PostgreSQL 18; `data-pipeline-spec.json` description updated to ODCS v3.2.0.
- New `SPEC-CURRENCY-LOCK`, unratified-spec anti-pattern, and a 2026-10 modernization-gates section; `build-data-pipeline`, `optimize-olap-database`, and `query-analytical-engine` versioned 2.0.0, `database-maintenance` 1.0.0, all with official OWASP ASI guardrail titles.

### AWS Engineering (silicon and toolchain generations)

- `aws-engineer` and `aws-infrastructure` default to **Graviton5** (c9g/m9g/r9g, all GA by 2026-08) and **Trainium3** (trn3) UltraServers (GA 2025-12); `GRAVITON5-FIRST-LOCK` allows Graviton4 only as a documented regional fallback.
- Toolchain: OpenTofu v1.13+, Crossplane v2.4+ (namespaced composite resources; claims deprecated), EKS Auto Mode as the default for new clusters with self-managed Karpenter v1.x retained for custom node control.
- Adds Bedrock AgentCore (GA 2025-10) with Nova 2 ARN scoping, Aurora DSQL (GA 2025-05), Database Savings Plans, and `AWS-CURRENCY-LOCK` with quarterly re-validation.

### Quality Engineering (stack parity)

- `qa-engineer` ephemeral test parity moves to Go 1.27+ and PostgreSQL 18 Testcontainers; browser automation to Playwright v1.64+ (1.64.1, 2026-10-13). `write-tests` versioned 2.0.0 with official ASI titles. New stack-currency, playwright-currency, and toolchain-alignment gates.

### Content Governance (live compliance)

- EU AI Act **Article 50** transparency obligations are enforced as in force (2026-08-02, grace to 2026-12), with the C2PA implementation guide (2026-07) as the machine-readable marking path.
- GEO citation tracking refreshed to Google AI Overviews and AI Mode, ChatGPT Search, and Perplexity; the obsolete SearchGPT naming is retired. Share of Model (SoM) is tracked alongside AI Share of Voice.
- All six `content/*` skills versioned 2.0.0 with official ASI titles; new article-50-live, geo-engine-currency, som-metric, and asi-title gates.

### Solution Architecture

- Clean-architecture pins move from Go 1.25+ to Go 1.27+; new gates require Streamable HTTP for adopted MCP servers (HTTP+SSE rejected) and silicon-agnostic GPU sizing.

### Tests

- 79 new modernization challenge tests across five suites, including absence tests that block regression to superseded pins (unratified specs, previous-generation silicon and language versions, obsolete engine names, non-official ASI titles).

## [5.6.1] - 2026-10-24

Patch release: npm distribution hardening and a token-free release pipeline.

### npm CLI fixes

- `agent-skills --version` now works as a standalone flag; the argument parser no longer mistakes a leading flag for the command name.
- `agent-skills list` matches the documented catalog (38 roles, 25 workflows) by excluding README, role-standard, and INDEX files when scanning.

### Release pipeline

- Releases publish from CI via npm trusted publishing (OIDC) with automatic provenance attestations; no registry token is stored as a CI secret.
- `repository.url` switched to the canonical https form so the OIDC repository claim matches exactly.

## [5.6.0] - 2026-10-23

SOTA Deep Research Modernization of the Principal Researcher role, `conduct-research` core skill, and `research-report.json` Draft 2020-12 data contract across the canonical framework. Formalizes Stanford STORM multi-perspective persona discovery and conversational interview probing before search execution. Enforces mathematical Citation Directed Acyclic Graph (DAG) acyclicity via 3-color DFS cycle detection, multi-source triangulation ($\ge 3$ independent primary sources), zero-AI-primary source citation lock, Chain-of-Verification (CoVe) atomic verification matrix with C2PA cryptographic provenance inspection, and quantitative Information Density ($\text{ID} \ge 0.12$).

### Core Roles Modernized

- `researcher` (`core/roles/researcher.md`):
  Integrated Stanford STORM persona discovery protocol (Skeptical Auditor, Compliance Reviewer, Domain Specialist, Technical Architect) and simulated conversational interviews. Enforces Citation DAG acyclicity, multi-source triangulation ($\ge 3$ independent primary records), CoVe atomic claim decomposition matrix, C2PA cryptographic Content Credentials provenance checks, strict quantitative Information Density threshold ($\text{ID} \ge 0.12$), and zero AI primary source citations (`ZERO-AI-PRIMARY-CITATION-LOCK`). Updated Deliverable Routing and role review checklist.

### Core Skills Modernized

- `conduct-research` (`core/skills/foundation/conduct-research/SKILL.md`):
  Upgraded to v2.0.0 with standardized YAML frontmatter (`owners: primary: "@researcher"`, `taxonomy: foundation`, `tags: [research, deep-research, cove, citation-dag, information-gain]`, `version: "2.0.0"`) and concise line budget (< 200 lines). Codifies canonical 5-phase execution flow: (1) Objective & Persona Discovery (STORM), (2) Sub-Task Decomposition & DAG Planning, (3) Deep Multi-Hop Search, (4) CoVe & Provenance Verification, (5) Information Density Synthesis & Contract Emission. Accompanied by authoritative reference dossier `references/sota-deep-research-architecture.md`.

### Data Contracts Modernized

- `core/contracts/schemas/research-report.json`:
  JSON Schema Draft 2020-12 data contract modernized with explicit schemas for `citation_dag` (nodes, edges, is_acyclic, cycle_check_algorithm, validation_status), `cove_verification_matrix` (atomic propositions, verification questions, isolated queries, primary source URLs, status enums, C2PA flags), and `information_density` (named entities, quantified metrics, total words, score $\ge 0.12$, status). Validated with zero errors in `validate-contracts.py`.

### Test Suite & Challenge Harness Added

- `tests/test_researcher_sota_challenge.py`:
  Automated programmatic challenge test suite covering JSON Schema Draft 2020-12 meta-schema conformance, adversarial negative mutations, researcher role invariant locks, conduct-research skill structure, Citation DAG 3-color DFS cycle detection algorithm, quantitative Information Density calculation engine, and CoVe atomic proposition logic. Passes 100% in pytest.

## [5.5.0] - 2026-10-21

SOTA Dual-Memory Architecture upgrade decoupling in-flight context window management from persistent on-disk storage hygiene. Modernizes `agent-memory-compaction` to v2.0.0 with 10-slot anchored schema, 60/80% token utilization triggers, and Head-Tail Tool Output Truncation (TOC). Upgrades `memory-hygiene` to v2.0.0 with seamless `@clean-memory` fast-invocation alias routing and compaction checkpoint handoff. Introduces Draft 2020-12 data contract `compact-working-state.json` (schema #60), new deterministic CLI utility `compact-context.py`, and extends `prune-memory.py` with `--ingest-checkpoint` for automated persistent memory ingestion and OWASP ASI06 sanitization.

### Core Skills Modernized

- `agent-memory-compaction` (v2.0.0, assigned Primary to `@agent-coordinator`, Supporting to `@prompt-engineer`, `@reviewer`, `@researcher`):
  Formalizes the 10-slot anchored working state schema, 60/80% compaction triggers, Head-Tail Tool Output Truncation (TOC) algorithm (head lines 1–5, tail last 15 lines), Smart Zone Attention Allocation, and quantitative compaction metrics ($\text{TCR} \in [5\times, 15\times]$, $\text{CIRR} \ge 98\%$, $\text{GDM} \le 0.05$, $\text{TRW} \le 1.0\%$). Emits `contracts/schemas/compact-working-state.json`.
- `memory-hygiene` (v2.0.0, assigned Primary to `@prompt-engineer`, Supporting to `@security-engineer`, `@agent-coordinator`, `@reviewer`):
  Harmonizes dual-naming `@clean-memory` and `@memory-hygiene` alias routing in `INDEX.md`. Codifies handoff protocol ingesting `compact-working-state.json` checkpoints directly into Tier 1 persistent storage (`MEMORY.md`, `.agents/memory.md`) while offloading resolved items and anti-patterns to `MEMORY_ARCHIVE.md`.

### Tooling & CLI Utilities Added & Extended

- `core/scripts/compact-context.py`:
  Deterministic CLI utility to parse conversation logs, execute head-tail TOC truncation on verbose tool outputs, construct and validate 10-slot candidate states against `compact-working-state.json`, and emit compact in-context checkpoints. Accompanied by unit test suite (`tests/test_compact_context.py`).
- `core/scripts/prune-memory.py`:
  Extended with `--ingest-checkpoint` flag to ingest structured `compact-working-state.json` checkpoints directly, probe referenced files against live disk (`is_dead_path()`), quarantine secrets and prompt injections (OWASP ASI06), update active persistent memory, and offload resolved tasks to archive.

### Contract Schemas Added

- `core/contracts/schemas/compact-working-state.json`:
  JSON Schema Draft 2020-12 data contract (schema #60) formalizing the 10-slot anchored working state schema (`current_goal`, `work_type`, `phase_control`, `active_constraints`, `files_modified_and_inspected`, `decisions_and_tradeoffs`, `verification_and_evidence`, `failed_attempts_and_antipatterns`, `preserved_invariants`, `next_single_safe_action`) with property constraints and bundled examples. Registered in `core/contracts/schemas/INDEX.md` and `core/contracts/README.md`.

### Alias Harmonization & Release Sync

- Registered `@clean-memory` as first-class skill alias mapping to `memory-hygiene` in `core/scripts/generate-index.py` alongside `@clean_memory` and `@memory-hygiene`.
- Synchronized version-pinned files across adapters, configs, and guides to v5.5.0. Catalog inventory maintains 38 roles, 182 skills (167 core + 15 overlays), 25 workflows, and 60 contract schemas across 18 automated validation gates.

## [5.4.0] - 2026-10-21

Memory Hygiene & Clean Memory Suite release ingesting Linkly AI Skills ecosystem indexing insights (Rank #128 `memory-hygiene`, Rank #83 `memory`, Rank #14 `self-improving`) and OWASP Top 10 for Agentic AI 2026 (ASI06 Context & Memory Poisoning). Adds the `memory-hygiene` core skill, deterministic memory pruning engine (`prune-memory.py`), JSON Schema Draft 2020-12 data contract (`memory-audit-report.json`), updates owning roles (`@prompt-engineer`, `@security-engineer`, `@agent-coordinator`), and expands catalog to 38 roles, 182 skills (167 core + 15 overlays), 25 workflows, and 59 contract schemas.

### Core Skills Ingested

- `memory-hygiene` (assigned Primary to `@prompt-engineer`, Supporting to `@security-engineer`, `@agent-coordinator`):
  Deterministic 4-phase memory lifecycle (Audit → Triage `[active]`, `[stale]`, `[redundant]`, `[resolved]`, `[poisoned]` → Compaction → Archival), strict line and token budget enforcement (`MEMORY.md` $\le 100$ lines, $\le 1500$ tokens), Single-Source-of-Truth (SSOT) live filesystem verification, and OWASP ASI06 context & memory poisoning defense (secret detection via Shannon entropy $H > 4.5$ and prompt injection isolation). Emits `contracts/schemas/memory-audit-report.json`.

### Tooling & CLI Utilities Added

- `core/scripts/prune-memory.py`:
  Deterministic CLI utility to parse memory markdown files, verify backtick and link file paths against live repository filesystem, detect duplicate and redundant instructions via exact and fuzzy n-gram matching, enforce token/line budgets, quarantine OWASP ASI06 prompt injection and high-entropy credentials, offload stale entries to archive, and emit structured audit reports conforming to `memory-audit-report.json`. Accompanied by full pytest unit test suite (`tests/test_prune_memory.py`).

### Contract Schemas Added

- `core/contracts/schemas/memory-audit-report.json`:
  JSON Schema Draft 2020-12 data contract specifying machine-readable memory audit metadata, token consumption metrics and delta savings, line metrics, 5-tier entry triage breakdown, granular findings, OWASP ASI06 security sanitization, and archival destinations. Registered in `core/contracts/schemas/INDEX.md` as schema #59.

### Roles & Governance Updates

- `@prompt-engineer`: Assigned Primary ownership of `memory-hygiene`, added `contracts/schemas/memory-audit-report.json` to outputs produced, and updated Deliverable Routing table.
- `@security-engineer`: Added `memory-hygiene` as Supporting skill, reinforced OWASP ASI06 Context & Memory Poisoning defense rules and guardrails.
- `@agent-coordinator`: Added `memory-hygiene` as Supporting skill for multi-agent durable session compaction and handoffs.
- Total catalog inventory expanded to 38 roles, 182 skills (167 core + 15 overlays), 25 workflows, and 59 contract schemas.

## [5.3.0] - 2026-10-20

AI Agent Systems, Prompt Engineering, UI Craft, and Web Quality release synthesized from `seb1n/awesome-ai-agent-skills` (context engineering, agent evaluation, prompt injection defense) and `ui-skills.com` / `ibelick/ui-skills` (DESIGN.md token standards, motion hardware acceleration, web quality audits). Ingests 6 portable core skills, 2 JSON Schema Draft 2020-12 data contracts (`design-tokens-spec.json`, `agent-eval-report.json`), establishes 2 new delivery roles (`prompt-engineer`, `sdet`), and synchronizes 38 roles and 181 total skills.

### Core Skills Ingested

- `context-optimization` (assigned Primary to `@prompt-engineer`, Supporting to `@agent-coordinator`):
  Token budget allocation (system 15%, grounding 35%, memory 25%, scratchpad 10%, reserve 15%), syntactic n-gram and semantic vector cosine deduplication, relevance density scoring, and lost-in-the-middle boundary placement to mitigate attention dilution.
- `agent-evaluation` (assigned Primary to `@sdet`, Supporting to `@qa-engineer`):
  Representative evaluation benchmark suites (nominal 40%, edge 40%, safety 20%), hybrid deterministic assertions and LLM-as-a-judge rubrics, standardized failure taxonomies (hallucination, goal hijack, schema violation, trajectory loop, timeout), and release gating. Emits `contracts/schemas/agent-eval-report.json`.
- `prompt-injection-defense` (assigned Primary to `@security-engineer`, Supporting to `@reviewer`):
  Defenses against direct jailbreaks and indirect prompt injection attacks, enforcing bounded tool schemas, structural delimiter isolation (`<untrusted_data>`), and ephemeral canary token integrity verification. Emits `contracts/schemas/security-audit.json`.
- `design-md-specification` (assigned Primary to `@ui-ux-designer`, Supporting to `@frontend-developer`):
  Authoring machine-readable `DESIGN.md` frontmatter token schemas, two-tier token hierarchy, concentric border radii ($R_{\text{outer}} = R_{\text{inner}} + P + B$), OpenType `tabular-nums` numeric alignment for data grids, and 44px mobile touch targets. Emits `contracts/schemas/design-tokens-spec.json`.
- `motion-performance-engineering` (assigned Primary to `@frontend-developer`):
  Fluid 60fps/120fps animations enforcing GPU composite-only transforms (`transform`, `opacity` only), spring physics calibration ($\zeta \ge 0.80$), main-thread frame budgeting (<10ms), and `@media (prefers-reduced-motion: reduce)` accessibility fallbacks. Emits `contracts/schemas/implementation-result.json`.
- `web-quality-audit` (assigned Primary to `@qa-engineer`, Supporting to `@frontend-developer`):
  Core Web Vitals profiling (LCP $\le 2.5\text{s}$, INP $\le 200\text{ms}$, CLS $\le 0.10$), Long Animation Frames (LoAF) and main-thread task diagnostics, DOM depth budgets, and Lighthouse CI regression gates (Perf $\ge 90$, A11y $\ge 95$). Emits `contracts/schemas/performance-audit.json`.

### Contract Schemas Added

- `core/contracts/schemas/design-tokens-spec.json`:
  JSON Schema Draft 2020-12 specification defining machine-readable DESIGN.md frontmatter tokens, two-tier token architecture (OKLCH color ramps, semantic mappings, concentric radii, tabular-nums typography, elevation, and motion curves).
- `core/contracts/schemas/agent-eval-report.json`:
  JSON Schema Draft 2020-12 specification defining agent evaluation benchmark runs, suite metadata, weighted rubrics, individual test case assertions and graders, failure taxonomy distribution, and automated verdicts (`pass`, `conditional_approval`, `fail_closed`).

### Roles & Governance Updates

- Authored new delivery roles: `core/roles/prompt-engineer.md` (Primary: `context-optimization`) and `core/roles/sdet.md` (Primary: `agent-evaluation`).
- Updated existing roles: `security-engineer.md`, `ui-ux-designer.md`, `frontend-developer.md`, `qa-engineer.md`, `agent-coordinator.md`, and `reviewer.md`.
- Expanded action boundaries in `core/policies/action-boundaries.yaml` to govern `prompt-engineer` and `sdet`.
- Updated role and skill indexes in `core/roles/README.md` and `core/skills/README.md`.
- Total catalog inventory expanded to 38 roles, 181 skills (166 core + 15 overlays), 25 workflows, and 58 contract schemas.

## [5.2.0] - 2026-10-19

Document Processing Suite (Anthropic benchmark ingestion) and Foundation skills release. Adds 6 portable core skills (`docx`, `xlsx`, `pdf`, `pptx`, `discernment-nudge`, `webapp-server-runner`), 5 executable supporting Python scripts (`recalc.py`, `thumbnail.py`, `add_slide.py`, `clean.py`, `with_server.py`), 1 JSON Schema Draft 2020-12 data contract (`document-manifest.json`), and updates role assignments across 9 engineering roles.

### Document Processing Suite (Anthropic)

- `docx` (assigned Primary to `@content-writer`):
  Word document creation, modification, formatting, and conversion via Python `python-docx`, pandoc AST filtering, and LibreOffice headless rendering. Emits `contracts/schemas/document-manifest.json`.
- `xlsx` (assigned Primary to `@data-analyst`):
  Spreadsheet generation, financial formulas, tab formatting, and headless recalculation via LibreOffice and openpyxl (`recalc.py`). Emits `contracts/schemas/document-manifest.json`.
- `pdf` (assigned Primary to `@technical-writer`):
  PDF generation, AcroForm field manipulation, PDF/A compliance validation, and document conversion using pdfcpu, qpdf, and headless rendering tools. Emits `contracts/schemas/document-manifest.json`.
- `pptx` (assigned Primary to `@ui-ux-designer`):
  Presentation slide deck generation, layout templating, thumbnail rendering, and asset hygiene (`thumbnail.py`, `add_slide.py`, `clean.py`). Emits `contracts/schemas/document-manifest.json`.

### Foundation Additions

- `discernment-nudge` (assigned Primary to `@reviewer`, Supporting to `@task-planner`, `@technical-architect`, `@security-engineer`):
  Socratic inquiry, deliberate friction, epistemic humility, and discernment prompt engineering to challenge unexamined assumptions before irreversible execution.
- `webapp-server-runner` (assigned Primary to `@qa-engineer`):
  Ephemeral dev/test server lifecycle management, port allocation, readiness health checking, and automatic process teardown via `with_server.py`.

### Contracts & Schemas

- `core/contracts/schemas/document-manifest.json`:
  JSON Schema Draft 2020-12 specification defining metadata for generated and validated binary artifacts (docx, xlsx, pdf, pptx, html), including file paths, SHA-256 checksums, page/sheet counts, and rendering toolchain versions.

### Monorepo & Catalog Updates

- Total skills inventory expanded to 175 (160 portable core skills + 15 overlay skills).
- Total JSON contract schemas expanded to 56 (added `document-manifest.json`).
- Updated role definitions across `@content-writer`, `@data-analyst`, `@technical-writer`, `@ui-ux-designer`, `@reviewer`, `@qa-engineer`, `@task-planner`, `@technical-architect`, and `@security-engineer`.
- Regenerated A2A agent registry, agent cards, and master markdown router `INDEX.md`.

## [5.1.0] - 2026-10-15

External skill ecosystem benchmark ingestion and engineering hardening release, synthesized from the comprehensive benchmark research dossier (`reports/external-skills-ecosystem-benchmark-research.md`). Adds 7 portable core skills, 1 JSON Schema Draft 2020-12 data contract, 3 specialized domain overlays (each with rules and overlay skills), a zero-execution AST static security scanner for third-party skills, and expands the automated validation pipeline to 18 gates.

### P0 Foundational Skills & AST Security Tooling

- `design-system-engineering` (assigned Primary to `@ui-ux-designer`):
  Codifies concentric border radius mathematical formula ($R_{\text{outer}} = R_{\text{inner}} + \text{padding} + \text{borderWidth}$) with cutoff invariant for $\text{padding} > 24\text{px}$, OKLCH lightness ramp delta step rules ($\Delta L \approx 0.04-0.05$ light, $\Delta L \approx 0.07-0.10$ mid, floor $\ge 0.03$), constant hue angle $\Delta H = 0^\circ$, and APCA contrast thresholds ($L_c \ge 75$ body text, $L_c \ge 60$ fluent text). Composes with `overlays/ui-design-system`.
- `frontend-micro-polish` (assigned Primary to `@frontend-developer`):
  Codifies $2\text{px}$ optical button padding offsets (`ps-3.5 pe-4`), $+2\text{px}$ play button centroid shift (`transform: translateX(2px)`), $16\text{px}$ iOS Safari font-size zoom guard, unitless `line-height` multipliers, $0.96$ active tap scale with $150\text{ms}$ transition tokens, 3-layer light elevation shadows, and dark mode 1px highlight rings. Emits `contracts/schemas/implementation-result.json`.
- `skill-preflight-ast-check` (assigned Primary to `@security-engineer`):
  Codifies zero-execution static AST security analysis for third-party skills, enforcing OWASP AST01–AST10 governance rules and mathematical evaluation of the Lethal Trifecta ($\mathcal{T}_{\text{lethal}}(\mathcal{S}) = \mathcal{D}_{\text{priv}} \wedge \mathcal{C}_{\text{untrusted}} \wedge \mathcal{E}_{\text{net}}$). Establishes mandatory Network Level 0 air-gap enforcement and 4-tier execution sandbox hierarchy. Emits `contracts/schemas/security-audit.json`.
- `anti-ui-slop-finish-gate` (assigned Primary to `@ui-ux-designer`, Supporting to `@reviewer`):
  Codifies objective finish criteria requiring 100% interaction state coverage (empty, loading, error, hover, active, focus-visible), the 13 universal escalation triggers causing immediate pipeline `Block`, and negative asset constraints banning synthetic quotes and abstract SVG swirls. Emits `contracts/schemas/ui-component-spec.json`.
- `core/scripts/validate-thirdparty-skills.py` (AST Static Security Scanner):
  Zero-dependency Python AST static analysis scanner detecting dangerous builtins (`eval`, `exec`), subprocess invocation, unapproved network module imports, environment variable harvesting, prompt injection markers, and pipe-to-shell hazards. Includes 7 automated self-test vectors and is wired into `core/scripts/validate-all.py` as Gate 18.

### P1 Resilient Testing, Assumptions Ledger & Interactive Workbench

- `hostile-component-stress-testing` (assigned Primary to `@qa-engineer`):
  Codifies the 6 hostile scenario axes (content length, shape, quantity, container bounds, lifecycle states, environment) adapted from `jakubkrehel/break`. Incorporates regex watchers for removed accessibility and layout signals.
- `core/contracts/schemas/assumptions-ledger.json` (The Enso Method Assumptions Ledger):
  JSON Schema Draft 2020-12 specification defining open questions, hypotheses, confidence ratings (0.0–1.0), impact assessment enums, computed risk scores ($\text{Impact} \times (6 - \text{Confidence})$), and unblocking verification paths. Emits `assumptions-ledger` discriminator. Registered in `core/contracts/schemas/INDEX.md`, `core/contracts/README.md`, and declared in `@business-analyst` and `@task-planner` deliverable routing.
- `interactive-component-workbench` (assigned Primary to `@frontend-developer`):
  Codifies scratch-route URL search param switchers (`?__state=`, `?__variant=`) for isolated multi-state component testing across 5 permissible variation axes (Structure, Density, Emphasis, Type, Voice) with container query collapse and screenshot visibility shortcuts.
- `playwright-evidence-qa` (assigned Primary to `@qa-engineer`):
  Codifies tripartite evidence triage (screenshot + DOM snapshot + console/telemetry) for diagnosing Playwright flakiness, defining a 3-way root cause taxonomy (Application Defect, Selector Drift, Timing Flakiness) and 10-iteration verification gates.

### P2 Specialized Engineering Overlays

- `overlays/cad-projection/`:
  Establishes CAD vector projection standards, Landscape A3 sheet sizing (`viewBox="0 0 420 297"`), ISO 128 stroke hierarchy ($0.35, 0.22, 0.16, 0.13\text{mm}$), SVG millimeter coordinate transformations, and the $3\text{D} \to 2\text{D}$ isometric transformation matrix. Contains skill `isometric-svg-projection` and `rules/cad-conventions.md`.
- `overlays/fintech-compliance/`:
  Establishes credit risk modeling and financial regulatory compliance, codifying monotonic Weight of Evidence (WOE) binning, automated $\chi^2$ bin pooling, Information Value (IV) feature selection thresholds, Points to Double Odds (PDO) score scaling, and Population Stability Index (PSI) drift monitoring. Contains skill `build-credit-scorecard` and `rules/credit-scorecard-rules.md`.
- `overlays/security-research/`:
  Establishes binary disassembly, decompilation triage, and reverse engineering governance. Codifies Source Code Presence Guard, Tier 2 (gVisor OCI container) and Tier 3 (Firecracker microVM) sandbox isolation, multi-toolchain triage (Ghidra, radare2, Electron asar unpackers), and formal Reverse Engineering Artifact (REA) evidence ledger standards. Contains skill `reverse-engineer-binary` and `rules/reverse-engineering-rules.md`.

### Monorepo & Catalog Updates

- Total skills inventory expanded to 168 (153 portable core skills + 15 overlay skills).
- Total JSON contract schemas expanded to 55 (added `assumptions-ledger.json`).
- Total domain overlays expanded to 21 (added `cad-projection`, `fintech-compliance`, `security-research`).
- Automated validation test suite expanded to 18 gates (integrated `validate-thirdparty-skills.py`).
- Updated role definitions across `@ui-ux-designer`, `@frontend-developer`, `@security-engineer`, `@qa-engineer`, `@reviewer`, `@business-analyst`, and `@task-planner`.
- Regenerated A2A agent registry, agent cards, and master markdown router `INDEX.md`.

## [5.0.0] - 2026-09-07

Standards-2027 alignment release, grounded in a five-track deep research pass
(protocol, data, content, security, platform — sources dated through
September 2026). Breaking changes are listed first.

### Breaking / renamed standards

- A2A well-known URI: `/.well-known/agent.json` is now
  `/.well-known/agent-card.json` (IANA permanent; rename dates to A2A
  v0.3.0). The pack's canonical endpoint file, `ai-catalog.json`, the
  registry generator, the 2026-compliance validator, the Antigravity
  adapter template, and the agent-card schema description all reference
  the correct URI, and `generate-a2a-registry.py` now emits
  `agent-card.json` instead of `agent.json` (the old file is removed).
- A2A v1.0.x wire conventions adopted: `SCREAMING_SNAKE_CASE` task states,
  unified `Part` object (no `kind`), `google.rpc.Status` errors with
  `domain: "a2a-protocol.org"`, Agent Card signature verification
  (JCS RFC 8785 + JWS RFC 7515), multi-tenancy `tenant` field, `ListTasks`
  cursor pagination. Protocol floor noted as v1.0.1 (2026-05-26); governance
  references updated to AAIF/Linux Foundation.
- ODCS version strings bumped from "v3" to **v3.1.0** (the single surviving
  data-contract standard — the Data Contract Specification is deprecated
  with CLI support ending 2026-12-31). Media type
  `application/odcs+yaml;version=3.1.0`.

### Protocol & discovery (Phase 1)

- `configure-mcp`: full stateless-era rewrite of Core Rules — mandatory
  `server/discover`, `_meta` per-request versioning, MRTR
  (`resultType: input_required`), `subscriptions/listen`, explicit state
  handles (SEP-2567), deprecation guardrails (Roots/Sampling/Logging/
  HTTP+SSE/DCR), CIMD migration before DCR removal after summer 2027,
  MCP Registry publishing (`server.json`, reverse-DNS verification), and
  required cache hints (`ttlMs`/`cacheScope`). Security Guardrails extended
  with the full OWASP MCP Top 10 (MCP01-MCP10). WebMCP downgraded to a
  watch-item (primary spec unreachable).
- `manage-api-catalog`: new "2027 Three-Tier Agentic Discovery" section —
  A2A `agent-card.json` / RFC 9727 `api-catalog` / AI Catalog
  `ai-catalog.json` (typed container, Trust Manifest, adoption votes
  pending).
- `configure-agent-commerce`: rail-selection decision matrix (x402
  stablecoin vs MPP/SPTs card rails), execution-time authorization
  (execution-finality alignment: signed instruction ≠ settlement), and
  agent-spend guardrails (caps, velocity, settlement attestations).

### Security & compliance (Phase 2)

- `role-standard.md`: new Universal Agentic Skill Security Standard
  (OWASP AST10 v1.0-2026 — skill-layer governance after the 2026
  skill-supply-chain incidents) with four new locks
  (SKILL-PROVENANCE, IDENTITY-FILE-PROTECTION, EGRESS-ALLOWLIST,
  EXECUTION-TIME-AUTHZ), WIMSE/NHI federation alignment (SPIFFE/SVID,
  RFC 8693 token exchange, secrets-less preference), and the
  execution-time authorization principle.
- `supply-chain-security`: SLSA v1.2 Build Environment + Dependency tracks
  (L3 Screened), unsigned-undeployable gate with Cosign/Sigstore
  verification, immutable hash pinning.
- `manage-secrets`: WIMSE alignment, per-agent identity inventory,
  secrets-less preference.
- `ai-risk-assessment`: full 2027-2028 EU AI Act runway (GPAI legacy-model
  cliff 2027-08-02, CSAM/NCII prohibitions 2026-12-02, post-market
  monitoring guidance 2027-09-02, sandboxes 2027-08-02).

### Data stack (Phase 3)

- `data-engineer` role + `build-data-pipeline`: catalog-as-control-plane
  rules (Iceberg REST protocol: scan planning, ETag freshness,
  Idempotency-Key commits, credential vending), Iceberg v4 readiness
  (metadata-only restructuring; never data rewrites), Variant as the
  canonical semi-structured path, Spark 4.1+ floor, Flink 2.3 sinks,
  native table encryption (KMS), DLQ triggers wired to contract SLA
  fields, OpenLineage explicit lineage facets.
- `analyze-data`: Text-to-SQL prevention recast as architecture
  (semantic-layer-first, show-the-definition policy, `agent_accessible`
  flags, read-only personas, MCP as the controlled channel), Apache Ossie
  interchange, agent query costs as a FinOps line item, DuckDB v2.0
  readiness (breaking storage format, VARIANT, Quack server mode).

### Platform & Astro (Phase 4)

- `overlays/astro-cloudflare`: Workers + Static Assets mandated as the only
  greenfield target (Pages in maintenance-only mode since April 2025),
  Pages→Workers migration checklist, MCP-on-Workers rewrite
  (`createMcpHandler` replaces obsolete `McpAgent`; CIMD before DCR
  removal), AI Gateway unified control plane
  (`{ gateway: { id: 'default' } }` on every `env.AI.run`), Astro v7
  migration notes (Rust compiler strictness, Sätteri, `src/fetch.ts`,
  `cacheCloudflare()`, Live Content Collections, CSP API).
- `edge-deployment-spec.json`: new `runtime_capabilities` (Containers,
  Sandbox SDK, DO SQLite, 64 MiB limit, Access), structured
  `edge_ai_integration` (gateway ID, model naming, model-first routing),
  and `mcp_handler` fields.
- `add-telemetry-instrumentation`: GenAI semconvs sourced from the
  dedicated `semantic-conventions-genai` repository including agent spans
  (`invoke_agent`, `execute_tool`) and MCP spans.

### Content & SEO (Phase 5)

- `optimize-seo`: GEO/AEO reframed as **AI-surface SEO** per Google's
  official guidance (no chunking, no AI-specific schema, no rewrite-for-AI);
  information-gain gate retooled into a **non-commodity / unique-POV gate**;
  GEO over-optimization guard (information-distorting rewrites are a
  detection target); repeated citation sampling rule (LLM brand
  recommendations unstable); Gen AI performance report as a first-class
  weekly KPI; "Search generative AI features" eligibility check; spam-policy
  risk rules (no page-per-variant sprawl, authorship requirements, AI
  disclosure when substantial).
- `write-article` / `audit-content` / `seo-analyst` / `content-manager` /
  `researcher` / `content-writer` roles and the `seo-keyword-brief` /
  `content-audit` workflows: non-commodity language synced from
  `optimize-seo` (single source of truth preserved). Schema field names
  (`information_gain*`) are unchanged for contract compatibility; only
  prose and descriptions moved.
- `configure-llms-txt`: v2 format (per-subpath files, `.md` twins,
  `rel="describedby"`), honest scoping ("agents only, no Google effect"),
  AI Catalog added to the dual-audience link set.
- `seo-weekly-board.json` + `content-handoff.json`: new gen-AI visibility
  fields (`gen_ai_report`, `gen_ai_visibility` with impressions,
  citation samples, authorship block, eligibility flag).

### Notes

- No new skills, roles, or workflows were added in this release; counts
  remain 34 roles / 107 skills / 24 workflows / 50 contracts.
- Watch-items intentionally NOT built into rules: WebMCP primary spec,
  AI Catalog adoption votes, Flink Agents (0.3.x), "SLSA for data"
  (does not exist as a standard), AAIF memory-interop WGs.

## [4.1.0] - 2026-09-01

Standard 2026 consistency upgrade release. No breaking changes; every upgrade
adds the optional `## Failure Modes`, `## Output Contracts`, and
`## Security Guardrails (OWASP ASI)` sections without renumbering steps,
renaming files, or changing the validator contract.

### Skills (107 core)

- Added `## Failure Modes` to 97 core skills (all of them).
- Added `## Security Guardrails (OWASP ASI)` references to skills that touch
  tools, agents, identity, memory, or untrusted content.
- Renamed `## Output Format` to `## Output Contracts` and added explicit
  `contracts/schemas/<name>.json` references where applicable.
- Extracted long sections to `references/<topic>.md` for skills that exceeded
  the 200-line cap; validator passes with 0 files over 200 lines.

### Roles (34)

- Added `## Failure Modes` to 34 role files (all of them), inserted before
  `## Anti-Patterns To Reject` so the 17 mandatory sections keep their order.
- Items are role-specific (4-6 per role, tiered by importance), with a
  Scenario + Mitigation format.

### Policies (3 YAML + 1 hook + 1 README)

- `action-boundaries.yaml`: added explicit `denied` tier placement for 16
  previously-unclassified infra/deploy verbs (apply_iac, drop_storage_volume,
  terminate_instance, modify_iam_policy, modify_network_topology_production,
  modify_payment_gateway_config, self_approve_iam,
  shipping_label_generation, delete_cloudflare_resource, run_migration,
  delete_file, modify_environment_config, modify_prompt_template, run_build,
  export_data, write_database) so the file is fail-closed.
- `data-classification.yaml`: added `schema_version: "1"`, an untrusted
  inversion comment, an `internal` soft-PII list, and an ephemeral OIDC
  token example under `restricted`.
- `mcp-tool-map.yaml`: deduplicated the `drop database` pattern and added
  Python (uv, poetry, pipx), Docker, kubectl (delete, rollout, scale, exec),
  GitHub CLI, npx, and pnpm dlx coverage.
- `core/scripts/hooks/check-policy.py`: fixed the misleading exit-code
  docstring, fixed the SARIF emission structure, implemented
  `AGENT_ACTIVE_ROLE_LEVEL=read_only` to downgrade any non-allowed verdict
  to denied, and added `--emit-audit` to write OCSF 99001 audit events to
  the configured path.
- `README.md`: bumped the role count from 26 to 34, added the version
  footer, the example decision table, and the EU AI Act / OCSF / check-policy
  references.

### Workflows (18)

- Added `### Failure Modes` to 18 workflow files (all of them) using H3
  (the workflow validator requires exactly 1 H2 per file).
- Added `### Output Contracts` to 18 workflow files, naming the exact JSON
  schemas the workflow emits (a2a-task.json, incident-report.json,
  deployment-plan.json, etc.).
- Added `### Security Guardrails (OWASP ASI)` to the 10 Tier-1 workflows
  whose steps are irreversible, security-sensitive, or blast-radius
  decisions.
- Tier 1 (10): agent-a2a-delegation, build-deploy, data-migration,
  dependency-upgrade, hotfix-production, revert-deployment,
  security-incident-response, tech-repo-review, service-review-release,
  troubleshooting.
- Tier 2 (6): add-new-feature, content-audit, content-publishing,
  qa-validation, refactoring, setup-new-service.
- Tier 3 (2): seo-content-lifecycle, seo-keyword-brief.
- Ad-hoc H3 failure lists (troubleshooting, data-migration, tech-repo-review,
  service-review-release) preserved; the new `### Failure Modes` section
  is added beneath them for cross-workflow consistency.

### Overlays (10 skills + 6 workflows)

- Added `## Failure Modes` + `## Output Contracts` to 10 overlay skills
  (debug-3d-scene, integrate-r3f-three-legacy, optimize-3d-assets,
  develop-obj-feature, develop-laravel-ecommerce-feature,
  write-real-estate-astro-data, develop-laravel-feature,
  develop-b2b-catalog-feature, develop-b2b-golf-feature, write-hugo-twin-content).
- Added `## Security Guardrails (OWASP ASI)` to overlay skills that touch
  3D, AI-generated assets, payment, or commerce surfaces.
- Added `### Failure Modes` + `### Output Contracts` to 6 overlay workflows
  (deploy-laravel, deploy-laravel-ecommerce, publish-real-estate-content, affiliate-publishing,
  content-audit-refresh, publish-series).

### Validation

- All 16 validators pass with 0 errors and 0 warnings.
- `validate-skills.py`: 107 skills checked.
- `validate-roles.py`: 34 roles checked.
- `validate-workflows.py`: 18 workflows checked.
- `validate-policy-consistency.py`: 34 role profiles checked.
- `validate-2026-compliance.py`: 34 roles, 34 policies wired.
- `validate-a2a-compliance.py`: A2A 1.0 + Antigravity adapter.
- `validate-agent-cards.py`: 34 cards checked.
- `validate-overlays.py`: 17 overlays checked.
- `validate-packs.py`: 13 packs checked.
- `validate-rules.py`: source and adapters checked.
- `validate-skill-ownership.py`: 97/97 core skills have a Primary owner.
- `validate-contract-coverage.py`: 34 roles checked.
- `validate-contracts.py`: 43 schemas checked.
- `validate-indexes.py`: all indexes current.
- `validate-version-sync.py`: VERSION 4.0.1 consistent.
- `validate-standardization.py`: 100% standardization score.

## [4.0.1] - 2026-08-26

Consistency-hardening release from a full skill/role/rule refactor audit.
No breaking changes; all drift classes found by the audit now fail the
quality gate instead of passing silently.

### Roles

- `Deliverable Routing` promoted from de-facto convention to a mandatory,
  order-checked section in `role-standard.md` and `validate-roles.py`; every
  routing table now uses the canonical `| Situation | Primary deliverable |
  Notes |` header.
- Footer hygiene enforced: exactly one `Last updated: YYYY-MM-DD` line, as
  the final non-empty line of every role file. Fixed `seo-analyst.md`,
  which carried two footers and overlay content after the footer; that
  content moved into a proper `## Optional Overlays` section.
- `ai-systems-engineer` gained its missing Deliverable Routing table;
  `technical-architect` heading normalized; `technical-writer` and
  `ui-ux-designer` routing tables re-headered.
- Duplicate lock names resolved: `cloudflare-engineer` second BOUNDARY LOCK
  renamed to SCOPE LOCK; `agent-coordinator` duplicate IRREVERSIBLE ACTION /
  TRACE locks renamed to SIGN-OFF LOCK / PHASE-TRACE LOCK.
- `agent-discovery-engineer` Level raised from Senior to Principal,
  matching the roles README level claim.
- Formatting repairs: missing blank lines before headings in
  `task-planner` and `agent-coordinator`; split Supporting Skills list in
  `data-analyst`.
- Writing roles upgraded from the top-installed writing skills on
  skills.sh: `content-writer` gained line-level conversion-copywriting
  discipline (clarity over cleverness, specificity, voice-of-customer,
  weak-word substitution pass, CTA craft — from `copywriting`);
  `technical-writer` gained agent-facing writing discipline (context
  pointers, information hierarchy, checkable completion criteria, leading
  words, prompt-the-positive, cache-auditor pruning — from
  `writing-for-agents`); `content-manager` gained the searchable vs
  shareable lens with explicit calendar ratios, pillar criteria check,
  word-level substitution tables and sweep-order editing standards in the
  style guide, and a quarterly AI visibility audit (from `content-strategy`,
  `copy-editing`, `ai-seo`).

### Skills

- Contract-emission guidance standardized on `## Output Contracts`;
  variant headings (`## Output Schema`, `## Output Artifact Guidance`)
  are rejected by `validate-skills.py`. Renamed in `agent-delegation`,
  `meeting-review`, `manage-vietnam-accounting`; merged the duplicate
  output section in `agent-graph-orchestration`.
- `write-article` reduced from 325 to ~200 lines by extracting the AI
  outline/image/drafting templates into
  `references/ai-drafting-playbook.md` per the References Subdirectory
  Policy.
- Overlay skill `develop-golf-feature` rewritten to the SKILL baseline:
  added When to Use, real step bodies under Suggested Process (previously
  empty step headings).
- `commit-code` OpenAI interface prompt no longer narrows the skill to
  microservice changes.
- `review-code` upgraded to a two-axis review (Standards / Spec) adapted
  from the `code-review` skill in `mattpocock/skills`: fixed-point diff
  pinning with fail-fast validation, spec-source resolution order, Fowler
  smell baseline as a repo-overridable judgement-call layer, parallel
  sub-agent execution with self-contained prompts, and aggregation that
  never cross-reranks axes. Full baseline and sub-agent briefs live in
  `review-code/references/two-axis-review.md`; existing domain checks,
  severity levels, and the `code-review-finding.json` contract retained.
- `optimize-seo` upgraded with five practices merged from the
  agentic-awesome-skills catalog (sickn33): internal-linking discipline
  (typed links cluster→pillar/pillar→cluster/cluster→cluster/contextual
  boost, orphan-page-first ordering, anchor-text hygiene with exact-match
  reuse ban and ~100 outgoing-link cap), explicit cannibalization
  resolution tactics plus keyword-to-page mapping prevention, four-axis
  scored audits (overall/SEO/AEO/readability out of 100 with pass bands,
  Blocking/Important/Follow-Up fixes, projected post-fix score),
  TL;DR-block extractability signal and 4-entry FAQ minimum, per-engine
  citation measurement (numbered vs inline styles, UTM tagging,
  entity-consistency lever), and a decay-signal-prioritized freshness
  queue (>3-position drops, stats older than 2 years).
- Skills inventory note corrected: `create-automation-script` is
  classified under MMO, not Platform.

### Rules And Adapters

- Three rules previously unmirrored across adapters are now mirrored in
  all seven adapters and machine-checked as new parity groups in
  `validate-rules.py`: environment-file protection (`.dev.vars`/`.env`),
  repo-local override, and full comment hygiene. Adapter parity standard
  updated from six to nine groups.

### Tooling

- `generate-index.py` computes all INDEX.md heading counts and the
  version pin from disk instead of hard-coding them; new `--check` flag
  verifies generated artifacts without writing.
- `validate-indexes.py` now runs the generator in check mode, so stale
  `INDEX.md` / `role-skill-index.json` fail the gate.

## [4.0.0] - 2026-08-07

Major refactoring release driven by a full role↔skill ownership audit plus a
taxonomy restructure. **Breaking**: three skills renamed or moved out of core;
four taxonomy directories added; several role toolboxes changed ownership.

### Breaking Changes

- **R3F/Three.js cluster migrated out of core** — `debug-3d-scene`,
  `integrate-r3f-three-legacy`, and `optimize-3d-assets` moved from
  `core/skills/frontend/` to the live overlay `overlays/r3f-stack/skills/`.
  Update any path-based tooling (`core/skills/frontend/<name>`) to the new
  overlay location. `3d-graphics-engineer` role references resolve by skill
  name and are unaffected.
- **`debug-workos-integration` renamed to `debug-identity-provider`** —
  vendor-generic naming per the pack's own rule. All references in
  `configure-mcp`, `configure-oauth-metadata`, `manage-auth-md`,
  `agent-discovery-engineer`, and the A2A agent card updated.
- **Foundation taxonomy split** — `core/skills/foundation/` reduced from 26 to
  12 skills. New taxonomies: `core/skills/meetings-analysis/`
  (`meeting-review`, `analyze-business-requirements`, `analyze-data`),
  `core/skills/repo-ops/` (`navigate-service`, `troubleshoot-service`,
  `review-code`, `review-service`, `commit-code`), and `core/skills/content/`
  (`write-article`, `repurpose-content`, `audit-content`, `optimize-seo`).
- **MMO cluster colocated** — seven skills (`generate-mmo-content`,
  `analyze-campaign-roi`, `deploy-mmo-infrastructure`, `deploy-proxyware-fleet`,
  `create-automation-script`, `manage-mmo-assets`, `setup-tracking-system`)
  moved from `foundation/`, `platform/`, and `security-data/` into
  `core/skills/mmo/`.

### Role Ownership Fixes (audit-driven)

- `agent-semantic-memory`: Primary moved from `teacher` to `agent-coordinator`
  (teacher now Supporting).
- `configure-agent-commerce`: `agent-discovery-engineer` demoted to Supporting;
  `ecommerce-engineer` is sole Primary.
- `navigate-service` ownership inversion fixed: developers (`backend`,
  `frontend`, `mobile` engineers) are now Primary; `business-analyst`,
  `solution-architect`, `technical-architect`, `technical-lead`,
  `ui-ux-designer` demoted to Supporting.
- `analyze-business-requirements`: `business-analyst` is sole Primary; four
  other roles demoted.
- `conduct-research`: `researcher` sole Primary; `solution-architect` demoted.
- `write-product-brief`: `product-manager` sole Primary; `content-manager` and
  `task-planner` demoted.
- `supply-chain-security`: `security-engineer` sole Primary; `devops-engineer`
  demoted.
- `review-service`: `reviewer` sole Primary; `qa-engineer`,
  `technical-architect`, `technical-lead` demoted.
- `meeting-review`: ownership narrowed to `project-manager` and
  `technical-lead`; six other roles demoted to Supporting.
- `task-planner` toolbox rebuilt after cascading demotions —
  `meeting-review`+`design-ux-flow` Primary (demoted in cleanup),
  task-planner now has `meeting-review` P retained and `design-ux-flow`
  promoted.
- Speculative Supporting entries trimmed: `devops-engineer`
  (`durable-objects`, `manage-api-catalog`), `data-analyst` (`sandbox-sdk`).

### Added

- `validate-contract-coverage.py` — new advisory validator that flags when a
  role names a contract under Outputs Produced but no toolbox skill declares
  emitting it. Wired into `validate-all.py`. Currently reports 40 advisory
  warnings to be backfilled over the next minors; does not block.
- **`write-article`** — three new sections: AI-Assisted Outline Protocol
  (5-component context prompt, SERP grounding pass, heading hygiene audit,
  iterate-until-depth loop, outline sign-off capture), AI Image Generation
  Brief (structured image prompt template + image SEO rules), and Prompt
  Framework For AI-Assisted Drafting (canonical five-component table every
  section-level LLM call must include).
- **`content-writer` role** — AI-Assisted Drafting Discipline block and three
  new Guardrail locks (OUTLINE-ITERATION, IMAGE-BRIEF, PROMPT-FRAMEWORK).
- Output Contracts sections in `write-tech-radar` (adr-spec,
  architecture-options), `write-product-brief` (solution-brief),
  `add-api-endpoint` and `add-ui-component` (implementation-result),
  `wrangler` (edge-deployment-spec), `design-learning-plan`
  (learning-handoff).
- Content Manager tagged into `content-publishing` step 6 and
  `seo-content-lifecycle` step 4, closing the README ↔ workflow drift where
  the role was recommended for both flows but never assigned in them.

### Fixed

- `validate-skills.py` `PLACEHOLDER_REFS` extended with `yes`, `no`,
  `oauth-protected-resource`, `oauth-authorization-server`, `api-catalog`,
  `server-card.json` so role prose literals are not misread as dangling skill
  references. Removed a dead `server-card.json` entry that the lookup regex
  could never match.
- `wrangler/SKILL.md` structural repair — 2026 Wrangler v4 block moved above
  Checklist; literal `\n` artifacts removed.
- `core/skills/README.md` — added References Subdirectory Policy, Size
  Guidance, and Domain Cluster Notes sections; counts updated (91 core + 10
  overlay = 101 total).
- `AGENTS.md` taxonomy list now reflects the 13 active taxonomy directories.

## [3.5.0] - 2026-07-28

Corrective release from a full-pack audit. All 12 existing validators passed before this
work, so every item below was invisible to the quality gate — four new validators close
those gaps.

### Added
- `validate-version-sync.py`: checks `VERSION` against the A2A registry, all 32 agent cards, adapter templates, and the newest CHANGELOG entry. Catches a version bump where generated artifacts were not regenerated.
- `validate-indexes.py`: checks that every skill, schema, role, workflow, overlay, and pack is listed in its index, and that declared counts match disk.
- `validate-policy-consistency.py`: cross-checks `action-boundaries.yaml` against role files — no verb in two tiers, no irreversible action pre-authorized, every role able to create its own outputs, every tool-map action classified.
- `validate-skill-ownership.py`: every skill has a Primary owner, no Primary/Supporting conflict, no Primary skill contradicted by the role's own boundaries, and every workflow step's named skill is reachable from its tagged role.
- `delegate_task` action verb in `action-boundaries.yaml`, classified for all 32 roles (allowed for Agent Coordinator, approval-gated for roles holding `agent-delegation` as Supporting, denied otherwise). A2A delegation and sub-agent invocation previously had no policy verb at all.
- `run_deployment_preview` verb so deploy-owning roles keep ephemeral preview deploys ungated while `run_deployment` is gated.
- `apply_iac` mappings in `mcp-tool-map.yaml` for `terraform apply`, `pulumi up`, and `cdk deploy`; delegation mappings for `delegate_task`, `invoke_sub_agent`, `spawn_agent`, `a2a_send_task`.
- `## Role Boundaries` ownership tables for `agent-discovery-engineer` and `mmo-engineer`; all 32 roles now carry one.
- Skill Toolbox Standard and Contract Path Convention sections in `role-standard.md`.
- Skill Toolbox Rule for workflow steps in `core/workflows/README.md`.

### Fixed
- **Accessibility criteria** in `accessibility-review`: `aria-braillevaluedescription` does not exist (correct attributes are `aria-braillelabel` and `aria-brailleroledescription`); 2.4.11 is Focus Not Obscured (Minimum) at AA, not Focus Appearance (which is 2.4.13, AAA); added the binding-regulation note that EN 301 549 and DOJ ADA Title II both map to WCAG 2.1 AA, and that the DOJ deadline was extended to 26 April 2027.
- **x402 headers** in `configure-agent-commerce`: v2 uses `PAYMENT-REQUIRED` (server), `PAYMENT-SIGNATURE` (client), `PAYMENT-RESPONSE` (receipt). The file previously had the server sending `X-PAYMENT`, which was a client-sent v1 header. Removed the unsourced `WWW-Authenticate: X-Payment-Required` challenge and the unsourced `/.well-known/acp-manifest.json` path (ACP is defined by REST endpoints; UCP publishes `/.well-known/ucp`). Corrected "Merchant Payment Protocol" to Machine Payments Protocol.
- **A2A spec claims** in `agent-a2a-protocol`: the spec streams `TaskStatusUpdateEvent` / `TaskArtifactUpdateEvent` with `TASK_STATE_*` states, not `task_started`/`task_progress`; card signing is a JWS with the key resolved from the JWS header and no mandated algorithm (Ed25519 and key pinning were pack additions); `application/json-seq` and `X-A2A-Signature` are not in the spec. Pack-local names (`task.*` events, `agent.invoke`/`agent.stream`) are now explicitly labelled as the Antigravity adapter binding, and the `task.*` list is aligned with the `a2a-task-progress.json` enum it previously contradicted.
- **MCP baseline** in `configure-mcp`: the pre-migration revision is `2025-11-25`, not `2025-03-26` (two revisions stale). Server Cards are an experimental extension (SEP-2127), not core spec, so the path is no longer described as non-negotiable. `navigator.modelContext` documented as a flag-gated draft where polyfills are legitimate. Added the `MCP-Protocol-Version` header to the stateless migration steps.
- **`content-manager` self-contradiction**: `write-article` was a Primary skill while the role's own boundaries stated it "does not write full articles". Moved to Supporting. Also stopped it emitting `content-handoff.json` (Content Writer) and `coordination-plan.json` (Agent Coordinator), and scoped its KPI ownership to content pillars so it no longer collides with Data Analyst metric definitions.
- **Inference placement ownership** contested by `technical-architect` (EDGE-INFERENCE LOCK) and `system-engineer` (Role Boundaries denying the architect AI infra). Split: architect owns the decision and ADR rationale; System Engineer owns provisioning, routing implementation, and supplies the latency/capacity/cost evidence.
- **`qa-engineer` inverted policy tiers**: `write_file` was allowed while `create_file` required approval, gating the role's own `test-report.json` and `validation-result.json` while permitting arbitrary overwrites.
- **Irreversible actions pre-authorized**: `rotate_agent_credentials` (devops-engineer, security-engineer), `apply_iac` (system-engineer, aws-engineer), and `run_deployment` (cloudflare-engineer, devops-engineer) moved from `allowed` to `requires_approval`, matching the Irreversible Action Standard and the policy file's own footer.
- **`reviewer` and `sre` could not produce their primary contracts**: added `create_file` for Reviewer (`code-review-finding.json`) and `create_file`/`write_file` for SRE (runbooks, `incident-report.json`) while keeping code and infrastructure mutations gated.
- **`agent-discovery-engineer` policy profile** carried Cloudflare Engineer's `modify_dns_production`, `purge_cache_zone`, and `run_deployment`; those are now denied, matching the role's stated boundaries.
- **Commit gate weakened in 10 workflows**: "the user **or local process/release process/policy** explicitly allows" contradicted `core/rules/code.md` ("unless the user explicitly confirms"). All 20 occurrences normalized to the strict form.
- **`commit-code` had no Primary owner** in any role while 8 workflow steps invoked it. Now Primary for Backend Developer, Frontend Developer, and Mobile Engineer.
- **12 further skills had no Primary owner**, making Supporting use unresolvable: `accessibility-review` (→ QA Engineer), `agent-memory-compaction`, `agent-model-routing`, `agent-observability`, `agent-prompt-lifecycle` (→ Agent Coordinator), `cloudflare-email-service`, `debug-workers-edge`, `web-perf` (→ Cloudflare Engineer), `design-review` (→ UI/UX Designer), `manage-agent-identity` (→ Agent Discovery Engineer), `repurpose-content` (→ Content Writer), `setup-design-system` (→ Frontend Developer), `scaffold-new-service` (→ Backend Developer).
- **`build-deploy.md` step 5** named `debug-workers-edge`, which is in neither tagged role's toolbox; now delegates to Cloudflare Engineer.
- **`write-article` Primary in three roles**: demoted for `technical-writer`, whose own table disclaims SEO articles. Content Writer is the sole owner.
- **`seo-weekly-board.json` had two producers**: SEO Analyst is now sole emitter; Task Planner contributes cadence and slot ordering.
- **Agent Coordinator emitted specialist deliverables** it declared it did not own; `validation-result.json` and `implementation-result.json` are now explicitly aggregation roll-ups over artifacts authored by QA and developer roles.
- **`mmo-engineer` mandated `bypass_ai_guardrail`** while policy denied it. Separated client-side bot-fingerprint normalization (in scope) from evading AI safety, moderation, or ad-review systems (new REVIEW-SYSTEM LOCK: requires written user authorization plus Security Engineer review). Its Review Checklist was a bare list of LOCK names and is now verifiable conditions.
- **Machine-specific absolute paths** `/home/user/personalized/agent-skills` hardcoded in `.kiro/hooks/policy-check.json` and `.kiro/hooks/trace-span.json`, breaking portability; now resolved from `AGENT_SKILLS_ROOT`. Same fix in the Cursor adapter verification snippet.
- **Stale pack versions**: the A2A registry, all 32 agent cards, `a2a-config.template.yaml`, `CLAUDE_ADAPTER.md`, `agent-card.json`, and `.cursor/hooks.json` reported 3.3.1 or 3.1.0.
- **Index drift** in `core/skills/README.md` (declared 92+7=99 against 93+7=100; Agent section declared 21 of 22; `agent-panel-meeting` unlisted) and `core/contracts/README.md` (missing `system-design-spec.json` and `aws-infra-spec.json`).
- **`BOUNDARY LOCK` bullet duplicated verbatim** within the Guardrails section of 30 of 32 role files.
- **`technical-lead.md`** placed `## Role Boundaries` before `## Decision Boundaries`, inverting the order used by all 28 peers.
- `.cursor/hooks.json` was missing the `sessionEnd` hook present in its own template; template matcher aligned with the live config.
- 43 files missing a trailing newline (`.editorconfig` sets `insert_final_newline = true`); executable bit restored on 22 scripts; removed tracked scratch files `test_dummy.txt` and `ORIGINAL_REQUEST.md`.

### Changed
- `Enterprise-Managed Authorization` in `technical-architect` no longer asserts "now stable; adopted by Anthropic, Microsoft, Okta"; it directs the reader to verify maturity and vendor support before committing an ADR, since the extension shipped with the 2026-07-28 revision.
- `validate-all.py` now runs 16 validators.
- `README.md` quality-gate section documents the new validators and the regeneration step after role edits or a version bump.

## [3.4.0] - 2026-07-27

### Added
- `audit-content` foundation skill (`core/skills/foundation/audit-content/SKILL.md`) for the content refresh cycle: baseline audit → read → research latest standards → update → post-update SEO/GEO/AEO audit. Added to the Content Manager Primary Skill Toolbox.
- `content-audit` workflow (`core/workflows/content-audit.md`): Content Manager-led refresh cycle coordinating Data Analyst, Researcher, Content Writer, and SEO Analyst from baseline audit through post-update SEO re-audit and republish.
- Two contract schemas that roles/skills referenced but were missing: `solution-brief.json` (Solution Architect scoping handoff) and `ai-risk-register.json` (ai-risk-assessment output; NIST AI RMF + 600-1, EU AI Act tier, OWASP ASI). Contract inventory: 40 → 42.
- Adapter coverage for the AGENTS.md-standard ecosystem: Kiro-native steering (`.kiro/steering/agent-skills.md`), Kilo Code native rules (`.kilocode/rules/agent-skills.md`), and a Codex adapter (`core/codex/README.md` + A2A 1.0-versioned `.a2a-config.json`). Both new rule mirrors are now parity-enforced by `validate-rules.py`; the Agent Compatibility table documents Kiro, Kilo Code, and VS Code Copilot.

### Changed
- Refreshed role definitions to current 2026 standards:
  - **EU AI Act timeline** corrected across `technical-architect`, `solution-architect`, `project-manager`, `product-manager`, and `business-analyst`: high-risk (Annex III) obligations deferred to 2 December 2027 (embedded-in-product high-risk to 2 August 2028), with Article 50 transparency obligations and GPAI penalty powers live from 2 August 2026.
  - **MCP 2026-07-28** stateless protocol core, AAIF (Linux Foundation) governance, and hardened authorization (OAuth Resource Server, RFC 8707, Enterprise-Managed Authorization) reflected in `technical-architect`, `devops-engineer`, and `data-engineer`.
  - **Agentic commerce protocol landscape** corrected in `configure-agent-commerce` and `ecommerce-engineer`: ACP (OpenAI/Stripe), UCP (Universal Commerce Protocol, Google/Shopify), MPP (Stripe Machine Payments Protocol), x402 (Coinbase/Cloudflare), and AP2 (Google/FIDO) with accurate names and layering.
  - `agent-coordinator`: inter-agent trust controls — signed Agent Card verification (OWASP ASI07) and task-scoped, non-inherited identity per delegation (OWASP ASI03).
  - `mobile-engineer`: first-party on-device LLM frameworks (Apple Foundation Models, Android AICore + Gemini Nano) with device-capability gating.
  - `ui-ux-designer`: European Accessibility Act (enforceable 28 June 2025) as the accessibility compliance driver (WCAG 2.2 AA / EN 301 549).
  - `seo-analyst`, `content-writer`, `technical-writer`, `backend-developer`: Google AI Mode, `llms.txt` scoped to agent-facing docs (no Search ranking value), and WebMCP as the emerging agent-interaction surface.
  - `researcher`: agentic Deep Research tool verification discipline and content-provenance checks (C2PA Content Credentials + watermark detection).
  - `system-engineer`: SGLang and NVIDIA Dynamo inference serving plus disaggregated prefill/decode.
- Corrected malformed literal 2026-section headings and trailing characters across `agent/`, `frontend/`, and `foundation/` skills.

## [3.3.1] - 2026-07-22

### Changed
- Hardened runtime policy hooks: approval-required operations now stop with a distinct non-zero status, denied operations remain blocked, and the bundled YAML fallback correctly reads nested policy mappings without PyYAML.
- Updated the Cursor hook configuration to use portable repository-relative commands and documented the blocking behavior.
- Corrected bundled JSON contract examples and extended contract validation to check example required fields and discriminators.
- Synced contract documentation with the current 40-schema inventory.

## [3.3.0] - 2026-07-22

### Added
- `agent-panel-meeting` skill (`core/skills/agent/agent-panel-meeting/SKILL.md`) for orchestrating 6-round multi-role cross-examination panel meetings for feature and architecture designs.

### Changed
- Standardized all 32 role definitions in `core/roles/` with 2026 guardrail LOCKs (`BOUNDARY LOCK`, `SECURITY LOCK`, `IRREVERSIBLE ACTION LOCK`, `TRACE LOCK`, `UNCERTAINTY LOCK`) and optimized skill toolbox token footprints.
- Updated policy boundaries in `core/policies/action-boundaries.yaml` to include complete policy definitions for `3d-graphics-engineer`.

## [3.2.0] - 2026-07-16

### Added
- `## When to Use` section (with concrete trigger bullets) to all 74 skills and roles that previously lacked it, improving execution consistency across the pack.
- Concrete code examples to 12 thin infrastructure/MMO skills (`aws-infrastructure`, `deploy-mmo-infrastructure`, `deploy-proxyware-fleet`, `create-automation-script`, `debug-runtime-platform`, `turnstile-spin`, `add-api-endpoint`, `setup-tracking-system`, `manage-mmo-assets`, `analyze-campaign-roi`, `generate-mmo-content`, `repurpose-content`).

## [3.1.0] - 2026-07-01

### Added
- `mmo-engineer` role to handle Performance Marketing and MMO automation.
- `manage-agent-identity` skill to manage NHI lifecycle, aligned with OWASP ASI03.
- `rotate_agent_credentials` action to `action-boundaries.yaml`.
- AP2 (Agent Payments Protocol) capability support to `agent-card.json`.
- OTel GenAI experimental observability guide (`otel-genai.md`).
- Missing `livestream-web` overlay README.

### Changed
- Expanded `role-standard.md` to cover all 10 OWASP ASI risks.
- Added MCP 2026-07-28 stateless migration steps to `configure-mcp` skill.
- Added `contract_type` discriminator to all 5 SEO schemas.

### Fixed
- Fixed trigger phrases, checklist requirements, and `playwright-stealth` references across 7 MMO skills.
- Fixed `mmo-engineer` decision boundaries and added to role inventory.

## [3.0.0] - 2026-06-22

### Changed
- **Major 2026 Standards Upgrade:** Upgraded all 85 skills across 9 clusters (Agent, Backend, Commerce, Documentation, Education, Foundation, Frontend, Platform, Security-Data) to 2026 industry standards.
- **Roles Upgrade:** Upgraded all 31 Agent Roles (Tech Lead, Tech Architect, Frontend Developer, UI/UX Designer, etc.) with new 2026 guardrails (e.g., `AI-PAIR-GOVERNANCE`, `AGENT-UX-LOCK`, `ZERO-TRUST-A2A`).
- **A2A Security:** Introduced strict Zero-Trust A2A communication rules and Confused Deputy Prevention (OWASP ASI03) to delegation skills.
- **Platform Enhancements:** Added support for Wrangler v4, Cloudflare Remote Bindings, and Durable Objects Actor Model patterns.
- **Data & Security:** Upgraded pgvector index maintenance (`CONCURRENTLY`) for Postgres 17 and added K8s debugging tools.

## [2.11.0] - 2026-06-17

### Added
- `seo-content-lifecycle` workflow: End-to-end topic plan, SEO brief, deep research, draft, audit, and publish lifecycle for content roles.

### Fixed
- `action-boundaries.yaml`: Added missing capability policies for `content-manager` and `solution-architect` roles.
- `agent-coordinator.md`: Fixed heading formatting to pass strict `validate-roles.py` checks.
- `validate-skills.py`: Updated `PLACEHOLDER_REFS` to allow backticked terms from `business-analyst.md`.

## [2.10.0] - 2026-06-16

### Added — Content Manager Role

- **`content-manager` role**: Principal-level role owning full website content strategy — content pillar architecture, editorial calendar, brand voice, content audit & lifecycle, performance measurement, content distribution & repurposing, and SME collaboration. Bridges business goals with daily content production.
- **A2A agent card** `content-manager.agent-card.json` registered in `core/a2a/.well-known/agent-registry.json`
- **Content Distribution & Repurposing** responsibility block: content loop design, repurposing matrix (long-form → social → email → video → newsletter), distribution gate guardrail (`DISTRIBUTION GATE`)
- **SME Collaboration & Thought Leadership** responsibility block: SME roster, structured interview process, YMYL review gate (`SME LOCK`), E-E-A-T experience signal enforcement
- **Product-led content** direction: `/tools`, `/templates`, `/glossary`, `/calculators` — coordinated with Frontend Developer and Product Manager
- New guardrails: `DISTRIBUTION GATE`, `SME LOCK`
- Distribution Plan and SME Roster tables in Output Template
- Review checklist groups: Distribution & Repurposing, SME & Thought Leadership
- New collaboration partners: Frontend Developer (interactive tools), Social Media Manager, Email Marketing Specialist, SMEs

### Changed — Roles & Registry

- **`core/roles/README.md`**: added `Content Strategy And Editorial` lifecycle section; `content-manager` registered in Release and Content And SEO lifecycle phases; workflow mapping table updated
- **`core/a2a/.well-known/agent-registry.json`**: `content-manager` entry added (alphabetical order, between `cloudflare-engineer` and `content-writer`)
- **`content-manager.md` Mission**: expanded from production-only scope to full lifecycle: sản xuất → phân phối → SME → AI search optimisation



### Added — E-commerce Engineer Role & Commerce Skill Taxonomy

- **`ecommerce-engineer` role**: Principal-level role owning the full e-commerce stack (catalog, checkout, payment, fulfillment) with 5 primary skills and commerce-specific LOCK guardrails (`PAYMENT-LOCK`, `PRICE-TRUST LOCK`, `IDEMPOTENCY LOCK`, `STATE-MACHINE LOCK`)
- **`integrate-payment-gateway` skill** (`commerce/`): Stripe, VNPay, PayPal, Momo integration with idempotency keys, webhook signature validation, and PCI-safe tokenization
- **`handle-checkout-flow` skill** (`commerce/`): End-to-end checkout funnel — cart, tax, shipping, coupon, payment, confirmation — with server-side price enforcement
- **`manage-product-catalog` skill** (`commerce/`): Product and variant data model, SKU uniqueness, atomic inventory operations, pricing versioning, multi-channel sync
- **`manage-order-fulfillment` skill** (`commerce/`): Order state machine, carrier label generation, tracking webhooks, return/refund flows
- New **Commerce** taxonomy in `core/skills/` (4 skills)
- `ecommerce-engineer` action boundary policy (`action-boundaries.yaml`) — `modify_payment_gateway_config` and `shipping_label_generation` require approval
- A2A agent card for `ecommerce-engineer` generated and registered in `core/a2a/.well-known/agent-registry.json`

### Changed — Core Rules & Skills Audit

- **`core/rules/code.md`**: Added mandatory `POLICY-AS-CODE` rule requiring all agents to verify against `action-boundaries.yaml` and `data-classification.yaml` before state-changing actions
- **`validate-rules.py`**: Added `policy_enforcement` parity group to enforce that all adapters reference both policy files
- **`.github/copilot-instructions.md`**: Added missing `data-classification.yaml` reference to pass policy parity check
- **`core/skills/security-data/data-engineer/`**: Removed deprecated redirect skill (zero remaining references confirmed); skill count updated accordingly
- **Education skills** (`create-exercises`, `design-learning-plan`, `grade-and-review`): Generalized from hardcoded Vietnamese MOET / THCS to portable global education standards (Bloom's Taxonomy, configurable grading scale, standard academic calendar). Vietnamese-specific conventions may be provided as context by the caller or via overlay.
- **`teacher` role**: Generalized to portable educator role (removed hardcoded MOET references); Output Template now in English with bilingual-friendly structure
- **`core/skills/README.md`**: Updated taxonomy counts, added Commerce section; counts now 76 core + 7 overlay = 83 total
- **`core/roles/README.md`**: Registered `ecommerce-engineer` in Architecture & Engineering, Implementation lifecycle, and Workflow mapping table
- **`overlays/sport-icm/`**: Restored missing directory and `rules/sport-project-rules.md` referenced by `packs/sport-team/manifest.yaml`
- **Root `README.md`**: Updated Overlay list (added `astro-cloudflare`, `data-analyst-stack`, `go-microservices`); fixed stale skill references (`manage-wrangler-deploy` → `wrangler`, `data-engineer` → `build-data-pipeline`); added Commerce domain to delivery domains table

### Validation — All Validators Green

- Rules: ✅ | Skills: ✅ 83 checked | Roles: ✅ 27 checked | Workflows: ✅ 16 checked
- Packs: ✅ 12 checked | Overlays: ✅ 15 checked | Contracts: ✅ 38 checked
- 2026 Compliance: ✅ 27 roles / 27 policies / graph + coordinator A2A wired
- A2A Full Compliance: ✅ | Agent Cards: ✅ 27 checked | Standardization: ✅ 100%

## [2.8.0] - 2026-06-05

### Changed — 2026 AI Governance & Standards Upgrade Wave

Systematic upgrade of **17 roles** to 2025–2026 industry standards. Each role received two new domain sections with concrete guardrails (LOCK rules), expanded review checklists, updated anti-patterns, and updated Definition of Done.

#### Universal Additions Across All Upgraded Roles
- **AI-generated code/artifact governance**: tiered trust validation proportional to risk (High: Auth/Payments/PII; Medium: Logic/Async; Low: Scaffolding)
- **Guardrail naming convention**: `LOCK` suffix on all hard-stop rules (e.g., `AI-CODE LOCK`, `HITL-SPEC LOCK`)
- **Probabilistic thinking**: requirements, SLOs, and acceptance criteria updated to accommodate non-deterministic AI system behavior
- **EU AI Act awareness**: risk tier classification embedded in relevant role outputs (BA ticket, Security review, Architecture ADR)

#### Role-by-Role Changes

**`role-standard.md`** — Added AI Governance universal layer (hard locks: `AI-CODE LOCK`, `OBSERVABILITY LOCK`); Fail-Safe Protocol section; Agent Governance Standards

**`agent-coordinator.md`** — Added Multi-Agent Governance (trust verification, blast-radius analysis before delegation, kill-switch); Progressive Delivery orchestration

**`content-writer.md`** — Added GEO/AEO (Generative Engine Optimization); E-E-A-T signal engineering; AI-assisted draft discipline; AI-Disclosure requirements

**`researcher.md`** — Added AI-Augmented Research Methodology (source triangulation, AI hallucination detection); Research Provenance standards; Epistemic Confidence framework

**`seo-analyst.md`** — Added GEO/AEO optimization layer; AI-native SERP features (SGE, featured snippets); semantic content clustering; entity-based SEO

**`technical-lead.md`** — Added Technical Debt Governance (quantified register, interest rate tracking); AI-Assisted Development Oversight (tiered code validation); Progressive Delivery (feature flags, canary releases)

**`technical-architect.md`** — Added AI/ML System Architecture patterns (RAG, agent orchestration, feature store, vector DB); Architecture Decision Record discipline with AI-specific risk tiers

**`qa-engineer.md`** — Added AI/LLM Testing Discipline (probabilistic AC, LLM-as-Judge, adversarial prompting, hallucination detection); Non-Deterministic Test Architecture (golden datasets, property-based testing)

**`product-manager.md`** — Added AI Product Stewardship (EU AI Act, XAI, HITL); Hypothesis-Driven Discovery (kill-early protocol); Outcome Metrics Framework

**`backend-developer.md`** — Added AI-Assisted Development Governance (tiered trust validation); Observability-First Engineering (OpenTelemetry universal standard, GenAI observability); `AI-CODE LOCK`, `OBSERVABILITY LOCK`, `LLM-INTEGRATION LOCK`, `PROMPT-INJECTION LOCK`

**`frontend-developer.md`** — Added AI-Generated UI Governance (tiered trust model, visual regression discipline); Performance-as-a-Product (INP-first CWV metrics, CI-enforced budgets, rendering strategy framework); `AI-UI LOCK`, `PERFORMANCE-BUDGET LOCK`, `RENDERING-STRATEGY LOCK`, `PERMISSION-BOUNDARY LOCK`

**`data-engineer.md`** — Added AI/ML Data Product Engineering (embedding pipelines, feature stores with training-serving parity, multimodal lakehouse, context engineering, training data quality gates); Data Contracts as Engineering Artifacts (machine-readable, version-controlled, CI/CD validated); `AI-PIPELINE LOCK`, `FEATURE-STORE LOCK`, `DATA-CONTRACT LOCK`, `TRAINING-DATA LOCK`

**`data-analyst.md`** — Added AI-Augmented Analysis (LLM-assisted SQL validation discipline, AI narrative validation, semantic layer alignment); Causal Reasoning Standards (mandatory correlation-causation disclosure, causal methods table, statistical vs. practical significance); `AI-SQL LOCK`, `AI-NARRATIVE LOCK`, `CAUSATION LOCK`, `SEMANTIC-LAYER LOCK`

**`business-analyst.md`** — Added AI Feature Requirements Specification (behavioral boundaries not deterministic outputs, probabilistic AC format, HITL escalation trigger specification, AI accountability model, EU AI Act tier in ticket); Assumption Mapping & Continuous Discovery (living assumption register with risk scoring, Event Storming, JTBD, Impact Mapping, kill-early signals); `AI-AC LOCK`, `HITL-SPEC LOCK`, `ASSUMPTION LOCK`, `EU-AI-ACT LOCK`; expanded Output Template with AI Feature Requirements section and Assumption Register table

**`ui-ux-designer.md`** — Added AI Interaction Design (5-state AI model: Generating/Uncertain/Fallback/Overridden/Corrected; confidence indicators; transparency hooks; human override patterns; Red Path design; HITL interface requirements; AI accessibility extensions beyond WCAG 2.2); Design System as Living Infrastructure (W3C DTCG three-tier token architecture; automated design-to-code pipeline; AI governance for design system); `AI-STATE LOCK`, `AI-OVERCONFIDENCE LOCK`, `TRUST-DESIGN LOCK`, `TOKEN-EXPORT LOCK`

**`devops-engineer.md`** — Added AI/ML Pipeline Governance (model promotion gates, shadow testing, canary rollout with model-specific rollback triggers, inference deployment safety, monitoring gates); GitOps-First Infrastructure & Supply Chain Security (SLSA framework, SBOM, dependency provenance, pinned CI action SHAs); `GITOPS LOCK`, `AI-DEPLOY LOCK`, `SUPPLY-CHAIN LOCK`

**`security-engineer.md`** — Added AI/LLM Security (prompt injection as OWASP LLM01 #1 attack vector, training data poisoning, model output exploitation, LLM-specific STRIDE threat model extensions, EU AI Act high-risk compliance sign-off); Shift-Left Security Engineering (threat modeling before design sign-off, SAST/DAST in CI, dependency and secret scanning gates); `PROMPT-INJECTION LOCK`, `AI-THREAT-MODEL LOCK`, `SHIFT-LEFT LOCK`

**`sre.md`** — Added AI/ML System Reliability (AI-specific SLO dimensions: output quality, inference latency, token cost, model availability, context window utilization; model degradation as P1 reliability incident; LLM-specific operational considerations); Proactive Reliability Engineering (error budget burn rate alerts, chaos engineering, game days, automated runbooks with dry-run mode); `AI-SLO LOCK`, `ERROR-BUDGET LOCK`

## [2.7.0] - 2026-06-02

### Added
- `build-data-pipeline` skill (replaces `data-engineer` skill to resolve naming collision)
- `mobile-engineer` role and corresponding action boundary policy
- `incident-report` and `release-notes` foundation skills
- 100% role compliance: `Role Boundaries` and `Deliverable Routing` added to 8 previously non-compliant roles
- `agents/openai.yaml` stubs added for all missing education and foundation skills

### Changed
- `data-engineer` skill deprecated (redirects to `build-data-pipeline`)
- Education skills (`create-exercises`, `design-learning-plan`, `grade-and-review`) expanded from Grade 6-7 to full Grade 6-9 range
- `setup-deployment`, `database-maintenance`, `add-service-client` skills hardened with extra safety and output format checks
- `write-article` broken overlay references replaced with generic guidance
- All 25 roles and 68 skills now fully compliant with validation scripts

## [2.6.6] - 2026-05-22

### Added
- Skills `design-review` and `accessibility-review` (foundation)
- `build-deploy` workflow: optional Cloudflare edge release step (4b) and `debug-workers-edge` verification

### Changed
- `core/skills/README.md`: full inventory sync (57 core), `conduct-research`, skill boundary table, backlog cleanup
- `data-engineer` skill: *When To Use Data Analyst Instead* boundary section
- `agent-model-routing`: *When Agent Coordinator Enables This* guidance
- Role toolboxes: UI/UX, Reviewer, QA, Frontend, Data Engineer, Agent Coordinator notes for new skills

## [2.6.5] - 2026-05-22

### Changed
- Deliverable Routing and Role Boundaries: `business-analyst`, `content-writer`, `seo-analyst`, `technical-architect`, `agent-coordinator`
- Personalized workspace `AGENTS.md`: Astro Cloudflare sites, cloudflare-engineer mapping, engineering handoffs

## [2.6.4] - 2026-05-22

### Added
- Contract `learning-handoff.json` for Teacher role MOET handoffs

### Changed
- Role hygiene audit: Deliverable Routing and Role Boundaries for DevOps, QA, SRE, PM, Product, Security, Reviewer, Data Engineer, Task Planner, Teacher
- `data-analyst`: fix `contracts/schemas/data-analysis-report.json` in Outputs (A2A card)
- `devops-engineer`, `teacher`: structured contract emission in Definition of Done

## [2.6.3] - 2026-05-22

### Added
- Role `cloudflare-engineer` for Wrangler, Pages/Workers, bindings, and edge incidents
- Contract `edge-deployment-spec.json`
- Skills `manage-wrangler-deploy`, `configure-cloudflare-bindings`, `debug-workers-edge`
- Policy profile `cloudflare-engineer` in action-boundaries.yaml

### Changed
- `devops-engineer`, `sre`, `frontend-developer`: Cloudflare Engineer handoff references
- `overlays/astro-cloudflare`: recommended role pairing

## [2.6.2] - 2026-05-22

### Added
- `research-report.json`: `depth_mode` (deep|scoped), `recommended_next_roles`, `inferences`, `residual_risks`, optional `feature_ticket_ref`

### Changed
- `researcher`: R1 toolbox (Primary `conduct-research` only), R2 handoff parity, R3 contract depth alignment
- `conduct-research` skill: depth_mode rules and scoped waiver

## [2.6.1] - 2026-05-22

### Changed
- `frontend-developer`, `backend-developer`, `3d-graphics-engineer`: D1–D3 developer handoff parity
- All three: `implementation-result.json` in Outputs; Inputs path-ified; Deliverable Routing tables
- `frontend-developer`: Role Handoff aligned with UX/Architect/Lead triangle; FE↔3D two-way handoff
- `backend-developer`: Collaboration expanded; Technical Writer and Lead consumption paths
- `3d-graphics-engineer`: Lead/UX/Architect integration; Primary toolbox cleanup; optional overlays

## [2.6.0] - 2026-05-22

### Added
- Contracts: `architecture-options.json`, `technical-delivery-plan.json`, `documentation-handoff.json`
- Skill `plan-technical-delivery` for Technical Lead

### Changed
- `adr-spec.json`: affected_services, api_contract_refs, supersedes_adr, rollback_plan, feature_ticket_ref
- `technical-architect`, `technical-lead`, `technical-writer`: full triangle handoffs (packages A/B/C)
- `business-analyst`, `agent-coordinator`, `backend-developer`, `frontend-developer`: aligned contracts
- `write-tech-radar`: role routing vs ADR and Technical Writer

## [2.5.4] - 2026-05-22

### Added
- `ux-flow-spec.json` contract for multi-screen UX handoff
- `overlays/ui-design-system` with flow/component handoff conventions
- UI/UX Designer: BA/Researcher/Data Analyst handoffs, deliverable decision table, optional overlays

### Changed
- `ui-component-spec.json`: flow_id, events, copy_per_state, api_fields, feature_ticket_ref
- `design-ux-flow` skill: layered contracts and deliverable decision table
- `frontend-developer`, `business-analyst`, `researcher`, `data-analyst`: UX spec handoffs

## [2.5.3] - 2026-05-22

### Added
- `write-article` foundation skill for editorial drafting
- `content-handoff.json` contract for article deliverables
- Content Writer: Research Depth table, overlay activation, publish-log duty under seo-publishing

### Changed
- `content-writer`: primary toolbox write-article + write-documentation; supporting overlay site skills
- `write-documentation`: role routing (articles vs Technical Writer)
- `researcher`, `business-analyst`, `task-planner`, `seo-publishing`: Content Writer handoffs

## [2.5.2] - 2026-05-22

### Added
- `feature-ticket.json`: business_rules, preserved/changed behavior, open_questions, analytics_request, seo_content_request
- Business Analyst: Research and SEO handoffs; Research Request and SEO Content Request template sections

### Changed
- `business-analyst`: conduct-research supporting skill; expanded collaboration and guardrails
- `analyze-business-requirements` skill: ticket JSON, delegation table, checklist
- `generate-a2a-registry.py`: output schemas derived from Outputs Produced only (fixes BA agent card)
- `researcher`, `seo-analyst`: explicit handoff from Business Analyst

## [2.5.1] - 2026-05-22

### Added
- `overlays/seo-publishing`: dual-site sprint cadence, plan/baiviet board, publish-log, and cannibalization rules
- Contract `seo-weekly-board.json` for structured 7-day topic boards

### Changed
- `seo-analyst` and `task-planner`: optional seo-publishing overlay activation

## [2.5.0] - 2026-05-22

### Added
- `seo-analyst` role with skill `optimize-seo`
- Contracts `seo-content-brief.json` and `seo-audit-report.json`
- A2A agent card and policy profile for SEO Analyst

### Changed
- `content-writer` and `task-planner`: explicit SEO Analyst handoff for briefs, audits, and topic boards
- `core/roles/README.md`: Content And SEO lifecycle mapping

## [2.4.2] - 2026-05-22

### Added
- `overlays/data-analyst-stack`: DuckDB, Metabase, and BI conventions for the data-analyst role

### Changed
- `business-analyst`: analytics handoff to Data Analyst, guardrails on unverified KPIs, optional Analytics Request template section

## [2.4.1] - 2026-05-22

### Added
- `data-analyst` role: business-facing metrics, SQL/tabular analysis, and `data-analysis-report.json`
- `analyze-data` foundation skill for analyst workflows

### Changed
- `data-engineer` role refocused on pipelines, ETL, migrations, and operational data platforms (analyst work moved to Data Analyst)

## [2.4.0] - 2026-05-22

### Added
- Schemas: `a2a-push-notification-config.json`, `a2a-task-cancel.json`, `agent-trace-span.json`; optional JWS `signature` on `agent-card.json`
- `validate-agent-cards.py`, `validate-standardization.py` (>=90% gate)
- Cursor adapter: `adapters/cursor/hooks.template.json`, `check-policy.py`, `log-trace-span.py`
- `core/policies/mcp-tool-map.yaml`, `core/prompts/golden/` sample dataset
- `capability-role-map.generated.yaml` from `generate-a2a-registry.py`

### Changed
- Wired `agent-prompt-lifecycle` and `agent-semantic-memory` to Coordinator, Technical Lead, SRE, Researcher
- QA role: `validation-result.json`, `agent-quality-gate`, `agent-observability`
- `CLAUDE.md`, `.cursor/rules/agent-skills.md`, Copilot instructions — A2A/Antigravity parity
- `validate-all.py` includes agent-card and standardization validators

## [2.3.0] - 2026-05-22

### Added
- Full **A2A 1.0** contracts: `agent-card.json`, `a2a-task-status.json`, `a2a-task-progress.json`, `a2a-message.json`, `a2a-jsonrpc-envelope.json`
- `agent-a2a-protocol` skill: discover, invoke, stream, get/list/cancel, scatter-gather
- **Antigravity adapter**: `adapters/antigravity/` (`ANTIGRAVITY.md`, `rules.template.md`, `a2a-config.template.yaml`)
- `core/a2a/` registry with `generate-a2a-registry.py` (21 role Agent Cards)
- Workflow `/agent-a2a-delegation`
- Validators: `validate-contracts.py`, `validate-a2a-compliance.py`

### Changed
- `a2a-task.json` / `a2a-artifact.json`: A2A lifecycle states, streaming, multimodal `parts`
- `agent-coordinator`: primary `agent-a2a-protocol`, registry discovery, progress/status contracts
- `AGENTS.md`: Antigravity + full A2A lifecycle requirements

## [2.2.0] - 2026-05-22

### Added
- `agent-graph-orchestration` skill: phase graphs, parallel groups, merge gates, and coordination-plan publishing
- `core/contracts/schemas/coordination-plan.json`: structured phase graph for Agent Coordinator
- `core/scripts/validate-2026-compliance.py`: validates A2A coverage, coordinator wiring, policy coverage, and policy hooks in tool orchestration

### Changed
- `agent-coordinator` role: primary `agent-delegation` and `agent-graph-orchestration`; A2A and JSON contract handoffs
- `project-manager`, `technical-writer`, `teacher` roles: Collaboration & A2A Delegation and contract references
- `agent-tool-orchestration` skill: Policy-as-Code checks for `action-boundaries.yaml` and `data-classification.yaml`
- `action-boundaries.yaml`: policy entries for all 21 delivery roles (was 9)
- `validate-all.py`: includes 2026 compliance validator

## [2.1.0] - 2026-05-13

### Fixed
- `core/scripts/common.py`: `parse_frontmatter` now supports YAML block scalars (`>`, `|`, `>-`, `|-`). Multi-line descriptions no longer trigger false "invalid frontmatter line" errors.
- `core/skills/security-data/data-engineer/SKILL.md`: restored multi-line description now that the parser handles it correctly.

### Added
- `overlays/hugo-authority-content/rules/content-brand.md`: populated with real voice/tone guidelines, style constraints (meta ≤ 160 chars, Production Failure template, code linting rules), and publishing constraints for authority blog and Learn sites.
- `overlays/hugo-authority-content/workflows/publish-series.md`: end-to-end workflow for producing and publishing multi-part technical series across both Hugo sites. Covers planning, drafting, translation, review, and go-live steps.
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
- 3 overlays (hugo-authority-content, real-estate-content, ecommerce-microservices)
- 3 pack manifests (global-engineering, real-estate-team, hugo-authority-team)
- Adapter parity standard with automated checking
- OpenAI Codex skill adapters for all applicable skills
