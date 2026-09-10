---
name: series-sync-upgrade
description: Per-post 100-round deep research and synchronized twin upgrade of a full Hugo series across vesviet (English) and learn (Vietnamese), with review, audit, and index refresh on both repos.
version: 1.0.0
roles:
  - researcher
  - content-writer
  - content-manager
  - seo-analyst
  - technical-writer
  - reviewer
---

# Series Sync Upgrade Workflow (`learn` + `vesviet`)

Per-post deep-research and twin-synchronized series upgrade. One series = N chapters ×
100 research rounds each, executed chapter by chapter (not batched 20-posts-per-100-rounds
as in `masterclass-batch-upgrade`). Designed for series where twins are incomplete or
below the 2027 SOTA bar — reference campaign: `prompt-standard`.

Difference from `masterclass-batch-upgrade`: research is per-post (1 dossier per chapter),
English side may **author missing twins** (not only mirror upgrades), and both repos get
a dedicated series content index before the campaign starts.

## Preconditions

- Baseline series content index exists in BOTH repos: `learn/reports/<series>-content-index.md`
  and `vesviet/reports/<series>-content-index.md` (metrics matrix, gap classification,
  upgrade targets, verification checklist). Create these first if missing.
- Gap classification labels every chapter: `upgrade VI`, `upgrade EN`, `new EN twin`, `index-only`.
- Commit baseline (both repos) before editing content; never mix baseline commits with upgrade commits.

## Role Pipeline (chapter loop)

| Phase | Owner | Gate |
| :--- | :--- | :--- |
| 1. Deep research (100 rounds) | `researcher` | DEPTH LOCK: 100 distinct rounds, primary-source traceable |
| 2. Series index refresh & tracking | `content-manager` | baseline verified against live files |
| 3. Vietnamese chapter upgrade | `content-writer` | 7 gates (2027 SOTA bar) |
| 4. English twin upgrade / authoring | `content-writer` | information gain beyond translation |
| 5. Documentation & FAQ/runbook hygiene | `technical-writer` | FAQ/schema/tool-definition sync |
| 6. SEO & GEO audit | `seo-analyst` | Entity-First, BLUF, schema, extractability ≥80 |
| 7. Final review & audit sign-off | `reviewer` + `content-manager` | approve/reject, decay tiers |

Each chapter passes phases 1→7 before the next chapter starts (serial loop), unless the
user explicitly requests parallel fan-out.

## Chapter Loop (repeat per chapter)

### Phase 1 — Deep Research (100 rounds, `researcher`)
- One dossier per chapter: `reports/research-<series>-<chapter-slug>-100-rounds.{md,json}`.
- Partition 100 rounds into 10 thematic clusters × 10 rounds (e.g., for `prompt-standard`:
  context engineering, 8-block anatomy, layered stacks, MCP tool schemas, hybrid RAG,
  DSPy compilation, PromptOps CI/CD, injection defense, evaluation, team adoption).
- Every round: experimental result / algorithm / benchmark with tool versions, traceable
  to a primary source. AI outputs generate queries only — never cited (AI SOURCE LOCK).
- Populate information-gain fields: `unique_insights`, `AI_coverage_gap`,
  `firsthand_evidence_available`, `YMYL_elevation_required`.
- Mirror the dossier to BOTH repos' `reports/` so each side drafts from the same evidence.

### Phase 2 — Series Index Refresh (`content-manager`)
- Before the first chapter: verify the baseline index metrics against live files
  (word counts, Mermaid, FAQ, weights, badges) and correct drift.
- After every chapter: update the chapter's row in the metrics matrix; keep gap
  classifications current; track planned vs upgraded status.

### Phase 3 — Vietnamese Chapter Upgrade (`content-writer`)
- Draft from the chapter's dossier (editorial passes only for gaps — no re-research).
- 2027 SOTA bar: >20 KB, ≥2,500 words, production-grade version-pinned code, 2 AST-valid
  Mermaid, 3 FAQ, Answer-first ≤60 words preserved, Production Failure story, rejected
  alternatives, ≥3 verifiable data points / 500 words, ≥3 internal links.
- Extend-only: never remove published substance or break inbound anchors.
- `canonicalURL` stays on `learn.tanhdev.com`.

### Phase 4 — English Twin (`content-writer`)
- Upgrade the existing English twin, or author the missing twin for Track 1 completion.
- The English chapter must add information gain beyond translation (2026-2027 spam-policy
  duplication rules): deeper benchmark framing, additional production failure story, or
  expanded comparison matrix — dossier-backed.
- Reciprocal navigation badges: VI chapter → `Bản tiếng Anh` link up; EN chapter →
  `Bản tiếng Việt` link back. Badges are navigation, not authority transfer.
