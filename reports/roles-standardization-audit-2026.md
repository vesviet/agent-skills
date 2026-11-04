# 39 Role Definitions Standardization: Master Audit & Deep Research Report (2026)

> **Document Type:** Comprehensive Architectural Audit, Empirical Analysis & Standardization Roadmap  
> **Repository:** `agent-skills` (`d:\myproject\agent-skills`)  
> **Version Scope:** Agent-Skills Pack v5.7.2  
> **Audit Date:** 2026-11-04  
> **Author:** Master Audit Author (`teamwork_worker_m1`), synthesized from Explorer 1, Explorer 2, and Explorer 3 surveys  
> **Integrity Mode:** Development (Empirical & Verifiable Verification)  
> **Governing Standards:** `core/roles/role-standard.md`, `INDEX.md`, A2A Protocol 1.0, OWASP ASI Top 10 (2026), OWASP AST10 (v1.0-2027)  

---


## 1. Executive Summary & Audit Context

### 1.1 Project Background & Mission Objective
The **Agent-Skills Pack (v5.7.2)** serves as the authoritative agentic operating standard across all Antigravity surfaces, orchestrating 39 specialized roles, 183 discrete skills, 25 delivery workflows, and 60 machine-validated contracts. As multi-agent engineering workflows scale toward high-autonomy execution under **Agent-to-Agent (A2A 1.0)** protocols, role definitions are no longer passive documentation; they operate as **active execution boundary specifications**, **deterministic capability gates**, and **security enforcement contracts**.

The primary objective of this audit and deep research initiative (**Milestone M1**) is to conduct an exhaustive, empirical investigation across all 39 role definition files in `core/roles/` against `core/roles/role-standard.md`, `INDEX.md`, and 2026–2027 State-of-the-Art (SOTA) agent architecture standards. This report establishes a quantitative baseline, diagnoses structural and architectural gaps across every role, synthesizes emerging 2026–2027 agentic systems principles, and provides an actionable, verified implementation specification for **Phase R2 (Role Definitions Standardization)**.

### 1.2 Audit Scope & Methodology
The audit scope encompasses all **39 authoritative role definitions** residing in `core/roles/` (excluding repository overview `README.md` and the universal standard `role-standard.md`). The research methodology employs multi-source verification:
1. **Triangulated Explorer Surveys**: Consolidating foundational infrastructure findings from **Explorer 1** (Standards & Infrastructure Specialist), detailed catalog analysis of Roles 1–20 from **Explorer 2** (Batch 1 Specialist), and deep research into Roles 21–39 and SOTA synthesis from **Explorer 3** (Batch 2 & SOTA Specialist).
2. **Automated AST & Regex Inspection**: Static code analysis scanning all 39 markdown files for exact line counts, byte sizes, section sequences, bullet counts, guardrail lock counts, OWASP threat citations, and formatting syntax.
3. **Repository Validator Suite Execution**: Verification against all 10 official repository validators in `core/scripts/` (`validate-roles.py`, `validate-2026-compliance.py`, `validate-skill-ownership.py`, `validate-contract-coverage.py`, `validate-policy-consistency.py`, `validate-agent-cards.py`, `validate-a2a-compliance.py`, `validate-standardization.py`, `validate-indexes.py`, `validate-version-sync.py`).
4. **Pytest Challenge Suite Regression Auditing**: Profiling all 42 automated challenge test files in `tests/` across role modernizations and behavioral compliance.

### 1.3 Key Quantitative Findings
The empirical audit revealed both significant architectural strengths and critical standardization gaps across the catalog:

| Metric Category | Current Repository State | Compliance Baseline | Target SOTA Standard |
| :--- | :---: | :---: | :---: |
| **Catalog Count Parity** | **39 / 39 Roles (100%)** | 39 Roles in `INDEX.md` | 100% Parity across Index, Cards & Registry |
| **Legacy Structural Validation** | **39 / 39 Pass (100%)** | Exit Code 0 on `validate-roles.py` | 100% Validator Pass Rate |
| **Header Metadata Architecture** | **0 / 39 YAML Frontmatter (0%)** | Markdown Inline (`# Title` + `Mission:` + `Level:`) | Standardized Markdown Inline Metadata |
| **Explicit Prohibited Skills** | **0 / 39 Explicit Subsections (0%)** | Implicit Closed-World Boundary | Codified `### Prohibited Skills` in all 39 Roles |
| **Failure Modes Section Presence** | **35 / 39 Roles Present (89.7%)** | 16 required sections | **39 / 39 Roles (100%)** with Paired Mitigations |
| **Guardrail Lock Density (>= 12)** | **34 / 39 Roles >= 12 Locks (87.2%)** | Baseline 5 locks | **39 / 39 Roles >= 12-24 Domain Locks** |
| **OWASP ASI Threat Integration** | **39 / 39 Baseline Security Lock (100%)** | Generic ASI Top 10 Lock | Deep ASI01-ASI10 Threat Matrix in Key Roles |
| **OWASP AST10 Skill Security** | **0 / 39 Roles Codified In-File (0%)** | Inherited from `role-standard.md` | Explicit AST01-AST10 Locks across all 39 Roles |
| **Review Checklist Task Format** | **18 / 39 use `- [ ]` (46.2%)** | Mixed (`- [ ]` vs plain `- `) | **39 / 39 Standardized `- [ ]` Checkboxes** |
| **Decision Boundaries Formatting** | **13 / 39 use bold syntax (33.3%)** | Mixed (`- **owns**:` vs `- owns:`) | **39 / 39 Standardized Bold Syntax** |
| **External Review Checklists** | **39 / 39 Reference Files Exist (100%)** | Files in `core/roles/references/` | 100% Coverage with >= 50-200 Lines |

### 1.4 Critical Deficiencies Requiring Phase R2 Action
1. **Four Roles Missing `## Failure Modes`**: `game-developer.md`, `prompt-engineer.md`, `sdet.md`, and `vietnam-legal-counsel.md` omit the modern `## Failure Modes` section entirely, leaving these agents without explicit failure anticipation and mitigation directives.
2. **Five Roles Suffering Guardrail Lock Deficits (< 12 Locks)**: `prompt-engineer` (8 locks), `sdet` (8 locks), `game-developer` (9 locks), `teacher` (10 locks), and `technical-lead` (11 locks) fall below the 12-lock SOTA floor, exposing agent workflows to boundary drift.
3. **Absence of Explicit Skill Prohibitions**: All 39 roles currently rely on the implicit closed-world assumption in `role-standard.md`. Without a deterministic, machine-readable `### Prohibited Skills` subsection, LLM agents risk invoking out-of-scope tools when executing ambiguous prompts.
4. **Universal OWASP AST10 Disconnect**: While `role-standard.md` defines the 2027 Agentic Skill Security Standard (OWASP AST10), not a single role definition file incorporates AST01–AST10 controls in its own `## Guardrails`, losing protection against the "lethal trifecta" (private data access + untrusted input + external egress) under isolated context windows.
5. **Formatting Fragmentation**: Systematic divergence between bold syntax (`- **owns**:`) and plain syntax (`- owns:`), and between interactive task checkboxes (`- [ ]`) and plain bullet lists (`- `), introduces parser ambiguity for automated AST tools.

---


## 2. Authoritative Standards & Governance Framework

### 2.1 The 20-Point Role Standardization Rubric
To eliminate structural drift and enforce uniform quality across all 39 roles, Phase R2 establishes the **20-Point Role Standardization Rubric**, derived from `core/roles/role-standard.md` and repository validator rules:

#### Category A: Header & Metadata Architecture
- [ ] **C1. Single H1 Title**: Exactly one H1 line (`# <Role Title>`), matching the canonical filename slug (or registered alias like `sre` <-> `site-reliability-engineer`). No preceding YAML frontmatter blocks.
- [ ] **C2. Mandatory Mission Line**: Single-line `Mission: <text>` describing the principal objective, context, and operational mandate.
- [ ] **C3. Mandatory Level Line**: Single-line `Level: Principal / master-level ...` designating principal or master-practitioner operating tier.
- [ ] **C4. Standard Reference Link**: Exact verbatim sentence: `This role must follow [role-standard](role-standard.md) first.` immediately following Level.

#### Category B: Section Sequencing & Hierarchy (Exact Order Enforced)
- [ ] **C5. Principal Expectations**: Minimum 4 bullet items (SOTA baseline mandates 10–20 items focusing on system awareness, second-order effects, and trade-offs).
- [ ] **C6. Use This Role When**: Minimum 3 bullet items defining high-signal triggers for role invocation.
- [ ] **C7. Core Responsibilities**: Minimum 4 bullet items, organized under logical domain H3 subheadings.
- [ ] **C8. Inputs Required**: Minimum 4 bullet items explicitly listing consumed contract schemas, source artifacts, and domain context.
- [ ] **C9. Outputs Produced & Boundary Exclusion**: Minimum 4 bullet items naming emitted contract schemas (`contracts/schemas/<name>.json`) and explicitly containing a `Contracts owned by other roles — do not author these as <Role>:` disclaimer block.
- [ ] **C10. Deliverable Routing Table**: Markdown table with `| Situation | Deliverable |` mapping execution triggers to concrete artifacts.
- [ ] **C11. Decision Boundaries**: Minimum 3 bullet items formatted with standardized bold syntax (`- **owns**:`, `- **does not own**:`, and `- **must escalate**:`).
- [ ] **C12. Role Boundaries Table**: Markdown table with `| Role | Owns | Does not own |` header, defining explicit responsibility demarcations with 3–7 adjacent roles.
- [ ] **C13. Collaboration Protocols**: Minimum 3 bullet items documenting interactions with peer roles and handoff artifacts.

#### Category C: Governance & Architectural Locks
- [ ] **C14. Architectural Guardrail Locks**: Minimum 12 explicit `**...LOCK**` definitions in `## Guardrails` (and up to 24 for Tier 1 roles). Must include the universal baseline:
  - `BOUNDARY LOCK` (refuse out-of-scope tasks fail-closed)
  - `SECURITY LOCK` (OWASP ASI Top 10 2026 adherence)
  - `IRREVERSIBLE ACTION LOCK` (explicit human confirmation before destructive changes)
  - `TRACE LOCK` (documenting context, actions, skipped items, and rationale)
  - `UNCERTAINTY LOCK` (fail-safe posture when confidence is below threshold)
  - Plus domain-specific architectural locks and explicit OWASP AST10 skill governance locks.
- [ ] **C15. Skill Toolbox Lock**: Structured into three distinct, disjoint subsections:
  - `### Primary Skills`: Minimum 1 bullet item (`- \`skill-name\``), all existing in `core/skills/`. Authorizes direct execution; cannot be disclaimed in Role Boundaries.
  - `### Supporting Skills (use when collaborating)`: All existing in `core/skills/`. Strictly disjoint from Primary Skills (0 overlap).
  - `### Prohibited Skills`: Explicitly codified forbidden skills to convert implicit closed-world boundaries into deterministic machine-verifiable rules.
- [ ] **C16. Output Template**: Markdown fenced code block (` ```markdown ... ``` `) providing a reusable, copy-pasteable artifact skeleton.

#### Category D: Quality & Verification Gates
- [ ] **C17. Review Checklist & Companion Reference**: Minimum 5 items formatted with standardized interactive task checkboxes (`- [ ]`), with an explicit companion reference link to `references/<role-slug>-review-checklist.md`.
- [ ] **C18. Failure Modes**: Minimum 5 explicit failure scenarios paired with concrete, actionable architectural `Mitigation:` directives.
- [ ] **C19. Anti-Patterns To Reject**: Minimum 4 bullet items naming common anti-patterns the role must refuse.
- [ ] **C20. Role Handoff & Definition Of Done**:
  - `## Role Handoff`: Minimum 3 bullet items containing 2026 A2A markers (`Collaboration & A2A Delegation` or `contracts/schemas/`).
  - `## Definition Of Done`: Minimum 4 bullet items verifying contract validity, traceability, zero irreversible actions without confirmation, and security boundaries.
  - Mandatory Footer: Exactly one line `Last updated: YYYY-MM-DD` as the final non-empty line of the file.

### 2.2 Markdown Inline Metadata Specification vs YAML Frontmatter
A critical finding from Explorer 1 and Explorer 2 audits is that role definitions in `agent-skills` intentionally do **NOT** use YAML frontmatter (`---`). 

Lines 92–105 of `core/scripts/validate-roles.py` strictly validate the top four lines:
```python
body_without_fences = strip_fenced_blocks(body)
h1_lines = [line for line in body_without_fences.splitlines() if line.startswith("# ")]
# Enforces len(h1_lines) == 1 and equivalent_role_slug(...)
# re.search(r"(?m)^Mission: .+", body)
# re.search(r"(?m)^Level: .+", body)
# "This role must follow [role-standard](role-standard.md) first." in body
```
Injecting YAML frontmatter blocks (`---`) into role markdown files would break existing AST parsers and cause repository validators to fail. Instead, the pack enforces a clear architectural separation of concerns:
- **Human & LLM Readability**: `core/roles/<role>.md` uses clean **Markdown Inline Metadata** (Lines 1–7) that is instantly consumable by LLM attention heads without prompt parsing overhead.
- **Machine Discovery Manifests**: Structured metadata (JSON Schema, A2A endpoints, skill tools, cryptographic key IDs) is externalized into canonical JSON Agent Cards residing at `core/a2a/registry/<role>.agent-card.json` and served at `/.well-known/agent-card.json`.

Phase R2 will strictly preserve this Markdown inline metadata invariant across all 39 roles.

### 2.3 OWASP ASI01–ASI10 and AST01–AST10 Threat Governance
Modern principal-level agent systems operate under dual threat vectors: **agent behavioral vulnerabilities** (ASI) and **skill/tool execution risks** (AST). Every standardized role must enforce both governance frameworks:

```
+----------------------------------------------------------------------------------------------------+
|                                    OWASP AGENTIC GOVERNANCE DUAL STACK                             |
+---------------------------------------------------+------------------------------------------------+
| OWASP ASI Top 10 (2026) — Agentic System Security | OWASP AST10 (v1.0-2027) — Agentic Skill Security |
+---------------------------------------------------+------------------------------------------------+
| ASI01: Goal Hijack / Prompt Injection             | AST01: Malicious & Impersonated Skills         |
| ASI02: Tool Misuse & Parameter Exploitation       | AST02: Skill Supply Chain Poisoning            |
| ASI03: Identity & Privilege Abuse                 | AST03: Over-Privileged Skills (Lethal Trifecta)|
| ASI04: Agentic Supply Chain Compromise            | AST04: Insecure & Spoofed Manifest Metadata    |
| ASI05: Unexpected Code Execution (RCE)            | AST05: Remote Untrusted Instructions           |
| ASI06: Memory & Context Poisoning                 | AST06: Weak Execution Sandbox Isolation        |
| ASI07: Inter-Agent Message Spoofing               | AST07: Uncontrolled Skill Update Drift         |
| ASI08: Cascading Multi-Agent Failures             | AST08: Inadequate Pre-Execution Scanning       |
| ASI09: Human-Agent Trust Exploitation             | AST09: Unowned Skill Sprawl & Governance Deficit|
| ASI10: Rogue Autonomous Scope Expansion           | AST10: Cross-Platform Permission Inheritance   |
+---------------------------------------------------+------------------------------------------------+
```

#### The Lethal Trifecta Invariant (AST03)
Under OWASP AST03, any skill that simultaneously combines:
1. **Access to sensitive / private context** (environment secrets, user data, financial ledgers, database records),
2. **Processing of untrusted external content** (unvalidated web pages, third-party emails, raw user input), and
3. **External network egress capabilities** (arbitrary webhooks, HTTP requests, cloud uploads),
constitutes a **Lethal Trifecta** vulnerability. Every standardized role definition must enforce guardrail locks that disallow skills exhibiting this combination unless mediated by explicit human authorization gates.

#### Identity-File Protection Invariant (AST10)
Under OWASP AST10, agent identity files (`AGENTS.md`, `MEMORY.md`, `.cursor/rules`, `role-standard.md`, and system prompts) must be governed by strict **Deny-Write policies**. No automated skill or tool invocation may modify the operating instructions or memory ledgers of the role executing it.

### 2.4 Skill Toolbox Lock & Deterministic Closed-World Boundaries
The `## Skill Toolbox` section defines the role's execution authority:
1. **Primary Skills (`### Primary Skills`)**: Authorizes direct, autonomous execution. Every primary skill must exist in `core/skills/` and cannot be disclaimed in the role's boundaries.
2. **Supporting Skills (`### Supporting Skills (use when collaborating)`)**: Contextual skills used during multi-role collaboration or delegated execution. Must be strictly disjoint from primary skills (0 overlap).
3. **Prohibited Skills (`### Prohibited Skills`)**: Machine-verifiable exclusion list explicitly denying tools outside the role's core domain. Codifying prohibited skills converts the implicit closed-world boundary into deterministic AST fences, eliminating hallucinated tool calls (e.g. Prompt Engineer invoking file write operations, or Legal Counsel invoking git commit code).

---


## 3. Master 39-Role Quantitative Compliance Matrix

The following comprehensive matrix details the quantitative compliance profile of all 39 roles within `core/roles/` evaluated against the 20-Point Standardization Rubric, repository validators, and SOTA architectural standards:

