---
name: define-product-strategy
description: Formulate, stress-test, and document product strategy using Amazon Working Backwards (PR/FAQ), Hamilton Helmer 7 Powers moat analysis, Teresa Torres Opportunity Solution Trees (OST), and Rob Fitzpatrick The Mom Test problem validation. Use when shaping new product initiatives, framing strategic bets, analyzing competitive defensibility, validating customer demand without leading bias, or activating the Framing Gate to push back on underspecified requirements.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Define Product Strategy

Use this skill to transform visionary or ambiguous product ideas into rigorous, customer-anchored, defensible product strategies before committing engineering capacity.

## When to Use

- shaping new product initiatives, zero-to-one bets, or major platform pivots
- drafting Amazon Working Backwards PR/FAQ documents (Press Release & FAQs)
- evaluating competitive defensibility and sustainable moats using Hamilton Helmer's 7 Powers
- structuring discovery research using Teresa Torres Opportunity Solution Trees (OST)
- formulating objective problem discovery interview protocols using The Mom Test
- activating the **Framing Gate** to challenge solution-biased or unsubstantiated feature requests
- establishing pre-committed kill criteria and pivot triggers before build phase

## Core Rules

- **Enforce the Framing Gate Guardrail**:
  - Never accept a solution-first feature request without validating the underlying customer problem
  - Push back immediately if the request lacks: target user segment, quantified pain point, verifiable evidence, or measurable business outcome
  - Mandate the 4 validation pillars: Problem, Solution, Demand, and Pricing validation
- **Apply Amazon Working Backwards (PR/FAQ)**:
  - Author a 1-page future Press Release written from the customer perspective on launch day
  - Required sections: Headline, Subheadline, Summary, Problem, Solution, Leader Quote, Customer Quote, Call to Action
  - Pair with Customer FAQ (practical user questions) and Internal FAQ (architecture, unit economics, risks)
- **Analyze 7 Powers Moat Defensibility (Hamilton Helmer)**:
  - Evaluate the initiative against the 7 Powers: Scale Economies, Network Effects, Counter-Positioning, Switching Costs, Branding, Cornered Resource, Process Power
  - For every identified power, distinguish the *Benefit* (what creates customer value) from the *Barrier* (what prevents competitor imitation)
- **Construct Opportunity Solution Trees (OST - Teresa Torres)**:
  - Anchor the tree on a single Desired Business Outcome
  - Map branch layers: Desired Outcome → Customer Opportunities (unmet needs) → Potential Solutions → Specific Assumption Tests
  - Prevent the "Solution-First Trap" by comparing at least 3 distinct solutions per high-priority opportunity
- **Adhere to The Mom Test Interview Protocol (Rob Fitzpatrick)**:
  - Never pitch ideas or ask hypothetical questions ("Would you buy an AI feature that does X?")
  - Inquire strictly about past historical behavior, actual workflows, current workarounds, and quantified costs (hours lost, budget wasted)
- Detailed templates, question rubrics, and 7 Powers matrix: [`references/strategy-frameworks-and-pr-faq.md`](references/strategy-frameworks-and-pr-faq.md)

## Suggested Process

### 1. Execute Framing Gate & Problem Discovery
Inspect the incoming initiative. Evaluate against the Framing Gate. If the problem is unvalidated, design a Mom Test interview script to discover past behavior and existing workarounds.

### 2. Map the Opportunity Solution Tree (OST)
Define the primary Desired Business Outcome. Group customer interview findings into distinct Opportunity clusters. Brainstorm competing solution candidates for each opportunity.

### 3. Conduct 7 Powers Defensibility Assessment
Evaluate whether the preferred solution creates a durable moat. Identify which of the 7 Powers can be established, the mechanism of the Barrier, and whether competitor incumbent counter-positioning is viable.

### 4. Author the Amazon PR/FAQ Document
Draft the Press Release capturing customer delight and core value propositions. Write the Customer FAQ answering pricing, migration, and UX questions. Write the Internal FAQ addressing risks, dependencies, and unit economics.

### 5. Define Kill Criteria & Validation Gates
Set explicit, pre-committed negative signals that will trigger an immediate kill or pivot before engineering commitment.

## Checklist

- [ ] Framing Gate executed; verified customer pain and evidence documented
- [ ] Opportunity Solution Tree links business outcome directly to customer opportunities
- [ ] at least 3 competing solutions considered per opportunity branch
- [ ] 7 Powers analysis identifies both Benefit and defensible Barrier
- [ ] Amazon Press Release written in customer-centric present tense
- [ ] Customer FAQ and Internal FAQ address key operational and financial questions
- [ ] Mom Test interview guide uses only past behavioral inquiries, zero hypothetical pitches
- [ ] pre-committed Kill Criteria defined to prevent sunk-cost traps

## Related Skills

- **prioritize-roadmap**: score and sequence validated initiatives using RICE and Kano
- **model-saas-metrics**: calculate unit economics, LTV/CAC, and AI outcome TCO
- **build-story-map**: slice validated PRD into Epic-to-Story releases and CPM Gantt
- **write-product-brief**: produce standardized product briefs for team handoff
- **elicit-requirements**: conduct deep stakeholder elicitation interviews
