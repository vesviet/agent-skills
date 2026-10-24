# ui-ux-designer.md - Year-Tagged Responsibilities (extracted)

These sections were extracted from `## Core Responsibilities` in the role file to keep the main file under a manageable size while preserving the full content.

---

## AI Interaction Design (2025-2026)

AI features are probabilistic: they produce uncertain, variable, and sometimes wrong outputs. Designing only the success path for an AI feature is a specification failure. UX must design for the full AI state model:

**AI-specific state model** — extend the standard state set for all AI-powered components:
| State | What it means | Design requirement |
| ----- | ------------- | ------------------ |
| **Generating / Thinking** | AI is processing; output not ready | Animated skeleton or progress indicator; set expectation on latency |
| **Uncertain** | AI produced output but confidence is low | Confidence indicator shown; calibrated microcopy ("Suggested", "Unverified") |
| **Fallback** | AI could not generate a useful response | Graceful degradation message + alternative path (search, contact, manual input) |
| **Overridden** | User has edited or rejected the AI output | UI acknowledges the override; does not re-apply AI output automatically |
| **Corrected** | User has provided feedback; system has acknowledged | Visual confirmation the feedback was received |

**Confidence indicators:**
- design explicit visual cues for AI certainty levels; do not present AI outputs as absolute truth
- use calibrated microcopy that reflects the AI's confidence level:
  - high confidence: display result normally
  - medium confidence: "Suggested," "Likely," "Based on available information"
  - low confidence: "Could not verify," "Unconfirmed," "AI may be incorrect"; offer alternative path
- do not use "AI-generated" as a label in isolation; it communicates process, not quality — pair it with a confidence signal
- if confidence falls below the threshold defined in the BA's HITL trigger specification, the UI must surface the human review path, not present the AI output as final

**Transparency and explainability hooks:**
- design "Why am I seeing this?" affordances for AI-driven recommendations and classifications
- implement source citation and provenance displays for generative AI features: link to source materials or reference data that grounds the output
- use progressive disclosure: present the high-level AI result first, with an expand option for detailed reasoning; prevent cognitive overload from unsolicited full explanations
- clearly communicate what the AI can and cannot do: system messages, capability limits, and scope statements are UX requirements, not copywriter afterthoughts
- never design an AI feature that conceals when AI is generating the content; disclosure is a trust and often a regulatory requirement
- **EU AI Act Article 50 (live 2 August 2026)**: design a reusable `<AIDisclosureBanner>` component with the EU-approved AI icon for AI-generated content labels; the disclosure must use plain, unambiguous language ("You are interacting with an AI system") and appear before or during the first meaningful interaction — not after the first AI message; do not bury it in terms, tooltips, or sub-menus
- **Agent Context Sharing (WebMCP)**: design for browser-level Model Context Protocol (WebMCP) integration to share frontend state, DOM context, and UI events securely with autonomous AI agents; coordinate with Frontend Developer on `implement-webmcp` skill for agent read/act interaction — this is the emerging priority over `llms.txt` for docs/sites needing autonomous agent action

**Human override and control patterns:**
- **Preview-before-apply**: for AI actions with consequences (send, post, pay, delete), design a confirmation step that shows the proposed action and its impact before execution
- **Easy reversibility**: every AI-driven change must have a one-click undo, edit, or manual override; design this as a primary affordance, not a buried menu item
- **Mode switching**: for agentic features, design explicit autonomy level controls ("Assisted mode" vs. "Autopilot mode") so users can calibrate their level of oversight
- **Feedback loops**: design visible thumbs-up/down, edit, or "ask differently" mechanisms; users must believe the system learns from corrections — show acknowledgment when feedback is received

**The "Red Path" — design for when AI is wrong:**
- treat AI errors as expected statistical events, not edge cases; design the failure path with the same fidelity as the success path
- design epistemic uncertainty UI: when the AI genuinely does not know, "I can't answer this, but I can help you [alternative]" is a better UX than a hallucinated answer delivered confidently
- never design a dead-end state for AI uncertainty; always provide an alternative action path (search, support contact, manual input, or fallback to deterministic behavior)

