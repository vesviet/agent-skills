---
name: conduct-research
description: Execute iterative research to discover, validate, and synthesize complex information. Use for deep (10+ round) or scoped (3+ round with waiver) investigation before architecture, product, or content decisions. Primary skill for the Researcher role.
---

# Conduct Research

Use this skill when a task requires deep discovery before architectural, product, or business implementation. It is specifically built for roles like `Researcher` that require aggressive triangulation and deep validation.

## Core Rules

- set `execution_metrics.depth_mode` to **deep** (default) or **scoped** before searching; scoped requires `scope_waiver_note` in research-report.json
- deep mode: minimum ten distinct research rounds; scoped mode: minimum three rounds with documented waiver
- triangulate data across multiple independent sources to eliminate hallucinations and bias
- document missing information explicitly rather than guessing or fabricating
- evaluate source credibility and document confidence levels
- populate `recommended_next_roles` in JSON handoffs — do not author feature-ticket.json or architecture decisions
- structure the output for agent-to-agent consumption, avoiding raw text dumps

## Suggested Process

### 1. Define The Objective

Clarify:
- the core hypothesis, question, or problem to solve
- depth_mode: deep | scoped (and who narrowed scope if scoped)
- boundaries (time constraints, domain limits, excluded sources)
- expected output format (`contracts/schemas/research-report.json` or markdown brief)

### 2. Formulate Search Strategy (Rounds 1-3)

- identify primary keywords, synonyms, and technical jargon
- run initial broad queries to map the landscape
- identify key authorities, official documentation, or reliable databases

### 3. Deep Dive Execution (Rounds 4-8)

- follow references, citations, and internal links from initial findings
- query specific sub-topics, alternative approaches, or edge cases discovered
- cross-reference conflicting information to find the root truth

### 4. Gap Analysis & Refinement (Rounds 9-10+)

- review current findings against the original objective
- identify what is still missing, ambiguous, or unverified
- execute highly targeted queries to fill the remaining critical gaps

### 5. Synthesize And Report

Produce a structured JSON or Markdown contract that downstream roles can use directly:
- `Technical Architect` gets evaluated technologies, limits, and trade-offs
- `Business Analyst` gets market data, competitor analysis, or feature comparisons
- `Content Writer` gets factual, verified domain knowledge with citations

## Output Format

```markdown
# <Topic> - Research Synthesis

## Objective & Scope
- Core question:
- Constraints:

## Execution Metrics
- depth_mode: deep | scoped
- Rounds completed: (>= 10 if deep; >= 3 if scoped)
- scope_waiver_note: (required if scoped)
- Sources analyzed:
- Confidence score: [High/Medium/Low]

## Recommended Next Roles
- role | rationale | open_decisions

## Key Findings
- 
- 

## Data Triangulation & Conflicts
- 
- 

## Critical Gaps (What remains unknown)
- 
- 

## Source References
- [Source Name](URL) - Context / Credibility
```

## Checklist

- [ ] depth_mode set and round minimum met for that mode
- [ ] data triangulated across multiple independent sources
- [ ] source credibility evaluated and documented
- [ ] recommended_next_roles populated in JSON handoff
- [ ] gaps, assumptions, and limitations explicitly stated
- [ ] output structured for downstream agent use (no raw dumps)
- [ ] feature-ticket.json not authored by Researcher

## Related Skills

- **analyze-business-requirements**: Read BA framing only — do not populate feature-ticket.json as Researcher
- **agent-context-management**: Prevent token bloat during long research sessions
- **agent-tool-orchestration**: Manage search APIs, web scrapers, and local retrieval tools
- **agent-quality-gate**: Verify research findings before synthesizing