- `canonicalURL` stays on `tanhdev.com`; twins never cross-canonicalize.

### Phase 5 — Documentation Hygiene (`technical-writer`)
- FAQ components: verify each Q mirrors an on-page BLUF block; keep 1:1 with schema
  `FAQPage` microdata expectations.
- Frontmatter conformance: `slug`, `weight` sequence (no collisions with `_index.md`),
  `lastmod` bump, `mermaid: true` when diagrams exist, series taxonomy consistent.
- Terminology and code-adjacent prose (tool versions, CLI flags) point at live sources,
  not restated values (prune-like-a-cache-auditor rule).

### Phase 6 — SEO & GEO Audit (`seo-analyst`)
- Entity-First: primary entity Wikidata QID as grammatical subject of H2 lead sentences;
  semantic triples validated by the narrative.
- BLUF per H2 (≤30w answer + ≤30w metric proof); query fan-out sub-questions in H3s.
- GEO Extractability Index ≥80; AI bot crawlability re-verified if `robots.txt` changed.
- Twin duplication check: VI and EN chapters must not share title/meta/slug; cross-host
  duplication limited to the navigation badge pattern.

### Phase 7 — Review & Audit Sign-off (`reviewer` + `content-manager`)
- 7-gate audit per chapter (`audit-technical-article`): per-gate scores; Gate 2/6/7
  failures are Blocking.
- Content Manager: Top 10 SERP information-gain re-check (Non-Commodity Score ≥75),
  decay-tier tagging, editorial calendar row close.
- Reject loop: any Blocking finding returns the chapter to Phase 3/4; re-audit before close.

## Campaign Close (after final chapter)

1. Restructure both `_index.md` files to the completed TOC (chapter count, tracks,
   reciprocal series links, weight normalization).
2. Hugo build both repos (`--minify`, 0 errors); Mermaid AST audit across the series.
3. Rerun `vesviet/reports/check_posts.py`; refresh `vesviet/reports/CONTENT_INDEX.md`
   and `learn/plan/CONTENT_INDEX.md` (series row counts, compliance snapshot, known gaps).
4. Archive the campaign: mark gap classifications resolved in both series content indexes;
   log commit hashes of each chapter upgrade.

## Failure Modes

- **Round shortcut**: a chapter dossier has fewer than 100 distinct rounds. **Mitigation:** Phase 1 DEPTH LOCK; reject the dossier and re-research before drafting.
- **Untraceable round**: a round cites a benchmark with no primary source. **Mitigation:** reject the round; never draft from ungrounded evidence.
- **AI citation**: the dossier cites an AI summary as a source. **Mitigation:** AI SOURCE LOCK; strip and replace with the primary document.
- **Translation-only twin**: the English chapter mirrors the Vietnamese without information gain. **Mitigation:** Phase 4 gate; reject the sync until differential value is added.
- **Twin drift**: EN/VI chapters diverge in chapter count, weights, or TOC claims. **Mitigation:** Phase 2 index tracking; campaign close restructures both `_index.md` files.
- **Badge missing after upgrade**: an upgraded chapter loses its reciprocal navigation badge. **Mitigation:** Phase 4 verification; reject the diff.
- **Cross-canonicalization**: either twin points `canonicalURL` at the other host. **Mitigation:** Phase 3/4 gates; reject the diff.
- **Index staleness**: series or corpus indexes not refreshed after the campaign. **Mitigation:** campaign close step 3 is mandatory; reject close when stale.
- **Phase skip**: chapters jump to drafting without a dossier, or to publish without review. **Mitigation:** role pipeline gates are serial; the chapter loop restarts at Phase 1.

## Output Contracts

- **`contracts/schemas/research-report.json`** per chapter from Phase 1 (100 rounds, cluster map, citations, information-gain fields).
- **`contracts/schemas/content-handoff.json`** per chapter from Phases 3–4 (gate verdicts, word count, Mermaid count, internal links, twin badge status).
- **`contracts/schemas/seo-audit-report.json`** per chapter from Phase 6 (GEO Extractability ≥80, entity mapping, duplication checks).
- **`contracts/schemas/documentation-handoff.json`** from Phase 5 when FAQ/schema/frontmatter restructuring is machine-tracked.
- **`contracts/schemas/content-audit-report.json`** from Phase 7 / campaign close (per-chapter gate scores, resolved gap classifications).

Regenerate this workflow's entry in `overlays/vesviet-content/workflows/README.md` when renaming or adding workflows. Run `python3 core/scripts/validate-all.py` from `agent-skills/` after any overlay change.
