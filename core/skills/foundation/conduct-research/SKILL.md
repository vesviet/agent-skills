---
name: conduct-research
description: Execute iterative, deeply-verified research to discover, validate, and synthesize complex information. Use for deep (10+ round) or scoped (3+ round with waiver) investigation before architecture, product, or content decisions. Applies AI-era source discipline (primary source hierarchy, Chain-of-Verification, hallucination mitigation, grounding protocol) and delivers information gain assessment for SEO/content handoffs. Primary skill for the Researcher role.
---

# Conduct Research

Use this skill when a task requires deep discovery before architectural, product, or business implementation. It is specifically built for roles like `Researcher` that require aggressive triangulation, deep validation, and AI-era source integrity.

## Core Rules

### Research Integrity
- set `execution_metrics.depth_mode` to **deep** (default) or **scoped** before searching; scoped requires `scope_waiver_note` in research-report.json
- deep mode: minimum ten distinct research rounds; scoped mode: minimum three rounds with documented waiver
- triangulate data across multiple independent sources to eliminate hallucinations and bias
- document missing information explicitly rather than guessing or fabricating
- evaluate source credibility per claim type (fact, statistic, expert quote, trend, policy) and document confidence levels
- populate `recommended_next_roles` in JSON handoffs — do not author feature-ticket.json or architecture decisions
- structure the output for agent-to-agent consumption, avoiding raw text dumps

### AI-Era Source Discipline (2025-2026)

**Source hierarchy — apply in strict order:**

| Tier | Source type | Citable? |
|------|-------------|----------|
| 1 — Primary | Government records, official docs, peer-reviewed journals, primary interviews, original datasets, institutional publications | ✅ Yes — cite directly |
| 2 — Secondary | Reputable news organizations, academic syntheses, verified expert commentary, recognized industry reports | ✅ Yes — cite with context |
| 3 — Tertiary | Wikipedia, well-maintained reference sites | ⚠️ Orientation only — do not cite as final source |
| 4 — AI-generated | Google AI Overviews, Perplexity answers, ChatGPT outputs, Bing AI summaries | ❌ Never cite — use only to formulate queries and identify sub-topics |

**Hallucination mitigation protocol:**
- treat every URL, statistic, or quote from an AI tool as **unverified** until confirmed against the original document
- when an AI cites a source, retrieve and read that source directly — do not trust the AI's representation of it
- if a cited URL returns 404 or does not contain the claimed information → label `[AI-CITATION MISMATCH]` and flag in source list
- never silently drop a mismatched citation — always flag it

**Grounding protocol:**
- every material claim in the output must include a clickable, verifiable source URL
- claims without verifiable URL must be explicitly labeled: `[INFERENCE]`, `[UNKNOWN]`, or `[UNVERIFIED — source not retrieved]`
- do not paraphrase AI search result summaries and present them as grounded facts

### Chain-of-Verification (CoVe)

Apply for all critical claims; mandatory for YMYL-adjacent topics (health, legal, financial, safety):

1. Extract each major finding as an atomic sub-claim: "Regulation X states Y" or "Study Z found N%"
2. Retrieve the original source document directly (not via AI summary)
3. Verify the exact wording or statistic in the original document
4. If verified → label confirmed in synthesis; if unverified → label `[UNVERIFIED]`
5. Document CoVe results in the output (which claims passed, which remain unverified)

### Information Gain Quality Gate

When research feeds Content Writer or SEO Analyst, document in output:
- **unique_insights**: findings not present in top-5 SERP results for the target keyword
- **firsthand_evidence_available**: whether primary interviews, original data, or firsthand accounts are accessible
- **AI_coverage_gap**: topics where AI Overviews / AI answers are wrong, incomplete, or missing — high-value citation opportunities
- **YMYL_elevation_required**: flag when human expert review is needed before publication

## Suggested Process

### 1. Define The Objective

Clarify:
- the core hypothesis, question, or problem to solve
- depth_mode: deep | scoped (and who narrowed scope if scoped)
- boundaries (time constraints, domain limits, excluded sources)
- expected output format (`contracts/schemas/research-report.json` or markdown brief)
- YMYL-adjacent: yes/no (if yes, CoVe is mandatory)

### 2. Decompose Into Sub-Tasks

Before searching:
- break the research goal into atomic sub-questions
- identify which sub-tasks can run in parallel
- prioritize sub-tasks by criticality and source availability
- document decomposition in the Research Decomposition section of the output template

### 3. Formulate Search Strategy (Rounds 1–3)

- identify primary keywords, synonyms, and technical jargon
- run initial broad queries using search tools
- identify key authorities, official documentation, or reliable databases
- use AI search tools (Perplexity, Google AI Overview) **only for sub-topic discovery and query ideas** — do not extract claims from them

