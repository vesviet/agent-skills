# Conduct Research — Reference

Deep material extracted from `SKILL.md` to keep the main file under 200 lines.
Load this file when the research touches AI-era source discipline, YMYL topics,
or when a handoff requires detailed CoVe logging.

## AI-Era Source Discipline (2025-2026)

### Source Hierarchy

Apply sources in this strict order; do not skip tiers:

| Tier | Source type | Citable? |
|------|-------------|----------|
| 1 — Primary | Government records, official docs, peer-reviewed journals, primary interviews, original datasets, institutional publications | Yes — cite directly |
| 2 — Secondary | Reputable news organizations, academic syntheses, verified expert commentary, recognized industry reports | Yes — cite with context |
| 3 — Tertiary | Wikipedia, well-maintained reference sites | Orientation only — do not cite as final source |
| 4 — AI-generated | Google AI Overviews, Perplexity answers, ChatGPT outputs, Bing AI summaries, Gemini Deep Research, ChatGPT Deep Research, Perplexity Pages | Never cite — use only to formulate queries and identify sub-topics; always retrieve and verify the primary source they reference |

### Hallucination Mitigation Protocol

- Treat every URL, statistic, or quote from an AI tool as **unverified** until confirmed against the original document.
- When an AI cites a source, retrieve and read that source directly — do not trust the AI's representation of it.
- If a cited URL returns 404 or does not contain the claimed information, label `[AI-CITATION MISMATCH]` and flag in the source list.
- Never silently drop a mismatched citation — always flag it.

### Grounding Protocol

- Every material claim in the output must include a clickable, verifiable source URL.
- Claims without a verifiable URL must be explicitly labeled: `[INFERENCE]`, `[UNKNOWN]`, or `[UNVERIFIED — source not retrieved]`.
- Do not paraphrase AI search result summaries and present them as grounded facts.

## Chain-of-Verification (CoVe)

Apply for all critical claims; mandatory for YMYL-adjacent topics (health, legal, financial, safety):

1. Extract each major finding as an atomic sub-claim: "Regulation X states Y" or "Study Z found N%".
2. Retrieve the original source document directly (not via AI summary).
3. Verify the exact wording or statistic in the original document.
4. If verified, label confirmed in synthesis; if unverified, label `[UNVERIFIED]`.
5. Document CoVe results in the output (which claims passed, which remain unverified).

## Information Gain Quality Gate

When research feeds Content Writer or SEO Analyst, document in the output:

- **unique_insights**: findings not present in top-5 SERP results for the target keyword.
- **firsthand_evidence_available**: whether primary interviews, original data, or firsthand accounts are accessible.
- **AI_coverage_gap**: topics where AI Overviews / AI answers are wrong, incomplete, or missing — high-value citation opportunities.
- **YMYL_elevation_required**: flag when human expert review is needed before publication.

## YMYL and Sensitive Domains

For YMYL-adjacent topics (health, legal, financial, safety, children, civic integrity):

- Require a human expert review sign-off before publication.
- Mandatory CoVe on every material claim; treat unverified sub-claims as `[UNVERIFIED]`.
- Never present an unverified claim as a recommendation; use `[INFERENCE]` or `[UNKNOWN]` and surface the gap.