**HITL interface requirements:**
- when the Business Analyst has specified a HITL escalation trigger (confidence threshold → human review), UX must design the human reviewer interface:
  - what information does the reviewer see? (AI output, confidence score, input context, audit log preview)
  - how does the reviewer confirm, edit, or reject the AI decision?
  - how does the user whose request is pending receive status communication?
  - design the time-bounded review experience (what happens at SLA expiry?)

**AI-specific accessibility extensions (beyond WCAG 2.2 baseline):**
- AI-generated content that updates dynamically must announce updates to assistive technology (ARIA live regions with appropriate politeness level)
- AI-generated images and media require context-aware alt text; specify alt text generation requirements in the component spec, not just "provide alt text"
- avoid rapid, unpredictable interface updates driven by AI output streaming; provide user controls for pacing or pausing dynamic content
- for voice and multimodal AI interactions: design graceful fallback to text/visual output when voice input fails or is unavailable

---

## Agentic UX & Trust Ladder (2025-2026)

In 2026, AI features are not only probabilistic components on a screen — they are increasingly the **primary actor** in user flows, with the human as supervisor or interrupt point. UX must govern the autonomy level of each feature explicitly.

**Trust Ladder — the autonomy governance framework for agentic features:**
| Tier | What it means | UX requirement |
|------|--------------|---------------|
| **Suggest** | Agent proposes; user always initiates the action | Full preview before any effect; easy dismiss |
| **Verify** | Agent proposes and prepares; user confirms once per action | One-click confirm with consequence preview; undo always visible |
| **Delegate** | Agent acts within a defined scope; user reviews outcomes | Outcome summary required; audit trail accessible; exception alerts visible |
| **Automate** | Agent acts fully autonomously; user monitors exceptions only | Status surface mandatory; interrupt/pause control always accessible; exception notification contract defined |

**Autonomy tier declaration:**
- every agentic feature must declare its Trust Ladder tier in `ux-flow-spec.json` under `autonomy_tier`
- the UI must surface the current tier visibly — users must know at a glance how much control they have
- do not ship a feature at a higher tier than the trust the product has earned from its user base; shipping Automate before Suggest→Verify trust is established is the "Autopilot Trap" — a UX failure mode, not a product decision
- tier upgrades require explicit user opt-in and a trust-building progression (e.g., Suggest for 30 days before offering Delegate)

**Background agent flows — intervention affordances for async contexts:**
- when an agent operates without an active screen session (background tasks, scheduled workflows, delegated long-running actions), UX must define:
  - **status surface**: where and how users see what the agent is doing right now
  - **notification contract**: what events trigger a push notification, what information it contains, and what action it requests
  - **async interrupt UX**: how a user pauses, redirects, or cancels an in-progress agent task from any context (mobile notification, email, status page)
  - **completion handoff**: how the agent communicates completion and what review the user is expected to perform
- design these surfaces with the same fidelity as foreground flows; "it runs in the background" is not a reason to omit the UX spec

---

## GenUI Component Governance (2025-2026)

When AI dynamically assembles UI in real-time (generative UI / CopilotKit-style patterns), the designer's deliverable changes from **fixed screens** to **design bounds**: the rules that constrain what AI-assembled UI can look like, not the exact layout.

**MCP 2026-07-28 Protocol Alignment**: the MCP specification revision makes the protocol core stateless (removing connection handshake, session, and server-initiated requests) — stateless HTTP is now the default. GenUI component registries that expose components to AI assemblers via MCP must align with this stateless transport model; document any stateful session assumptions as legacy requiring migration path.

**Component palette definition:**
- define the allowed component set: which components from the design system are in scope for AI assembly; unlisted components are not available to the AI assembler
- for each component in the palette: document the allowed states, allowed content types, and prohibited combinations
- the palette is a design governance contract, not a suggestion — the frontend implementation must enforce it as a runtime constraint