### 4. Deep Dive Execution (Rounds 4–8)

- follow references, citations, and internal links from primary/secondary findings
- query specific sub-topics, alternative approaches, or edge cases discovered
- cross-reference conflicting information to find the root truth
- for each significant claim: retrieve and read the original source document directly

### 5. Chain-of-Verification & Gap Analysis (Rounds 9–10+)

- apply CoVe: decompose each major finding into atomic sub-claims and verify each against original source
- review current findings against the original objective
- identify what is still missing, ambiguous, or unverified
- execute highly targeted queries to fill remaining critical gaps
- flag all AI-citation mismatches discovered during verification

### 6. Information Gain Assessment

Before synthesis, compare findings against top-5 SERP results for the target keyword:
- what is unique in these findings?
- where do AI Overviews provide incorrect or incomplete information?
- is firsthand data or primary interview material available?
- does topic touch YMYL domains?

### 7. Synthesize And Report

Produce a structured contract that downstream roles can use directly:
- `Technical Architect`: evaluated technologies, limits, trade-offs
- `Business Analyst`: market data, competitor analysis, feature comparisons
- `Content Writer`: verified domain knowledge with citations, information gain assessment, CoVe log
- `SEO Analyst`: unique insights vs SERP, AI coverage gaps, YMYL flags

## Output Format

```markdown
# <Topic> — Research Synthesis

## Objective & Scope
- Core question:
- Constraints:
- YMYL-adjacent: [yes/no]

## Research Decomposition
- Sub-tasks: [list atomic sub-questions]
- Execution order: [sequential/parallel]

## Execution Metrics
- depth_mode: deep | scoped
- Rounds completed: (≥ 10 if deep; ≥ 3 if scoped)
- scope_waiver_note: (required if scoped)
- Sources analyzed:

## Source Hierarchy Applied
- Primary sources: [list]
- Secondary sources: [list]
- AI tools used for queries only (not cited): [list]
- AI-citation mismatches: [list or "none"]

## Chain-of-Verification Log
- Claims submitted to CoVe: [list]
- Verified (URL confirmed): [list]
- Unverified [UNVERIFIED]: [list]

## Recommended Next Roles
- role | rationale | open_decisions

## Key Findings (Verified — Grounded with URL)
- [claim] — Source: [URL]

## Inferences [INFERENCE]
- [claim without verifiable source]

## Unknown / Unverified [UNKNOWN]
-

## Data Triangulation & Conflicts
-

## Crucial Gaps (What remains unknown)
-

## Information Gain Assessment
- unique_insights: [not in top-5 SERP]
- firsthand_evidence_available: [yes/no]
- AI_coverage_gap: [AI answers wrong/incomplete on]
- YMYL_elevation_required: [yes/no]

## Confidence Per Claim Type
- Facts / statistics: High | Medium | Low
- Expert quotes / positions: High | Medium | Low
- Trends / projections: High | Medium | Low
- Policy / legal claims: High | Medium | Low

## Source References
| Source | Type | Credibility | URL | Notes |
|--------|------|-------------|-----|-------|

## Grounding Completeness
- Claims with verifiable URL: N/M (%)
```

## Checklist

### Depth & Coverage
- [ ] depth_mode set and round minimum met for that mode
- [ ] research decomposed into sub-tasks before execution
- [ ] data triangulated across multiple independent sources
- [ ] source credibility evaluated per claim type
- [ ] gaps, assumptions, and limitations explicitly stated
- [ ] output structured for downstream agent use (no raw dumps)
- [ ] feature-ticket.json not authored by Researcher

### AI-Era Source Discipline
- [ ] no AI-generated summaries cited as primary or secondary sources
- [ ] AI tools documented as query sources only (not cited)
- [ ] all material claims have clickable, verifiable source URLs
- [ ] ungrounded claims labeled [INFERENCE], [UNKNOWN], or [UNVERIFIED]
- [ ] AI-citation mismatches flagged [AI-CITATION MISMATCH]

### Chain-of-Verification
- [ ] CoVe applied to major claims (mandatory for YMYL-adjacent)
- [ ] atomic sub-claims traced to original source documents
- [ ] verified vs unverified claims separated in synthesis

### Information Gain Gate
- [ ] unique_insights documented
- [ ] AI_coverage_gap documented
- [ ] YMYL_elevation_required flag set when applicable
- [ ] recommended_next_roles populated with rationale

## Related Skills

- **analyze-business-requirements**: Read BA framing only — do not populate feature-ticket.json as Researcher
- **agent-context-management**: Prevent token bloat during long research sessions
- **agent-tool-orchestration**: Manage search APIs, web scrapers, and local retrieval tools
- **agent-quality-gate**: Verify research findings before synthesizing; validate grounding completeness
