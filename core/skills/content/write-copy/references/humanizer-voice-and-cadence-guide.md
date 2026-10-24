# Humanizer Voice, Cadence & Anti-AI Slop Guide

This guide establishes the linguistic standards, rhythm discipline, and vocabulary governance required to produce natural, authentic human copy that eliminates synthetic AI clichés and corporate filler.

---

## 1. Zero-Tolerance Marketing Cliché Blacklist

Artificial intelligence models default to predictable tropes when asked to write marketing or promotional copy. These words and phrases destroy reader credibility, signal synthetic generation, and dilute technical substance.

Every copy deliverable must be screened against this blacklist. Any occurrence will trigger an immediate revision.

### 1.1 The Marketing Cliché Substitution Catalog

| Banned AI Marketing Cliché | Why It Fails | Mandatory Human Replacement / Solution |
| :--- | :--- | :--- |
| **"Supercharge your..."** | Vague, overused hyperbole with zero technical meaning | "Accelerate", "cut build times by 40%", "automate" |
| **"Unleash the power of..."** | Melodramatic fantasy trope; sounds like a video game | "Deploy", "query", "run", "configure" |
| **"Game-changer"** | Empty corporate buzzword; claims unearned significance | "Architectural shift", "breakthrough", describe the specific performance gain |
| **"Cutting-edge / Revolutionary"** | Unprovable puffery that breeds skepticism | "Production-tested", "latest stable v2.4 spec", "sub-millisecond" |
| **"All-in-one solution"** | Conveys bloat and mediocre compromises to engineers | "Unified platform", "single CLI", "integrated toolkit" |
| **"Seamless integration"** | Tech debt euphemism; integration is rarely seamless | "Zero-config sync", "native webhook binding", "2-line SDK import" |
| **"Elevate your business / game"** | Abstract corporate speak with zero tangible outcome | "Grow pipeline by 25%", "ship features without regressions" |
| **"Look no further"** | 1990s infomercial slogan; patronizing to smart readers | **DELETE ENTIRELY** — state the primary customer benefit immediately |
| **"In today's fast-paced world..."** | Ponderous, throat-clearing intro that bores readers | **DELETE ENTIRELY** — lead with the bleeding-neck problem directly |
| **"Delve / Delving deep"** | High-frequency AI marker word; unnatural in normal speech | "Examine", "inspect", "audit", "trace", "break down" |
| **"A testament to..."** | Stilted Victorian phrasing common in LLM outputs | "Demonstrates", "proves", "validates", cite the benchmark metric |
| **"Tapestry / Mosaic / Symphony"** | Pseudo-poetic fluff used by AI to describe simple workflows| "Architecture", "system", "stack", "pipeline", "network" |
| **"Foster / Fostering growth"** | Passive HR speak that lacks commercial agency | "Increase", "build", "expand", "accelerate" |
| **"Empower / Empowering teams"** | Trite corporate abstraction; overused to the point of numbness | "Give developers direct control", "let engineers deploy without tickets" |
| **"Bespoke / Tailored solution"** | Pretentious agency jargon | "Custom configuration", "modular architecture", "tailored to your stack" |

---

## 2. The 20/60/20 Sentence Burstiness Calibration

A universal signature of synthetic LLM writing is **rhythmic monotony**: generating paragraph after paragraph of medium-length sentences (14–18 words) with uniform clause structures. Human speech and persuasive copy possess **high burstiness**: short, punchy declarative statements mixed with detailed explanatory mechanics and complex conditional clauses.

```
+---------------------------------------------------------------------------------------+
| Sentence Length Distribution Target (20 / 60 / 20)                                    |
+---------------------------------------------------------------------------------------+
| [~20% Short: 3-7 words]  ====> Hooks, rhythm breakers, visceral truth-bombs         |
| [~60% Medium: 8-18 words] ====> Explanatory value propositions, mechanics, proof     |
| [~20% Long: 19-28 words]  ====> Architectural nuance, trade-offs, conditional logic    |
+---------------------------------------------------------------------------------------+
```

### 2.1 Cadence Breakdown by Tier

1. **Short Punchy Sentences (~20%, 3–7 words)**:
   - Purpose: Grab attention, reset mental fatigue, emphasize an indisputable takeaway.
   - *Examples*:
     - "Stop guessing your cloud spend."
     - "Latency kills conversion."
     - "Deploy in seconds."
     - "Here is the catch."
     - "That is unacceptable."

