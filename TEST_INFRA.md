# Test Infrastructure Specification: Phase 3 Two-Tier JIT Skill Discovery & Adapter Alignment

## 1. Overview & Purpose
This document specifies the comprehensive End-to-End (E2E) testing infrastructure for Phase 3 of the Agent-Skills repository modernisation. Phase 3 establishes the Two-Tier Just-In-Time (JIT) Skill Discovery & Adapter Alignment architecture, transitioning the platform from monolithic skill ingestion to token-efficient progressive disclosure.

The test infrastructure validates:
- Synchronisation of 39 active roles across adapter templates (`a2a-config.template.yaml`).
- Authoritative documentation of Two-Tier JIT discovery mechanics, hybrid ranking formula ($S_{\text{match}} = 0.45 \cdot \text{BM25} + 0.55 \cdot \text{Dense}$ with $\tau = 0.72$), and token budget (< 5 KB) in `ANTIGRAVITY.md`.
- Router progressive disclosure instructions in `INDEX.md`.
- The Tier-1 discovery engine script `core/scripts/generate-tier1-index.py` and its generated artifact `adapters/antigravity/INDEX_TIER1.json` (< 5 KB, canonical SHA-256 digests, 183 skills).
- Reconciliation of governance and guardrail locks in `core/roles/agent-coordinator.md` and `core/roles/agent-discovery-engineer.md`.
- Repository validation suite integration (`core/scripts/validate-indexes.py`, `validate-skill-ownership.py`, `validate-all.py`).

---

## 2. Testing Philosophy
The testing framework adheres to strict software engineering standards:
1. **Opaque-Box Verification**: Tests operate against externally observable contracts, file artifacts, CLI flags, schema specifications, and cryptographic digests without internal white-box monkey-patching or tautological mocks.
2. **Requirement-Driven**: Every assertion traces directly to requirements R1–R5 codified in `ORIGINAL_REQUEST.md` and Section 5 of `reports/ROADMAP_2026_2027.md`.
3. **No Facade Tests**: Tautological assertions (e.g. `assert True`), dummy passes, and mock assertions that mask real failure conditions are strictly forbidden. Tests verify genuine file states and live execution outputs.
4. **Deterministic Output Derivation**: Expected outputs (e.g. canonical SHA-256 digests, role counts, schema conformance, CLI exit codes) are deterministically derived from platform standards and normative JSON schemas.
5. **Cross-Platform Resiliency**: Digest computations, newline normalisation, and path separators are validated across Windows (CRLF, backslashes) and POSIX (LF, forward slashes) environments.

---

## 3. Feature Inventory (Features 1–10 across R1–R5)

| Feature # | Requirement | Feature Name | Description | Authoritative Target File |
|:---:|:---:|---|---|---|
| **F1** | **R1** | A2A Config Template 39-Role Sync | Full mapping of 39 active roles across 7 functional clusters in adapter template | `adapters/antigravity/a2a-config.template.yaml` |
| **F2** | **R2** | Antigravity Adapter Modernization | Two-Tier JIT mechanics, candidate ranking formula ($S_{\text{match}} = 0.45 \cdot \text{BM25} + 0.55 \cdot \text{Dense}$, $\tau = 0.72$), budget (< 5 KB), AST02 failure mode | `adapters/antigravity/ANTIGRAVITY.md` |
| **F3** | **R3** | Router Progressive Disclosure Specs | Two-Tier progressive disclosure rules and JIT retrieval instructions in router section | `core/scripts/generate-index.py`, `INDEX.md` |
| **F4** | **R4** | Tier-1 Discovery Index Generator | CLI script scanning 183 skills, newline-normalized SHA-256 digests, `--check` flag support | `core/scripts/generate-tier1-index.py` |
| **F5** | **R4** | Tier-1 Manifest Artifact | Lightweight JSON manifest conforming to `agent-skills-discovery.json` (< 5 KB, 183 skills) | `adapters/antigravity/INDEX_TIER1.json` |
| **F6** | **R4** | Tier-1 Validation Integration | Integration of `generate-tier1-index.py --check` into repository index validation suite | `core/scripts/validate-indexes.py` |
| **F7** | **R5** | Agent Coordinator Reconciliation | Two-Tier governance, $\tau=0.72$ ranking threshold, `JIT-PROGRESSIVE-DISCLOSURE LOCK`, `DISCOVERY-RANKING LOCK` | `core/roles/agent-coordinator.md` |
| **F8** | **R5** | Agent Discovery Engineer Reconciliation | Ownership of `INDEX_TIER1.json`, $< 5\text{ KB}$ budget, `TIER1-BUDGET-LOCK`, `JIT-DIGEST-VERIFY-LOCK` | `core/roles/agent-discovery-engineer.md` |
| **F9** | **E2E** | Independent E2E Test Suite | 4-tier opaque-box test suite verifying all Phase 3 deliverables and specifications | `tests/test_phase3_e2e.py` |
| **F10** | **Gates** | Repository Quality Gates | 100% PASS (exit code 0) for `validate-indexes.py`, `validate-skill-ownership.py`, `validate-all.py` | `core/scripts/validate-all.py` |