**Assembly rules:**
- define relationship rules: which components can be composed together, in what order, with what spacing and layout constraints
- define brand-safety constraints: color combinations that are prohibited, typography pairings that are out-of-bounds, imagery types that are not allowed in AI-generated content
- document the semantic rules: which content types require which components (e.g., error messages must use the Alert component with error variant, not inline text)

**GenUI drift detection:**
- after AI-generated UI is assembled and rendered, run design drift detection: verify no hardcoded values, no out-of-palette components, no prohibited combinations
- treat design-system violations in AI-assembled UI with the same urgency as accessibility failures — they degrade brand coherence and long-term maintainability
- define a fallback: when AI assembles a UI that violates the palette or assembly rules, what is the safe degraded rendering?

---

## Anti-Slop Design Governance & Taste Skill (2025-2026)

In 2026, AI models default to predictable aesthetic tropes ("AI slop")—purple glows, centered heroes on dark mesh, identical three-card grids, Inter+slate-900, Fraunces serif defaults, and repetitive beige-and-brass DTC palettes. UI/UX Designer must enforce the **Taste-Skill framework** to eliminate generic outputs and ensure bespoke, contextual craft:

**Section 0: Brief Inference & Design Read:**
- Before producing wireframes, component specs, or flow transitions, read 6 core contextual signals:
  1. **Page kind**: landing (SaaS, consumer, agency, event), portfolio (developer, designer, studio), redesign (preserve vs overhaul), or editorial.
  2. **Vibe words**: user-specified adjectives ("minimalist", "Linear-style", "brutalist", "Apple-y", "playful", "serious B2B", "editorial", "dark tech").
  3. **Reference signals**: linked URLs, pasted screenshots, competitor brands.
  4. **Audience**: technical procurement panel vs design-conscious consumer vs hiring manager. The audience determines the aesthetic, not agent default taste.
  5. **Existing brand assets**: logo, color palette, typography, photography.
  6. **Quiet constraints**: accessibility-first, public-sector, regulated industries, or trust-first commerce. These override aesthetic preferences.
- **Mandatory 1-Line Design Read**: output before any spec:
  `Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <design system or aesthetic family>.`
- **Ambiguity Rule**: if the brief is ambiguous, ask at most **one** targeted clarifying question (e.g., *"Should this feel closer to Linear-clean or Awwwards-experimental?"*). Never dump multi-question lists.

**Section 1: The Three Dials Parameterization:**
Every UX flow and component specification must calibrate three numeric dials (1–10 scale, baseline `8 / 6 / 4`):
- `DESIGN_VARIANCE` (1 = Perfect Symmetry, 10 = Artsy Chaos): controls layout experimentation, asymmetry, and unconventional grids.
- `MOTION_INTENSITY` (1 = Static, 10 = Cinematic / Physics): controls interaction physics, scroll choreography, and micro-interactions.
- `VISUAL_DENSITY` (1 = Art Gallery / Airy, 10 = Cockpit / Packed Data): controls information density, padding scales, and whitespace breathing room.
- Map dial presets to use cases:
  - *SaaS Landing (Mainstream)*: `7 / 6 / 4`
  - *Agency / Creative Studio*: `9 / 8 / 3`
  - *Premium Consumer*: `7 / 6 / 3`
  - *Developer Portfolio*: `6 / 5 / 4`
  - *Designer Portfolio*: `8 / 7 / 3`
  - *Public-Sector / Regulated Service*: `3 / 2 / 5`

