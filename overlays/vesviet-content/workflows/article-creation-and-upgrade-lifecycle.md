---
name: article-creation-and-upgrade-lifecycle
description: Standard operating lifecycle for creating new technical articles or upgrading existing posts across the vesviet and learn twin Hugo sites, enforcing 100-round deep research and the 4-role swarm pipeline.
version: 1.0.0
roles:
  - content-writer
  - content-manager
  - technical-writer
  - seo-analyst
  - reviewer
---

# Article Creation & Upgrade Lifecycle Workflow

Use this workflow whenever a new article is drafted or an existing article is upgraded on `vesviet` (`tanhdev.com`) or `learn` (`learn.tanhdev.com`). It mandates 100 rounds of deep research prior to drafting and coordinates the 4-role swarm pipeline.

## Preconditions

- Target article scope defined (new topic brief or existing article slug).
- Target site designated: `learn` (Vietnamese notes twin) or `vesviet` (English flagship masterclass), or synchronized twin pair.
- Content indexes reviewed: `learn/plan/CONTENT_INDEX.md` and `vesviet/reports/CONTENT_INDEX.md`.

## 5-Phase Production Pipeline

### Phase 1: Deep Research (100 Rounds) (`seo-analyst` / `researcher`)
- Execute 100 distinct research rounds structured into 5 technical clusters:
  1. *Cluster 1 (Rounds 01–20)*: Architecture Roots, RFCs, Whitepapers & Context.
  2. *Cluster 2 (Rounds 21–40)*: Algorithms, Consensus, Distributed Models & Math.
  3. *Cluster 3 (Rounds 41–60)*: Production Benchmarks, P95/P99 Latency & Hardware Conditions.
  4. *Cluster 4 (Rounds 61–80)*: Production Outages, Real-World Failures & Post-Mortems.
  5. *Cluster 5 (Rounds 81–100)*: Trade-off Matrices, Alternatives Rejected & SOTA Standards.
- Emit structured dossier: `reports/research/<slug>-dossier.json` and `<slug>-research-notes.md`.
- Contract emitted: `contracts/schemas/research-report.json`.

### Phase 2: Masterclass Drafting (`@content-writer`)
- Draft or extend the article using `write-vesviet-learn-content` and `write-article`.
- Strictly enforce the **7 Technical Content Gates** (`rules/technical-article-2027.md`):
  - Gate 1: `> **Answer-first:**` block (≤60 words) + section BLUFs.
  - Gate 2: Production-grade version-pinned code (zero pseudo-code).
  - Gate 3: Quantitative depth (≥3 data points per 500 words with measurement conditions).
  - Gate 4: Architecture diagrams in Mermaid (`mermaid: true`).
  - Gate 5: Production Failure story (`> 🔥 **[Production Failure]: ...**`).
  - Gate 6: Trade-off framing (competing options compared, alternative rejected).
  - Gate 7: Verifiable claims with primary citations.
- Word count target: ≥2,500 words (>20 KB) for masterclasses; ≥1,400 words for standard posts.
- Contract emitted: `contracts/schemas/content-handoff.json`.

### Phase 3: Dual Audit (`@content-manager` + `@technical-writer`)
Parallel execution by editorial and technical specialists:
- **`@content-manager`**:
  - Audit brand voice, E-E-A-T, TOC hierarchy, and Non-Commodity Information Gain (target score ≥75).
  - Verify twin differentiation: English version must add value beyond translation.
- **`@technical-writer`**:
  - Audit code execution validity: verify syntax, imports, context handling, and error checking.
  - Verify deployable configurations (Kubernetes manifests, Dockerfiles, Cloudflare configs).
  - Audit benchmark claims against stated hardware conditions.

### Phase 4: SEO Authority & Link Audit (`@seo-analyst`)
- Audit Answer-First compliance (≤60 words, no slow-burn intros).
- Audit internal link topology: ≥3 links per post, connected to at least one of the 10 Anchor Pillar Hubs.
- Enforce one-way authority rule: `learn` → `vesviet` only. Zero `learn.tanhdev.com` links on `vesviet`.
- Verify Schema.org JSON-LD microdata (`TechArticle`, `Person`, `FAQPage`, `BreadcrumbList`).
- Contract emitted: `contracts/schemas/seo-audit-report.json`.

### Phase 5: Reviewer Sign-off & Index Synchronization (`@reviewer`)
- Execute 7-gate scoring (`audit-technical-article`); Gate 2, 6, 7 failures are Blocking.
- Update `learn/plan/CONTENT_INDEX.md` and `vesviet/reports/CONTENT_INDEX.md` with refreshed word counts and compliance states.
- Run `python core/scripts/validate-all.py` to confirm repository integrity.

## Failure Modes

- **Drafting without 100-round dossier**: an author begins writing before the research dossier is generated. **Mitigation:** Phase 1 gate blocks Phase 2; reject draft without research dossier.
- **Pseudo-code or unpinned versions**: code snippet uses placeholder functions or unpinned dependencies. **Mitigation:** Gate 2 audit by `@technical-writer` rejects the commit.
- **Reverse authority link**: `vesviet` article links to `learn.tanhdev.com`. **Mitigation:** `@seo-analyst` audit immediately rejects the link.
- **Translation-only twin**: English twin has zero incremental information gain. **Mitigation:** `@content-manager` rejects the twin sync until unique benchmarks or case studies are added.
- **Stale indexes**: article published without refreshing `CONTENT_INDEX.md`. **Mitigation:** Phase 5 gate requires index refresh before task closure.

## Output Contracts

- `contracts/schemas/research-report.json` (Phase 1)
- `contracts/schemas/content-handoff.json` (Phase 2)
- `contracts/schemas/seo-audit-report.json` (Phase 4)
- `contracts/schemas/content-audit-report.json` (Phase 5)

## Standard 2026 Alignment

- **OWASP ASI**: Follows ASI01 (Goal Hijack prevention) and ASI06 (Context Poisoning defense).
- **Toolbox Lock**: Enforced by tagged roles via `check-policy.py`.
- **Commit Gate**: Follows META-RULE in `core/rules/code.md` — no commit or push without explicit user approval.