---

## 4. 4-Tier Test Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        4-TIER TEST ARCHITECTURE                        │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 4: Real-World Acceptance Scenarios                                │
│   • End-to-end execution of validate-indexes.py                        │
│   • End-to-end execution of validate-skill-ownership.py                │
│   • Full repo validator validate-all.py integration                    │
│   • Two-Tier JIT dynamic retrieval workflow simulation                 │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 3: Cross-Feature Combinations                                     │
│   • Interaction of generate-index.py --check & generate-tier1-index.py│
│   • Cross-referencing INDEX_TIER1.json against INDEX.md / role-skill   │
│   • AST02 digest verification against live SKILL.md files on disk      │
│   • Template vs generated capability map consistency                   │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 2: Boundary & Corner Cases                                        │
│   • CRLF vs LF newline normalization in SHA-256 digest computation     │
│   • Duplicate skill reverse-engineer-binary overlay override (183 cnt) │
│   • Manifest footprint & token budget thresholds (< 5 KB)              │
│   • Negative schema validation (missing fields, malformed digests)     │
│   • Description length boundaries (20 <= len(desc) <= 1024)            │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 1: Feature Coverage (>=5 test cases per requirement: R1 - R5)     │
│   • R1: A2A config template 39 roles, YAML valid, 7 clusters (5 tests) │
│   • R2: ANTIGRAVITY.md formula, tau=0.72, budget < 5 KB, AST02 (5 tsts)│
│   • R3: INDEX.md Two-Tier JIT instructions, prompt budget (5 tests)    │
│   • R4: Tier-1 generator script, manifest schema, 183 skills (5 tests) │
│   • R5: Roles coordinator & discovery engineer locks, DoD (5 tests)    │
└────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Tier 1: Feature Coverage
Validates the happy-path behavior and contract compliance for every requirement (minimum 5 tests per requirement):
- **Requirement R1 (A2A Template Sync)**:
  1. `test_t1_r1_a2a_config_template_exists_and_valid_yaml`: Validates file existence and clean YAML parsing.
  2. `test_t1_r1_all_39_roles_present`: Validates that all 39 active roles are present in `capability_role_map`.
  3. `test_t1_r1_seven_clusters_represented`: Validates that all 7 functional clusters (Coordination, Software Engineering, QA/Security, Architecture, Analysis/Research, Content, Design) are mapped.
  4. `test_t1_r1_role_target_files_exist`: Validates that every mapped role in `capability_role_map` corresponds to an existing markdown definition in `core/roles/<role>.md`.
  5. `test_t1_r1_core_a2a_metadata_fields`: Validates protocol version (`1.0`), pack version (`5.7.3` or newer), streaming schemas, and coordinator configuration.
