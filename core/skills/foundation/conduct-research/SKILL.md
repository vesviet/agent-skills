---
name: conduct-research
description: Execute iterative, deep-dive research to discover, validate, and synthesize complex information. Use when building context, evaluating technologies, or mapping ambiguous domains, specifically designed for 10-round deep dive requirements.
---

# Conduct Research

Use this skill when a task requires deep discovery before architectural, product, or business implementation. It is specifically built for roles like `Researcher` that require aggressive triangulation and deep validation.

## Core Rules

- enforce the 10-round deep dive minimum: do not stop at the first relevant result
- triangulate data across multiple independent sources to eliminate hallucinations and bias
- document missing information explicitly rather than guessing or fabricating
- evaluate source credibility and document confidence levels
- structure the output for agent-to-agent consumption, avoiding raw text dumps

## Suggested Process

### 1. Define The Objective

Clarify:
- the core hypothesis, question, or problem to solve
- boundaries (time constraints, domain limits, excluded sources)
- expected output format (e.g., `research-report.json`, detailed markdown)

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
- Rounds completed: (must be >= 10)
- Sources analyzed:
- Confidence score: [High/Medium/Low]

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

- [ ] minimum 10 distinct research iterations executed
- [ ] data triangulated across multiple independent sources
- [ ] source credibility evaluated and documented
- [ ] gaps, assumptions, and limitations explicitly stated
- [ ] output structured for downstream agent use (no raw dumps)

## Related Skills

- **analyze-business-requirements**: Clarify the exact business need before starting research
- **agent-context-management**: Prevent token bloat during the 10 rounds of context building
- **agent-tool-orchestration**: Manage search APIs, web scrapers, and local retrieval tools
- **agent-quality-gate**: Verify research findings before synthesizing
