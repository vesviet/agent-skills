# Reports & Research Knowledge Hub

> **Ecosystem:** `agent-skills` (v5.8.0)  
> **Governance Standard:** `core/rules/knowledge.md` (Root Directory Limit $\le 5$ files, zero scratch files)  
> **Classification:** Living Platform Index & Historical Archive Directory  

This directory serves as the centralized repository for strategic engineering roadmaps, authoritative audits, active pack research, and deep domain research dossiers.

---

## 1. Active Platform Reports (Root Directory)

The root of `reports/` is strictly constrained to living, authoritative platform documents:

| Document | Purpose & Scope | Status | Last Updated |
| :--- | :--- | :---: | :---: |
| [`INDEX.md`](INDEX.md) | Master navigation directory and archival taxonomy index. | **Living** | 2026-11-08 |
| [`agent-skills-round-2-audit-report.md`](agent-skills-round-2-audit-report.md) | Authoritative Round 2 Forensic Audit baseline evaluating 39 roles, 183 skills, 25 workflows, and test coverage. | **Active Baseline** | 2026-11-08 |
| [`ROADMAP_2026_2027.md`](ROADMAP_2026_2027.md) | Multi-phase strategic engineering modernization and capability expansion plan. | **Active** | 2026-10-30 |
| [`RESEARCH_2026_2027_SOTA.md`](RESEARCH_2026_2027_SOTA.md) | Comprehensive state-of-the-art architectural research across AI, backend, platform, and edge technologies. | **Active** | 2026-10-30 |

---

## 2. Active Pack Research (`reports/research/`)

Specialized research artifacts maintained for domain-specific engineering packs:

| Artifact | Pack Binding | Description |
| :--- | :--- | :--- |
| [`research/mmo-2027-sota-dossier.json`](research/mmo-2027-sota-dossier.json) | `packs/mmo-growth-team` | Structured JSON dossier specifying 2026–2027 MMO growth, anti-detect orchestration, and tracking architectures. |
| [`research/mmo-2027-sota-research-notes.md`](research/mmo-2027-sota-research-notes.md) | `packs/mmo-growth-team` | Qualitative research notes, proxyware economics, and programmatic SEO operational guidelines. |

---

## 3. Historical Archives (`reports/archive/`)

Legacy audit snapshots and exhaustive 100-round domain research dossiers are preserved in dedicated archive vaults.

### 3.1 Domain Research Dossiers (`reports/archive/research-dossiers/`)

Comprehensive 100-round technical research investigations for engineering roles:

| Research Dossier | Target Role / Domain | Focus & Invariants |
| :--- | :--- | :--- |
| [`backend-developer-repo-research.md`](archive/research-dossiers/backend-developer-repo-research.md) | `backend-developer` | Go 1.25+, Kratos, transactional outbox, Postgres optimization, distributed locking. |
| [`business-analyst-repo-research.md`](archive/research-dossiers/business-analyst-repo-research.md) | `business-analyst` | BABOK v3, DDD event storming, RTM blast radius analysis, BDD acceptance criteria. |
| [`data-engineer-data-analyst-repo-research.md`](archive/research-dossiers/data-engineer-data-analyst-repo-research.md) | `data-engineer` / `data-analyst` | Apache Iceberg v3, Write-Audit-Publish, lakehouse compaction, chDB/DuckDB federation. |
| [`devops-engineer-repo-research.md`](archive/research-dossiers/devops-engineer-repo-research.md) | `devops-engineer` | Kubernetes 1.31+, Karpenter v1.0+, EKS Pod Identity, GitOps drift reconciliation. |
| [`gamedev-skills-repo-research.md`](archive/research-dossiers/gamedev-skills-repo-research.md) | `game-developer` | Fixed-timestep determinism, CCD collision, Behavior Tree blackboards, headless CI runners. |
| [`qa-qc-engineer-repo-research.md`](archive/research-dossiers/qa-qc-engineer-repo-research.md) | `qa-engineer` | Tripartite Playwright triage, combinatorial pairwise matrices, hostile stress testing. |
| [`solution-architect-repo-research.md`](archive/research-dossiers/solution-architect-repo-research.md) | `solution-architect` | Distributed systems topology, ADR lifecycle, capacity modeling, NFR verification. |
| [`vietnam-legal-counsel-repo-research.md`](archive/research-dossiers/vietnam-legal-counsel-repo-research.md) | `vietnam-legal-counsel` | Vietnam AI Law No. 134/2025/QH15, PDPL No. 91/2025/QH15, Decree 13/2023/ND-CP. |
| [`anthropics-skills-ecosystem-benchmark-and-upgrade-plan.md`](archive/research-dossiers/anthropics-skills-ecosystem-benchmark-and-upgrade-plan.md) | Ecosystem Benchmark | Anthropic Model Context Protocol (MCP) and skill structure benchmarking. |
| [`cloudflare-skills-ecosystem-benchmark.md`](archive/research-dossiers/cloudflare-skills-ecosystem-benchmark.md) | Platform Benchmark | Cloudflare Workers, Durable Objects, Agents SDK, and edge runtime capabilities. |
| [`external-skills-ecosystem-benchmark-research.md`](archive/research-dossiers/external-skills-ecosystem-benchmark-research.md) | Industry Benchmark | Comparative analysis across open-source agentic tool frameworks and ecosystems. |

### 3.2 Historical Audits & Modernization Snapshots (`reports/archive/historical-audits/`)

Baseline audits and milestone transition reports:

| Report | Date / Epoch | Summary of Findings |
| :--- | :---: | :--- |
| [`agent-skills-audit-report.md`](archive/historical-audits/agent-skills-audit-report.md) | 2026-10-20 | Round 1 baseline audit across initial skills and role catalogs. |
| [`repository-audit-and-drift-analysis-2026-10-25.md`](archive/historical-audits/repository-audit-and-drift-analysis-2026-10-25.md) | 2026-10-25 | Pre-sprint drift analysis, schema verification, and A2A compliance scan. |
| [`role-skill-matrix-sota-audit-2026-2027.md`](archive/historical-audits/role-skill-matrix-sota-audit-2026-2027.md) | 2026-10-05 | 35-role / 137-skill matrix audit evaluating SOTA 2026–2027 modernization. |
| [`roles-standardization-audit-2026.md`](archive/historical-audits/roles-standardization-audit-2026.md) | 2026-10-15 | Milestone M1 standardization audit for principal roles and review checklists. |
| [`sprint-2-modernization-completion-report.md`](archive/historical-audits/sprint-2-modernization-completion-report.md) | 2026-10-28 | Sprint 2 modernization completion report and transition sign-off. |

---

## 4. Archival and Knowledge Invariants

1. **Root Directory Limit**: The root of `reports/` must never contain more than 5 markdown files.
2. **Zero Scratch Files**: No temporary shell scripts, Python dumps, or ad-hoc test logs may be placed in `reports/`.
3. **Distribution Packaging Exclusion**: `package.json` and `.npmignore` strictly exclude `reports/` from published npm packages.
4. **Test Suite Compatibility**: Automated test fixtures asserting on research dossiers must implement fallback paths supporting both `reports/archive/research-dossiers/<name>.md` and `reports/<name>.md`.