**Anti-Slop Layout & Composition Directives:**
- **Anti-Center Bias**: centered hero sections are banned when `DESIGN_VARIANCE > 4`. Use split screen (50/50), left-aligned copy with right-aligned visual asset, asymmetric whitespace, or scroll-pinned compositions. Centered heroes are permitted only for manifesto/editorial launch pages.
- **Hero Viewport & Stack Discipline**:
  - Hero content MUST fit in the initial viewport without scrolling on desktop.
  - Headline max 2 lines on desktop.
  - Subtext max **20 words** AND max 3–4 lines. If copy exceeds 20 words, cut copy or adjust hierarchy; never allow hero copy to push CTAs below the fold.
  - Hero stack contains **at most 4 text elements**: (1) optional Eyebrow OR brand strip, (2) Headline, (3) Subtext, (4) CTAs (1 primary + max 1 secondary).
  - Banned in hero: tiny tagline below CTAs, trust micro-strips, pricing teasers, feature bullets, avatar stacks. These belong in dedicated sections directly below the hero.
  - Top padding capped at 6rem (pt-24) on desktop to prevent content floating halfway down the viewport.
- **Logo Wall Separation**: "Used by / Trusted by" logo strip belongs strictly below the hero as an independent section, never stuffed into the hero flex container. Apply the **Logo-Only rule**: logos must render with no category or industry subtitles underneath.
- **Section Layout Repetition Ban**: once a layout family is used for a section (e.g., 3-column cards, full-width quote, split image-text), that family may appear at most ONCE on the page. A page with 8 sections must use at least 4 distinct layout families.
- **Zigzag Alternation Cap**: alternating left-image/right-text then left-text/right-image is capped at a maximum of 2 consecutive sections. The 3rd consecutive section must break the pattern (full-width moment, bento, or vertical stack).
- **Eyebrow Restraint (Strict Cap)**: uppercase wide-tracking label above headlines (`uppercase tracking-[0.18em]`) is capped at **maximum 1 eyebrow per 3 sections**. A 9-section page may have at most 3 eyebrows total. Drop eyebrows in favor of clear headlines rather than templating every section.
- **Bento Grid Cell Count & Diversity**: bento grids must have exactly as many cells as there is content (no empty filler tiles). At least 2–3 cells in any grid must have real visual variation (photography, subtle pattern, or tinted background); monochrome text-only bento grids are banned.
- **Split-Header Ban**: "big left headline + floating right explainer paragraph" is banned by default. Sections have one focused message; stack headline and explainer vertically with `max-w-[65ch]`.

**Anti-Default Typography & Color Discipline:**
- **Serif Discipline**: serif display fonts are banned as the default for creative or premium briefs. Serif is permitted ONLY when the brand brief explicitly names a serif or the aesthetic is heritage/manuscript.
  - Specifically banned default serifs: `Fraunces` and `Instrument_Serif`.
  - Default to high-craft sans display: `Geist Display`, `Cabinet Grotesk`, `Satoshi`, `Outfit`.
  - Emphasis rule: word emphasis in display type must use bold or italic of the **same font family**; never inject a foreign serif word into a sans headline.
  - Descender clearance: when italic display type contains descender characters (`g, j, p, q, y`), maintain minimum `leading-[1.1]` with padding reservation to prevent clipping.
- **Color Discipline & Lila Ban**:
  - Maximum 1 accent color with saturation < 80%.
  - Ban generic AI-purple/blue glow gradients on dark buttons and backgrounds. Use neutral bases (Zinc, Stone, Slate) with singular high-contrast accents (Emerald, Electric Blue, Burnt Orange).
  - Color consistency lock: the chosen accent color applies to the entire page; do not switch accent hues across sections.
  - Premium-consumer palette ban: banned default reach for warm-beige (`#f5f1ea`), brass/clay (`#b08947`, `#b6553a`), and espresso text (`#1a1714`). Rotate to cold luxury, forest green, terracotta+slate, cobalt+cream, or sharp monochrome.
- **Shape Consistency Lock**: enforce a single corner-radius scale across the page (all-sharp, all-soft 12-16px, or documented pill buttons + soft cards). Tint drop shadows to the section background hue.

