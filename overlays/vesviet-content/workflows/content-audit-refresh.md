---
name: content-audit-refresh
description: 4-Sprint workflow for auditing, repairing schema, expanding content, and enforcing link topology for vesviet.
version: 1.0.0
roles:
  - seo-analyst
  - content-writer
  - content-manager
  - backend-developer
---

# Content Audit & Refresh Workflow (`vesviet`)

This workflow dictates the 4-sprint operational execution plan for resolving technical content debt and maintaining GEO/AEO standards on the `vesviet` flagship site.

## When to Use

Use this workflow during quarterly maintenance sprints or content remediation campaigns when `vesviet` articles require schema fixes, technical depth expansion, orphan elimination, or consolidation.

## Preconditions

- Corpus inventory verified against live files (374 content files on `vesviet` as of 2026-09-13).
- Repository crawler and auditing scripts available (`vesviet/reports/check_posts.py`).
- Link topology rules (`rules/link-topology.md`) and brand standards (`rules/content-brand.md`) reviewed.

## Roles

| Sprint | Owner Roles | Deliverable & Quality Gate |
|---|---|---|
| Sprint 1: Schema Repair & GEO Baseline | `seo-analyst`, `content-writer`, `content-manager` | 100% schema completeness; top 50 posts equipped with Answer-first blocks |
| Sprint 2: Content Refresh & Technical Depth | `content-writer`, `reviewer` | All target posts exceed 1,400w with production code and Mermaid diagrams |
| Sprint 3: Link Topology & Orphan Elimination | `seo-analyst`, `content-writer`, `content-manager` | 0 orphan pages reported by `check_posts.py`; reading maps updated |
| Sprint 4: Consolidation & Redirects | `content-manager`, `seo-analyst`, `backend-developer` | Thin content merged; 301 redirects verified; clean build under explicit user confirmation |

## 4-Sprint Execution Workflow

### Sprint 1 — Schema Repair & GEO Baseline

Role: `seo-analyst`, `content-writer`, `content-manager`

1. **Audit Schema Coverage (`seo-analyst`)**: Identify all files missing mandatory schema fields (`tags`, `categories`, `cover`).
2. **Inject GEO Baseline (`content-writer`)**: Add `> **Answer-first:**` summary blocks (≤60 words, direct answer + key takeaway) to the top 50 performing posts.
3. **Verify Conformance (`content-manager`)**: Ensure 100% schema validation passes across all scanned files.

### Sprint 2 — Content Refresh & Technical Depth

Role: `content-writer`, `reviewer`

1. **Identify Target Articles (`content-writer`)**: Select all underperforming articles and series sub-articles currently under the 1,400-word baseline.
2. **Inject Technical Assets (`content-writer`)**: Add production-grade Go structs, Kubernetes manifests, system design sequence diagrams (Mermaid), and quantitative benchmarks. Reject pseudo-code and ungrounded claims.
3. **Verify Depth Baseline (`reviewer`)**: Confirm all target posts exceed 1,400 words with verifiable technical substance.

### Sprint 3 — Link Topology & Orphan Elimination

Role: `seo-analyst`, `content-writer`, `content-manager`

1. **Map Spoke Architecture (`seo-analyst`)**: Map any orphan pages to the 10 Anchor Pillar Hubs per `rules/link-topology.md` (treat any orphan count above 0 as a regression).
2. **Inject Spoke-to-Hub Links (`content-writer`)**: Inject contextual in-body links from orphan spokes up to their parent Anchor Pillar Hubs.
3. **Maintain Navigation Pathways (`content-manager`)**: Update `reading-map.md` with 6 curated learning paths and diversify anchor texts across `hire.md`.
4. **Verify Topology (`seo-analyst`)**: Execute `vesviet/reports/check_posts.py` to confirm the crawler reports exactly 0 orphan pages.

### Sprint 4 — Consolidation & Redirects

Role: `content-manager`, `seo-analyst`, `backend-developer`