- **Requirement R2 (Antigravity Adapter Modernization)**:
  1. `test_t1_r2_adapter_spec_exists_and_readable`: Verifies `adapters/antigravity/ANTIGRAVITY.md` is present and non-empty.
  2. `test_t1_r2_two_tier_candidate_ranking_formula`: Verifies documentation of hybrid ranking formula ($S_{\text{match}} = 0.45 \cdot \text{BM25} + 0.55 \cdot \text{Dense}$ or equivalent hybrid weights).
  3. `test_t1_r2_threshold_tau_specification`: Verifies exact specification of ranking threshold $\tau = 0.72$ and fail-closed human escalation.
  4. `test_t1_r2_tier1_budget_limit_documented`: Verifies Tier 1 footprint constraint (< 5 KB or ~40 tokens/skill, total ~7.3k tokens, 97.3% reduction).
  5. `test_t1_r2_ast02_digest_verification_documented`: Verifies documentation of AST02 cryptographic verification against `INDEX_TIER1.json` before tool execution.
- **Requirement R3 (Router Progressive Disclosure Specs)**:
  1. `test_t1_r3_index_md_exists`: Validates `INDEX.md` existence and freshness.
  2. `test_t1_r3_router_progressive_disclosure_instructions`: Verifies that `INDEX.md` resolution rules describe Tier 1 passive discovery and Tier 2 JIT retrieval.
  3. `test_t1_r3_router_ranking_formula_and_threshold`: Verifies candidate ranking formula and $\tau = 0.72$ threshold in `INDEX.md`.
  4. `test_t1_r3_router_prohibited_skills_exclusion`: Verifies explicit exclusion of skills listed in the active role's `### Prohibited Skills`.
  5. `test_t1_r3_router_sha256_verification_instruction`: Verifies that runtime retrieval instructs cryptographic verification of SHA-256 digest against `INDEX_TIER1.json`.
- **Requirement R4 (Tier-1 Generator & Manifest)**:
  1. `test_t1_r4_generator_script_exists_and_executable`: Verifies `core/scripts/generate-tier1-index.py` exists.
  2. `test_t1_r4_manifest_artifact_exists`: Verifies `adapters/antigravity/INDEX_TIER1.json` exists.
  3. `test_t1_r4_manifest_conforms_to_schema`: Validates `INDEX_TIER1.json` against `core/contracts/schemas/agent-skills-discovery.json`.
  4. `test_t1_r4_manifest_contains_exact_183_skills`: Verifies that exactly 183 skills are indexed.
  5. `test_t1_r4_generator_cli_check_flag`: Tests `python core/scripts/generate-tier1-index.py --check` returns exit code 0.
- **Requirement R5 (Role Configurations Reconciliation)**:
  1. `test_t1_r5_agent_coordinator_responsibilities`: Verifies `core/roles/agent-coordinator.md` contains Two-Tier JIT progressive disclosure responsibilities.
  2. `test_t1_r5_agent_coordinator_guardrail_locks`: Verifies `JIT-PROGRESSIVE-DISCLOSURE LOCK` and `DISCOVERY-RANKING LOCK` in `agent-coordinator.md`.
  3. `test_t1_r5_agent_discovery_engineer_responsibilities`: Verifies `core/roles/agent-discovery-engineer.md` contains Tier 1 manifest governance.
  4. `test_t1_r5_agent_discovery_engineer_guardrail_locks`: Verifies `TIER1-BUDGET-LOCK` and `JIT-DIGEST-VERIFY-LOCK` in `agent-discovery-engineer.md`.
  5. `test_t1_r5_role_standard_conformance`: Verifies both roles satisfy `role-standard.md` section structure and guardrail density (12–24 locks).

