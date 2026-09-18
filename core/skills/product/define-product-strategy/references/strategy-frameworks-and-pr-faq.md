# Product Strategy Frameworks & Amazon PR/FAQ Standard

> Comprehensive guide for high-impact product strategy, defensible competitive moats, opportunity mapping, and bias-free discovery.

---

## 1. The Framing Gate Guardrail

Before committing time, research, or engineering effort, every proposed product initiative must pass through the **Framing Gate**.

```
                       [ Incoming Feature Request ]
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │          Framing Gate Audit          │
                 │ 1. Who is the specific user segment? │
                 │ 2. What is the quantified pain point?│
                 │ 3. What evidence proves this pain?   │
                 │ 4. What is the target metric outcome?│
                 └──────────────────┬───────────────────┘
                                    │
                    All 4 verified? │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
                 [ YES ]                         [ NO ]
                    │                               │
                    ▼                               ▼
          Proceed to Strategy             Pushed Back to Originator:
          (OST / 7 Powers / PR/FAQ)       Require Discovery & Evidence
```

### The 4 Pillars of Product Validation
1. **Problem Validation**: Do customers actually experience this pain in their daily workflow? (Tested via Mom Test interviews).
2. **Solution Validation**: Does our proposed approach effectively eliminate the pain better than existing alternatives? (Tested via interactive prototypes).
3. **Demand Validation**: Are customers willing to adopt, allocate budget, or sign up? (Tested via smoke tests, landing pages, LOIs).
4. **Pricing Validation**: Can we capture sustainable economic surplus? (Tested via Van Westendorp Price Sensitivity and Willingness-to-Pay).

---

## 2. Amazon Working Backwards (PR/FAQ) Template

The Amazon PR/FAQ consists of a future Press Release (1 page) and two sets of FAQs (Customer FAQ and Internal FAQ).

### A. Press Release Format
```markdown
# [Product/Feature Name] — Launch Day Press Release

**FOR IMMEDIATE RELEASE**  
[City, Country] — [Target Launch Date] — [Company Name] today announced [Product Name], a new [category description] that enables [target customer segment] to [primary benefit/outcome] without [existing painful trade-off].

### The Problem
[Describe the status quo pain point, quoting specific user friction, lost hours, or wasted capital under existing alternatives.]

### The Solution & Core Value
[Describe how the new product solves the problem elegantly, highlighting the primary mechanism of action and user experience.]

### Leader Quote
"[Quote from Product Leader / CEO explaining the strategic vision, customer obsession, and long-term commitment.]"

### Customer Delight Quote
"[Quote from a target customer describing how the product transformed their workflow, citing concrete outcomes (e.g. 'Reduced reconciliation time from 3 days to 15 minutes').]"

### How to Get Started & Call to Action
[Clear instructions on how users can sign up, migrate, or try the feature today, including pricing tier availability and URL.]
```

### B. Customer FAQ (5-10 Questions)
- How does this differ from [Existing Feature / Competitor]?
- How much does it cost, and what plan do I need to be on?
- How do I migrate my existing data or workflow?
- What happens if my network goes offline or the system encounters an error?
- How is my data protected and kept confidential?

### C. Internal FAQ (Engineering, Operations, Business)
- What is the total engineering effort and infrastructure dependency?
- What are the unit economics (COGS, inference/compute cost per transaction)?
- What are the primary technical and operational risks (security, scalability, third-party vendor lock-in)?
- How will this impact customer support load and operational overhead?
- What are the launch-kill criteria if leading indicators fail to reach targets?

---

## 3. Hamilton Helmer's 7 Powers Defensibility Matrix

A product strategy without a defensible "Power" creates transient value that will be competed away. Every significant bet must identify its power.

| Power | Definition | Benefit Mechanism | Barrier Mechanism |
|---|---|---|---|
| **Scale Economies** | Cost per unit decreases as production volume increases | Lower operational cost structure | Competitor must match scale to match margins |
| **Network Effects** | Value of service increases with each incremental user | Superior liquidity or utility | High switching friction; two-sided lock-in |
| **Counter-Positioning** | A new business model that incumbents cannot copy without harming existing business | Novel, attractive customer offering | Incumbent cannibalization dilemma (Innovator's Dilemma) |
| **Switching Costs** | Value loss incurred by a customer when migrating to a competitor | Customer retention & predictable cash flows | High financial, operational, or data migration penalty |
| **Branding** | Objective trust and positive emotional affinity built over time | Premium pricing power & lower acquisition cost | Decades of consistent quality cannot be bought overnight |
| **Cornered Resource** | Preferential access to an elusive, non-replicable asset | Exclusive capability or regulatory advantage | IP patents, regulatory licenses, exclusive talent/data |
| **Process Power** | Embedded operational dexterity and organizational muscle | Speed, quality, or defect rate far superior to peers | Tacit knowledge accumulated through complex iteration |

---

## 4. Teresa Torres Opportunity Solution Trees (OST)

Structure continuous discovery by maintaining a living Opportunity Solution Tree:

```
[ Desired Outcome: Increase 30-Day Paid Conversion from 4.2% to 6.5% ]
   │
   ├── Opportunity 1: Users abandon during complex workspace setup
   │     ├── Solution 1A: 1-Click Interactive Template Gallery
   │     │     ├── Assumption Test: Click-through on preview cards
   │     │     └── Assumption Test: Setup completion time < 3 mins
   │     ├── Solution 1B: AI-Assisted Guided Onboarding Wizard
   │     └── Solution 1C: Pre-populated Sandbox Workspace
   │
   └── Opportunity 2: Stakeholders lack visibility to approve purchase
         ├── Solution 2A: Automated Executive Summary PDF Export
         └── Solution 2B: Free Read-Only Stakeholder Reviewer Seats
```

**OST Rules**:
1. Never evaluate a single solution in a vacuum; always compare at least 3 solutions per opportunity.
2. Break solutions down into testable assumptions (Value, Usability, Feasibility, Viability, Ethics).
3. Test assumptions using the fastest, lowest-cost method before writing production code.

---

## 5. Rob Fitzpatrick The Mom Test Interview Protocol

The Mom Test establishes how to talk to customers and validate demand when everyone is lying to you to be polite.

### The 3 Core Rules of The Mom Test
1. **Talk about their life and past behavior, not your idea.**
2. **Ask about specifics in the past, not generic opinions or promises about the future.**
3. **Listen more than you talk (80/20 rule); never defend or pitch.**

### Bad Questions vs. Mom Test Questions

| ❌ Flawed / Pitch Questions (Biased) | ✅ Mom Test Questions (Objective) | Why |
|---|---|---|
| "Do you think an AI PRD writer is a good idea?" | "When was the last time you wrote a PRD? How did you gather the inputs?" | Opinions are free; past behavior reveals actual friction. |
| "Would you pay $50/month for automated sprint planning?" | "How much did you spend last quarter solving workload imbalance across squads?" | Hypothetical willingness-to-pay is almost always fabricated. |
| "Would you use an interactive story mapping tool?" | "How do you currently visualize releases for your executive team? Walk me through your screen." | Reveals existing tools, manual workarounds, and real pains. |
| "Don't you hate how long it takes to review customer tickets?" | "How many hours did your team spend on ticket tagging this week? What broke because of it?" | Avoids leading the witness; anchors on quantified impact. |