1. **Consolidate Thin Content (`content-manager`)**: Merge thin content (< 1,000 words) into parent Series or monthly Tech Radar Digests.
2. **Configure 301 Permanent Redirects (`seo-analyst`)**: Implement 301 Permanent Redirects via Hugo aliases in frontmatter and Cloudflare `_redirects` file.
3. **Build & Alias Verification (`content-manager`)**: Run `hugo --gc --minify` to confirm zero build warnings, zero broken aliases, and clean HTML output.
4. **Explicit User Approval Gate (`backend-developer`)**: Present staged diff and redirect maps to the user. Require explicit user confirmation before committing and deploying per `core/rules/code.md` (META-RULE).

## Checklist

- [ ] Sprint 1: All files audited for mandatory schema fields (`tags`, `categories`, `cover`)
- [ ] Sprint 1: `> **Answer-first:**` summary blocks added to top 50 performing posts
- [ ] Sprint 1: 100% schema validation verified across all target content files
- [ ] Sprint 2: Underperforming articles (< 1,400 words) identified and cataloged
- [ ] Sprint 2: Production Go/K8s code snippets, Mermaid diagrams, and benchmarks injected
- [ ] Sprint 2: Technical depth verified; all target posts exceed 1,400-word baseline
- [ ] Sprint 3: Orphan pages mapped to the 10 Anchor Pillar Hubs
- [ ] Sprint 3: Spoke-to-hub link injections completed without breaking anchor equity
- [ ] Sprint 3: `reading-map.md` updated with 6 learning paths and `hire.md` anchors diversified
- [ ] Sprint 3: `vesviet/reports/check_posts.py` executed and reports 0 orphan pages
- [ ] Sprint 4: Thin content (< 1,000 words) merged into parent Series or Tech Radar Digests
- [ ] Sprint 4: 301 Permanent Redirects configured via Hugo aliases and Cloudflare `_redirects`
- [ ] Sprint 4: `hugo --gc --minify` builds with 0 warnings and 0 broken links
- [ ] Sprint 4: Explicit user approval obtained before staging, committing, or deploying changes

## Failure Modes

- **Schema repair without GEO baseline**: a Sprint 1 audit focuses on tags and categories but skips the `> **Answer-first:**` block on the top posts. **Mitigation:** the sprint timeline requires both; reject the sprint as incomplete when the answer-first sweep is missing.
- **Content expansion drifts above 1,400 words without depth**: a writer expands to 1,400 words but adds fluff instead of code samples, manifests, sequence diagrams, and benchmarks. **Mitigation:** the Sprint 2 criteria require concrete technical depth; reject the expansion that does not add depth.
- **Orphan mapping skips regression pages**: Sprint 3 only links a subset of newly found orphan pages. **Mitigation:** the verification step requires zero orphan pages; reject the sprint when the count is non-zero.
- **Redirects ship without 301 Permanent status**: Hugo aliases or Cloudflare `_redirects` are added with 302 or no status. **Mitigation:** the verification step requires 301 Permanent; reject the change when the status is wrong.
- **Consolidation loses traffic**: a merge or redirect loses inbound links or canonical authority. **Mitigation:** Step 4 requires a 301 from every old URL to the new one; reject the merge when the redirect map is incomplete.
- **Build warnings after consolidation**: `hugo --gc --minify` reports warnings or broken aliases. **Mitigation:** the verification step requires zero warnings; reject the build that emits warnings.
- **Audit runs on stale corpus snapshot**: the audit uses `content-audit-report.json` from before the latest batch. **Mitigation:** rerun `reports/check_posts.py` first; reject audits whose scanned-file count differs from the live corpus count (374 files as of 2026-09-13).
- **Unconfirmed commit or deploy of redirects**: redirect changes or content consolidations are committed or deployed without explicit user confirmation. **Mitigation:** Sprint 4 enforces explicit user approval gates per `core/rules/code.md` (META-RULE).

## Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/seo-audit-report.json`** from Sprint 1, capturing the four-axis scores per file and the projected post-fix score.
- **`contracts/schemas/coordination-plan.json`** from Sprint 3, capturing the orphan mappings to the 10 Anchor Pillar Hubs.
- **`contracts/schemas/deployment-plan.json`** from Sprint 4, capturing the 301 Permanent redirects and the canonical URL decisions.