### 4.2 Tier 2: Boundary & Corner Cases
Validates strict edge cases, defensive programming, and resource boundary conditions:
- **T2.1: CRLF vs LF Newline Normalization**: Confirms that calculating SHA-256 on bytes where `b"\r\n"` is converted to `b"\n"` produces identical hashes regardless of host OS git checkout line endings.
- **T2.2: Duplicate Skill Collision Resolution**: Confirms that the dual occurrence of `reverse-engineer-binary` (in `core/skills/security-data/` and `overlays/kilo-code/skills/`) is properly deduplicated to exactly 1 entry in `INDEX_TIER1.json`, with the overlay version prevailing.
- **T2.3: Token Budget & Footprint Threshold**: Confirms `adapters/antigravity/INDEX_TIER1.json` filesize is strictly `< 5120` bytes (5 KB) or an average of `< 50` tokens per skill entry.
- **T2.4: Negative Schema Validation**: Tests that manifests with missing required fields (`name`, `digest`, `url`), invalid types, or malformed regex digests (`sha256:XYZ`) are rejected by `Draft202012Validator`.
- **T2.5: Description Length Boundaries**: Asserts all skill descriptions satisfy `20 <= len(description) <= 1024` chars and include operational triggers (`Use when` / `Use for`).

### 4.3 Tier 3: Cross-Feature Combinations
Validates subsystem interoperability and cross-component invariants:
- **T3.1: Freshness Checker Synchronization**: Tests interaction of `generate-index.py --check` and `generate-tier1-index.py --check` when invoked in sequence.
- **T3.2: Complete Skill Catalog Parity**: Verifies that every skill name in `INDEX_TIER1.json` exists in `INDEX.md` and `adapters/antigravity/role-skill-index.json`.
- **T3.3: Live Disk AST02 Digest Verification**: Samples live `SKILL.md` files from disk, computes their normalized SHA-256 digests, and verifies 100% bitwise equality with the `digest` recorded in `INDEX_TIER1.json`.
- **T3.4: Role Capability Map Parity**: Verifies that all 39 roles in `a2a-config.template.yaml` match the 39 roles in `adapters/antigravity/capability-role-map.generated.yaml`.

### 4.4 Tier 4: Real-World Acceptance Scenarios
Validates system-level workflow execution:
- **T4.1: Validator Suite Index Freshness Gate**: Executes `python core/scripts/validate-indexes.py` and asserts exit code 0.
- **T4.2: Validator Suite Skill Ownership Gate**: Executes `python core/scripts/validate-skill-ownership.py` and asserts exit code 0.
- **T4.3: Full Repository Quality Gate (`validate-all.py`)**: Executes `python core/scripts/validate-all.py` and confirms all checks pass without errors.
- **T4.4: JIT Resolution Workflow Simulation**: Simulates an incoming agent task query, verifies candidate scoring, threshold gate ($\tau=0.72$), prohibited skills disqualification, and digest verification.

---

## 5. Verification Protocol & Execution

### 5.1 Test Execution Command
To execute the comprehensive Phase 3 E2E test suite:
```bash
python -m unittest tests/test_phase3_e2e.py -v
```

### 5.2 Repository Validation Commands
To run the full suite of static and repository validation gates:
```bash
python core/scripts/validate-indexes.py
python core/scripts/validate-skill-ownership.py
python core/scripts/validate-all.py
```

---

## 6. Traceability Matrix

| Requirement | Deliverable Files | Tier 1 Tests | Tier 2 Edge Cases | Tier 3 Combinations | Tier 4 Acceptance |
|---|---|---|---|---|---|
| **R1** | `adapters/antigravity/a2a-config.template.yaml` | 5 tests | Empty/invalid YAML | Role map parity | `validate-all.py` |
| **R2** | `adapters/antigravity/ANTIGRAVITY.md` | 5 tests | Formula bounds | Spec references | Quality review |
| **R3** | `core/scripts/generate-index.py`, `INDEX.md` | 5 tests | Stale index flag | Index parity | `validate-indexes.py` |
| **R4** | `core/scripts/generate-tier1-index.py`, `INDEX_TIER1.json` | 5 tests | CRLF normalisation, 183 collision, < 5 KB budget | AST02 disk verification | `validate-indexes.py` |
| **R5** | `core/roles/agent-coordinator.md`, `agent-discovery-engineer.md` | 5 tests | Guardrail density (12–24) | Contract coverage | `validate-roles.py` |