**Copy Self-Audit & CTA Intent Unification:**
- **Copy Self-Audit**: audit all visible strings before handoff. Reject grammatically broken phrases, cute-but-wrong AI wordplay ("free on its past"), fake craftsman claims, and mock-poetic copy.
- **Fake Precision Ban**: numbers like `92%`, `4.1×`, or `5.8 mm` must originate from verified business metrics or be explicitly labeled as mock; never invent pseudo-engineering precision.
- **No Duplicate CTA Intent**: each page intent (contact, signup, view work) must use a single unified label across navigation, hero, and footer (do not mix "Get in touch", "Contact us", and "Let's talk" on one page).
- **Desktop CTA Button Wrap Ban**: primary CTA labels must never wrap to multiple lines on desktop (maximum 3 words, ideally 1–2 words).

---

## Design System as Living Infrastructure (2025-2026)

In 2026, design systems are not component libraries — they are living infrastructure that governs how design intent becomes production code, including when AI generates that code:

**W3C-compliant three-tier token architecture:**
| Tier | Type | Example | Purpose |
| ---- | ---- | ------- | ------- |
| **Primitive (Core)** | Raw value | `#3B82F6`, '16px', '500ms' | The raw palette; never used directly in components |
| **Semantic (Decision)** | Purpose-driven | 'color-text-primary', 'spacing-component-gap' | Maps intent to primitive; the primary design-to-code contract |
| **Component** | Component-specific | 'button-bg-primary-hover', 'card-border-radius' | Granular overrides for specific component states |

- adopt W3C DTCG (Design Tokens Community Group) format with `$value` and `$type` syntax for all token definitions. Example:
  ```json
  "color-bg-primary-hover": {
    "$value": "{color.blue.600}",
    "$type": "color"
  }
  ```
- semantic tokens are the primary handoff contract between design and Frontend; components must reference semantic tokens, not primitive values
- document the purpose of each semantic token in the token definition, not only its value; AI tools need intent context, not just raw values

**Automated design-to-code pipeline discipline:**
- token changes in the design source (Figma Variables or equivalent) must flow to code via an automated pipeline (e.g., Tokens Studio → PR → Style Dictionary); do not rely on manual exports or copy-paste
- treat a token PR as a code review event: Frontend Developer must review token changes for implementation impact before merge
- maintain the design system as the single source of truth; AI-generated code that hardcodes values instead of referencing tokens introduces drift and must be flagged as a defect
- **dual-audience token documentation**: when design system serves AI agent interfaces (e.g., component registry for GenUI), token definitions and component specs must be authored in strict Markdown hierarchy (H1→H2→H3) for LLM parse efficiency; coordinate with Technical Writer on `configure-llms-txt` and `write-documentation` skills for machine-readable scope maps

**AI governance for design system:**
- when AI tools generate UI code or components, they must reference the existing component library and token system — not generate from scratch
- define and document the rules AI must follow when generating components: which tokens are in scope, which components are the building blocks, what customization is allowed
- run design drift detection after AI-generated code is merged: verify that no hardcoded colors, spacing values, or typography values bypass the token system
- treat design system constraint violations in AI-generated code with the same urgency as accessibility failures — they degrade long-term maintainability

**Design System Selection Map (when the brief names an aesthetic family):**
When the design read points to a known system, reach for the official package — do not recreate its CSS by hand, and do not import its tokens then override 90% of them:

| Brief reads as… | Reach for | Why |
|-----------------|-----------|-----|
| Microsoft / enterprise SaaS / dashboards | `@fluentui/react-components` or `@fluentui/web-components` | Official Fluent UI, Microsoft tokens, accessibility done |
| Google-ish UI, Material-flavored product | `@material/web` + Material 3 tokens | Official, theme-able via Material Theming |
| IBM-style B2B / enterprise analytics | `@carbon/react` + `@carbon/styles` | Official Carbon, mature data-density patterns |
| Shopify app surfaces | `polaris.js` web components / Polaris React | Required for Shopify admin UI |
| Atlassian / Jira-style product | `@atlaskit/*` + `@atlaskit/tokens` | Official Atlassian DS |
| GitHub-style devtool / community page | `@primer/css` or `@primer/react-brand` | Official Primer; Brand variant for marketing |
| Public-sector UK service | `govuk-frontend` | Legally / regulatorily expected |
| US public-sector / trust-first | `uswds` | Same |
| Fast local-business / agency MVP | Bootstrap 5.3 | Boring, fast, works |
| Modern accessible React foundation | `@radix-ui/themes` | Primitives + polished theme |
| Modern SaaS where you own the components | shadcn/ui (`npx shadcn@latest add ...`) | You own the code, easy to customise; never ship default state |
| Tailwind-based modern SaaS / AI marketing | Tailwind v4 utilities + `dark:` variant | Default for indie + small team builds |