2. **Medium Explanatory Sentences (~60%, 8–18 words)**:
   - Purpose: Deliver the functional core of the message with clarity and momentum.
   - *Examples*:
     - "Our query optimizer rewrites slow PostgreSQL joins before they hit your production database."
     - "Every customer request routes to the nearest edge location across 310 points of presence."
     - "You get instant visibility into memory leaks without redeploying your Docker containers."

3. **Complex Persuasive Sentences (~20%, 19–28 words)**:
   - Purpose: Articulate engineering trade-offs, compare multi-variable realities, and handle subtle objections.
   - *Examples*:
     - "While traditional APM tools sample only 1% of production traces to minimize CPU overhead, our eBPF collector captures every single transaction with less than half a percent runtime degradation."
     - "If your database migration triggers table locks during peak traffic, our shadow-write proxy intercepts the queries and safely buffers them until indexing completes."

### 2.2 The Monotony Audit (The Rule of Three)
- **Check**: Never allow three consecutive sentences of similar length (e.g. 15 words, 16 words, 15 words).
- **Fix**: If you spot three uniform sentences, break one into two punchy fragments, or fuse two clauses using a colon or em-dash.

---

## 3. Active Voice Agency Mandate (≥85%)

In high-conversion copywriting, the reader or the product must be the direct grammatical subject taking decisive action. Passive voice obscures responsibility, weakens emotional impact, and sounds evasive.

### 3.1 Passive vs. Active Transformations

| Passive AI Evasion (Weak) | Grammatical Defect | High-Agency Active Transformation (Strong) |
| :--- | :--- | :--- |
| "A 45% latency reduction can be achieved by utilizing our cache." | Passive voice; missing agent; prepositional bloat | **"You cut API latency by 45% with our edge cache."** |
| "Decisions should be made based on telemetry data." | Passive imperative; who makes the decision? | **"Your engineering team makes deployment decisions using real-time telemetry."** |
| "Microservice costs are tracked and visualized automatically." | Passive construction hides product agency | **"CloudPrune tracks and graphs every container cost down to the dollar."** |
| "It is believed that distributed transactions are brittle." | Impersonal dummy pronoun ("It is...") | **"Senior architects know that distributed two-phase commits inevitably fail at scale."** |

### 3.2 Grammatical Audit Procedure
1. Search the draft for passive auxiliary forms: `is + [verb]ed`, `are + [verb]ed`, `was + [verb]ed`, `can be + [verb]ed`, `has been + [verb]ed`.
2. Identify the true actor (the developer, the engineering lead, the compiler, the platform).
3. Move the actor to the beginning of the clause as the subject, followed immediately by an active transitive verb.

---

## 4. Conversational Cadence & Line-Level Rhythm

Conversion copy is written to be spoken aloud. It is dialogue, not an academic thesis.

### 4.1 One-Thought-Per-Line Formatting
Modern readers scan content on mobile devices. Dense paragraphs of 6–8 lines appear intimidating and trigger scroll-past behavior.
- Structure key sales arguments in single-thought paragraphs of **1 to 3 lines**.
- Use visual whitespace as punctuation to create anticipation and pacing.

#### Example: Monolithic Corporate vs. Human Conversational Formatting

*Monolithic Corporate Block (Fails Engagement)*:
> Our next-generation database proxy provides automated connection pooling and intelligent read-write splitting which ensures that your application layer never exhausts available PostgreSQL backend sockets during seasonal traffic surges while concurrently reducing master database replication lag through localized caching mechanisms.

*Human Conversational Formatting (High Engagement)*:
> Your application should never crash because PostgreSQL ran out of connection sockets.
>
> That sounds obvious. Yet during Black Friday surges, unpooled database connections take down more checkout carts than distributed denial-of-service attacks.
>
> Our proxy acts as a shock absorber. It pools 10,000 incoming app connections into 50 multiplexed database sockets.
>
> Zero socket exhaustion. Sub-millisecond routing. Zero code changes.

### 4.2 Conversational Bridges & Connectors
Use conversational connective tissue to pull the reader down the page effortlessly:
- "Here is why that matters."
- "Let's look at the numbers."
- "Notice what just happened."
- "The result?"
- "Now consider the alternative."

### 4.3 The Read-Aloud Test
Before finalizing any copy asset, read every line aloud at normal speaking speed:
- If you run out of breath before finishing a sentence, the sentence is too long.
- If your tongue trips over adjacent consonant clusters or repetitive vowel sounds, rewrite for phonetic fluidity.
- If a sentence sounds like something no human would say across a coffee table or at a whiteboard, strike it immediately.