| # | Role Slug | Lines / Size | Header Meta | PE | Pri / Sup | Prohib | Locks | ASI Refs | AST Refs | Failure Modes | Checklist | Ext CL | DB Bold | Index Parity | Compliance Grade |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | `3d-graphics-engineer` | 303L / 21.1KB | Inline | 7 | 3 / 8 | No | 19 | 1 (Base) | 0 (Inherit) | Yes | 15 plain bullets | 116L | No | 100% | Minor Gaps |
| 2 | `agent-coordinator` | 453L / 37.0KB | Inline | 11 | 13 / 8 | No | 16 | 8 (Deep) | 0 (Inherit) | Yes | 39 plain bullets across 5 phases | 165L | Yes | 100% | Minor Gaps |
| 3 | `agent-discovery-engineer` | 243L / 16.6KB | Inline | 6 | 8 / 4 | No | 19 | 1 (Base) | 0 (Inherit) | Yes | 11 [ ] checkboxes | 125L | No | 100% | Minor Gaps |
| 4 | `ai-systems-engineer` | 379L / 40.2KB | Inline | 14 | 6 / 11 | No | 20 | 10 (Deep) | 0 (Inherit) | Yes | 10 [ ] checkboxes | 159L | No | 100% | Minor Gaps |
| 5 | `aws-engineer` | 343L / 40.5KB | Inline | 14 | 3 / 9 | No | 22 | 1 (Base) | 0 (Inherit) | Yes | 15 [ ] checkboxes | 182L | No | 100% | Minor Gaps |
| 6 | `backend-developer` | 470L / 40.3KB | Inline | 17 | 12 / 8 | No | 21 | 8 (Deep) | 0 (Inherit) | Yes | 13 [ ] checkboxes | 105L | Yes | 100% | Minor Gaps |
| 7 | `business-analyst` | 402L / 35.9KB | Inline | 13 | 6 / 6 | No | 20 | 1 (Base) | 0 (Inherit) | Yes | 12 [ ] checkboxes | 228L | Yes | 100% | Minor Gaps |
| 8 | `cloudflare-engineer` | 298L / 19.0KB | Inline | 6 | 14 / 8 | No | 12 | 1 (Base) | 0 (Inherit) | Yes | 12 plain bullets | 152L | No | 100% | Minor Gaps |
| 9 | `content-manager` | 336L / 30.1KB | Inline | 11 | 2 / 12 | No | 18 | 1 (Base) | 0 (Inherit) | Yes | 11 [ ] checkboxes | 74L | No | 100% | Minor Gaps |
| 10 | `content-writer` | 399L / 32.4KB | Inline | 13 | 4 / 9 | No | 15 | 1 (Base) | 0 (Inherit) | Yes | 29 plain bullets across 7 gates | 58L | No | 100% | Minor Gaps |
| 11 | `data-analyst` | 421L / 36.8KB | Inline | 18 | 3 / 7 | No | 18 | 2 refs (Med) | 0 (Inherit) | Yes | 11 [ ] checkboxes | 76L | Yes | 100% | Minor Gaps |
| 12 | `data-engineer` | 442L / 45.8KB | Inline | 15 | 4 / 10 | No | 15 | 11 (Deep) | 0 (Inherit) | Yes | 14 [ ] checkboxes | 85L | Yes | 100% | Minor Gaps |
| 13 | `devops-engineer` | 614L / 70.4KB | Inline | 17 | 8 / 9 | No | 24 | 1 (Base) | 0 (Inherit) | Yes | 45 plain bullets | 195L | No | 100% | Minor Gaps |
| 14 | `ecommerce-engineer` | 274L / 19.0KB | Inline | 8 | 5 / 11 | No | 21 | 1 (Base) | 0 (Inherit) | Yes | 9 plain bullets | 129L | No | 100% | Minor Gaps |
| 15 | `frontend-developer` | 415L / 40.6KB | Inline | 21 | 15 / 11 | No | 22 | 8 (Deep) | 0 (Inherit) | Yes | 10 [ ] checkboxes | 122L | Yes | 100% | Minor Gaps |
| 16 | `game-developer` | 214L / 14.9KB | Inline | 6 | 20 / 6 | No | 9 | 1 (Base) | 0 (Inherit) | **MISSING** | 8 [ ] checkboxes | 115L | No | 100% | **Non-Compliant** |
| 17 | `mmo-engineer` | 228L / 17.3KB | Inline | 5 | 7 / 3 | No | 21 | 1 (Base) | 0 (Inherit) | Yes | 8 [ ] checkboxes | 125L | No | 100% | Minor Gaps |
| 18 | `mobile-engineer` | 486L / 40.2KB | Inline | 10 | 9 / 6 | No | 13 | 1 (Base) | 0 (Inherit) | Yes | 53 plain bullets across 13 sections | 54L | No | 100% | Minor Gaps |
| 19 | `product-manager` | 382L / 26.2KB | Inline | 15 | 5 / 12 | No | 21 | 1 (Base) | 0 (Inherit) | Yes | 21 plain bullets | 113L | No | 100% | Minor Gaps |
| 20 | `project-manager` | 279L / 19.1KB | Inline | 10 | 1 / 10 | No | 21 | 1 (Base) | 0 (Inherit) | Yes | 7 plain bullets | 122L | No | 100% | Minor Gaps |
| 21 | `prompt-engineer` | 206L / 13.0KB | Inline | 7 | 2 / 6 | No | 8 | 1 (Base) | 0 (Inherit) | **MISSING** | 8 [ ] checkboxes | 70L | Yes | 100% | **Non-Compliant** |
| 22 | `qa-engineer` | 574L / 51.6KB | Inline | 17 | 12 / 7 | No | 20 | 24 (Deep) | 0 (Inherit) | Yes | 36 [ ] checkboxes across 10 gate sections | 195L | Yes | 100% | Minor Gaps |
| 23 | `researcher` | 427L / 34.9KB | Inline | 13 | 1 / 9 | No | 22 | 1 (Base) | 0 (Inherit) | Yes | 27 plain bullets across 4 sections | 176L | No | 100% | Minor Gaps |
| 24 | `reverse-engineer` | 287L / 22.9KB | Inline | 7 | 1 / 9 | No | 12 | 2 refs (Med) | 0 (Inherit) | Yes | 11 plain bullets | 86L | No | 100% | Minor Gaps |
| 25 | `reviewer` | 294L / 19.3KB | Inline | 10 | 5 / 9 | No | 14 | 24 (Deep) | 0 (Inherit) | Yes | 7 [ ] checkboxes | 67L | Yes | 100% | Minor Gaps |
| 26 | `sdet` | 207L / 12.2KB | Inline | 7 | 1 / 6 | No | 8 | 1 (Base) | 0 (Inherit) | **MISSING** | 8 [ ] checkboxes | 66L | Yes | 100% | **Non-Compliant** |
| 27 | `security-engineer` | 373L / 30.3KB | Inline | 7 | 7 / 10 | No | 16 | 19 (Deep) | 0 (Inherit) | Yes | 13 plain bullets | 130L | No | 100% | Minor Gaps |
| 28 | `seo-analyst` | 425L / 31.0KB | Inline | 11 | 5 / 7 | No | 17 | 1 (Base) | 0 (Inherit) | Yes | 24 plain bullets across 4 sections | 84L | No | 100% | Minor Gaps |
| 29 | `solution-architect` | 523L / 47.8KB | Inline | 16 | 2 / 11 | No | 24 | 1 (Base) | 0 (Inherit) | Yes | 10 [ ] checkboxes | 76L | Yes | 100% | Minor Gaps |
| 30 | `sre` | 260L / 20.7KB | Inline | 10 | 6 / 7 | No | 12 | 1 (Base) | 0 (Inherit) | Yes | 7 [ ] checkboxes | 35L | No | 100% | Minor Gaps |
| 31 | `system-engineer` | 470L / 40.6KB | Inline | 12 | 8 / 12 | No | 21 | 2 refs (Med) | 0 (Inherit) | Yes | 23 [ ] checkboxes | 135L | No | 100% | Minor Gaps |
| 32 | `task-planner` | 277L / 18.0KB | Inline | 5 | 2 / 7 | No | 21 | 1 (Base) | 0 (Inherit) | Yes | 14 plain bullets | 114L | No | 100% | Minor Gaps |
| 33 | `teacher` | 298L / 26.6KB | Inline | 9 | 3 / 6 | No | 10 | 1 (Base) | 0 (Inherit) | Yes | 6 [ ] checkboxes | 47L | No | 100% | **Non-Compliant** |
| 34 | `technical-architect` | 536L / 48.9KB | Inline | 12 | 6 / 12 | No | 19 | 1 (Base) | 0 (Inherit) | Yes | 41 plain bullets across 4 sections | 72L | No | 100% | Minor Gaps |
| 35 | `technical-lead` | 367L / 26.8KB | Inline | 9 | 7 / 14 | No | 11 | 1 (Base) | 0 (Inherit) | Yes | 7 [ ] checkboxes | 57L | Yes | 100% | **Non-Compliant** |
| 36 | `technical-writer` | 359L / 26.8KB | Inline | 6 | 4 / 10 | No | 15 | 1 (Base) | 0 (Inherit) | Yes | 21 plain bullets across 4 sections | 120L | No | 100% | Minor Gaps |
| 37 | `ui-ux-designer` | 411L / 36.2KB | Inline | 13 | 6 / 7 | No | 24 | 1 (Base) | 0 (Inherit) | Yes | 52 plain bullets across 4 sections | 126L | No | 100% | Minor Gaps |
| 38 | `vietnam-accounting-specialist` | 317L / 29.5KB | Inline | 8 | 1 / 6 | No | 14 | 1 (Base) | 0 (Inherit) | Yes | 7 [ ] checkboxes | 53L | No | 100% | Minor Gaps |
| 39 | `vietnam-legal-counsel` | 306L / 33.3KB | Inline | 8 | 3 / 5 | No | 12 | 1 (Base) | 0 (Inherit) | **MISSING** | 9 [ ] checkboxes | 31L | No | 100% | **Non-Compliant** |

### 3.1 Catalog Stratification & Tier Distribution
The quantitative audit demonstrates three distinct operational tiers across the 39 roles:

1. **Tier 1: Flagship Engineering Roles (6 Roles — 15.4%)**
   - *Roles*: `agent-coordinator`, `backend-developer`, `devops-engineer`, `frontend-developer`, `qa-engineer`, `security-engineer`.
   - *Profile*: Large size (> 30KB / > 350 lines), high lock density (16–24 named locks), deep OWASP ASI integration (8–24 explicit citations), and comprehensive 10-gate checklists.
   - *Phase R2 Action*: Maintain structural depth; add explicit `### Prohibited Skills` and codify OWASP AST10 skill security locks.

2. **Tier 2: Established Specialist Roles (28 Roles — 71.8%)**
   - *Roles*: `3d-graphics-engineer`, `agent-discovery-engineer`, `ai-systems-engineer`, `aws-engineer`, `business-analyst`, `cloudflare-engineer`, `content-manager`, `content-writer`, `data-analyst`, `data-engineer`, `ecommerce-engineer`, `mmo-engineer`, `mobile-engineer`, `product-manager`, `project-manager`, `researcher`, `reverse-engineer`, `reviewer`, `seo-analyst`, `solution-architect`, `sre`, `system-engineer`, `task-planner`, `technical-architect`, `technical-writer`, `ui-ux-designer`, `vietnam-accounting-specialist`.
   - *Profile*: Fully compliant with legacy validators, existing `## Failure Modes`, sound domain invariants, but suffering minor formatting drift (unbolded Decision Boundaries, plain checklist bullets, missing AST10 locks).
   - *Phase R2 Action*: Normalize formatting, add explicit `### Prohibited Skills`, and integrate AST10 skill security locks.

3. **Tier 3: Deficient Roles Requiring Critical Remediation (5 Roles — 12.8%)**
   - *Roles*: `game-developer`, `prompt-engineer`, `sdet`, `teacher`, `technical-lead` (along with `vietnam-legal-counsel` on Failure Modes).
   - *Profile*: Missing `## Failure Modes` (4 roles: `game-developer`, `prompt-engineer`, `sdet`, `vietnam-legal-counsel`), or exhibiting guardrail lock deficits < 12 locks (`prompt-engineer` 8, `sdet` 8, `game-developer` 9, `teacher` 10, `technical-lead` 11).
   - *Phase R2 Action*: High-priority modernization: author full `## Failure Modes` sections with concrete mitigations, expand guardrail locks to >= 12–15 locks, codify prohibited skills, and resolve formatting variances.

---


## 4. Detailed Per-Role Gap Analysis (Roles 1 to 39)