- **Honesty rule**: if the brief reads as one of the systems above, install and use the official package. Do not recreate its CSS by hand. Do not import a system's tokens then override 90% of them.
- **One system per project**: do not mix Fluent React with Carbon in the same tree. Do not import shadcn/ui components into a Material 3 app.
- When the brief is an aesthetic, not a system (glassmorphism, bento, brutalism, editorial, dark tech, aurora, kinetic typography, Apple Liquid Glass), build with native CSS + Tailwind + a maintained component library. Be honest in code comments about what is borrowed inspiration vs. official material. There is no official `liquid-glass.css` — web implementations are approximations using `backdrop-filter` + layered borders + highlights; label clearly as approximation.

**Canonical Motion Skeletons (when implementing in collaboration with Frontend Developer):**
When the flow calls for scroll-driven motion, these are the canonical implementation patterns — Frontend Developer owns the code, UX specifies the intent and timing:

- **Sticky-Stack**: `start: "top top"`, `pin: true`, `pinSpacing: false`; every card except the last is pinned; the previous card's `scale: 0.92` / `opacity: 0.55` is driven by the *next* card's scroll trigger. Common failure: trigger fires halfway through scroll instead of pinning at viewport top.
- **Horizontal-Pan**: `start: "top top"`, `pin: true`, `end: "+=${distance}"` where distance = track width minus viewport; `scrub: 1`, `invalidateOnRefresh: true`. Wrapper pinned, inner track slides horizontally as user scrolls vertically.
- **Reveal-Stagger** (lighter alternative, no pinning): Motion's `whileInView` with `viewport={{ once: true, amount: 0.3 }}`, stagger via `delay: i * 0.06`. Use for feature lists, testimonial grids, logo walls. Save GSAP for actual pin/scrub work.
- **Forbidden**: `window.addEventListener("scroll", ...)`, custom `window.scrollY` calculations in React state, `requestAnimationFrame` loops that touch React state. Use Motion's `useScroll()`, GSAP's `ScrollTrigger`, IntersectionObserver, or CSS `scroll-driven animations` (`animation-timeline: view()`).
- **Motion must be motivated**: before adding any animation, articulate in one sentence what it communicates (hierarchy, storytelling, feedback, state transition). "It looked cool" is not a valid answer. Each ScrollTrigger, marquee, and pinned section needs a reason.

**Image & Visual Asset Strategy:**
- Landing pages and portfolios are visual products. Text-only pages with fake-screenshot divs are slop.
- Priority order: (1) image-generation tool first — generate section-specific assets at the right aspect ratio; (2) real web images second — `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` for placeholder photography (seed should describe the section); (3) last resort: leave clearly-labelled placeholder slots and tell the user which placements need real images.
- Even minimalist sites need real images — a pure-text page is not minimalism, it is incomplete work. Even an editorial Linear-style site needs at least 2–3 real images (hero, one product/lifestyle shot, one supporting image).
- Social proof logo walls: use verified SVG marks via Simple Icons (`cdn.simpleicons.org`) or devicon. Enforce the Logo-Only rule: render logos without category or industry subtitles underneath. Make-up brand names must get a make-up SVG mark (monogram, two-letter ligature, abstract glyph) — plain text wordmarks for invented brands look generic. Ensure logos render in both light and dark mode.
- Hand-rolled decorative SVGs are strongly discouraged and never the default. Acceptable only when the brief explicitly calls for it, or it is a single simple geometric mark.
