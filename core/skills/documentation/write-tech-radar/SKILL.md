---
name: write-tech-radar
description: Draft or update a technology radar entry by summarizing context, trade-offs, recommendation, and adoption guidance in a concise decision-oriented format. Use when documenting technology choices, trials, or directional guidance.
---

# Write Tech Radar

Use this skill when a team needs a technology radar, adoption note, or concise engineering recommendation artifact.

**Role routing:** Binding architecture decisions → **Technical Architect** with `contracts/schemas/adr-spec.json`. Delivery sequencing → **Technical Lead** with `technical-delivery-plan.json`. Runbooks and API docs → **Technical Writer** with `write-documentation`. This skill is for **radar-style** adopt/hold/trial guidance, not a substitute for ADRs.

## When to Use

- documenting a technology choice or trial
- giving directional adoption guidance
- summarizing context + trade-offs + recommendation
- concise decision-oriented entry

## Core Rules

- optimize for decision clarity, not essay length — every entry must answer "should my team use this, and under what conditions?" without prose padding
- state the recommendation ring explicitly using the **four standard ThoughtWorks ring names only**: `Adopt`, `Trial`, `Assess`, or `Caution` (not "Hold", "Avoid", or custom names); custom ring names break organizational radar consistency
- capture trade-offs, not just benefits; every entry requires a risk/trade-off analysis alongside the adoption rationale
- separate observed production evidence from inferred judgment; explicitly label claims that are POC-only versus verified-in-production
- **Caution ring sign-off gate**: technologies assigned to `Caution` require explicit Architecture Board or Technical Lead sign-off before any new service or repository adopts them — this is an enforced governance gate, not a soft recommendation
- **Time-bounded Assess phase**: entries in `Assess` must declare measurable POC success criteria and a deadline; without a defined evaluation window, `Assess` becomes a permanent parking lot
- link radar entries to ADRs using **MADR format** (Markdown Architectural Decision Records) — radar entries are navigation aids, ADRs are the binding record
- track AI tool adoption in a dedicated quadrant or sub-radar with rings explicitly applied; re-evaluate AI tool entries at minimum **bi-annually** (AI maturity evolves faster than conventional tooling)
- keep the entry useful to future readers who were not in the original discussion — avoid jargon and internal acronyms without expansion

## Suggested Process

### 1. Define The Technology Decision Scope

Clarify:

- what technology or practice is being assessed
- whether the team is adopting, trialing, holding, or avoiding it
- what context or constraints matter most

### 2. Gather Relevant Evidence

Collect:

- current use cases
- known strengths
- known risks
- operational or migration impact
- alternatives that were considered

### 3. Draft The Radar Entry

A strong entry usually includes:

- title
- status or recommendation
- summary of why it matters
- where it fits well
- where it should be avoided
- migration or adoption guidance

### 4. Make The Recommendation Actionable

The reader should understand:

- whether to use it now
- under what conditions
- who should care
- what follow-up work or validation is still needed

### 5. Review For Signal

Check:

- the recommendation is obvious
- evidence and trade-offs are balanced
- internal jargon is minimized
- unsupported claims are removed or softened

### 2026: Tech Radar Structuring and AI Tool Tracking

To capture architecture-aligned decisions and rapid AI developments:

- **ADR Integration**: Every radar entry representing a significant shift must link directly to an Architectural Decision Record in MADR format (Markdown Architectural Decision Records), ensuring full lineage from high-level assessment to concrete technical design.
- **AI Tool Adoption Tracking**: Separate AI tools, libraries, and sub-agents into a dedicated "AI Tools" ring or sub-radar. This tracks:
  - **Adopt**: Verified AI tools integrated safely into standard development flows.
  - **Trial**: AI tools undergoing sandbox security and efficiency audits.
  - **Assess**: New AI technologies being monitored for enterprise-grade maturity.
  - **Hold**: AI systems restricted due to data privacy or licensing risks.
- **Standard Radar Entry Template**: Use the following inline block format for all technology additions:
  ```yaml
  name: "Technology Name"
  ring: "Adopt / Trial / Assess / Hold"
  quadrant: "Languages & Frameworks / Tools / Platforms / Infrastructure"
  rationale: "Brief summary of technical or business motivation."
  adr_link: "Relative path or URL to the MADR file."
  justification: "Detailed context explaining why this specific lifecycle state is selected."
  ```

## Output Contracts

When the engagement moves beyond a radar entry into a binding technical decision, this skill emits machine-readable artifacts so Technical Architect and Technical Lead can consume them without re-interviewing stakeholders:

- **`contracts/schemas/architecture-options.json`** — emit when the assessment surfaced 2+ viable options that require explicit comparison before commitment. Populate `options[]` with the same context / trade-off pairs summarized in the radar entry; reference the radar entry path in `evidence_radar_link`.
- **`contracts/schemas/adr-spec.json`** — emit once a single recommendation is accepted and becomes a binding decision. Fill `title`, `context`, `decision`, `consequences`, and `alternatives_considered[]` directly from the radar entry; set `madr_path` to the inline MADR block linked from the radar entry. This is the artifact `technical-architect` records when consuming this skill's output.

Skip emission when the output is a non-binding adoption note or AI-tool tracker entry — those remain radar-only.

## Checklist

- [ ] decision scope identified
- [ ] relevant evidence gathered
- [ ] recommendation made explicit
- [ ] trade-offs captured
- [ ] adoption guidance included
- [ ] wording kept concise and decision-oriented
- [ ] ADR references provided in MADR format
- [ ] AI tool adoption explicitly tracked under AI Tools rings
- [ ] Inline radar entry template fully populated with lifecycle justification

## Related Skills

- **meeting-review**: Gather multi-role input before writing a recommendation
- **write-documentation**: Expand the radar entry into deeper technical docs
- **review-service**: Use service findings as evidence for technology guidance
- **security-audit**: Include security posture in technology assessment
- **commit-code**: Prepare the entry for delivery