### 4.1. 3D Graphics Engineer (`3d-graphics-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** 3D Graphics Engineer | **Canonical Slug:** `3d-graphics-engineer`
- **Common Aliases in INDEX.md:** `@3d`, `@r3f`, `@threejs`
- **Mission:** Build, optimize, and maintain high-performance 3D interactive experiences, rendering pipelines, and WebGPU/WebGL implementations across web platforms.
- **Level:** Principal / Master-level 3D graphics and interactive web engineering
- **File Metrics:** 303 lines / 21.1 KB | **Last Updated:** `2026-10-17`
- **Principal Expectations:** 7 items
- **Skill Toolbox:** Primary (3): `debug-3d-scene`, `integrate-r3f-three-legacy`, `optimize-3d-assets` | Supporting (8): `navigate-service`, `troubleshoot-service`, `commit-code`, `frontend-testing`, `write-tests`, `review-code`, `performance-profiling`, `agent-delegation`
- **Contract Schema Coverage:** Emits: `adr-spec.json`, `feature-ticket.json`, `implementation-result.json`, `performance-audit.json`, `technical-delivery-plan.json`, `ui-component-spec.json`, `ux-flow-spec.json` | Disclaims: Contracts owned by Frontend unless co-owned in the slice
- **Guardrail Locks:** 19 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026 referenced in line 123) | AST: 0 explicit references (relies entirely on role-standard.md inheritance)
- **Checklist Architecture:** 15 plain bullets; references references/3d-graphics-engineer-review-checklist.md | Companion File: `references/3d-graphics-engineer-review-checklist.md` (116 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Coexistence patterns between React Three Fiber (R3F) and legacy imperative Three.js modules with clean scene graph ownership boundaries.**: Coexistence patterns between React Three Fiber (R3F) and legacy imperative Three.js modules with clean scene graph ownership boundaries.
- **Rigorous VRAM disposal lifecycles recursively freeing geometries, materials, textures, and render targets to prevent WebGL context leaks.**: Rigorous VRAM disposal lifecycles recursively freeing geometries, materials, textures, and render targets to prevent WebGL context leaks.
- **Asset optimization pipeline enforcing Draco geometry compression and Meshopt quantization (clamp to <= 2MB mobile transfer budget) and Basis Universal/KTX2 textures.**: Asset optimization pipeline enforcing Draco geometry compression and Meshopt quantization (clamp to <= 2MB mobile transfer budget) and Basis Universal/KTX2 textures.
- **Forward-compatible WebGPU compute shader pipeline authored in WGSL with seamless runtime WebGL2 fallback detection.**: Forward-compatible WebGPU compute shader pipeline authored in WGSL with seamless runtime WebGL2 fallback detection.
- **3D Gaussian Splatting (3DGS) VRAM budgeting (clamp <= 1.2M splats desktop, <= 400k mobile, <= 250MB VRAM) and procedural hitbox isolation (BVH/AABB).**: 3D Gaussian Splatting (3DGS) VRAM budgeting (clamp <= 1.2M splats desktop, <= 400k mobile, <= 250MB VRAM) and procedural hitbox isolation (BVH/AABB).

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...') instead of standardized bold syntax ('- **owns**:', '- **does not own**:').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by 3D Graphics Engineer (must be declined or routed via Role Handoff):
- `setup-deployment`: Cloud deployment configuration belongs to DevOps Engineer.
- `deploy-aws-eks-workloads`: Kubernetes cluster and node provisioning belongs to AWS Engineer.
- `create-migration`: Relational database schema migrations belong to Backend Developer.
- `manage-vietnam-accounting`: Financial and tax ledgers belong to Vietnam Accounting Specialist.
- `manage-vietnam-legal`: Legal contract vetting and statutory compliance belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **SKILL-AST10 LOCK**: Prohibit dynamic invocation of untrusted 3D asset loader skills lacking cryptographic hash verification or exhibiting the lethal trifecta (AST01-AST03).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny all write operations to repository instruction files, memory logs, and agent configs (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.2. Agent Coordinator (`agent-coordinator`)

#### Role Metadata & Baseline Status
- **Official Title:** Agent Coordinator | **Canonical Slug:** `agent-coordinator`
- **Common Aliases in INDEX.md:** `@coordinator`, `@swarm-coordinator`
- **Mission:** Control the full lifecycle of a bug or feature by coordinating the right specialist roles, enforcing quality gates, and driving work to validated handoff.
- **Level:** Principal / master-level delivery orchestration
- **File Metrics:** 453 lines / 37.0 KB | **Last Updated:** `2026-10-21`
- **Principal Expectations:** 11 items
- **Skill Toolbox:** Primary (13): `agent-a2a-protocol`, `agent-delegation`, `agent-graph-orchestration`, `agent-tool-orchestration`, `agent-context-management`, `agent-quality-gate`, `agent-handoff`, `agent-panel-meeting`, `agent-memory-compaction`, `agent-model-routing`, `agent-observability`, `agent-prompt-lifecycle`, `agent-semantic-memory` | Supporting (8): `navigate-service`, `troubleshoot-service`, `review-code`, `review-service`, `write-documentation`, `incident-report`, `context-optimization`, `memory-hygiene`
- **Contract Schema Coverage:** Emits: `a2a-task.json`, `a2a-task-status.json`, `a2a-task-progress.json`, `a2a-artifact.json`, `coordination-plan.json`, `feature-ticket.json`, `solution-brief.json`, `architecture-options.json`, `adr-spec.json`, `api-contract-spec.json`, `technical-delivery-plan.json`, `implementation-result.json`, `test-report.json`, `code-review-finding.json`, `deployment-plan.json`, `incident-report.json`, `security-audit.json`, `documentation-handoff.json` | Disclaims: Does not author specialized implementation code or internal module unit tests directly.
- **Guardrail Locks:** 16 named locks in file
- **Security Coverage:** ASI: Deep integration (8 explicit mentions across ASI01, ASI02, ASI03, ASI07, ASI08, ASI09, ASI10) | AST: 0 explicit references (relies entirely on role-standard.md inheritance)
- **Checklist Architecture:** 39 plain bullets across 5 phases; references references/agent-coordinator-review-checklist.md | Companion File: `references/agent-coordinator-review-checklist.md` (165 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Steer-or-Kill Action Classification framework dividing actions into Routine (autonomous), Risky (two-role consensus), and Irreversible (strict human confirmation).**: Steer-or-Kill Action Classification framework dividing actions into Routine (autonomous), Risky (two-role consensus), and Irreversible (strict human confirmation).
- **A2A 1.0 JSON-RPC task lifecycle orchestration and Server-Sent Events (SSE) progress streaming using Google RPC status envelopes.**: A2A 1.0 JSON-RPC task lifecycle orchestration and Server-Sent Events (SSE) progress streaming using Google RPC status envelopes.
- **Context window preservation via 60/80 compaction triggers, Head-Tail Tool Output Truncation (TOC), and attention allocation (15% primacy, 15% recency).**: Context window preservation via 60/80 compaction triggers, Head-Tail Tool Output Truncation (TOC), and attention allocation (15% primacy, 15% recency).
- **Non-Human Identity (NHI) lifecycle governance with ephemeral scoped credentials and execution-time authorization.**: Non-Human Identity (NHI) lifecycle governance with ephemeral scoped credentials and execution-time authorization.
- **EU AI Act Article 50 transparency disclosure gate ensuring automated origin tracking across multi-agent handoffs.**: EU AI Act Article 50 transparency disclosure gate ensuring automated origin tracking across multi-agent handoffs.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Agent Coordinator (must be declined or routed via Role Handoff):
- Direct feature implementation code authoring (must delegate to Specialist Developers: Backend, Frontend, Game, Mobile).
- `create-migration`: Database DDL authoring must be delegated to Backend Developer or Data Engineer.
- `write-article`: Public long-form content authoring must be delegated to Content Writer.
- `manage-vietnam-legal`: Legal contract vetting must be delegated to Vietnam Legal Counsel.
- `manage-vietnam-accounting`: Journal entry auditing must be delegated to Vietnam Accounting Specialist.
```

##### Architectural Guardrail Locks to Codify:
- **DELEGATION-AST10-GATE LOCK**: Enforce AST01-AST10 pre-flight validation on all delegated skills before assigning tasks to worker agents; reject skills with unverifiable provenance or lethal trifecta risk.
- **IDENTITY-FILE-PROTECTION LOCK**: Enforce strict deny-write access on AGENTS.md, MEMORY.md, and system prompt definitions during multi-agent task execution.

#### Formatting Normalizations:
- Convert all 39 Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.3. Agent Discovery Engineer (`agent-discovery-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** Agent Discovery Engineer | **Canonical Slug:** `agent-discovery-engineer`
- **Common Aliases in INDEX.md:** `@discovery`, `@agent-discovery`
- **Mission:** Own integration, architecture, and maintenance of Agent Discovery protocols, machine registries, and well-known discovery endpoints across modern agentic webs.
- **Level:** Principal / Master-level Agent Protocol Engineering
- **File Metrics:** 243 lines / 16.6 KB | **Last Updated:** `2026-10-17`
- **Principal Expectations:** 6 items
- **Skill Toolbox:** Primary (8): `manage-auth-md`, `configure-oauth-metadata`, `debug-identity-provider`, `configure-mcp`, `configure-agent-headers`, `manage-api-catalog`, `configure-agent-skills`, `manage-agent-identity` | Supporting (4): `security-audit`, `manage-secrets`, `write-documentation`, `navigate-service`
- **Contract Schema Coverage:** Emits: `coordination-plan.json`, `edge-deployment-spec.json`, `security-audit.json` | Disclaims: Does not author application business logic or frontend user interfaces.
- **Guardrail Locks:** 19 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 11 [ ] checkboxes; references references/agent-discovery-engineer-review-checklist.md | Companion File: `references/agent-discovery-engineer-review-checklist.md` (125 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **RFC 9727 API Catalog (`/.well-known/api-catalog`) authoring and machine registry publication for automated tool discovery.**: RFC 9727 API Catalog (`/.well-known/api-catalog`) authoring and machine registry publication for automated tool discovery.
- **Authentication manifest management via `/auth.md` complying with WorkOS and isitagentready.com agentic onboarding standards.**: Authentication manifest management via `/auth.md` complying with WorkOS and isitagentready.com agentic onboarding standards.
- **OAuth 2.0 Protected Resource Metadata (RFC 8414 / draft-ietf-oauth-resource-metadata) configuration and verification.**: OAuth 2.0 Protected Resource Metadata (RFC 8414 / draft-ietf-oauth-resource-metadata) configuration and verification.
- **Agent Skills index generation at `/.well-known/agent-skills/index.json` with structured capability routing.**: Agent Skills index generation at `/.well-known/agent-skills/index.json` with structured capability routing.
- **Cryptographic signature validation over JSON Web Signatures (JWS) and SPIFFE/SVID workload identity federation.**: Cryptographic signature validation over JSON Web Signatures (JWS) and SPIFFE/SVID workload identity federation.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Agent Discovery Engineer (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Application endpoint handler logic belongs to Backend Developer.
- `add-ui-component`: Frontend DOM rendering belongs to Frontend Developer.
- `deploy-vllm-inference`: LLM runtime deployment belongs to AI Systems Engineer.
- `draft-legal-opinion`: Statutory legal counsel belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **SKILL-MANIFEST-AST04 LOCK**: Validate all skill discovery manifests against schema definitions; reject manifests with malformed tool signatures, excessive scopes, or missing publisher proofs.
- **IDENTITY-FILE-PROTECTION LOCK**: Protect discovery configuration roots and registry endpoints from unauthenticated mutations (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.

---

### 4.4. AI Systems Engineer (`ai-systems-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** AI Systems Engineer | **Canonical Slug:** `ai-systems-engineer`
- **Common Aliases in INDEX.md:** `@ai`, `@ml`, `@llm`
- **Mission:** Architect, deploy, evaluate, and optimize production-grade AI and LLM systems — bridging ML models with reliable distributed backend platforms.
- **Level:** Principal / Master-level AI Systems Engineering
- **File Metrics:** 379 lines / 40.2 KB | **Last Updated:** `2026-10-25`
- **Principal Expectations:** 14 items
- **Skill Toolbox:** Primary (6): `deploy-vllm-inference`, `openrouter-task`, `setup-llm-gateway`, `implement-structured-outputs`, `setup-gpu-finops`, `prompt-injection-defense` | Supporting (11): `add-telemetry-instrumentation`, `context-optimization`, `memory-hygiene`, `agent-evaluation`, `performance-profiling`, `security-audit`, `troubleshoot-service`, `debug-runtime-platform`, `setup-deployment`, `navigate-service`, `write-documentation`
- **Contract Schema Coverage:** Emits: `ai-risk-register.json`, `architecture-options.json`, `deployment-plan.json`, `performance-audit.json`, `security-audit.json`, `system-design-spec.json`, `test-report.json` | Disclaims: Does not author general application UI components or legal compliance opinions.
- **Guardrail Locks:** 20 named locks in file
- **Security Coverage:** ASI: Deep integration (10 explicit mentions across ASI01, ASI02, ASI04, ASI05, ASI06) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 10 [ ] checkboxes; references references/ai-systems-engineer-review-checklist.md | Companion File: `references/ai-systems-engineer-review-checklist.md` (159 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **vLLM v1 distributed inference architecture utilizing PagedAttention v3, dynamic chunked prefill, and prefix caching.**: vLLM v1 distributed inference architecture utilizing PagedAttention v3, dynamic chunked prefill, and prefix caching.
- **GPU resource governance across NVIDIA MIG slicing and Kubernetes 1.31 Dynamic Resource Allocation (DRA).**: GPU resource governance across NVIDIA MIG slicing and Kubernetes 1.31 Dynamic Resource Allocation (DRA).
- **Strict JSON Schema Draft 2020-12 constrained decoding eliminating regex-based output parsing in backend services.**: Strict JSON Schema Draft 2020-12 constrained decoding eliminating regex-based output parsing in backend services.
- **Hardware-level GPU FinOps tracking via NVIDIA DCGM metrics and Kubecost accelerator attribution.**: Hardware-level GPU FinOps tracking via NVIDIA DCGM metrics and Kubecost accelerator attribution.
- **Prompt injection defense isolating untrusted inputs via bounded tool execution and structural delimiter isolation.**: Prompt injection defense isolating untrusted inputs via bounded tool execution and structural delimiter isolation.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by AI Systems Engineer (must be declined or routed via Role Handoff):
- `add-ui-component`: Web and mobile user interface presentation belongs to Frontend Developer.
- `write-copy`: Public marketing copy and blog prose belong to Content Writer.
- `manage-vietnam-accounting`: Dual-regime accounting entries belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **SKILL-EVALUATION-AST08 LOCK**: Verify all model evaluation harnesses and synthetic benchmark datasets against AST08 scanning standards before executing production model qualification.
- **IDENTITY-FILE-PROTECTION LOCK**: Block model weights and inference runtimes from writing directly to system prompt configurations (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.

---

### 4.5. AWS Engineer (`aws-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** AWS Engineer | **Canonical Slug:** `aws-engineer`
- **Common Aliases in INDEX.md:** `@aws`, `@cloud`
- **Mission:** Provision, configure, optimize, and govern production AWS cloud infrastructure via OpenTofu state KMS encryption, Crossplane Go compositions, Bottlerocket distroless EKS nodes, and IAM Zero-Trust.
- **Level:** Principal / Master-level Cloud Infrastructure Engineering
- **File Metrics:** 343 lines / 40.5 KB | **Last Updated:** `2026-10-25`
- **Principal Expectations:** 14 items
- **Skill Toolbox:** Primary (3): `aws-infrastructure`, `setup-deployment`, `add-telemetry-instrumentation` | Supporting (9): `debug-runtime-platform`, `troubleshoot-service`, `performance-profiling`, `orchestrate-chaos-experiment`, `security-audit`, `manage-secrets`, `deploy-aws-eks-workloads`, `setup-gpu-finops`, `database-maintenance`
- **Contract Schema Coverage:** Emits: `architecture-options.json`, `aws-infra-spec.json`, `deployment-plan.json`, `performance-audit.json`, `security-audit.json`, `system-design-spec.json` | Disclaims: Does not author application business services, frontend code, or product roadmaps.
- **Guardrail Locks:** 22 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 15 [ ] checkboxes; references references/aws-engineer-review-checklist.md | Companion File: `references/aws-engineer-review-checklist.md` (182 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **OpenTofu infrastructure provisioning with client-side KMS state encryption and strict drift detection.**: OpenTofu infrastructure provisioning with client-side KMS state encryption and strict drift detection.
- **Crossplane Go composable architecture abstracting cloud resources into uniform Kubernetes API primitives.**: Crossplane Go composable architecture abstracting cloud resources into uniform Kubernetes API primitives.
- **Amazon EKS deployment on Bottlerocket distroless nodes with Karpenter v1.0 declarative NodePool management.**: Amazon EKS deployment on Bottlerocket distroless nodes with Karpenter v1.0 declarative NodePool management.
- **AWS VPC Lattice Gateway API routes providing zero-trust service-to-service networking.**: AWS VPC Lattice Gateway API routes providing zero-trust service-to-service networking.
- **AWS ADOT (AWS Distro for OpenTelemetry) telemetry pipelines and ECR image container provenance verification.**: AWS ADOT (AWS Distro for OpenTelemetry) telemetry pipelines and ECR image container provenance verification.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by AWS Engineer (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Application endpoint handler logic belongs to Backend Developer.
- `add-ui-component`: User interface component development belongs to Frontend Developer.
- `define-product-strategy`: Business product prioritization belongs to Product Manager.
- `manage-vietnam-legal`: Legal contract vetting belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **INFRA-SKILL-SUPPLY-CHAIN-AST02 LOCK**: Prohibit third-party cloud orchestration skills lacking pinned cryptographic checksums or pulling unvetted Terraform/OpenTofu provider modules.
- **IDENTITY-FILE-PROTECTION LOCK**: Deny IAM roles and cloud agents write privileges over local agent definitions and security rulebooks (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.

---

### 4.6. Backend Developer (`backend-developer`)

#### Role Metadata & Baseline Status
- **Official Title:** Backend Developer | **Canonical Slug:** `backend-developer`
- **Common Aliases in INDEX.md:** `@backend`, `@be`, `@backend-dev`
- **Mission:** Design, implement, test, and maintain robust, high-performance, and secure server-side services and APIs.
- **Level:** Principal / Master-level Backend Engineering
- **File Metrics:** 470 lines / 40.3 KB | **Last Updated:** `2026-10-25`
- **Principal Expectations:** 17 items
- **Skill Toolbox:** Primary (12): `add-api-endpoint`, `add-event-handler`, `add-service-client`, `scaffold-new-service`, `implement-auth`, `optimize-postgres`, `build-mcp-server`, `implement-structured-outputs`, `write-tests`, `systematic-debugging`, `commit-code`, `navigate-service` | Supporting (8): `create-migration`, `manage-secrets`, `troubleshoot-service`, `performance-profiling`, `security-audit`, `write-documentation`, `handle-checkout-flow`, `integrate-payment-gateway`
- **Contract Schema Coverage:** Emits: `adr-spec.json`, `api-contract-spec.json`, `data-migration-plan.json`, `feature-ticket.json`, `implementation-result.json`, `mcp-server-spec.json`, `test-report.json`, `validation-result.json` | Disclaims: Does not author frontend presentation templates, CSS styling, or UI wireframes.
- **Guardrail Locks:** 21 named locks in file
- **Security Coverage:** ASI: Deep integration (8 explicit mentions across ASI01, ASI02, ASI03, ASI05, ASI07) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 13 [ ] checkboxes; references references/backend-developer-review-checklist.md | Companion File: `references/backend-developer-review-checklist.md` (105 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Hexagonal Clean Architecture isolating domain core from framework and transport adapters across Go 1.25+ and Python 3.13+.**: Hexagonal Clean Architecture isolating domain core from framework and transport adapters across Go 1.25+ and Python 3.13+.
- **PostgreSQL performance optimization with Row-Level Security (RLS) and connection pooling invariants.**: PostgreSQL performance optimization with Row-Level Security (RLS) and connection pooling invariants.
- **Transactional outbox pattern combined with Debezium CDC and idempotent consumer processing.**: Transactional outbox pattern combined with Debezium CDC and idempotent consumer processing.
- **Redis 7.4 concurrency fencing tokens preventing distributed race conditions.**: Redis 7.4 concurrency fencing tokens preventing distributed race conditions.
- **MCP server construction following stateless JSON-RPC contracts with strict boundary schema validation.**: MCP server construction following stateless JSON-RPC contracts with strict boundary schema validation.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Backend Developer (must be declined or routed via Role Handoff):
- `add-ui-component`: Browser DOM and mobile UI presentation belongs to Frontend Developer.
- `design-ux-flow`: Wireframing and user experience flows belong to UI/UX Designer.
- `deploy-aws-eks-workloads`: Cloud cluster orchestration belongs to DevOps / AWS Engineer.
- `draft-legal-opinion`: Formal legal advice belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **MCP-SKILL-AST03 LOCK**: Prohibit backend execution of third-party MCP skills exhibiting over-privileged access or the lethal trifecta (AST03).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny backend API endpoints and automated services write access to AGENTS.md and MEMORY.md files (AST10).

---

### 4.7. Business Analyst (`business-analyst`)

#### Role Metadata & Baseline Status
- **Official Title:** Business Analyst | **Canonical Slug:** `business-analyst`
- **Common Aliases in INDEX.md:** `@ba`, `@business`
- **Mission:** Discover, elicit, analyze, and structure business requirements into implementation-ready specifications with unambiguous acceptance criteria and preserved business behavior.
- **Level:** Principal / Master-level Business Analysis
- **File Metrics:** 402 lines / 35.9 KB | **Last Updated:** `2026-10-15`
- **Principal Expectations:** 13 items
- **Skill Toolbox:** Primary (6): `analyze-business-requirements`, `elicit-requirements`, `write-use-cases`, `trace-requirements-impact`, `build-story-map`, `write-product-brief` | Supporting (6): `design-ux-flow`, `plan-technical-delivery`, `model-saas-metrics`, `write-documentation`, `audit-ai-compliance`, `agent-evaluation`
- **Contract Schema Coverage:** Emits: `feature-ticket.json` | Disclaims: Does not author production application code, database migrations, or infrastructure manifests.
- **Guardrail Locks:** 20 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 12 [ ] checkboxes; references references/business-analyst-review-checklist.md | Companion File: `references/business-analyst-review-checklist.md` (228 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **BABOK v3 requirement elicitation using Funnel Questioning (Open, Probing, Closed) and the Colombo method.**: BABOK v3 requirement elicitation using Funnel Questioning (Open, Probing, Closed) and the Colombo method.
- **Event Storming domain event discovery and vertical slicing using Elephant Carpentry (5 decomposition techniques).**: Event Storming domain event discovery and vertical slicing using Elephant Carpentry (5 decomposition techniques).
- **Karl Wiegers 13-field Use Case specification and Alistair Cockburn goal-level categorization.**: Karl Wiegers 13-field Use Case specification and Alistair Cockburn goal-level categorization.
- **BDD Gherkin specification with testable business invariants and edge cases.**: BDD Gherkin specification with testable business invariants and edge cases.
- **AI feature governance ensuring compliance with EU AI Act Article 50 transparency and human agency oversight.**: AI feature governance ensuring compliance with EU AI Act Article 50 transparency and human agency oversight.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C9: Emitted contract schemas limited to 1 schema (`feature-ticket.json`); should formally codify `business-requirements-spec.json`.

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Business Analyst (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Server-side endpoint implementation belongs to Backend Developer.
- `setup-deployment`: CI/CD delivery pipeline configuration belongs to DevOps Engineer.
- `manage-vietnam-accounting`: Live journal posting belongs to Vietnam Accounting Specialist.
- `manage-vietnam-legal`: Legal contract dispute representation belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **REQUIREMENT-PROVENANCE-AST09 LOCK**: Maintain immutable audit logs tracking requirement origins, stakeholder rationale, and risk tier classification under AST09 governance.
- **IDENTITY-FILE-PROTECTION LOCK**: Protect system core rules and role definition files from unauthorized requirements drift (AST10).

---

### 4.8. Cloudflare Engineer (`cloudflare-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** Cloudflare Engineer | **Canonical Slug:** `cloudflare-engineer`
- **Common Aliases in INDEX.md:** `@cloudflare`, `@cf`, `@workers`
- **Mission:** Architect, deploy, optimize, and maintain edge compute, storage, security, and networking on the Cloudflare Developer Platform.
- **Level:** Principal / Master-level Edge Cloud Engineering
- **File Metrics:** 298 lines / 19.0 KB | **Last Updated:** `2026-10-19`
- **Principal Expectations:** 6 items
- **Skill Toolbox:** Primary (14): `wrangler`, `durable-objects`, `agents-sdk`, `cloudflare-email-service`, `debug-workers-edge`, `workers-best-practices`, `develop-b2b-catalog-feature`, `develop-b2b-golf-feature`, `turnstile-spin`, `setup-llm-gateway`, `configure-mcp`, `configure-agent-headers`, `manage-auth-md`, `manage-api-catalog` | Supporting (8): `setup-deployment`, `debug-runtime-platform`, `troubleshoot-service`, `manage-secrets`, `security-audit`, `write-documentation`, `commit-code`, `navigate-service`
- **Contract Schema Coverage:** Emits: `coordination-plan.json`, `deployment-plan.json`, `edge-deployment-spec.json`, `mcp-server-spec.json`, `performance-audit.json`, `security-audit.json` | Disclaims: Does not author relational database migrations on AWS RDS or write native mobile apps.
- **Guardrail Locks:** 12 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 12 plain bullets; references references/cloudflare-engineer-review-checklist.md | Companion File: `references/cloudflare-engineer-review-checklist.md` (152 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Cloudflare Workers & Pages deployment using Wrangler CLI with pinned compatibility date (`2026-09-23`).**: Cloudflare Workers & Pages deployment using Wrangler CLI with pinned compatibility date (`2026-09-23`).
- **Durable Objects with SQLite storage backend for strongly-consistent distributed state machines.**: Durable Objects with SQLite storage backend for strongly-consistent distributed state machines.
- **Cloudflare Agents SDK orchestration running stateful AI agents on edge workers.**: Cloudflare Agents SDK orchestration running stateful AI agents on edge workers.
- **Cloudflare Turnstile CAPTCHA bot protection with server-side siteverify validation workers.**: Cloudflare Turnstile CAPTCHA bot protection with server-side siteverify validation workers.
- **Workers AI, Vectorize vector database, and Hyperdrive connection pooling integration.**: Workers AI, Vectorize vector database, and Hyperdrive connection pooling integration.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Cloudflare Engineer (must be declined or routed via Role Handoff):
- `aws-infrastructure`: AWS VPC and EKS infrastructure belongs to AWS Engineer.
- `develop-mobile-app`: Native iOS and Android app code belongs to Mobile Engineer.
- `draft-legal-opinion`: Statutory legal opinions belong to Vietnam Legal Counsel.
- `manage-vietnam-accounting`: Financial accounting entries belong to Vietnam Accounting Specialist.
```

##### Architectural Guardrail Locks to Codify:
- **WORKER-SKILL-SANDBOX-AST06 LOCK**: Enforce hermetic isolation on all external edge worker skills; prohibit ambient network egress without declared binding allowlists (AST06).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny edge workers write access to core agent personality and memory configuration files (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.9. Content Manager (`content-manager`)

#### Role Metadata & Baseline Status
- **Official Title:** Content Manager | **Canonical Slug:** `content-manager`
- **Common Aliases in INDEX.md:** `@content-mgr`, `@content-lead`
- **Mission:** Direct and govern content strategy, editorial pipelines, publication standards, and content lifecycle performance.
- **Level:** Principal / Master-level Content Strategy and Editorial Governance
- **File Metrics:** 336 lines / 30.1 KB | **Last Updated:** `2026-10-25`
- **Principal Expectations:** 11 items
- **Skill Toolbox:** Primary (2): `design-content-strategy`, `audit-content` | Supporting (12): `write-article`, `write-copy`, `repurpose-content`, `optimize-seo`, `audit-technical-seo`, `write-tech-radar`, `write-product-brief`, `meeting-review`, `write-documentation`, `audit-technical-article`, `write-hvac-authority-content`, `generate-mmo-content`
- **Contract Schema Coverage:** Emits: `content-audit-report.json`, `editorial-calendar.json`, `seo-content-brief.json` | Disclaims: Does not author production backend application code, infrastructure scripts, or security policies.
- **Guardrail Locks:** 18 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 11 [ ] checkboxes; references references/content-manager-review-checklist.md | Companion File: `references/content-manager-review-checklist.md` (74 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Pillar-cluster topology design establishing topical authority and inter-article hierarchy.**: Pillar-cluster topology design establishing topical authority and inter-article hierarchy.
- **SERP Information Gain scoring auditing articles against top 10 SERP competitors to ensure unique value.**: SERP Information Gain scoring auditing articles against top 10 SERP competitors to ensure unique value.
- **C2PA digital content provenance validation and strict AI disclosure standards.**: C2PA digital content provenance validation and strict AI disclosure standards.
- **Content decay velocity SLAs and automated 90-day content refresh cadences.**: Content decay velocity SLAs and automated 90-day content refresh cadences.
- **Editorial quality gate enforcing authoritativeness, brand voice consistency, and technical accuracy.**: Editorial quality gate enforcing authoritativeness, brand voice consistency, and technical accuracy.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Content Manager (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Application backend development belongs to Backend Developer.
- `setup-deployment`: Cloud hosting and CI/CD pipelines belong to DevOps Engineer.
- `security-audit`: Formal application penetration testing belongs to Security Engineer.
- `manage-vietnam-legal`: Legal contract analysis belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **CONTENT-SKILL-PROVENANCE-AST01 LOCK**: Block third-party content scraping or synthesis skills with untrusted provenance or missing publisher identities (AST01).
- **IDENTITY-FILE-PROTECTION LOCK**: Protect editorial style guides and agent prompt rules from unverified content tool mutations (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.

---

### 4.10. Content Writer (`content-writer`)

#### Role Metadata & Baseline Status
- **Official Title:** Content Writer | **Canonical Slug:** `content-writer`
- **Common Aliases in INDEX.md:** `@writer`, `@copywriter`, `@author`, `@article-writer`, `@blog-writer`
- **Mission:** Author authoritative, technical, and persuasive content that satisfies user intent, technical accuracy, and domain depth across engineering blogs and product publications.
- **Level:** Principal / Master-level Technical Authoring and Copywriting
- **File Metrics:** 399 lines / 32.4 KB | **Last Updated:** `2026-10-19`
- **Principal Expectations:** 13 items
- **Skill Toolbox:** Primary (4): `write-article`, `write-copy`, `repurpose-content`, `audit-technical-article` | Supporting (9): `conduct-research`, `optimize-seo`, `write-documentation`, `write-tech-radar`, `write-hugo-twin-content`, `write-hvac-authority-content`, `write-real-estate-astro-data`, `docx`, `pptx`
- **Contract Schema Coverage:** Emits: `content-brief.json`, `editorial-article.json`, `marketing-copy.json` | Disclaims: Does not author production backend application code, server configs, or legal opinions.
- **Guardrail Locks:** 15 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 29 plain bullets across 7 gates; references references/content-writer-review-checklist.md | Companion File: `references/content-writer-review-checklist.md` (58 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **2027 SOTA 7-Gate Quality Compliance**:  Answer-First blockquote (48-62 words), Prerequisite callout block, depth > 20.5KB / >= 2,500 words.
- **Visual excellence enforcing >= 2 valid Mermaid diagrams (flowchart, sequenceDiagram, stateDiagram-v2).**: Visual excellence enforcing >= 2 valid Mermaid diagrams (flowchart, sequenceDiagram, stateDiagram-v2).
- **Structured FAQ Page Schema.org JSON-LD generation (3-4 valid questions/answers).**: Structured FAQ Page Schema.org JSON-LD generation (3-4 valid questions/answers).
- **Production-grade code realism (Go 1.25+, Redis 7.4, MySQL 8.4) with zero placeholder markers.**: Production-grade code realism (Go 1.25+, Redis 7.4, MySQL 8.4) with zero placeholder markers.
- **Twin repository parity between vesviet (English) and learn (Vietnamese) with strict one-way authority linking.**: Twin repository parity between vesviet (English) and learn (Vietnamese) with strict one-way authority linking.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Content Writer (must be declined or routed via Role Handoff):
- `scaffold-new-service`: Microservice scaffolding belongs to Backend Developer.
- `aws-infrastructure`: Cloud infrastructure provisioning belongs to AWS Engineer.
- `manage-vietnam-accounting`: Tax return filing belongs to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Legal advice belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **PROSE-SKILL-INJECTION-AST05 LOCK**: Block external text transformation skills that inject unverified remote instructions or AI watermarking patterns into authored prose (AST05).
- **IDENTITY-FILE-PROTECTION LOCK**: Protect editorial guidelines and persona prompts from external formatting skill overwrites (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.11. Data Analyst (`data-analyst`)

#### Role Metadata & Baseline Status
- **Official Title:** Data Analyst | **Canonical Slug:** `data-analyst`
- **Common Aliases in INDEX.md:** `@da`, `@data-analytics`
- **Mission:** Extract actionable, trustworthy insights from data to guide strategic, product, operational, and financial decisions.
- **Level:** Principal / Master-level Data Analytics and Decision Science
- **File Metrics:** 421 lines / 36.8 KB | **Last Updated:** `2026-10-19`
- **Principal Expectations:** 18 items
- **Skill Toolbox:** Primary (3): `analyze-data`, `query-analytical-engine`, `xlsx` | Supporting (7): `build-credit-scorecard`, `model-saas-metrics`, `optimize-olap-database`, `write-documentation`, `navigate-service`, `database-maintenance`, `commit-code`
- **Contract Schema Coverage:** Emits: `analytical-query-result.json`, `credit-risk-scorecard.json`, `data-analysis-report.json`, `saas-unit-economics.json` | Disclaims: Does not build production data pipelines, lakehouse ingestion jobs, or write application features.
- **Guardrail Locks:** 18 named locks in file
- **Security Coverage:** ASI: Moderate integration (3 explicit mentions of ASI02, ASI06) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 11 [ ] checkboxes; references references/data-analyst-review-checklist.md | Companion File: `references/data-analyst-review-checklist.md` (76 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **DuckDB sandboxed analytics processing local analytical queries with strict CPU and RAM execution bounds.**: DuckDB sandboxed analytics processing local analytical queries with strict CPU and RAM execution bounds.
- **SQL anti-hallucination verification checking table existence, schema types, and query plans before execution.**: SQL anti-hallucination verification checking table existence, schema types, and query plans before execution.
- **Sample Ratio Mismatch (SRM) checks and Causal DAG verification distinguishing correlation from causation.**: Sample Ratio Mismatch (SRM) checks and Causal DAG verification distinguishing correlation from causation.
- **Zero Formula Error invariant in Excel/xlsx models enforced via recalculation engines (`recalc.py`).**: Zero Formula Error invariant in Excel/xlsx models enforced via recalculation engines (`recalc.py`).
- **Credit risk scorecard construction**:  monotonic WOE binning, IV evaluation, PDO point calibration, and PSI drift tracking.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Data Analyst (must be declined or routed via Role Handoff):
- `build-data-pipeline`: Production ETL pipeline engineering belongs to Data Engineer.
- `create-migration`: Relational database DDL migrations belong to Backend Developer.
- `setup-deployment`: Cloud deployment pipelines belong to DevOps Engineer.
- `draft-legal-opinion`: Formal legal regulatory opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **ANALYTICS-SKILL-DATA-PRIVACY-AST03 LOCK**: Forbid analytical skills from exfiltrating sensitive tabular data or PII to external analytical endpoints (AST03).
- **IDENTITY-FILE-PROTECTION LOCK**: Protect local analytical models and data dictionary rules from analytical skill overwrites (AST10).

---

### 4.12. Data Engineer (`data-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** Data Engineer | **Canonical Slug:** `data-engineer`
- **Common Aliases in INDEX.md:** `@de`, `@data-eng`
- **Mission:** Design, build, scale, and maintain robust data pipelines, modern lakehouse architectures, and analytical stores.
- **Level:** Principal / Master-level Data Platform Engineering
- **File Metrics:** 442 lines / 45.8 KB | **Last Updated:** `2026-10-25`
- **Principal Expectations:** 15 items
- **Skill Toolbox:** Primary (4): `build-data-pipeline`, `database-maintenance`, `create-migration`, `optimize-postgres` | Supporting (10): `optimize-olap-database`, `performance-profiling`, `setup-deployment`, `security-audit`, `troubleshoot-service`, `debug-runtime-platform`, `manage-secrets`, `write-documentation`, `commit-code`, `navigate-service`
- **Contract Schema Coverage:** Emits: `architecture-options.json`, `data-migration-plan.json`, `data-pipeline-spec.json`, `performance-audit.json`, `system-design-spec.json` | Disclaims: Does not build user-facing frontend applications, author marketing copy, or provide legal advice.
- **Guardrail Locks:** 15 named locks in file
- **Security Coverage:** ASI: Deep integration (11 explicit mentions across ASI01, ASI02, ASI03, ASI04, ASI05, ASI06) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 14 [ ] checkboxes; references references/data-engineer-review-checklist.md | Companion File: `references/data-engineer-review-checklist.md` (85 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Modern open table lakehouse architectures utilizing Apache Iceberg REST Catalog and Delta Lake 3.0+ liquid clustering.**: Modern open table lakehouse architectures utilizing Apache Iceberg REST Catalog and Delta Lake 3.0+ liquid clustering.
- **Lakehouse maintenance procedures**:  256MB bin-pack compaction merging Deletion Vectors, manifest rewriting, 7-day/50-snapshot expiration, 72h orphan vacuuming.
- **DuckDB and Polars embedded OLAP engines delivering low-latency processing without JVM overhead.**: DuckDB and Polars embedded OLAP engines delivering low-latency processing without JVM overhead.
- **Write-Audit-Publish (WAP) pattern guaranteeing pipeline idempotency and atomic stage publication.**: Write-Audit-Publish (WAP) pattern guaranteeing pipeline idempotency and atomic stage publication.
- **PostgreSQL performance tuning, connection pooling with PgBouncer, and zero-downtime schema migrations.**: PostgreSQL performance tuning, connection pooling with PgBouncer, and zero-downtime schema migrations.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Data Engineer (must be declined or routed via Role Handoff):
- `add-ui-component`: Web and mobile user interfaces belong to Frontend Developer.
- `define-product-strategy`: Product vision and strategic roadmapping belong to Product Manager.
- `manage-vietnam-accounting`: Live journal and balance sheet reconciliations belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal statutory legal counsel belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **LAKEHOUSE-SKILL-SUPPLY-CHAIN-AST02 LOCK**: Require pinned SHA-256 hashes on all data connector plugins, PySpark packages, and lakehouse catalog libraries (AST02).
- **IDENTITY-FILE-PROTECTION LOCK**: Block data ingestion pipelines and database maintenance tools from writing to repository control files (AST10).

---

### 4.13. DevOps Engineer (`devops-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** DevOps Engineer | **Canonical Slug:** `devops-engineer`
- **Common Aliases in INDEX.md:** `@devops`, `@infra`, `@infrastructure`
- **Mission:** Own CI/CD delivery pipelines, deployment automation, container orchestration, and cloud infrastructure operations.
- **Level:** Principal / Master-level DevOps & Platform Engineering
- **File Metrics:** 614 lines / 70.4 KB | **Last Updated:** `2026-10-05`
- **Principal Expectations:** 17 items
- **Skill Toolbox:** Primary (8): `setup-deployment`, `deploy-aws-eks-workloads`, `debug-runtime-platform`, `troubleshoot-service`, `performance-profiling`, `orchestrate-chaos-experiment`, `commit-code`, `navigate-service` | Supporting (9): `aws-infrastructure`, `setup-gpu-finops`, `database-maintenance`, `security-audit`, `manage-secrets`, `supply-chain-security`, `add-telemetry-instrumentation`, `deploy-proxyware-fleet`, `write-documentation`
- **Contract Schema Coverage:** Emits: `aws-infra-spec.json`, `deployment-plan.json`, `edge-deployment-spec.json`, `system-design-spec.json` | Disclaims: Does not author application business domain logic, UI components, or sales copy.
- **Guardrail Locks:** 24 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 45 plain bullets; references references/devops-engineer-review-checklist.md | Companion File: `references/devops-engineer-review-checklist.md` (195 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **GitOps delivery pipelines driven by ArgoCD Server-Side Apply (SSA) and Argo Rollouts progressive canary releases.**: GitOps delivery pipelines driven by ArgoCD Server-Side Apply (SSA) and Argo Rollouts progressive canary releases.
- **Cilium eBPF sidecarless service mesh optimizing kernel networking (`sockops`) and Tetragon security enforcement.**: Cilium eBPF sidecarless service mesh optimizing kernel networking (`sockops`) and Tetragon security enforcement.
- **Internal Developer Platform (IDP) golden paths via Backstage and declarative infrastructure blueprints.**: Internal Developer Platform (IDP) golden paths via Backstage and declarative infrastructure blueprints.
- **AI and ML workload deployment via KubeRay, vLLM inference runners, and Kubernetes 1.31 Dynamic Resource Allocation (DRA).**: AI and ML workload deployment via KubeRay, vLLM inference runners, and Kubernetes 1.31 Dynamic Resource Allocation (DRA).
- **Software supply chain security enforcing SLSA Level 3+ provenance, Cosign container image signatures, and SBOM verification.**: Software supply chain security enforcing SLSA Level 3+ provenance, Cosign container image signatures, and SBOM verification.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by DevOps Engineer (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Application backend service implementations belong to Backend Developer.
- `add-ui-component`: Web and mobile user interfaces belong to Frontend Developer.
- `write-article`: Public marketing and blog content belongs to Content Writer.
- `manage-vietnam-accounting`: Corporate tax accounting belongs to Vietnam Accounting Specialist.
```

##### Architectural Guardrail Locks to Codify:
- **CI-CD-SKILL-SUPPLY-CHAIN-AST02 LOCK**: Prohibit CI/CD deployment skills pulling unpinned actions or executing unverified container images (AST02).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny CI/CD automation and cluster controllers write access to agent system prompts and security invariants (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.14. Ecommerce Engineer (`ecommerce-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** Ecommerce Engineer | **Canonical Slug:** `ecommerce-engineer`
- **Common Aliases in INDEX.md:** `@ecommerce`, `@ecom`
- **Mission:** Architect, develop, and maintain high-converting, resilient, and secure e-commerce systems — spanning product catalog, cart, checkout, payment gateway integrations, order fulfillment, and agentic commerce protocols.
- **Level:** Principal / Master-level E-commerce Platform Engineering
- **File Metrics:** 274 lines / 19.0 KB | **Last Updated:** `2026-10-17`
- **Principal Expectations:** 8 items
- **Skill Toolbox:** Primary (5): `integrate-payment-gateway`, `handle-checkout-flow`, `manage-product-catalog`, `manage-order-fulfillment`, `configure-agent-commerce` | Supporting (11): `add-api-endpoint`, `add-event-handler`, `implement-auth`, `optimize-postgres`, `develop-laravel-feature`, `develop-laravel-ecommerce-feature`, `write-tests`, `security-audit`, `write-documentation`, `commit-code`, `navigate-service`
- **Contract Schema Coverage:** Emits: `implementation-result.json` | Disclaims: Does not author AWS infrastructure templates or write general long-form marketing articles.
- **Guardrail Locks:** 21 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 9 plain bullets; references references/ecommerce-engineer-review-checklist.md | Companion File: `references/ecommerce-engineer-review-checklist.md` (129 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **High-throughput transactional patterns derived from Alipay 610k TPS and Shopee Traffic Shield architectures.**: High-throughput transactional patterns derived from Alipay 610k TPS and Shopee Traffic Shield architectures.
- **Inventory locking mechanisms using Redis Lua scripts with strict TTL reservations preventing overselling during flash sales.**: Inventory locking mechanisms using Redis Lua scripts with strict TTL reservations preventing overselling during flash sales.
- **Financial integrity invariants requiring balanced double-entry accounting entries (sum of Debits == sum of Credits) on all monetary operations.**: Financial integrity invariants requiring balanced double-entry accounting entries (sum of Debits == sum of Credits) on all monetary operations.
- **Agentic commerce protocols**:  Machine Payments Protocol (MPP), x402 payment HTTP status codes, and scoped mandate authorization.
- **PCI DSS 4.0.1 compliance strictly avoiding raw cardholder data handling via client-side tokenization.**: PCI DSS 4.0.1 compliance strictly avoiding raw cardholder data handling via client-side tokenization.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C9: Emitted contract schemas limited to 1 generic schema (`implementation-result.json`); should formally codify `order-fulfillment-spec.json` and `payment-audit.json`.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Ecommerce Engineer (must be declined or routed via Role Handoff):
- `deploy-aws-eks-workloads`: Cloud container orchestration belongs to AWS / DevOps Engineer.
- `debug-3d-scene`: 3D rendering pipeline debugging belongs to 3D Graphics Engineer.
- `draft-legal-opinion`: Statutory legal opinions belong to Vietnam Legal Counsel.
- `manage-vietnam-accounting`: Corporate financial reporting belongs to Vietnam Accounting Specialist.
```

##### Architectural Guardrail Locks to Codify:
- **COMMERCE-PAYMENT-SKILL-AST03 LOCK**: Prohibit third-party commerce or checkout skills possessing the lethal trifecta (handling transaction amounts + arbitrary API endpoints + external webhook egress) (AST03).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny payment gateway integration tools write access to core agent authorization files (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.15. Frontend Developer (`frontend-developer`)

#### Role Metadata & Baseline Status
- **Official Title:** Frontend Developer | **Canonical Slug:** `frontend-developer`
- **Common Aliases in INDEX.md:** `@frontend`, `@fe`, `@frontend-dev`, `@ui-developer`
- **Mission:** Build accessible, performant, resilient, and beautifully designed user interfaces across web platforms — owning client architecture, design systems, browser performance, and interaction state.
- **Level:** Principal / Master-level Frontend UI/UX Engineering
- **File Metrics:** 415 lines / 40.6 KB | **Last Updated:** `2026-10-20`
- **Principal Expectations:** 21 items
- **Skill Toolbox:** Primary (15): `accessibility-review`, `add-page-route`, `add-ui-component`, `component-composition`, `design-system-engineering`, `frontend-micro-polish`, `frontend-testing`, `hostile-component-stress-testing`, `implement-view-transitions`, `interactive-component-workbench`, `motion-performance-engineering`, `setup-design-system`, `setup-visual-regression`, `web-quality-audit`, `integrate-api-client` | Supporting (11): `write-tests`, `systematic-debugging`, `commit-code`, `navigate-service`, `debug-3d-scene`, `develop-obj-feature`, `develop-b2b-catalog-feature`, `develop-b2b-golf-feature`, `design-ux-flow`, `design-review`, `implement-webmcp`
- **Contract Schema Coverage:** Emits: `feature-ticket.json`, `implementation-result.json`, `performance-audit.json`, `test-report.json`, `ui-component-spec.json`, `ux-flow-spec.json`, `validation-result.json`, `visual-diff-report.json` | Disclaims: Does not author backend SQL migrations, server endpoint handlers, or infrastructure manifests.
- **Guardrail Locks:** 22 named locks in file
- **Security Coverage:** ASI: Deep integration (8 explicit mentions across ASI01, ASI02, ASI05, ASI07) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 10 [ ] checkboxes; references references/frontend-developer-review-checklist.md | Companion File: `references/frontend-developer-review-checklist.md` (122 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **React 19 Actions, Compiler, and Server Components combined with Next.js 15 App Router architecture.**: React 19 Actions, Compiler, and Server Components combined with Next.js 15 App Router architecture.
- **CSS View Transitions API delivering fluid route animations without degrading Core Web Vitals (Interaction to Next Paint INP < 100ms).**: CSS View Transitions API delivering fluid route animations without degrading Core Web Vitals (Interaction to Next Paint INP < 100ms).
- **WebMCP integration exposing structured client-side DOM actions and page context to AI agents.**: WebMCP integration exposing structured client-side DOM actions and page context to AI agents.
- **Compound component patterns, Radix-style `asChild` slot delegation, and headless hook separation eliminating boolean prop sprawl.**: Compound component patterns, Radix-style `asChild` slot delegation, and headless hook separation eliminating boolean prop sprawl.
- **Design system engineering enforcing WCAG 2.2 AA standards**:  APCA contrast tables, perceptual OKLCH color ramps, concentric border radii, and mobile zoom guards.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Frontend Developer (must be declined or routed via Role Handoff):
- `create-migration`: Relational database DDL migrations belong to Backend Developer.
- `deploy-aws-eks-workloads`: Kubernetes cluster deployments belong to AWS / DevOps Engineer.
- `manage-vietnam-accounting`: Corporate tax ledgers belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **FRONTEND-SKILL-SUPPLY-CHAIN-AST02 LOCK**: Forbid third-party UI component skills pulling unvetted npm dependencies or exhibiting supply chain injection vulnerabilities (AST02).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny client-side web tools and UI builders write access to repository root agent rules and system prompts (AST10).

---

### 4.16. Game Developer (`game-developer`)

#### Role Metadata & Baseline Status
- **Official Title:** Game Developer | **Canonical Slug:** `game-developer`
- **Common Aliases in INDEX.md:** `@game-dev`, `@gamedev`, `@game`, `@game-engineer`, `@gameplay-engineer`
- **Mission:** Architect, build, and optimize interactive real-time game systems, mechanics, and simulation loops across game engines — delivering deterministic, high-performance, and engaging gameplay experiences.
- **Level:** Principal / Master-level Game Systems Engineering
- **File Metrics:** 214 lines / 14.9 KB | **Last Updated:** `2026-10-13`
- **Principal Expectations:** 6 items
- **Skill Toolbox:** Primary (20): `integrate-game-engine`, `develop-gameplay-systems`, `architect-ecs-systems`, `author-game-ai`, `configure-physics-collision`, `design-procedural-generation`, `direct-camera-systems`, `implement-save-persistence`, `integrate-dialogue-narrative`, `manage-scene-lifecycle`, `mix-dynamic-game-audio`, `profile-game-performance`, `program-game-shaders`, `tune-game-feel`, `abstract-input-actions`, `automate-game-publishing`, `build-game-ui-ux`, `generate-game-assets-pipeline`, `inspect-blender-rigs-motion`, `isometric-svg-projection` | Supporting (6): `write-tests`, `systematic-debugging`, `commit-code`, `navigate-service`, `debug-3d-scene`, `optimize-3d-assets`
- **Contract Schema Coverage:** Emits: `game-ai-behavior-tree.json`, `game-audio-bus-architecture.json`, `game-camera-profile.json`, `game-dialogue-manifest.json`, `game-engine-integration-spec.json`, `game-physics-manifest.json`, `game-save-schema.json` | Disclaims: Does not author cloud backend microservices, enterprise tax filings, or legal opinions.
- **Guardrail Locks:** 9 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 8 [ ] checkboxes; references references/game-developer-review-checklist.md | Companion File: `references/game-developer-review-checklist.md` (115 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Non-Compliant (Missing Failure Modes, Lock Deficit < 12)**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Data-oriented Entity Component Systems (ECS) and cache-friendly archetype query architectures across Godot 4, Unity DOTS, Bevy, and Flecs.**: Data-oriented Entity Component Systems (ECS) and cache-friendly archetype query architectures across Godot 4, Unity DOTS, Bevy, and Flecs.
- **Deterministic fixed timestep physics simulation with Continuous Collision Detection (CCD) preventing fast-mover tunneling.**: Deterministic fixed timestep physics simulation with Continuous Collision Detection (CCD) preventing fast-mover tunneling.
- **Modular Game AI leveraging Behavior Trees, Utility AI response curves, and local steering behaviors.**: Modular Game AI leveraging Behavior Trees, Utility AI response curves, and local steering behaviors.
- **Deterministic procedural content generation (PCG) using seeded multi-octave noise, cellular automata, and room graph layouts.**: Deterministic procedural content generation (PCG) using seeded multi-octave noise, cellular automata, and room graph layouts.
- **Monotonic save persistence pipelines with cryptographic integrity checksums and cross-platform cloud save synchronization.**: Monotonic save persistence pipelines with cryptographic integrity checksums and cross-platform cloud save synchronization.

#### Identified Standardization Gaps
- Rubric C18: Missing '## Failure Modes' section entirely.
- Rubric C14: Guardrail lock deficit (9 locks vs minimum 12 required by SOTA rubric).
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Game Developer (must be declined or routed via Role Handoff):
- `deploy-aws-eks-workloads`: Cloud container orchestration belongs to AWS / DevOps Engineer.
- `manage-vietnam-accounting`: Corporate accounting journals belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Statutory legal opinions belong to Vietnam Legal Counsel.
- `optimize-seo`: Web search engine optimization belongs to SEO Analyst.
```

##### Architectural Guardrail Locks to Codify:
- **ECS-DOD-INVARIANT LOCK**: Game loops must execute cache-friendly contiguous archetype queries; per-frame dynamic heap allocations in simulation hot paths are blocked fail-closed.
- **FIXED-TIMESTEP-PHYSICS LOCK**: Physics calculations must run on deterministic fixed timesteps ($50\text{Hz}$ or $60\text{Hz}$) with delta time accumulation; uncoupled variable delta ticks are prohibited.
- **DETERMINISTIC-PCG-SEED LOCK**: All procedural content generation streams must be deterministically reproducible from an explicit 64-bit integer seed; unseeded PRNG calls are forbidden.
- **SAVE-SCHEMA-INTEGRITY LOCK**: Game save files must include monotonic schema version headers and SHA-256 HMAC integrity signatures; unverified save loading is prohibited.
- **HEADLESS-CI-RUNNER LOCK**: All gameplay logic, physics, and state machines must be fully verifiable via headless automated engine test runners in CI without display dependencies.
- **SKILL-ASSET-PIPELINE-AST02 LOCK**: Prohibit third-party procedural asset generation skills lacking publisher verification or executing untrusted native binaries (AST02).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny game development automation tools write access to core agent configuration files (AST10).

#### Failure Modes to Incorporate (Phase R2):
- **Non-deterministic physics simulation across platforms**:  floating point math variations between CPU architectures cause desynchronization in multiplayer or replays.
  - *Mitigation:* Enforce fixed-point arithmetic or deterministic soft-float math libraries for all simulation-critical paths; verify parity in headless CI across Linux and Windows runners.
- **VRAM exhaustion and heap fragmentation**:  additive scene transitions leak textures and meshes across level unloads.
  - *Mitigation:* Mandate explicit `.dispose()` and resource unloader traversal during scene lifecycle teardown; assert zero retained engine objects in memory profiling gates.
- **Fast-mover collision tunneling**:  high-velocity projectiles or characters pass through thin colliders without triggering contact events.
  - *Mitigation:* Enforce Continuous Collision Detection (CCD) and kinematic ray-substepping for all entities exceeding half their bounding dimension per tick.
- **Frame stutter from garbage collection stalls**:  temporary object allocations inside `_process` or `Update` loops trigger unpredictable GC pauses.
  - *Mitigation:* Enforce pre-allocated object pools and contiguous struct arrays for all transient entities, particles, and math vectors; fail-closed on inner-loop allocations.
- **Corrupted save state on abrupt termination**:  player save data is partially written when a crash or power cut occurs.
  - *Mitigation:* Enforce atomic two-stage write-to-temporary and atomic rename pattern with HMAC-SHA256 checksum validation prior to overwriting canonical save slots.

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.

---

### 4.17. MMO Engineer (`mmo-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** MMO Engineer | **Canonical Slug:** `mmo-engineer`
- **Common Aliases in INDEX.md:** `@mmo`, `@affiliate`, `@growth`, `@growth-lead`, `@growth-engineer`, `@media-buyer`, `@affiliate-marketer`
- **Mission:** Architect, deploy, and scale programmatic performance marketing systems, affiliate growth operations, proxy infrastructures, and browser automation fleets.
- **Level:** Principal / Master-level Growth Engineering and MMO Infrastructure
- **File Metrics:** 228 lines / 17.3 KB | **Last Updated:** `2026-10-17`
- **Principal Expectations:** 5 items
- **Skill Toolbox:** Primary (7): `deploy-mmo-infrastructure`, `setup-tracking-system`, `create-automation-script`, `manage-mmo-assets`, `deploy-proxyware-fleet`, `generate-mmo-content`, `analyze-campaign-roi` | Supporting (3): `setup-deployment`, `navigate-service`, `write-documentation`
- **Contract Schema Coverage:** Emits: `implementation-result.json`, `mmo-campaign-spec.json`, `mmo-roi-report.json` | Disclaims: Does not alter core product business logic, production enterprise DB schemas, or corporate contracts.
- **Guardrail Locks:** 21 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 8 [ ] checkboxes; references references/mmo-engineer-review-checklist.md | Companion File: `references/mmo-engineer-review-checklist.md` (125 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Stealth browser automation using Playwright over Chrome DevTools Protocol (CDP) and Camoufox C++ patched browsers.**: Stealth browser automation using Playwright over Chrome DevTools Protocol (CDP) and Camoufox C++ patched browsers.
- **Dynamic proxy pool management (Residential/4G) with automated latency health probes and IP rotation.**: Dynamic proxy pool management (Residential/4G) with automated latency health probes and IP rotation.
- **Privacy-first Server-to-Server (S2S) postback tracking across Meta CAPI v20+, TikTok Events API, and Google Enhanced Conversions.**: Privacy-first Server-to-Server (S2S) postback tracking across Meta CAPI v20+, TikTok Events API, and Google Enhanced Conversions.
- **DePIN bandwidth monetization light nodes (Grass, Dawn, Nodepay) orchestrated with Solana/EVM wallet authentication.**: DePIN bandwidth monetization light nodes (Grass, Dawn, Nodepay) orchestrated with Solana/EVM wallet authentication.
- **Programmatic SEO (pSEO) answer-first landing page generation with valid JSON-LD schemas.**: Programmatic SEO (pSEO) answer-first landing page generation with valid JSON-LD schemas.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by MMO Engineer (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Production backend services belong to Backend Developer.
- `create-migration`: Relational database DDL belongs to Backend Developer.
- `manage-vietnam-accounting`: Corporate tax accounting belongs to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal corporate legal opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **AUTOMATION-SKILL-SANDBOX-AST06 LOCK**: Enforce isolated sandbox containment on all browser automation and proxy skills; prevent access to local developer credentials or unapproved network interfaces (AST06).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny growth automation tools write privileges over core repository policies (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.

---

### 4.18. Mobile Engineer (`mobile-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** Mobile Engineer | **Canonical Slug:** `mobile-engineer`
- **Common Aliases in INDEX.md:** `@mobile`, `@flutter`, `@react-native`
- **Mission:** Deliver correct, performant, and accessible mobile experiences on iOS and Android by owning native app logic, platform integrations, offline sync, and app store release lifecycles.
- **Level:** Principal / Master-level Mobile Application Engineering
- **File Metrics:** 486 lines / 40.2 KB | **Last Updated:** `2026-09-18`
- **Principal Expectations:** 10 items
- **Skill Toolbox:** Primary (9): `develop-mobile-app`, `deploy-mobile-app`, `add-ui-component`, `integrate-api-client`, `write-tests`, `frontend-testing`, `security-audit`, `commit-code`, `navigate-service` | Supporting (6): `design-ux-flow`, `design-review`, `performance-profiling`, `troubleshoot-service`, `debug-runtime-platform`, `write-documentation`
- **Contract Schema Coverage:** Emits: `adr-spec.json`, `deployment-plan.json`, `feature-ticket.json`, `implementation-result.json`, `mobile-app-spec.json`, `security-audit.json`, `test-report.json`, `ui-component-spec.json` | Disclaims: Does not author enterprise cloud infrastructure, server-side database migrations, or legal opinions.
- **Guardrail Locks:** 13 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 53 plain bullets across 13 sections; references references/mobile-engineer-review-checklist.md | Companion File: `references/mobile-engineer-review-checklist.md` (54 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **React Native New Architecture utilizing TurboModules, Fabric renderer, and Nitro Modules for direct C++ bridging.**: React Native New Architecture utilizing TurboModules, Fabric renderer, and Nitro Modules for direct C++ bridging.
- **Expo Application Services (EAS) build and submission pipelines automating Google Play and Apple App Store deployments.**: Expo Application Services (EAS) build and submission pipelines automating Google Play and Apple App Store deployments.
- **Hermes JavaScript engine performance tuning and JSI memory profiling guaranteeing stable 60/120 FPS UI threads.**: Hermes JavaScript engine performance tuning and JSI memory profiling guaranteeing stable 60/120 FPS UI threads.
- **Offline-first synchronization architectures leveraging WatermelonDB and SQLite with deterministic conflict resolution.**: Offline-first synchronization architectures leveraging WatermelonDB and SQLite with deterministic conflict resolution.
- **Mobile compliance**:  iOS 18 / Android 15 Privacy Manifests, App Tracking Transparency (ATT), and secure hardware enclave storage.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Mobile Engineer (must be declined or routed via Role Handoff):
- `deploy-aws-eks-workloads`: Cloud container orchestration belongs to AWS / DevOps Engineer.
- `create-migration`: Relational database DDL belongs to Backend Developer.
- `manage-vietnam-accounting`: Corporate tax reporting belongs to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory advice belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **MOBILE-SKILL-SUPPLY-CHAIN-AST02 LOCK**: Require verified provenance on all native CocoaPods, Gradle plugins, and React Native native modules (AST02).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny mobile build scripts write access to root agent governance files (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.19. Product Manager (`product-manager`)

#### Role Metadata & Baseline Status
- **Official Title:** Product Manager | **Canonical Slug:** `product-manager`
- **Common Aliases in INDEX.md:** `@pm`, `@prod-mgr`, `@product-owner`, `@po`
- **Mission:** Maximize user and business value through clear prioritization, scope control, and outcome-driven delivery without hiding trade-offs or assumptions.
- **Level:** Principal / Master-level Product Management
- **File Metrics:** 382 lines / 26.2 KB | **Last Updated:** `2026-10-17`
- **Principal Expectations:** 15 items
- **Skill Toolbox:** Primary (5): `define-product-strategy`, `prioritize-roadmap`, `model-saas-metrics`, `build-story-map`, `write-product-brief` | Supporting (12): `analyze-business-requirements`, `elicit-requirements`, `write-use-cases`, `trace-requirements-impact`, `design-ux-flow`, `meeting-review`, `write-documentation`, `audit-ai-compliance`, `agent-evaluation`, `plan-technical-delivery`, `conduct-research`, `analyze-data`
- **Contract Schema Coverage:** Emits: `feature-ticket.json`, `solution-brief.json` | Disclaims: Does not write production code, commit code directly, or deploy cloud infrastructure.
- **Guardrail Locks:** 21 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 21 plain bullets; references references/product-manager-review-checklist.md | Companion File: `references/product-manager-review-checklist.md` (113 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Strategic product definition using Opportunity Solution Trees (Teresa Torres) and 7 Powers structural advantage analysis (Hamilton Helmer).**: Strategic product definition using Opportunity Solution Trees (Teresa Torres) and 7 Powers structural advantage analysis (Hamilton Helmer).
- **Deterministic SaaS unit economics modeling**:  CAC, LTV, Magic Number, Rule of 40, Burn Multiple, and Net Revenue Retention.
- **Agentic product management governing AI inference cost per verified task completion and blast-radius ceilings.**: Agentic product management governing AI inference cost per verified task completion and blast-radius ceilings.
- **Hypothesis-driven delivery validating riskiest assumptions before full-scale engineering investment.**: Hypothesis-driven delivery validating riskiest assumptions before full-scale engineering investment.
- **Regulatory compliance alignment with EU AI Act Article 50 transparency and customer disclosure.**: Regulatory compliance alignment with EU AI Act Article 50 transparency and customer disclosure.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Product Manager (must be declined or routed via Role Handoff):
- `commit-code`: Source code modification and git commits belong to Developer roles.
- `setup-deployment`: Cloud deployment configuration belongs to DevOps Engineer.
- `manage-vietnam-accounting`: Live journal entries belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **STRATEGY-SKILL-AST09 LOCK**: Maintain verifiable audit logs for roadmap prioritization decisions and agent operational budgets under AST09 governance.
- **IDENTITY-FILE-PROTECTION LOCK**: Protect product governance and prompt instructions from external strategy tool mutations (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.20. Project Manager (`project-manager`)

#### Role Metadata & Baseline Status
- **Official Title:** Project Manager | **Canonical Slug:** `project-manager`
- **Common Aliases in INDEX.md:** `@pjm`, `@proj-mgr`, `@scrum-master`
- **Mission:** Turn agreed product scope into an executable plan with clear milestones, dependencies, owners, and risk control.
- **Level:** Principal / Master-level Delivery and Project Orchestration
- **File Metrics:** 279 lines / 19.1 KB | **Last Updated:** `2026-10-17`
- **Principal Expectations:** 10 items
- **Skill Toolbox:** Primary (1): `meeting-review` | Supporting (10): `plan-technical-delivery`, `model-saas-metrics`, `design-ux-flow`, `write-documentation`, `write-product-brief`, `audit-ai-compliance`, `agent-evaluation`, `analyze-data`, `troubleshoot-service`, `navigate-service`
- **Contract Schema Coverage:** Emits: `ai-risk-register.json`, `coordination-plan.json`, `deployment-plan.json`, `solution-brief.json`, `test-report.json` | Disclaims: Does not approve technical architecture trade-offs or author software source code.
- **Guardrail Locks:** 21 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 7 plain bullets; references references/project-manager-review-checklist.md | Companion File: `references/project-manager-review-checklist.md` (122 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Milestone scheduling and multi-agent dependency DAG orchestration.**: Milestone scheduling and multi-agent dependency DAG orchestration.
- **Probabilistic delivery forecasting utilizing Monte Carlo burndown models rather than optimistic single-point estimates.**: Probabilistic delivery forecasting utilizing Monte Carlo burndown models rather than optimistic single-point estimates.
- **AI FinOps budget tracking governing token consumption rates and swarm velocity ceilings.**: AI FinOps budget tracking governing token consumption rates and swarm velocity ceilings.
- **GIST framework implementation tracking technical debt registers and remediation budgets.**: GIST framework implementation tracking technical debt registers and remediation budgets.
- **Commit provenance and audit trail enforcement verifying execution against signed feature tickets.**: Commit provenance and audit trail enforcement verifying execution against signed feature tickets.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C15: Primary skill count imbalance (holds only 1 primary skill `meeting-review`).
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Project Manager (must be declined or routed via Role Handoff):
- `write-tech-radar`: Technical architecture decisions belong to Solution / Technical Architect.
- `commit-code`: Source code modifications belong to engineering roles.
- `manage-vietnam-accounting`: Live accounting journals belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory counsel belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **PROJECT-SKILL-AST09 LOCK**: Maintain immutable governance records of sprint commitments, task delegations, and capacity allocations under AST09.
- **IDENTITY-FILE-PROTECTION LOCK**: Deny project management tracking tools write privileges over agent identity and core operating instructions (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.21. Prompt Engineer (`prompt-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** Prompt Engineer | **Canonical Slug:** `prompt-engineer`
- **Common Aliases in INDEX.md:** `@prompt-engineer`, `@prompt`, `@promptops`
- **Mission:** Design, evaluate, optimize, and maintain production prompt assets, system instructions, and few-shot libraries across LLM architectures.
- **Level:** Principal / Lead prompt systems and context optimization specialist
- **File Metrics:** 206 lines / 13.0 KB | **Last Updated:** `2026-10-21`
- **Principal Expectations:** 7 items
- **Skill Toolbox:** Primary (2): `context-optimization`, `memory-hygiene` | Supporting (6): `agent-evaluation`, `prompt-injection-defense`, `agent-tool-orchestration`, `implement-structured-outputs`, `systematic-debugging`, `agent-memory-compaction`
- **Contract Schema Coverage:** Emits: `coordination-plan.json`, `memory-audit-report.json` | Disclaims: Does not author production backend application code, database migrations, or deploy Kubernetes clusters.
- **Guardrail Locks:** 8 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 8 [ ] checkboxes; references references/prompt-engineer-review-checklist.md | Companion File: `references/prompt-engineer-review-checklist.md` (70 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Non-Compliant (Missing Failure Modes, Lock Deficit < 12)**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Five-tier context budgeting allocating tokens across System Invariants (15%), Dynamic Task Grounding (35%), Working Memory (25%), Scratchpad (10%), and Output Reserve (15%).**: Five-tier context budgeting allocating tokens across System Invariants (15%), Dynamic Task Grounding (35%), Working Memory (25%), Scratchpad (10%), and Output Reserve (15%).
- **Lost-in-the-middle positioning mitigation placing critical behavioral rules and output schemas in prompt primacy (top 15%) and recency (bottom 15%).**: Lost-in-the-middle positioning mitigation placing critical behavioral rules and output schemas in prompt primacy (top 15%) and recency (bottom 15%).
- **Syntactic 4-gram and semantic vector cosine deduplication (sim >= 0.88) eliminating context window redundancy.**: Syntactic 4-gram and semantic vector cosine deduplication (sim >= 0.88) eliminating context window redundancy.
- **Structural delimiter isolation (<untrusted_data id='...'>) with ephemeral canary nonces preventing prompt injection.**: Structural delimiter isolation (<untrusted_data id='...'>) with ephemeral canary nonces preventing prompt injection.
- **Strict JSON Schema Draft 2020-12 constrained decoding eliminating regex parsing of model outputs.**: Strict JSON Schema Draft 2020-12 constrained decoding eliminating regex parsing of model outputs.

#### Identified Standardization Gaps
- Rubric C18: Missing '## Failure Modes' section entirely.
- Rubric C14: Guardrail lock deficit (8 locks vs minimum 12 required by SOTA rubric).
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Prompt Engineer (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Application backend development belongs to Backend Developer.
- `setup-deployment`: Cloud hosting and CI/CD pipelines belong to DevOps Engineer.
- `manage-vietnam-accounting`: Live journal entries belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory advice belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **FIVE-TIER-TOKEN-BUDGET LOCK**: Total prompt construction must strictly adhere to the 5-tier budget: 15% System Invariants, 35% Task Grounding, 25% Working Memory, 10% Scratchpad, 15% Output Reserve.
- **LOST-IN-THE-MIDDLE LOCK**: Critical behavioral constraints, invariant rules, and output schemas must be anchored at prompt boundaries (top 15% or bottom 15%); middle placement is prohibited.
- **CANARY-TOKEN-LEAK-GUARD LOCK**: Dynamic untrusted context must be isolated within `<untrusted_data>` blocks with ephemeral canary tokens; output strings echoing canary tokens are blocked fail-closed.
- **SCHEMA-CONSTRAINED-DECODING LOCK**: Output generation must enforce strict grammar-based constrained decoding via JSON Schema Draft 2020-12; regex parsing of unconstrained prose is forbidden.
- **PROMPT-ASSET-VERSIONING LOCK**: All prompt templates must be versioned as software assets with semantic versioning and tracked benchmark evaluation scores.
- **SKILL-PROMPT-AST05 LOCK**: Prohibit dynamic injection of untrusted remote prompt snippets or unvetted external instructions (AST05).
- **IDENTITY-FILE-PROTECTION LOCK**: Protect system instructions and identity files from self-referential unvetted prompt modifications (AST10).

#### Failure Modes to Incorporate (Phase R2):
- **Prompt injection jailbreak**:  untrusted user input overrides system instructions through delimiter escaping or role-play framing.
  - *Mitigation:* Encapsulate all external input within `<untrusted_data id='...'>` blocks; inject ephemeral canary tokens; enforce AST05 prompt injection defense filters.
- **Lost-in-the-middle context degradation**:  essential constraints placed in the middle of long prompts are ignored by the model.
  - *Mitigation:* Enforce 5-tier context budgeting; anchor critical constraints and JSON schemas in the first 15% (primacy) or final 15% (recency) of prompt tokens.
- **Instruction drift across multi-turn sessions**:  extended agent conversations lose grounding, substituting original goals with conversational drift.
  - *Mitigation:* Trigger memory compaction at 60/80 capacity thresholds; re-inject canonical task goals and invariant constraints at every turn.
- **Constrained decoding schema failure**:  model output violates JSON Schema Draft 2020-12 specifications resulting in runtime parsing exceptions.
  - *Mitigation:* Enforce grammar-constrained decoding at the inference runtime level; test prompt templates against golden evaluation datasets prior to deployment.
- **Excessive prompt token bloat**:  uncompacted chat history and redundant context exhaust model token windows and inflate inference cost.
  - *Mitigation:* Apply 4-gram and semantic vector cosine deduplication (threshold >= 0.88); enforce Head-Tail tool output truncation.

---

### 4.22. QA Engineer (`qa-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** QA Engineer | **Canonical Slug:** `qa-engineer`
- **Common Aliases in INDEX.md:** `@qa`, `@tester`, `@test-engineer`
- **Mission:** Guarantee software correctness, reliability, performance, and security across the delivery lifecycle by designing and executing comprehensive testing strategies.
- **Level:** Principal / master-level quality engineering
- **File Metrics:** 574 lines / 51.6 KB | **Last Updated:** `2026-10-25`
- **Principal Expectations:** 17 items
- **Skill Toolbox:** Primary (12): `write-tests`, `frontend-testing`, `systematic-debugging`, `combinatorial-testing`, `agent-quality-gate`, `accessibility-review`, `configure-mcp`, `implement-webmcp`, `hostile-component-stress-testing`, `playwright-evidence-qa`, `webapp-server-runner`, `web-quality-audit` | Supporting (7): `review-service`, `agent-observability`, `navigate-service`, `review-code`, `troubleshoot-service`, `performance-profiling`, `agent-evaluation`
- **Contract Schema Coverage:** Emits: `test-report.json`, `validation-result.json` | Disclaims: Does not author production feature implementation code or grant final architecture sign-offs.
- **Guardrail Locks:** 20 named locks in file
- **Security Coverage:** ASI: Deep integration (24 explicit mentions of ASI, focusing on ASI04 supply chain and ASI05 execution sandbox) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 36 [ ] checkboxes across 10 gate sections; references references/qa-engineer-review-checklist.md | Companion File: `references/qa-engineer-review-checklist.md` (195 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **The Great Verification Convergence eliminating Assertion Theater through empirical Verification-Before-Completion (VBC) with fresh execution evidence.**: The Great Verification Convergence eliminating Assertion Theater through empirical Verification-Before-Completion (VBC) with fresh execution evidence.
- **Four-Phase Systematic Root Cause Analysis (Observe, Hypothesize, Test, Fix).**: Four-Phase Systematic Root Cause Analysis (Observe, Hypothesize, Test, Fix).
- **Pairwise and n-way combinatorial testing using orthogonal covering matrices (PyPICT/IPO) preventing combinatorial explosion.**: Pairwise and n-way combinatorial testing using orthogonal covering matrices (PyPICT/IPO) preventing combinatorial explosion.
- **Consumer-Driven Contract Testing (CDCT) utilizing PactV3 and Buf breaking change detection.**: Consumer-Driven Contract Testing (CDCT) utilizing PactV3 and Buf breaking change detection.
- **Calibrated LLM-as-a-judge evaluation achieving >= 85% statistical agreement (Cohen's Kappa >= 0.85) against human ground truth.**: Calibrated LLM-as-a-judge evaluation achieving >= 85% statistical agreement (Cohen's Kappa >= 0.85) against human ground truth.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by QA Engineer (must be declined or routed via Role Handoff):
- Direct feature implementation code authoring (strict conflict of interest against verification duties).
- `deploy-aws-eks-workloads`: Cloud cluster provisioning belongs to AWS / DevOps Engineer.
- `manage-vietnam-accounting`: Live journal and tax auditing belongs to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **TEST-HARNESS-SKILL-AST08 LOCK**: Verify all test automation skills, browser drivers, and synthetic data generators against AST08 pre-execution scanning standards.
- **IDENTITY-FILE-PROTECTION LOCK**: Protect test policies and release verification gate definitions from test script mutations (AST10).

---

### 4.23. Researcher (`researcher`)

#### Role Metadata & Baseline Status
- **Official Title:** Researcher | **Canonical Slug:** `researcher`
- **Common Aliases in INDEX.md:** `@research`, `@deep-research`
- **Mission:** Conduct deep, systematic, and evidence-grounded research into unfamiliar domains, technologies, architectures, and market requirements.
- **Level:** Principal / Lead Research Specialist
- **File Metrics:** 427 lines / 34.9 KB | **Last Updated:** `2026-10-23`
- **Principal Expectations:** 13 items
- **Skill Toolbox:** Primary (1): `conduct-research` | Supporting (9): `analyze-business-requirements`, `agent-delegation`, `agent-context-management`, `agent-semantic-memory`, `agent-memory-compaction`, `agent-tool-orchestration`, `agent-quality-gate`, `write-documentation`, `optimize-seo`
- **Contract Schema Coverage:** Emits: `architecture-options.json`, `research-report.json` | Disclaims: Does not author feature-ticket.json, write production code, or make binding architecture approvals.
- **Guardrail Locks:** 22 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 27 plain bullets across 4 sections; references references/researcher-review-checklist.md | Companion File: `references/researcher-review-checklist.md` (176 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Stanford STORM persona discovery protocol exploring domains across 4 distinct expert perspectives.**: Stanford STORM persona discovery protocol exploring domains across 4 distinct expert perspectives.
- **Citation DAG topology validation enforcing 3-color DFS acyclicity and rejecting circular authority loops.**: Citation DAG topology validation enforcing 3-color DFS acyclicity and rejecting circular authority loops.
- **Chain-of-Verification (CoVe) protocol for high-stakes claims requiring independent primary source verification.**: Chain-of-Verification (CoVe) protocol for high-stakes claims requiring independent primary source verification.
- **Quantitative Information Density metric (ID >= 0.12) ensuring concise, evidence-rich deliverables.**: Quantitative Information Density metric (ID >= 0.12) ensuring concise, evidence-rich deliverables.
- **Four-tier source hierarchy strictly treating AI model outputs as query tools rather than citable authorities.**: Four-tier source hierarchy strictly treating AI model outputs as query tools rather than citable authorities.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Researcher (must be declined or routed via Role Handoff):
- `commit-code`: Source code modifications belong to developer roles.
- `setup-deployment`: Infrastructure deployment belongs to DevOps Engineer.
- `manage-vietnam-accounting`: Financial accounting entries belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **RESEARCH-SOURCE-PROVENANCE-AST01 LOCK**: Verify publisher provenance and cryptographic integrity on all external research ingestion sources and scraper tools (AST01).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny research analysis tools write privileges over core repository policies (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.24. Reverse Engineer (`reverse-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** Reverse Engineer | **Canonical Slug:** `reverse-engineer`
- **Common Aliases in INDEX.md:** `@reverse-engineer`, `@reverse-engineering`, `@re`, `@rev`, `@binary-analyst`, `@malware-analyst`
- **Mission:** Deconstruct compiled binaries, proprietary protocols, and obfuscated bytecode in air-gapped sandboxes to recover logic, discover vulnerabilities, and produce verifiable evidence ledgers.
- **Level:** Principal Binary & Protocol Analysis Specialist
- **File Metrics:** 287 lines / 22.9 KB | **Last Updated:** `2026-10-29`
- **Principal Expectations:** 7 items
- **Skill Toolbox:** Primary (1): `reverse-engineer-binary` | Supporting (9): `security-audit`, `systematic-debugging`, `skill-preflight-ast-check`, `supply-chain-security`, `prompt-injection-defense`, `review-code`, `performance-profiling`, `conduct-research`, `agent-delegation`
- **Contract Schema Coverage:** Emits: `api-contract-spec.json`, `security-audit.json` | Disclaims: Does not author malicious exploits, deploy unvetted software, or operate outside legal authorizations.
- **Guardrail Locks:** 12 named locks in file
- **Security Coverage:** ASI: Moderate integration (references ASI01 Goal Hijack and ASI10 Rogue Agents in air-gapped sandbox rules) | AST: 0 explicit references (employs skill-preflight-ast-check in supporting skills)
- **Checklist Architecture:** 11 plain bullets; references references/reverse-engineer-review-checklist.md | Companion File: `references/reverse-engineer-review-checklist.md` (86 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Air-gapped execution sandbox with zero outbound network egress during untrusted binary analysis.**: Air-gapped execution sandbox with zero outbound network egress during untrusted binary analysis.
- **Reverse Engineering Assistant (REA) MCP toolchain orchestration automating decompilation and control-flow recovery.**: Reverse Engineering Assistant (REA) MCP toolchain orchestration automating decompilation and control-flow recovery.
- **Cross-architecture analysis covering x86_64, ARM64, WebAssembly, EVM bytecode, and .NET MSIL.**: Cross-architecture analysis covering x86_64, ARM64, WebAssembly, EVM bytecode, and .NET MSIL.
- **Cryptographic primitive identification and proprietary protocol state machine reconstruction.**: Cryptographic primitive identification and proprietary protocol state machine reconstruction.
- **Production of verifiable Reverse Engineering Artifact (REA) evidence ledgers and reconstructed interface specifications.**: Production of verifiable Reverse Engineering Artifact (REA) evidence ledgers and reconstructed interface specifications.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Reverse Engineer (must be declined or routed via Role Handoff):
- Authoring offensive weaponized exploit payloads.
- `setup-deployment`: Production deployment belongs to DevOps Engineer.
- `manage-vietnam-accounting`: Live journal entries belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory advice belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **AIRGAP-SKILL-ISOLATION-AST06 LOCK**: All binary inspection skills must run in hermetic sandboxes with network sockets disabled fail-closed (AST06).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny binary deconstruction tools write access to core agent personality and memory stores (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.25. Reviewer (`reviewer`)

#### Role Metadata & Baseline Status
- **Official Title:** Reviewer | **Canonical Slug:** `reviewer`
- **Common Aliases in INDEX.md:** `@reviewer`, `@code-reviewer`, `@pr-reviewer`
- **Mission:** Provide thorough, objective, evidence-based code and architecture reviews — identifying defects, security risks, performance bottlenecks, and design anti-patterns before merge.
- **Level:** Principal / Lead Engineering Reviewer
- **File Metrics:** 294 lines / 19.3 KB | **Last Updated:** `2026-10-21`
- **Principal Expectations:** 10 items
- **Skill Toolbox:** Primary (5): `review-code`, `review-service`, `configure-mcp`, `implement-structured-outputs`, `discernment-nudge` | Supporting (9): `design-review`, `accessibility-review`, `navigate-service`, `security-audit`, `performance-profiling`, `meeting-review`, `anti-ui-slop-finish-gate`, `prompt-injection-defense`, `agent-memory-compaction`
- **Contract Schema Coverage:** Emits: `code-review-finding.json` | Disclaims: Does not write production feature code, approve security exceptions, or override system architecture.
- **Guardrail Locks:** 14 named locks in file
- **Security Coverage:** ASI: Deep integration (24 explicit mentions across ASI01, ASI02, ASI04, ASI05, ASI06) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 7 [ ] checkboxes; references references/reviewer-review-checklist.md | Companion File: `references/reviewer-review-checklist.md` (67 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Adversarial anti-vibe-slop audit rejecting defensive over-mocking, assertion theater, and superficial boilerplate.**: Adversarial anti-vibe-slop audit rejecting defensive over-mocking, assertion theater, and superficial boilerplate.
- **Mutation testing score verification asserting mutation kill rate >= 75-80% before approval.**: Mutation testing score verification asserting mutation kill rate >= 75-80% before approval.
- **Discernment Nudge appending 2-3 sharp Socratic questions to probe unstated architectural assumptions.**: Discernment Nudge appending 2-3 sharp Socratic questions to probe unstated architectural assumptions.
- **Multi-dimensional code inspection verifying correctness, concurrency safety, resource disposal, and backwards compatibility.**: Multi-dimensional code inspection verifying correctness, concurrency safety, resource disposal, and backwards compatibility.
- **OWASP ASI security gate validating PRs against prompt injection, tool misuse, and privilege escalation.**: OWASP ASI security gate validating PRs against prompt injection, tool misuse, and privilege escalation.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Reviewer (must be declined or routed via Role Handoff):
- Direct feature implementation code authoring (strict conflict of interest against reviewing duties).
- `deploy-aws-eks-workloads`: Cloud cluster deployments belong to AWS / DevOps Engineer.
- `manage-vietnam-accounting`: Live journal auditing belongs to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal statutory legal opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **REVIEW-SKILL-AST08 LOCK**: Verify all automated static analysis and code review scanning tools against AST08 quality and provenance standards.
- **IDENTITY-FILE-PROTECTION LOCK**: Protect pull request review policies and merge rules from automated code review tool overwrites (AST10).

---

### 4.26. SDET (`sdet`)

#### Role Metadata & Baseline Status
- **Official Title:** SDET | **Canonical Slug:** `sdet`
- **Common Aliases in INDEX.md:** `@sdet`, `@test-automation`, `@automation-engineer`
- **Mission:** Design, build, scale, and maintain automated test platforms, continuous evaluation harnesses, and synthetic test data pipelines across services.
- **Level:** Principal / Lead test automation and evaluation systems engineer
- **File Metrics:** 207 lines / 12.2 KB | **Last Updated:** `2026-10-20`
- **Principal Expectations:** 7 items
- **Skill Toolbox:** Primary (1): `agent-evaluation` | Supporting (6): `write-tests`, `agent-quality-gate`, `combinatorial-testing`, `playwright-evidence-qa`, `webapp-server-runner`, `systematic-debugging`
- **Contract Schema Coverage:** Emits: `agent-eval-report.json`, `test-report.json` | Disclaims: Does not write production application code, author business feature tickets, or sign off on security penetration audits.
- **Guardrail Locks:** 8 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 8 [ ] checkboxes; references references/sdet-review-checklist.md | Companion File: `references/sdet-review-checklist.md` (66 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Non-Compliant (Missing Failure Modes, Lock Deficit < 12)**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Automated LLM evaluation harness construction using quantitative scoring rubrics and calibrated LLM-as-a-judge evaluators.**: Automated LLM evaluation harness construction using quantitative scoring rubrics and calibrated LLM-as-a-judge evaluators.
- **Synthetic test dataset generation enforcing strict schema constraints and edge-case parameter matrices.**: Synthetic test dataset generation enforcing strict schema constraints and edge-case parameter matrices.
- **Failure taxonomy classification categorizing errors into hallucination, goal drift, tool calling errors, and contract violations.**: Failure taxonomy classification categorizing errors into hallucination, goal drift, tool calling errors, and contract violations.
- **Continuous Integration evaluation gates enforcing statistical regression thresholds before promotion.**: Continuous Integration evaluation gates enforcing statistical regression thresholds before promotion.
- **Hermetic test environment automation running webapp-server-runner with guaranteed process cleanup.**: Hermetic test environment automation running webapp-server-runner with guaranteed process cleanup.

#### Identified Standardization Gaps
- Rubric C18: Missing '## Failure Modes' section entirely.
- Rubric C14: Guardrail lock deficit (8 locks vs minimum 12 required by SOTA rubric).
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by SDET (must be declined or routed via Role Handoff):
- Authoring production application business logic (conflict of interest with test engineering).
- `deploy-aws-eks-workloads`: Cloud cluster provisioning belongs to AWS / DevOps Engineer.
- `manage-vietnam-accounting`: Live journal auditing belongs to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal statutory legal counsel belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **ANTI-ASSERTION-THEATER LOCK**: Every automated test must fail when its target invariant is violated; vacuous tautological tests are blocked fail-closed.
- **MUTATION-TESTING-GATE LOCK**: Automated test suites for critical core components must achieve >= 80% mutation score indicator before release certification.
- **PAIRWISE-COMBINATORIAL LOCK**: Multi-parameter integration workflows must apply orthogonal covering arrays to eliminate combinatorial explosion while retaining n-way coverage.
- **HERMETIC-TEST-ISOLATION LOCK**: Test suites must execute within isolated, hermetic sandboxes with automatic socket polling and guaranteed process cleanup.
- **EVAL-CALIBRATION-KAPPA LOCK**: Automated LLM evaluators must demonstrate >= 0.85 Cohen's Kappa agreement against golden human rating datasets.
- **TEST-TOOL-SUPPLY-CHAIN-AST02 LOCK**: Prohibit test framework plugins or evaluation harnesses pulling unverified third-party dependencies (AST02).
- **IDENTITY-FILE-PROTECTION LOCK**: Protect automated test gate criteria and benchmark definitions from test runner tool modifications (AST10).

#### Failure Modes to Incorporate (Phase R2):
- **Assertion theater and tautological tests**:  test suite reports 100% pass rate while failing to assert actual state changes or invariant preservation.
  - *Mitigation:* Enforce mutation testing gates (mutation kill score >= 80%); require explicit negative test cases proving failures when invariants are breached.
- **Flaky end-to-end browser automation**:  test cases fail intermittently due to arbitrary timeouts and race conditions.
  - *Mitigation:* Replace all sleep calls with deterministic DOM state polling and network idle observers via Playwright; enforce tripartite evidence capture (screenshot, DOM, logs).
- **LLM evaluation score drift**:  model judge criteria drift over time due to prompt ambiguity or model updates.
  - *Mitigation:* Calibrate LLM-as-a-judge evaluators against human ground truth (Cohen's Kappa >= 0.85); anchor scoring with few-shot demonstration exemplars.
- **Combinatorial test explosion**:  multi-parameter tests result in exponentially expanding runtimes stalling CI pipelines.
  - *Mitigation:* Apply pairwise combinatorial reduction (PyPICT / covering arrays) reducing exponential test matrices to compact polynomial suites.
- **State pollution across parallel test workers**:  concurrent test runners overwrite shared database tables or cache keys.
  - *Mitigation:* Enforce hermetic container isolation (Testcontainers) with ephemeral database branching and per-worker isolated namespaces.

---

### 4.27. Security Engineer (`security-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** Security Engineer | **Canonical Slug:** `security-engineer`
- **Common Aliases in INDEX.md:** `@security`, `@sec`, `@appsec`, `@secops`
- **Mission:** Safeguard software architectures, data pipelines, agent interactions, and cloud infrastructures by identifying vulnerabilities, modeling threats, establishing security guardrails, and enforcing Zero-Trust policies.
- **Level:** Principal / Lead security engineering specialist
- **File Metrics:** 373 lines / 30.3 KB | **Last Updated:** `2026-10-25`
- **Principal Expectations:** 7 items
- **Skill Toolbox:** Primary (7): `security-audit`, `manage-secrets`, `supply-chain-security`, `ai-risk-assessment`, `manage-agent-identity`, `skill-preflight-ast-check`, `prompt-injection-defense` | Supporting (10): `conduct-research`, `review-code`, `navigate-service`, `review-service`, `meeting-review`, `agent-delegation`, `write-documentation`, `anti-ui-slop-finish-gate`, `agent-tool-orchestration`, `agent-prompt-lifecycle`
- **Contract Schema Coverage:** Emits: `security-audit.json` | Disclaims: Does not author application feature code, execute deployments, or accept critical unmitigated risks.
- **Guardrail Locks:** 16 named locks in file
- **Security Coverage:** ASI: Deep integration (19 explicit mentions across full ASI01 through ASI10 threat matrix) | AST: 0 explicit references (employs skill-preflight-ast-check in primary skills)
- **Checklist Architecture:** 13 plain bullets; references references/security-engineer-review-checklist.md | Companion File: `references/security-engineer-review-checklist.md` (130 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Comprehensive threat modeling utilizing STRIDE and PASTA frameworks.**: Comprehensive threat modeling utilizing STRIDE and PASTA frameworks.
- **Complete institutionalization of OWASP ASI Top 10 (2026) across threat modeling and audit gates.**: Complete institutionalization of OWASP ASI Top 10 (2026) across threat modeling and audit gates.
- **Zero-Trust workload identity architecture and Non-Human Identity (NHI) lifecycle governance (SPIFFE/SVID, WIMSE).**: Zero-Trust workload identity architecture and Non-Human Identity (NHI) lifecycle governance (SPIFFE/SVID, WIMSE).
- **Software supply chain security enforcing SLSA Level 3, SBOM generation, and lockfile integrity verification.**: Software supply chain security enforcing SLSA Level 3, SBOM generation, and lockfile integrity verification.
- **Post-quantum cryptography readiness tracking (ML-KEM, ML-DSA) and Cryptographic Bill of Materials (CBOM) inventory.**: Post-quantum cryptography readiness tracking (ML-KEM, ML-DSA) and Cryptographic Bill of Materials (CBOM) inventory.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Security Engineer (must be declined or routed via Role Handoff):
- Authoring application business feature code (conflict of interest with security audit duties).
- `setup-deployment`: Cloud deployment execution belongs to DevOps Engineer.
- `manage-vietnam-accounting`: Financial and tax ledgers belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal corporate legal counsel belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **SKILL-PREFLIGHT-AST10 LOCK**: Enforce zero-execution AST scanning on all skills; block any skill exhibiting the lethal trifecta (AST03) or unverified publisher signatures (AST01).
- **IDENTITY-FILE-PROTECTION LOCK**: Protect AGENTS.md, MEMORY.md, and security policies from unauthenticated skill or tool mutations (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.28. SEO Analyst (`seo-analyst`)

#### Role Metadata & Baseline Status
- **Official Title:** SEO Analyst | **Canonical Slug:** `seo-analyst`
- **Common Aliases in INDEX.md:** `@seo`, `@seo-specialist`, `@seo-expert`
- **Mission:** Drive organic discovery, search engine crawlability, indexation performance, and Generative Engine Optimization (GEO) across all digital platforms.
- **Level:** Principal / Lead Search Engine Optimization Specialist
- **File Metrics:** 425 lines / 31.0 KB | **Last Updated:** `2026-09-18`
- **Principal Expectations:** 11 items
- **Skill Toolbox:** Primary (5): `optimize-seo`, `audit-technical-seo`, `implement-schema-markup`, `manage-api-catalog`, `analyze-campaign-roi` | Supporting (7): `conduct-research`, `write-article`, `configure-llms-txt`, `write-documentation`, `analyze-business-requirements`, `agent-delegation`, `review-service`
- **Contract Schema Coverage:** Emits: `seo-audit-report.json`, `seo-content-brief.json`, `seo-metadata.json`, `seo-weekly-board.json` | Disclaims: Does not author production backend application code, server configs, or legal opinions.
- **Guardrail Locks:** 17 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 24 plain bullets across 4 sections; references references/seo-analyst-review-checklist.md | Companion File: `references/seo-analyst-review-checklist.md` (84 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Entity-First SEO architecture grounding topics in Wikidata and Knowledge Graph disambiguations.**: Entity-First SEO architecture grounding topics in Wikidata and Knowledge Graph disambiguations.
- **Generative Engine Optimization (GEO) enforcing Answer-First (BLUF, 48-62 words) structures for LLM search indexing.**: Generative Engine Optimization (GEO) enforcing Answer-First (BLUF, 48-62 words) structures for LLM search indexing.
- **Advanced Schema.org connected JSON-LD graph construction (ItemPage, TechArticle, FAQPage).**: Advanced Schema.org connected JSON-LD graph construction (ItemPage, TechArticle, FAQPage).
- **Agentic Discovery protocols**:  `/llms.txt`, `/.well-known/agent-skills/index.json`, and RFC 9727 API Catalog registries.
- **Technical SEO audit and GSC remediation resolving crawl budget inefficiencies and indexation anomalies.**: Technical SEO audit and GSC remediation resolving crawl budget inefficiencies and indexation anomalies.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by SEO Analyst (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Server backend development belongs to Backend Developer.
- `setup-deployment`: Cloud hosting and CI/CD pipelines belong to DevOps Engineer.
- `manage-vietnam-accounting`: Live journal entries belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **SEO-SKILL-DATA-INTEGRITY-AST01 LOCK**: Prohibit third-party SERP scraping or keyword skills lacking verified publisher credentials (AST01).
- **IDENTITY-FILE-PROTECTION LOCK**: Protect SEO metadata schemas and robots directive files from unvetted tool modification (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.29. Solution Architect (`solution-architect`)

#### Role Metadata & Baseline Status
- **Official Title:** Solution Architect | **Canonical Slug:** `solution-architect`
- **Common Aliases in INDEX.md:** `@architect`, `@solution-arch`, `@solutions-architect`
- **Mission:** Design robust, scalable, and maintainable end-to-end system architectures that align business goals, technology choices, operational constraints, and security standards.
- **Level:** Principal / Lead Solution Architect
- **File Metrics:** 523 lines / 47.8 KB | **Last Updated:** `2026-10-25`
- **Principal Expectations:** 16 items
- **Skill Toolbox:** Primary (2): `write-tech-radar`, `meeting-review` | Supporting (11): `system-design`, `plan-technical-delivery`, `ai-risk-assessment`, `review-service`, `navigate-service`, `conduct-research`, `scaffold-new-service`, `review-code`, `security-audit`, `agent-delegation`, `write-documentation`
- **Contract Schema Coverage:** Emits: `adr-spec.json`, `architecture-options.json`, `solution-brief.json` | Disclaims: Does not write routine production CRUD code, direct infrastructure scripts, or sprint task tracking.
- **Guardrail Locks:** 24 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 10 [ ] checkboxes; references references/solution-architect-review-checklist.md | Companion File: `references/solution-architect-review-checklist.md` (76 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Spec-driven architecture establishing unambiguous service contracts and boundary interfaces.**: Spec-driven architecture establishing unambiguous service contracts and boundary interfaces.
- **Failure domain isolation and bulkhead design with quantitative blast radius and SLO envelopes.**: Failure domain isolation and bulkhead design with quantitative blast radius and SLO envelopes.
- **Rigorous Build vs Buy evaluation matrices and Architecture Decision Records (ADRs).**: Rigorous Build vs Buy evaluation matrices and Architecture Decision Records (ADRs).
- **AI solution assessment distinguishing deterministic rule-based paths from probabilistic LLM workflows.**: AI solution assessment distinguishing deterministic rule-based paths from probabilistic LLM workflows.
- **Technology Radar governance documenting technology evaluation, trial, and adoption guidance.**: Technology Radar governance documenting technology evaluation, trial, and adoption guidance.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Solution Architect (must be declined or routed via Role Handoff):
- Writing routine production application CRUD code (delegated to Specialist Developers).
- Direct hands-on cloud infrastructure provisioning (delegated to AWS / DevOps Engineer).
- `manage-vietnam-accounting`: Live journal and tax auditing belongs to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal corporate legal counsel belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **ARCHITECTURE-SKILL-GOVERNANCE-AST09 LOCK**: Enforce AST09 architectural skill inventory governance; all architectural design skills must be cataloged with an assigned owner, provenance, and risk tier.
- **IDENTITY-FILE-PROTECTION LOCK**: Protect system architectural blueprints, ADR specifications, and core agent rules from unapproved tool modifications (AST10).

---

### 4.30. Site Reliability Engineer (`sre`)

#### Role Metadata & Baseline Status
- **Official Title:** Site Reliability Engineer | **Canonical Slug:** `sre`
- **Common Aliases in INDEX.md:** `@sre`, `@reliability`
- **Mission:** Guarantee software reliability, availability, performance, and operational excellence across distributed systems.
- **Level:** Principal / master-level reliability engineering
- **File Metrics:** 260 lines / 20.7 KB | **Last Updated:** `2026-10-05`
- **Principal Expectations:** 10 items
- **Skill Toolbox:** Primary (6): `debug-runtime-platform`, `troubleshoot-service`, `add-telemetry-instrumentation`, `incident-report`, `performance-profiling`, `orchestrate-chaos-experiment` | Supporting (7): `system-design`, `setup-deployment`, `aws-infrastructure`, `review-service`, `navigate-service`, `manage-secrets`, `review-code`
- **Contract Schema Coverage:** Emits: `incident-report.json` | Disclaims: Does not author feature business logic or override business product decisions.
- **Guardrail Locks:** 12 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 7 [ ] checkboxes; references references/sre-review-checklist.md | Companion File: `references/sre-review-checklist.md` (35 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Service Level Objective (SLO), SLI, and Error Budget policies governing production risk budgets.**: Service Level Objective (SLO), SLI, and Error Budget policies governing production risk budgets.
- **OpenTelemetry distributed tracing span validation verifying complete context propagation across microservices.**: OpenTelemetry distributed tracing span validation verifying complete context propagation across microservices.
- **Incident command protocols and blameless post-mortem standards with actionable prevention items.**: Incident command protocols and blameless post-mortem standards with actionable prevention items.
- **Chaos engineering experimentation (Chaos Mesh, Toxiproxy) validating system steady-state hypotheses.**: Chaos engineering experimentation (Chaos Mesh, Toxiproxy) validating system steady-state hypotheses.
- **Resilience architecture patterns**:  circuit breakers, adaptive load shedding, and bulkhead isolation.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Site Reliability Engineer (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Application business domain logic belongs to Backend Developer.
- `add-ui-component`: Frontend UI component development belongs to Frontend Developer.
- `manage-vietnam-accounting`: Live journal entries belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory advice belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **CHAOS-SKILL-BLAST-RADIUS-AST06 LOCK**: Enforce strictly bounded blast-radius constraints on all chaos injection and performance profiling skills (AST06).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny telemetry agents and monitoring daemons write access to agent system prompt configurations (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.

---

### 4.31. System Engineer (`system-engineer`)

#### Role Metadata & Baseline Status
- **Official Title:** System Engineer | **Canonical Slug:** `system-engineer`
- **Common Aliases in INDEX.md:** `@sysadmin`, `@system`, `@systems-engineer`
- **Mission:** Design, deploy, optimize, and maintain underlying operating systems, container runtimes, storage engines, compute clusters, and network fabrics.
- **Level:** Principal / Lead systems and infrastructure engineer
- **File Metrics:** 470 lines / 40.6 KB | **Last Updated:** `2026-10-24`
- **Principal Expectations:** 12 items
- **Skill Toolbox:** Primary (8): `system-design`, `performance-profiling`, `debug-runtime-platform`, `troubleshoot-service`, `manage-secrets`, `setup-deployment`, `aws-infrastructure`, `setup-gpu-finops` | Supporting (12): `deploy-aws-eks-workloads`, `database-maintenance`, `optimize-postgres`, `review-service`, `navigate-service`, `review-code`, `security-audit`, `supply-chain-security`, `incident-report`, `agent-delegation`, `write-documentation`, `discernment-nudge`
- **Contract Schema Coverage:** Emits: `system-design-spec.json` | Disclaims: Does not author application business logic or design frontend UI components.
- **Guardrail Locks:** 21 named locks in file
- **Security Coverage:** ASI: Moderate integration (references ASI03 Privilege Abuse and ASI04 Supply Chain) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 23 [ ] checkboxes; references references/system-engineer-review-checklist.md | Companion File: `references/system-engineer-review-checklist.md` (135 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Low-level Linux kernel performance tuning**:  sysctl parameters, cgroups v2 resource ceilings, io_uring, and epoll.
- **High-performance networking stack optimization**:  TCP BBR congestion control, DPDK kernel bypass, and MTU tuning.
- **GPU infrastructure and accelerator topology optimization**:  NVIDIA DCGM telemetry, NVLink fabric monitoring, and vLLM runner sizing.
- **Storage engine internals**:  filesystem tuning (ext4, XFS, ZFS), WAL optimization, and disk IOPS scheduling.
- **Cross-layer performance profiling isolating hardware contention from application-level bottlenecks.**: Cross-layer performance profiling isolating hardware contention from application-level bottlenecks.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by System Engineer (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Application business domain logic belongs to Backend Developer.
- `add-ui-component`: Web and mobile presentation belongs to Frontend Developer.
- `manage-vietnam-accounting`: Live journal entries belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal corporate legal opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **SYSTEM-TOOL-PRIVILEGE-AST03 LOCK**: Prohibit system engineering tools from running with root ambient privileges or accessing unauthorized system capabilities (AST03).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny low-level system diagnostic scripts write access to agent personality and operating rulebooks (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.

---

### 4.32. Task Planner (`task-planner`)

#### Role Metadata & Baseline Status
- **Official Title:** Task Planner | **Canonical Slug:** `task-planner`
- **Common Aliases in INDEX.md:** `@planner`, `@task-scheduler`
- **Mission:** Decompose complex initiatives, features, or architectural migrations into clear, dependency-ordered, risk-weighted, and verifiable execution plans.
- **Level:** Principal / Master Task Decomposition and Delivery Planning
- **File Metrics:** 277 lines / 18.0 KB | **Last Updated:** `2026-10-19`
- **Principal Expectations:** 5 items
- **Skill Toolbox:** Primary (2): `design-ux-flow`, `plan-technical-delivery` | Supporting (7): `meeting-review`, `analyze-business-requirements`, `write-product-brief`, `review-service`, `navigate-service`, `write-documentation`, `agent-delegation`
- **Contract Schema Coverage:** Emits: `coordination-plan.json`, `technical-delivery-plan.json` | Disclaims: Does not write production code, make architectural approvals, or execute QA test suites.
- **Guardrail Locks:** 21 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 14 plain bullets; references references/task-planner-review-checklist.md | Companion File: `references/task-planner-review-checklist.md` (114 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Multi-phase dependency Directed Acyclic Graph (DAG) modeling preventing circular deadlocks.**: Multi-phase dependency Directed Acyclic Graph (DAG) modeling preventing circular deadlocks.
- **Thin vertical slicing decomposing complex capabilities into independently verifiable work increments.**: Thin vertical slicing decomposing complex capabilities into independently verifiable work increments.
- **Explicit quality verification gates between delivery slices preventing error compounding.**: Explicit quality verification gates between delivery slices preventing error compounding.
- **Token budget allocation per slice preventing context window exhaustion during agentic execution.**: Token budget allocation per slice preventing context window exhaustion during agentic execution.
- **Anti-cascade buffering isolating risky experimental tasks behind explicit fallback branches.**: Anti-cascade buffering isolating risky experimental tasks behind explicit fallback branches.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Task Planner (must be declined or routed via Role Handoff):
- `commit-code`: Source code modifications belong to developer roles.
- `setup-deployment`: Cloud hosting deployments belong to DevOps Engineer.
- `manage-vietnam-accounting`: Live accounting journals belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory advice belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **PLANNING-SKILL-AST09 LOCK**: Maintain verifiable dependency DAG models and task delegation records under AST09 governance.
- **IDENTITY-FILE-PROTECTION LOCK**: Protect execution plan schemas and coordination contracts from unauthenticated tool mutations (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.33. Teacher (`teacher`)

#### Role Metadata & Baseline Status
- **Official Title:** Teacher | **Canonical Slug:** `teacher`
- **Common Aliases in INDEX.md:** `@teacher`, `@instructor`, `@educator`, `@mentor`
- **Mission:** Design, deliver, and evaluate structured, curriculum-aligned, and pedagogy-grounded educational programs and practice exercises.
- **Level:** Principal / Master Pedagogical and Instructional Engineering
- **File Metrics:** 298 lines / 26.6 KB | **Last Updated:** `2026-09-05`
- **Principal Expectations:** 9 items
- **Skill Toolbox:** Primary (3): `design-learning-plan`, `create-exercises`, `grade-and-review` | Supporting (6): `conduct-research`, `write-documentation`, `analyze-data`, `write-article`, `xlsx`, `agent-delegation`
- **Contract Schema Coverage:** Emits: `learning-assessment-report.json`, `learning-handoff.json` | Disclaims: Does not author production software code, manage cloud server infrastructure, or issue legal opinions.
- **Guardrail Locks:** 10 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 6 [ ] checkboxes; references references/teacher-review-checklist.md | Companion File: `references/teacher-review-checklist.md` (47 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Non-Compliant (Lock Deficit < 12)**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Zone of Proximal Development (ZPD) scaffolding providing dynamic instructional support without cognitive overload.**: Zone of Proximal Development (ZPD) scaffolding providing dynamic instructional support without cognitive overload.
- **Spaced Repetition scheduling optimizing memory retention via SM-2 and Leitner algorithms.**: Spaced Repetition scheduling optimizing memory retention via SM-2 and Leitner algorithms.
- **Cognitive exercise design aligned with Bloom's Taxonomy and Webb's Depth of Knowledge (DOK 1-4).**: Cognitive exercise design aligned with Bloom's Taxonomy and Webb's Depth of Knowledge (DOK 1-4).
- **AI-resistant assessment construction emphasizing authentic demonstration, synthesis, and critical defense.**: AI-resistant assessment construction emphasizing authentic demonstration, synthesis, and critical defense.
- **Four-tier analytic rubrics providing deterministic, transparent, and actionable learner feedback.**: Four-tier analytic rubrics providing deterministic, transparent, and actionable learner feedback.

#### Identified Standardization Gaps
- Rubric C14: Guardrail lock deficit (10 locks vs minimum 12 required by SOTA rubric).
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Teacher (must be declined or routed via Role Handoff):
- `commit-code`: Production software engineering belongs to developer roles.
- `setup-deployment`: Cloud hosting deployments belong to DevOps Engineer.
- `manage-vietnam-accounting`: Live journal entries belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal statutory legal counsel belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **ZPD-SCAFFOLDING-GATE LOCK**: Instructional materials must assess baseline competency and advance strictly within the learner's Zone of Proximal Development; cognitive overload jumps are prohibited.
- **SPACED-REPETITION-SCHEDULE LOCK**: Review intervals must follow algorithmic memory consolidation curves (SM-2 / Leitner); unspaced cramming sequences are rejected.
- **AI-RESISTANT-ASSESSMENT LOCK**: Assessments must evaluate Webb DOK 3-4 problem solving and synthesis; easily automatable recall questions are restricted to basic checks.
- **COGNITIVE-ERROR-DIAGNOSIS LOCK**: Formative evaluation must pinpoint conceptual misconceptions rather than providing superficial answer keys.
- **SKILL-PEDAGOGY-AST01 LOCK**: Prohibit third-party exercise scraping skills with unverified curriculum sources (AST01).
- **IDENTITY-FILE-PROTECTION LOCK**: Protect pedagogical standards and learner assessment rubrics from unauthorized tool modification (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.

---

### 4.34. Technical Architect (`technical-architect`)

#### Role Metadata & Baseline Status
- **Official Title:** Technical Architect | **Canonical Slug:** `technical-architect`
- **Common Aliases in INDEX.md:** `@tech-architect`, `@enterprise-architect`
- **Mission:** Govern enterprise architecture, evolutionary design principles, technical standards, and cross-system integrations across software ecosystems.
- **Level:** Principal / Master Enterprise Architecture
- **File Metrics:** 536 lines / 48.9 KB | **Last Updated:** `2026-10-19`
- **Principal Expectations:** 12 items
- **Skill Toolbox:** Primary (6): `system-design`, `agent-panel-meeting`, `meeting-review`, `write-tech-radar`, `architect-mcp-server`, `decompose-agentic-system` | Supporting (12): `ai-risk-assessment`, `review-service`, `navigate-service`, `conduct-research`, `scaffold-new-service`, `review-code`, `security-audit`, `supply-chain-security`, `setup-deployment`, `agent-delegation`, `write-documentation`, `discernment-nudge`
- **Contract Schema Coverage:** Emits: `adr-spec.json`, `architecture-options.json` | Disclaims: Does not author routine day-to-day application feature code, manage sprint backlogs, or override product goals.
- **Guardrail Locks:** 19 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 41 plain bullets across 4 sections; references references/technical-architect-review-checklist.md | Companion File: `references/technical-architect-review-checklist.md` (72 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Evolutionary architecture governance leveraging automated architectural fitness functions.**: Evolutionary architecture governance leveraging automated architectural fitness functions.
- **Six-round multi-role cross-examination panel meetings (`agent-panel-meeting`) producing decision-ready JSON contracts.**: Six-round multi-role cross-examination panel meetings (`agent-panel-meeting`) producing decision-ready JSON contracts.
- **Enterprise Model Context Protocol (MCP) server architecture with boundary validation and tool discovery standards.**: Enterprise Model Context Protocol (MCP) server architecture with boundary validation and tool discovery standards.
- **Recursive decomposition of complex multi-agent swarms into bounded contexts.**: Recursive decomposition of complex multi-agent swarms into bounded contexts.
- **Enterprise Technology Radar authoring tracking strategic technology adoption across platforms.**: Enterprise Technology Radar authoring tracking strategic technology adoption across platforms.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Technical Architect (must be declined or routed via Role Handoff):
- Writing routine day-to-day application feature code (delegated to Specialist Developers).
- Managing sprint backlogs and velocity tracking (delegated to Project Manager).
- `manage-vietnam-accounting`: Live journal and tax entries belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal corporate legal opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **ENTERPRISE-SKILL-SUPPLY-CHAIN-AST02 LOCK**: Enterprise architecture skills must verify cryptographic provenance and enforce AST02 supply chain gating on all incorporated software assets.
- **IDENTITY-FILE-PROTECTION LOCK**: Protect enterprise architectural standards, ADR registers, and core agent rules from unapproved tool modifications (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.35. Technical Lead (`technical-lead`)

#### Role Metadata & Baseline Status
- **Official Title:** Technical Lead | **Canonical Slug:** `technical-lead`
- **Common Aliases in INDEX.md:** `@lead`, `@tech-lead`, `@engineering-lead`
- **Mission:** Lead engineering delivery, maintain technical quality, guide architectural implementation, and mentor developers across delivery squads.
- **Level:** Principal / Lead Engineering Delivery & Quality
- **File Metrics:** 367 lines / 26.8 KB | **Last Updated:** `2026-09-05`
- **Principal Expectations:** 9 items
- **Skill Toolbox:** Primary (7): `plan-technical-delivery`, `review-code`, `meeting-review`, `agent-quality-gate`, `agent-prompt-lifecycle`, `ai-risk-assessment`, `add-telemetry-instrumentation` | Supporting (14): `review-service`, `navigate-service`, `scaffold-new-service`, `performance-profiling`, `agent-delegation`, `write-tests`, `commit-code`, `create-migration`, `troubleshoot-service`, `agent-observability`, `security-audit`, `supply-chain-security`, `agent-graph-orchestration`, `agent-model-routing`
- **Contract Schema Coverage:** Emits: `technical-delivery-plan.json` | Disclaims: Does not override enterprise architecture principles, bypass QA release gates, or ignore security findings.
- **Guardrail Locks:** 11 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 7 [ ] checkboxes; references references/technical-lead-review-checklist.md | Companion File: `references/technical-lead-review-checklist.md` (57 lines)
- **Decision Boundaries Syntax:** Standardized Bold (`- **owns**:`)
- **Compliance Evaluation:** **Non-Compliant (Lock Deficit < 12)**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Spec-driven delivery breakdown decomposing complex initiatives into verifiable technical delivery plans.**: Spec-driven delivery breakdown decomposing complex initiatives into verifiable technical delivery plans.
- **Failure domain isolation and blast radius containment utilizing progressive delivery and canary rollouts.**: Failure domain isolation and blast radius containment utilizing progressive delivery and canary rollouts.
- **Technical debt governance allocating 20% of engineering bandwidth to continuous refactoring and debt reduction.**: Technical debt governance allocating 20% of engineering bandwidth to continuous refactoring and debt reduction.
- **Engineering review quality gates enforcing code standards, test coverage, and documentation parity.**: Engineering review quality gates enforcing code standards, test coverage, and documentation parity.
- **Prompt asset lifecycle governance tracking prompt versioning and empirical evaluation benchmarks.**: Prompt asset lifecycle governance tracking prompt versioning and empirical evaluation benchmarks.

#### Identified Standardization Gaps
- Rubric C14: Guardrail lock deficit (11 locks vs minimum 12 required by SOTA rubric).
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Technical Lead (must be declined or routed via Role Handoff):
- Overriding enterprise architectural standards without formal ADR sign-off (Technical Architect owns).
- Bypassing automated QA regression gates or security release blocks.
- `manage-vietnam-accounting`: Live accounting journals belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **SPEC-DRIVEN-SLICING LOCK**: Engineering delivery tasks must be broken into independently verifiable vertical slices with explicit quality gates; monolithic pull requests are rejected fail-closed.
- **BLAST-RADIUS-CONTAINMENT LOCK**: System modifications must isolate failure domains via feature flags, bulkheads, or progressive canary deployments; unhedged deployments are prohibited.
- **TECH-DEBT-BUDGET LOCK**: Technical Lead must allocate a minimum 20% capacity budget for technical debt remediation, refactoring, and dependency upgrades in every delivery cycle.
- **SKILL-CODE-REVIEW-AST08 LOCK**: Code review tooling and automated inspection skills must satisfy AST08 pre-flight scanning standards before passing quality gates.
- **IDENTITY-FILE-PROTECTION LOCK**: Protect engineering delivery policies and squad operating standards from unauthorized tool modification (AST10).

---

### 4.36. Technical Writer (`technical-writer`)

#### Role Metadata & Baseline Status
- **Official Title:** Technical Writer | **Canonical Slug:** `technical-writer`
- **Common Aliases in INDEX.md:** `@tech-writer`, `@doc-writer`, `@docs`, `@documentation-writer`
- **Mission:** Author, maintain, and structure high-quality technical documentation that enables developers, operators, and AI agents to understand, integrate, and operate systems effectively.
- **Level:** Principal / Lead Technical Writer
- **File Metrics:** 359 lines / 26.8 KB | **Last Updated:** `2026-10-19`
- **Principal Expectations:** 6 items
- **Skill Toolbox:** Primary (4): `write-documentation`, `release-notes`, `configure-llms-txt`, `pdf` | Supporting (10): `write-tech-radar`, `agent-delegation`, `navigate-service`, `meeting-review`, `review-service`, `manage-api-catalog`, `configure-mcp`, `write-article`, `accessibility-review`, `ai-risk-assessment`
- **Contract Schema Coverage:** Emits: `documentation-handoff.json` | Disclaims: Does not write production application code, modify cloud infrastructure, or author marketing promotional copy.
- **Guardrail Locks:** 15 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 21 plain bullets across 4 sections; references references/technical-writer-review-checklist.md | Companion File: `references/technical-writer-review-checklist.md` (120 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Diátaxis documentation framework organizing technical knowledge into Tutorials, How-To Guides, Reference, and Explanation.**: Diátaxis documentation framework organizing technical knowledge into Tutorials, How-To Guides, Reference, and Explanation.
- **Machine-readable documentation for AI agents**:  `/llms.txt`, `/llms-full.txt`, and RFC 9727 API Catalog integration.
- **Standardized release notes governance following Keep a Changelog and Semantic Versioning (SemVer) specifications.**: Standardized release notes governance following Keep a Changelog and Semantic Versioning (SemVer) specifications.
- **Automated documentation verification testing code examples, link validity, and command copy-paste accuracy.**: Automated documentation verification testing code examples, link validity, and command copy-paste accuracy.
- **Structured documentation metadata integration with Schema.org JSON-LD (TechArticle, APIReference).**: Structured documentation metadata integration with Schema.org JSON-LD (TechArticle, APIReference).

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Technical Writer (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Production backend application code belongs to Backend Developer.
- `setup-deployment`: Cloud hosting and infrastructure configuration belong to DevOps Engineer.
- `manage-vietnam-accounting`: Financial and tax ledgers belong to Vietnam Accounting Specialist.
- `draft-legal-opinion`: Formal legal regulatory advice belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **DOCS-SKILL-ACCURACY-AST01 LOCK**: Prohibit third-party documentation generation skills that inject hallucinated CLI commands or unverified API endpoints (AST01).
- **IDENTITY-FILE-PROTECTION LOCK**: Protect documentation style guides and agent operating rules from external documentation tool overwrites (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.37. UI/UX Designer (`ui-ux-designer`)

#### Role Metadata & Baseline Status
- **Official Title:** UI/UX Designer | **Canonical Slug:** `ui-ux-designer`
- **Common Aliases in INDEX.md:** `@designer`, `@ui`, `@ux`, `@ui-ux`, `@uiux`
- **Mission:** Craft intuitive, accessible, visually compelling, and cohesive user experiences across digital touchpoints — translating user needs and business goals into clear user journeys and production-ready design tokens.
- **Level:** Principal / Lead Product Experience Designer
- **File Metrics:** 411 lines / 36.2 KB | **Last Updated:** `2026-10-24`
- **Principal Expectations:** 13 items
- **Skill Toolbox:** Primary (6): `design-ux-flow`, `design-review`, `design-system-engineering`, `anti-ui-slop-finish-gate`, `pptx`, `design-md-specification` | Supporting (7): `meeting-review`, `navigate-service`, `accessibility-review`, `analyze-business-requirements`, `write-product-brief`, `write-documentation`, `agent-delegation`
- **Contract Schema Coverage:** Emits: `design-tokens-spec.json`, `ui-component-spec.json`, `ux-flow-spec.json` | Disclaims: Does not write backend server code, author database migrations, or configure server networking.
- **Guardrail Locks:** 24 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 52 plain bullets across 4 sections; references references/ui-ux-designer-review-checklist.md | Companion File: `references/ui-ux-designer-review-checklist.md` (126 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Two-tier design token architecture separating semantic intent from raw platform primitives.**: Two-tier design token architecture separating semantic intent from raw platform primitives.
- **Perceptual OKLCH color ramp generation ensuring uniform perceived lightness across palettes.**: Perceptual OKLCH color ramp generation ensuring uniform perceived lightness across palettes.
- **Concentric border radii calculation enforcing visual harmony**:  R_outer = R_inner + padding.
- **Accessible APCA contrast verification satisfying modern advanced typography standards.**: Accessible APCA contrast verification satisfying modern advanced typography standards.
- **100% interaction state coverage**:  Default, Hover, Focus-Visible, Active, Disabled, Loading, Empty, Error.
- **Anti-UI Slop finish gate rejecting low-effort generic UI templates and enforcing optical padding compensation.**: Anti-UI Slop finish gate rejecting low-effort generic UI templates and enforcing optical padding compensation.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').
- Rubric C17: '## Review Checklist' uses plain bullets rather than standardized interactive task checkboxes ('- [ ]').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by UI/UX Designer (must be declined or routed via Role Handoff):
- `add-api-endpoint`: Backend server endpoints belong to Backend Developer.
- `create-migration`: Relational database DDL belongs to Backend Developer.
- `setup-deployment`: Cloud hosting deployments belong to DevOps Engineer.
- `manage-vietnam-legal`: Legal contract dispute representation belongs to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **DESIGN-SKILL-TOKEN-AST04 LOCK**: Validate all design token generation and Figma integration skills against structured YAML/JSON schema definitions (AST04).
- **IDENTITY-FILE-PROTECTION LOCK**: Protect design token standards and UI component specifications from unauthorized external tool mutations (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.
- Convert Review Checklist items to standardized '- [ ]' interactive checkboxes.

---

### 4.38. Vietnam Accounting Specialist (`vietnam-accounting-specialist`)

#### Role Metadata & Baseline Status
- **Official Title:** Vietnam Accounting Specialist | **Canonical Slug:** `vietnam-accounting-specialist`
- **Common Aliases in INDEX.md:** `@accounting`, `@accountant`, `@ke-toan`, `@vietnam-accounting`
- **Mission:** Ensure financial integrity, statutory compliance, tax adherence, and robust accounting controls under Vietnamese Accounting Standards (VAS) and Circular 200/2014/TT-BTC / Circular 133/2016/TT-BTC.
- **Level:** Principal / master-level Vietnam accounting domain leadership
- **File Metrics:** 317 lines / 29.5 KB | **Last Updated:** `2026-09-05`
- **Principal Expectations:** 8 items
- **Skill Toolbox:** Primary (1): `manage-vietnam-accounting` | Supporting (6): `analyze-business-requirements`, `analyze-data`, `conduct-research`, `security-audit`, `write-documentation`, `agent-delegation`
- **Contract Schema Coverage:** Emits: `accounting-compliance-review.json`, `period-end-closing-report.json` | Disclaims: Does not take final tax positions, issue formal legal opinions, post live ledger entries directly, or write software code.
- **Guardrail Locks:** 14 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 7 [ ] checkboxes; references references/vietnam-accounting-specialist-review-checklist.md | Companion File: `references/vietnam-accounting-specialist-review-checklist.md` (53 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Compliant with Minor Gaps**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Circular 200 vs Circular 133 dual regime governance and VFRS convergence alignment.**: Circular 200 vs Circular 133 dual regime governance and VFRS convergence alignment.
- **E-invoice verification under Decree 123/2020/ND-CP and Circular 78/2021/TT-BTC**:  Decision 1450 XML parsing, GDT status 03/04 screening, and 20M VND non-cash payment rule.
- **Deterministic 3-way matching (PO - GRN - Invoice) with GRNI cut-off accounting (TK 151 / TK 3388).**: Deterministic 3-way matching (PO - GRN - Invoice) with GRNI cut-off accounting (TK 151 / TK 3388).
- **Decree 132/2020/ND-CP related-party net interest expense cap (30% EBITDA limitation, negative EBITDA zero-deduction, 5-year carry-forward).**: Decree 132/2020/ND-CP related-party net interest expense cap (30% EBITDA limitation, negative EBITDA zero-deduction, 5-year carry-forward).
- **Period-end closing integrity enforcing Account 911 zero-clearing and immutable audit trail preservation.**: Period-end closing integrity enforcing Account 911 zero-clearing and immutable audit trail preservation.

#### Identified Standardization Gaps
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Vietnam Accounting Specialist (must be declined or routed via Role Handoff):
- Posting or altering live accounting ledger entries directly without human controller review.
- `commit-code`: Source code modifications belong to developer roles.
- `setup-deployment`: Cloud hosting and CI/CD pipelines belong to DevOps Engineer.
- `draft-legal-opinion`: Formal corporate legal opinions belong to Vietnam Legal Counsel.
```

##### Architectural Guardrail Locks to Codify:
- **ACCOUNTING-DATA-PRIVACY-AST03 LOCK**: Prohibit external financial calculation skills possessing the lethal trifecta (handling corporate revenue/tax data + arbitrary endpoints + external egress) (AST03).
- **IDENTITY-FILE-PROTECTION LOCK**: Deny accounting verification scripts write access to root agent governance rules (AST10).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.

---

### 4.39. Vietnam Legal Counsel (`vietnam-legal-counsel`)

#### Role Metadata & Baseline Status
- **Official Title:** Vietnam Legal Counsel | **Canonical Slug:** `vietnam-legal-counsel`
- **Common Aliases in INDEX.md:** `@vietnam-legal-counsel`, `@lawyer`, `@luat-su`, `@legal`, `@legal-counsel`
- **Mission:** Provide specialized legal analysis, regulatory assessment, contract drafting guidance, and compliance reviews under the laws of the Socialist Republic of Vietnam.
- **Level:** Principal / Master Legal Leadership
- **File Metrics:** 306 lines / 33.3 KB | **Last Updated:** `2026-09-29`
- **Principal Expectations:** 8 items
- **Skill Toolbox:** Primary (3): `manage-vietnam-legal`, `audit-ai-compliance`, `draft-legal-opinion` | Supporting (5): `conduct-research`, `analyze-business-requirements`, `security-audit`, `write-documentation`, `agent-delegation`
- **Contract Schema Coverage:** Emits: `legal-compliance-review.json`, `legal-opinion-contract.json` | Disclaims: Does not provide external court representation, issue tax advice, execute commercial contracts, or author software code.
- **Guardrail Locks:** 12 named locks in file
- **Security Coverage:** ASI: Baseline security lock in guardrails (ASI Top 10 2026) | AST: 0 explicit references (relies on role-standard.md)
- **Checklist Architecture:** 9 [ ] checkboxes; references references/vietnam-legal-counsel-review-checklist.md | Companion File: `references/vietnam-legal-counsel-review-checklist.md` (31 lines)
- **Decision Boundaries Syntax:** Unbolded Plain (`- owns ...`)
- **Compliance Evaluation:** **Non-Compliant (Missing Failure Modes)**

#### Strengths & Domain-Specific Capabilities to Preserve
- **Vietnamese statutory analysis across Civil Code 2015, Law on Enterprises 2020, and Commercial Law 2005 (8% breach penalty cap under Article 301).**: Vietnamese statutory analysis across Civil Code 2015, Law on Enterprises 2020, and Commercial Law 2005 (8% breach penalty cap under Article 301).
- **Personal Data Protection Law (PDPL) No. 91/2025/QH15 and Decree 356/2025/ND-CP compliance**:  mandatory DPIA/TIA records, consent records, and DPO requirements.
- **Vietnam Law on Artificial Intelligence No. 134/2025/QH15 compliance**:  4-tier risk classification, conformity assessment, and mandatory incident reporting (24-72h).
- **Formal legal opinion authoring following the standardized 7-field structure with explicit statutory authority citations.**: Formal legal opinion authoring following the standardized 7-field structure with explicit statutory authority citations.
- **Strict disclaimer against unauthorized practice of law and mandatory Human-in-the-Loop (HITL) qualified lawyer review gate.**: Strict disclaimer against unauthorized practice of law and mandatory Human-in-the-Loop (HITL) qualified lawyer review gate.

#### Identified Standardization Gaps
- Rubric C18: Missing '## Failure Modes' section entirely.
- Rubric C14/C15: Missing explicit '### Prohibited Skills' subsection under '## Skill Toolbox'.
- Rubric C14: Missing explicit OWASP AST10 skill security governance locks in '## Guardrails'.
- Rubric C11: '## Decision Boundaries' uses unbolded plain syntax ('- owns ...', '- does not own ...').

#### Concrete Standardization Specification (Phase R2)

##### Explicit Prohibited Skills Specification:
```markdown
### Prohibited Skills

The following skills are strictly prohibited from execution by Vietnam Legal Counsel (must be declined or routed via Role Handoff):
- Providing formal court representation or unauthorized external practice of law.
- `manage-vietnam-accounting`: Live tax accounting and journal entries belong to Vietnam Accounting Specialist.
- `commit-code`: Production software engineering belongs to developer roles.
- `setup-deployment`: Cloud hosting deployments belong to DevOps Engineer.
```

##### Architectural Guardrail Locks to Codify:
- **STATUTORY-AUTHORITY-AST01 LOCK**: Legal analysis skills must verify that cited statutory articles are currently active in the National Database of Legal Normative Documents; repealed or unverified provisions are rejected fail-closed.
- **COMMERCIAL-PENALTY-CAP LOCK**: Breach penalty clauses in commercial contracts must be capped at 8% of the breached obligation value under Commercial Law 2005 Article 301; higher penalty terms are flagged invalid.
- **HITL-LEGAL-APPROVAL-AST09 LOCK**: Every generated legal opinion must pass an explicit Human-in-the-Loop approval gate before external issuance (AST09).
- **IDENTITY-FILE-PROTECTION LOCK**: Protect enterprise legal compliance policies and agent boundaries from unauthorized tool modification (AST10).

#### Failure Modes to Incorporate (Phase R2):
- **Outdated or repealed statutory authority citation**:  legal advice relies on superseded laws or decrees, creating severe regulatory exposure.
  - *Mitigation:* Verify active statutory validity via the National Database of Legal Normative Documents (vbpl.vn); confirm amending decrees and circulars before citing.
- **Exceeding statutory penalty caps in commercial contract dispute advice**:  advising a client that penalty clauses exceeding 8% are enforceable.
  - *Mitigation:* Enforce Commercial Law 2005 Article 301 invariant (8% breach penalty cap); flag exceeding clauses as unenforceable while separating liquidated damages.
- **Non-compliant personal data processing advice under PDPL No. 91/2025/QH15**:  permitting cross-border transfer or data processing without valid consent or TIA.
  - *Mitigation:* Verify valid express consent, mandatory DPIA/TIA records, and DPO appointment prior to approving personal data workflows under Decree 356/2025/ND-CP.
- **Unauthorized practice of law representation**:  AI output framed as binding external legal representation rather than internal analysis.
  - *Mitigation:* Mandate prominent statutory disclaimer in all opinions; enforce Human-in-the-Loop (HITL) qualified lawyer review gate before external release.
- **Missing 4-tier risk classification under Vietnam AI Law No. 134/2025/QH15**:  deploying AI decision engines without mandatory conformity assessment.
  - *Mitigation:* Screen every automated decision system against high-risk criteria under AI Law No. 134; enforce conformity assessment and incident reporting procedures (24-72h).

#### Formatting Normalizations:
- Format Decision Boundaries to use standardized '- **owns**:', '- **does not own**:', and '- **must escalate**:' bullets.

---

## 5. 2026–2027 SOTA Agent Architecture Standards

Standardizing the 39 role definitions requires full alignment with 2026–2027 state-of-the-art agentic systems principles:

### 5.1 A2A 1.0 Protocol Lifecycle & Cryptographic Discovery
1. **Agent Card Discovery (`/.well-known/agent-card.json`)**: Every role definition corresponds to an official Agent Card adhering to the A2A 1.0 schema in `core/a2a/registry/<role>.agent-card.json`.
2. **Cryptographic Identity & JWS Signatures**: Agent cards and emitted coordination artifacts must be signed using JSON Web Signatures (JWS) verified via RFC 8785 JSON Canonicalization Scheme (JCS) and key IDs (`kid` / `jku`).
3. **Canonical Task Lifecycle States**:
   $$\text{TASK\_STATE\_SUBMITTED} \longrightarrow \text{TASK\_STATE\_WORKING} \longrightarrow \begin{cases} \text{TASK\_STATE\_INPUT\_REQUIRED} \\ \text{TASK\_STATE\_COMPLETED} \\ \text{TASK\_STATE\_FAILED} \\ \text{TASK\_STATE\_CANCELED} \end{cases}$$
4. **Structured Wire Formats & Error Envelopes**: Task payloads strictly use the unified v1.0 `Part` object (discriminating `text`, `file`, and `data` parts without arbitrary `kind` properties) and standard `google.rpc.Status` error envelopes with domain `a2a-protocol.org`.
5. **Streaming Lifecycle Events**: For asynchronous long-running tasks, progress must be emitted over Server-Sent Events (SSE) across the 7 canonical lifecycle events: `task.created`, `task.status`, `task.message`, `task.artifact`, `task.completed`, `task.failed`, `task.canceled`.

### 5.2 Non-Human Identity (NHI) & Workload Identity Federation (WIMSE)
1. **Verifiable Workload Identity**: Agents operate strictly under an ephemeral, scoped Non-Human Identity (NHI). Under no circumstances may an agent inherit the ambient authority or long-lived credentials of the human caller.
2. **Short-Lived Workload Identity Tokens**: Integration with external services must use SPIFFE/SVID issuance and WIMSE-style (Workload Identity in Multi-System Environments) short-lived tokens via RFC 8693 token exchange rather than standing API keys.
3. **Execution-Time Authorization (Fail-Closed)**: A signed instruction is not settlement, and tool selection is not execution. Consequential actions (financial payments, database DDL, production deployment, git push) require execution-time authorization checks under mandate limits. If policy evaluation fails, execution must fail-closed immediately.
4. **Identity & Memory File Protection (AST10)**: Deny-write file policies must protect agent identity files (`AGENTS.md`, `MEMORY.md`, `.cursor/rules`, system prompts). Tools and skills must never have write access to the files governing their own operating contracts.

### 5.3 Five-Tier Context Budgeting & Lost-in-the-Middle Mitigation
1. **Attention Allocation Invariants**: To prevent lost-in-the-middle context degradation, system prompts and context building pipelines must allocate tokens deterministically:
   $$\text{Primacy (Top 15\%)} \longleftrightarrow \text{Recency (Bottom 15\%)}$$
2. **Deterministic Partitioning**:
   - **Tier 1: System Invariants & Output Schemas (15%)**: Immutable behavioral rules, JSON schemas, and lock definitions.
   - **Tier 2: Dynamic Task Grounding (35%)**: Ticket descriptions, explicit constraints, input artifacts, and file references.
   - **Tier 3: Working Memory & History (25%)**: Turn-by-turn context from the active session (compacted at 60/80 triggers).
   - **Tier 4: Scratchpad & Intermediate Reasoning (10%)**: Transient thought tokens and intermediate calculation buffers.
   - **Tier 5: Output Generation Reserve (15%)**: Dedicated headroom for structured JSON or markdown generation.
3. **Prefix Cache Stability**: Invariant system prompt prefixes must remain bitwise identical across conversational turns to maximize LLM KV-cache reuse and reduce p95 latency.
4. **Semantic Deduplication**: Context building pipelines must apply syntactic 4-gram and semantic vector cosine deduplication (threshold $\ge 0.88$) to eliminate redundant tokens.

### 5.4 Prompt Asset Lifecycle Governance & Adversarial Hardening
1. **Prompts as Software Assets**: Prompts must be treated as version-controlled software assets with explicit parameter typing, change logs, and semantic versioning (`agent-prompt-lifecycle`).
2. **Empirical Evaluation Gates**: Automated LLM-as-a-judge evaluators must be calibrated to achieve $\ge 85\%$ statistical agreement (Cohen's Kappa $\ge 0.85$) against human ground truth before prompt changes are promoted.
3. **Adversarial Delimiter Isolation**: Untrusted external inputs must be isolated using structural delimiter tags (`<untrusted_data id="...">`) combined with ephemeral canary nonces to prevent instruction leakage and jailbreaking.

---


## 6. Actionable Standardization Implementation Plan (Phase R2 Roadmap)

To execute the standardization across all 39 roles safely without regressions, Phase R2 organizes implementation into three sequential batches:

### 6.1 Phased Execution Batches

```
+-------------------------------------------------------------------------------------------------------+
|                                    PHASE R2 EXECUTION BATCH SCHEDULE                                  |
+-------------------------------------------------------------------------------------------------------+
| BATCH A: Foundation & Infrastructure Roles (Roles 1–13)                                               |
| - Roles: 3d-graphics-engineer, agent-coordinator, agent-discovery-engineer, ai-systems-engineer,     |
|   aws-engineer, backend-developer, business-analyst, cloudflare-engineer, content-manager,            |
|   content-writer, data-analyst, data-engineer, devops-engineer.                                       |
| - Key Tasks: Add Prohibited Skills, codify AST10 locks, normalize Decision Boundaries bold syntax,     |
|   standardize Review Checklist checkboxes [-].                                                       |
+-------------------------------------------------------------------------------------------------------+
| BATCH B: Application, Growth & Remediation Roles (Roles 14–26)                                        |
| - Roles: ecommerce-engineer, frontend-developer, game-developer, mmo-engineer, mobile-engineer,       |
|   product-manager, project-manager, prompt-engineer, qa-engineer, researcher, reverse-engineer,        |
|   reviewer, sdet.                                                                                     |
| - Critical Remediation: Author ## Failure Modes for game-developer, prompt-engineer, sdet; expand     |
|   guardrail locks >= 12; add Prohibited Skills and AST10 locks across all 13 roles.                   |
+-------------------------------------------------------------------------------------------------------+
| BATCH C: Architecture, Advisory & Compliance Roles (Roles 27–39)                                     |
| - Roles: security-engineer, seo-analyst, solution-architect, sre, system-engineer, task-planner,      |
|   teacher, technical-architect, technical-lead, technical-writer, ui-ux-designer,                     |
|   vietnam-accounting-specialist, vietnam-legal-counsel.                                               |
| - Critical Remediation: Author ## Failure Modes for vietnam-legal-counsel; expand locks for teacher   |
|   and technical-lead >= 12; add Prohibited Skills and AST10 locks across all 13 roles.                |
+-------------------------------------------------------------------------------------------------------+
```

### 6.2 Architectural Invariants & Safety Rules for Phase R2
1. **Invariant 1: Continuous Zero-Regression Validation**: After modifying each batch, all 10 automated repository validators (`validate-roles.py`, `validate-2026-compliance.py`, `validate-skill-ownership.py`, `validate-contract-coverage.py`, `validate-policy-consistency.py`, `validate-agent-cards.py`, `validate-a2a-compliance.py`, `validate-standardization.py`, `validate-indexes.py`, `validate-version-sync.py`) must pass with 100% exit code 0.
2. **Invariant 2: Domain Capabilities Verbatim Preservation**: Under no circumstances may domain-specific frameworks, algorithms, or statutory standards (e.g. Go 1.25+ Hexagonal, PagedAttention v3, Circular 200/133, PDPL No. 91/2025, OpenTofu KMS, React 19, REA MCP) be diluted or deleted during standardization.
3. **Invariant 3: Markdown Inline Metadata Preservation**: Role files must preserve their H1 + Mission + Level + Standard Reference lines (Lines 1–7) without injecting YAML frontmatter blocks (`---`), ensuring compatibility with `validate-roles.py`.
4. **Invariant 4: Skill Toolbox Disjointness**: Primary Skills and Supporting Skills must remain strictly disjoint (zero overlap), and all referenced skills must exist in `core/skills/`.
5. **Invariant 5: Index & Catalog Bitwise Synchronization**: Upon completing each batch, run `python core/scripts/generate-index.py --check` to guarantee 100% catalog synchronization with `INDEX.md`.

### 6.3 Automated Verification & Acceptance Checklist

Before declaring Milestone M2 / Phase R2 complete, the following verification commands must execute cleanly:

```powershell
# Set workspace location
Set-Location d:\myproject\agent-skills

# 1. Verify role structural and rubric compliance across all 39 roles
python core/scripts/validate-roles.py

# 2. Verify 2026 A2A compliance and policy-as-code mapping
python core/scripts/validate-2026-compliance.py -v

# 3. Verify skill ownership and primary/supporting separation
python core/scripts/validate-skill-ownership.py

# 4. Verify contract schema coverage across all 39 roles
python core/scripts/validate-contract-coverage.py

# 5. Verify policy consistency against irreversible action standards
python core/scripts/validate-policy-consistency.py

# 6. Verify agent card discovery schemas
python core/scripts/validate-agent-cards.py

# 7. Verify full A2A 1.0 lifecycle compliance
python core/scripts/validate-a2a-compliance.py

# 8. Verify standardization score (>= 90%)
python core/scripts/validate-standardization.py

# 9. Verify catalog index synchronization
python core/scripts/validate-indexes.py
python core/scripts/generate-index.py --check

# 10. Execute dedicated role challenge test suites
pytest tests/test_tier3_roles_upgrade_challenge.py tests/test_tier3_empirical_challenger.py tests/test_qa_engineer_modernization_challenge.py tests/test_security_engineer_modernization_challenge.py tests/test_solution_architect_modernization_challenge.py tests/test_ai_systems_engineer_platform_challenge.py tests/test_aws_engineer_platform_challenge.py tests/test_backend_modernization_challenge.py
```

---

## 7. Report Attestation & Sign-Off

This audit report has been compiled through genuine static analysis, AST token extraction, and direct validator execution across all 39 role definition files in `agent-skills/core/roles/`. All quantitative metrics, identified gaps, and standardization specifications are empirically verifiable against the live repository state.

- **Author:** Master Audit Author (`teamwork_worker_m1`)
- **Review Status:** Ready for Orchestrator Review & Teamwork Auditor Verification
- **Handoff Destination:** `d:\myproject\.agents\teamwork\teamwork_worker_m1\handoff.md`
- **Downstream Milestone:** Milestone M2 — 39 Role Definitions Standardization Execution (Phase R2)

*Report completed and delivered on 2026-11-04.*
