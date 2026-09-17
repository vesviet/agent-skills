# UI/UX Designer Anti-Slop Design Standards & Taste Skill Reference

This reference document defines the mandatory anti-slop directives, Three Dials calibration, Design System Selection Map, canonical motion skeletons, image asset strategy, and copy self-audit rules extracted from [`ui-ux-designer.md`](../ui-ux-designer.md).

---

## 1. Three Dials Calibration

Every UX flow and component specification must calibrate three numeric dials (1–10 scale, baseline `8 / 6 / 4`). These are global variables — cross-references must use these exact names, never aliases like `LAYOUT_VARIANCE` or `ANIM_LEVEL`.

| Dial | 1 | 10 |
|------|---|----|
| `DESIGN_VARIANCE` | Perfect Symmetry | Artsy Chaos |
| `MOTION_INTENSITY` | Static | Cinematic / Physics |
| `VISUAL_DENSITY` | Art Gallery / Airy | Cockpit / Packed Data |

### Dial Inference (design read → dial values)
| Signal | VARIANCE | MOTION | DENSITY |
|--------|----------|--------|---------|
| "minimalist / clean / calm / editorial / Linear-style" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury / brand" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9-10 | 8-10 | 3-4 |
| "landing page / portfolio / marketing site (default)" | 7-9 | 6-8 | 3-5 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3-4 | 2-3 | 4-5 |
| "redesign - preserve" | match existing | +1 | match existing |
| "redesign - overhaul" | +2 | +2 | match existing |

### Use-Case Presets
| Use case | VARIANCE | MOTION | DENSITY |
|----------|----------|--------|---------|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Landing (Premium consumer) | 7 | 6 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |
| Redesign - preserve | match | match+1 | match |
| Redesign - overhaul | +2 | +2 | match |

---

## 2. Design System Selection Map

When the design read points to a known system, reach for the official package — do not recreate its CSS by hand, and do not import its tokens then override 90% of them.

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
| Modern SaaS where you own the components | shadcn/ui (`npx shadcn@latest add …`) | You own the code, easy to customise; never ship default state |
| Tailwind-based modern SaaS / AI marketing | Tailwind v4 utilities + `dark:` variant | Default for indie + small team builds |

- **Honesty rule**: if the brief reads as one of the systems above, install and use the official package. Do not recreate its CSS by hand. Do not import a system's tokens but then override 90% of them.
- **One system per project**: do not mix Fluent React with Carbon in the same tree. Do not import shadcn/ui components into a Material 3 app.
- When the brief is an aesthetic, not a system (glassmorphism, bento, brutalism, editorial, dark tech, aurora, kinetic typography, Apple Liquid Glass), build with native CSS + Tailwind + a maintained component library. Be honest in code comments about what is borrowed inspiration vs. official material. There is no official `liquid-glass.css` — web implementations are approximations using `backdrop-filter` + layered borders + highlights; label clearly as approximation.

---

## 3. Anti-Slop Layout & Composition Directives

### Anti-Center Bias
Centered Hero / H1 sections are avoided when `DESIGN_VARIANCE > 4`. Use split screen (50/50), left-aligned copy with right-aligned visual asset, asymmetric whitespace, or scroll-pinned compositions. Centered heroes are permitted only for manifesto/editorial launch pages.

### Hero Viewport & Stack Discipline
- Hero content MUST fit in the initial viewport without scrolling on desktop.
- Headline max 2 lines on desktop.
- Subtext max **20 words** AND max 3–4 lines. If copy exceeds 20 words, cut copy or adjust hierarchy; never allow hero copy to push CTAs below the fold.
- Hero stack contains **at most 4 text elements**: (1) optional Eyebrow OR brand strip, (2) Headline, (3) Subtext, (4) CTAs (1 primary + max 1 secondary).
- Banned in hero: tiny tagline below CTAs, trust micro-strips, pricing teasers, feature bullets, avatar stacks. These belong in dedicated sections directly below the hero.
- Top padding capped at 6rem (pt-24) on desktop.

### Logo Wall Separation
"Used by / Trusted by" logo strip belongs strictly below the hero as an independent section. Apply the **Logo-Only rule**: logos must render with no category or industry subtitles underneath.

### Section Layout Repetition Ban
Once a layout family is used for a section, that family may appear at most ONCE on the page. A page with 8 sections must use at least 4 distinct layout families.

### Zigzag Alternation Cap
Alternating left-image/right-text then left-text/right-image is capped at a maximum of 2 consecutive sections. The 3rd consecutive section must break the pattern.

### Eyebrow Restraint (Strict Cap)
Uppercase wide-tracking label above headlines is capped at **maximum 1 eyebrow per 3 sections**. A 9-section page may have at most 3 eyebrows total. Drop eyebrows in favor of clear headlines.

### Bento Grid Cell Count & Diversity
Bento grids must have exactly as many cells as there is content (no empty filler tiles). At least 2–3 cells in any grid must have real visual variation. Monochrome text-only bento grids are banned.

### Split-Header Ban
"big left headline + floating right explainer paragraph" is banned by default. Sections have one focused message; stack headline and explainer vertically with `max-w-[65ch]`.

---

## 4. Anti-Default Typography & Color Discipline

### Serif Discipline
Serif display fonts are banned as the default for creative or premium briefs. Serif is permitted ONLY when the brand brief explicitly names a serif or the aesthetic is heritage/manuscript.
- Specifically banned default serifs: `Fraunces` and `Instrument_Serif`.
- Default to high-craft sans display: `Geist Display`, `Cabinet Grotesk`, `Satoshi`, `Outfit`.
- Emphasis rule: word emphasis in display type must use bold or italic of the **same font family**; never inject a foreign serif word into a sans headline.
- Descender clearance: when italic display type contains descender characters (`g, j, p, q, y`), maintain minimum `leading-[1.1]` with padding reservation to prevent clipping.

### Color Discipline & Lila Ban
- Maximum 1 accent color with saturation < 80%.
- Ban generic AI-purple/blue glow gradients on dark buttons and backgrounds. Use neutral bases (Zinc, Stone, Slate) with singular high-contrast accents (Emerald, Electric Blue, Burnt Orange).
- Color consistency lock: the chosen accent color applies to the entire page; do not switch accent hues across sections.
- Premium-consumer palette ban: banned default reach for warm-beige (`#f5f1ea`), brass/clay (`#b08947`, `#b6553a`), and espresso text (`#1a1714`). Rotate to cold luxury, forest green, terracotta+slate, cobalt+cream, or sharp monochrome.

### Shape Consistency Lock
Enforce a single corner-radius scale across the page (all-sharp, all-soft 12-16px, or documented pill buttons + soft cards). Tint drop shadows to the section background hue.

---

## 5. Copy Self-Audit & CTA Intent Unification

### Copy Self-Audit
Audit all visible strings before handoff. Reject:
- Grammatically broken phrases
- Cute-but-wrong AI wordplay ("free on its past")
- Fake craftsman claims
- Mock-poetic copy
- Fake-precision numbers (`92%`, `4.1×`, `5.8 mm`) that do not originate from verified business metrics or are not explicitly labeled as mock
- When in doubt, replace with a plain functional sentence — AI-generated cute copy is worse than boring copy

### CTA Intent Unification
- Each page intent (contact, signup, view work) must use a single unified label across navigation, hero, and footer.
- Do not mix "Get in touch", "Contact us", and "Let's talk" on one page.
- Primary CTA labels must never wrap to multiple lines on desktop (maximum 3 words, ideally 1–2 words).

---

## 6. Canonical Motion Skeletons

When scroll choreography is required, these are the canonical implementation patterns. Frontend Developer owns the code; UX specifies the intent and timing. All skeletons honor `prefers-reduced-motion` and degrade to static.

### Sticky-Stack
- `start: "top top"` — pin triggers when section top hits viewport top
- Every card except the last is pinned (`pin: true, pinSpacing: false`)
- Previous card shrinks (`scale: 0.92, opacity: 0.55`) driven by the *next* card's scroll trigger
- Common failure: trigger fires halfway through scroll instead of pinning at viewport top

### Horizontal-Pan
- Wrapper is pinned; inner track slides horizontally as the user scrolls vertically
- `start: "top top"`, `end: "+=${distance}"` where distance = track width minus viewport
- `scrub: 1`, `invalidateOnRefresh: true`

### Reveal-Stagger (lighter alternative, no pinning)
- Motion's `whileInView` with `viewport={{ once: true, amount: 0.3 }}`, stagger via `delay: i * 0.06`
- Use for feature lists, testimonial grids, logo walls
- Save GSAP for actual pin/scrub work

### Forbidden Patterns
- `window.addEventListener("scroll", ...)` — runs every frame, jank-prone, no batching
- Custom `window.scrollY` calculations in React state
- `requestAnimationFrame` loops that touch React state
- Use Motion's `useScroll()`, GSAP's `ScrollTrigger`, IntersectionObserver, or CSS `scroll-driven animations` (`animation-timeline: view()`)

### Motion Must Be Motivated
Before adding any animation, articulate in one sentence what it communicates — hierarchy, storytelling, feedback, or state transition. "It looked cool" is not a valid answer. Each ScrollTrigger, marquee, and pinned section needs a reason. If motion cannot be shipped in working form within the available scope, drop the dial and ship a clean static page; never half-build motion that breaks.

### Marquee Max-One-Per-Page
Horizontal scrolling text marquees are appropriate at most once per page. Two or more on the same page reads as lazy filler.

---

## 7. Image & Visual Asset Strategy

Landing pages and portfolios are visual products — text-only pages with fake-screenshot divs are slop.

### Priority Order
1. **Image-generation tool first** — generate section-specific assets at the right aspect ratio
2. **Real web images second** — `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` for placeholder photography (seed should describe the section)
3. **Last resort** — leave clearly-labelled placeholder slots (`<!-- TODO: hero product photo, 1600x1200 -->`) and report which placements need real images

### Rules
- Even minimalist sites need real images — a pure-text page is not minimalism, it is incomplete work
- Even an editorial Linear-style site needs at least 2–3 real images (hero, one product/lifestyle shot, one supporting image)
- Generate B&W minimalist photography if the brief is restrained; do not skip images entirely because the dial is low
- Social proof logo walls: use verified SVG marks via Simple Icons (`cdn.simpleicons.org`) or devicon. Enforce the Logo-Only rule
- Make-up brand names must get a make-up SVG mark (monogram, two-letter ligature, abstract glyph) — plain text wordmarks for invented brands look generic
- Ensure logos render in both light and dark mode
- Hand-rolled decorative SVGs are strongly discouraged and never the default
- Div-based fake screenshots are banned — use real screenshots, image-tool generations, or real interactive mini-components

---

## 8. Brief Inference & Design Read

Before producing wireframes, component specs, or flow transitions, read 6 core contextual signals:
1. **Page kind**: landing (SaaS, consumer, agency, event), portfolio (developer, designer, studio), redesign (preserve vs overhaul), or editorial
2. **Vibe words**: user-specified adjectives ("minimalist", "Linear-style", "brutalist", "Apple-y", "playful", "serious B2B", "editorial", "dark tech")
3. **Reference signals**: linked URLs, pasted screenshots, competitor brands
4. **Audience**: technical procurement panel vs design-conscious consumer vs hiring manager
5. **Existing brand assets**: logo, color palette, typography, photography
6. **Quiet constraints**: accessibility-first, public-sector, regulated industries, or trust-first commerce

### Mandatory 1-Line Design Read
Output before any spec: `Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <design system or aesthetic family>.`

### Ambiguity Rule
If the brief is ambiguous, ask at most **one** targeted clarifying question. Never dump multi-question lists.

---

## 9. Agentic UX & Trust Ladder

### Trust Ladder — Autonomy Governance Framework
| Tier | What it means | UX requirement |
|------|--------------|---------------|
| **Suggest** | Agent proposes; user always initiates the action | Full preview before any effect; easy dismiss |
| **Verify** | Agent proposes and prepares; user confirms once per action | One-click confirm with consequence preview; undo always visible |
| **Delegate** | Agent acts within a defined scope; user reviews outcomes | Outcome summary required; audit trail accessible; exception alerts visible |
| **Automate** | Agent acts fully autonomously; user monitors exceptions only | Status surface mandatory; interrupt/pause control always accessible; exception notification contract defined |

### Autonomy Tier Declaration
- Every agentic feature must declare its Trust Ladder tier in `ux-flow-spec.json` under `autonomy_tier`
- The UI must surface the current tier visibly
- Do not ship a feature at a higher tier than the trust the product has earned from its user base — shipping Automate before Suggest→Verify trust is established is the **Autopilot Trap**
- Tier upgrades require explicit user opt-in and a trust-building progression

### Background Agent Flows
When an agent operates without an active screen session, UX must define: status surface, notification contract, async interrupt UX, and completion handoff.

---

## 10. AI Interaction Design States

AI features are probabilistic — they produce uncertain, variable, and sometimes wrong outputs. UX must design for the full AI state model:

| State | What it means | Design requirement |
|-------|--------------|-------------------|
| **Generating / Thinking** | AI is processing; output not ready | Animated skeleton or progress indicator; set expectation on latency |
| **Uncertain** | AI produced output but confidence is low | Confidence indicator shown; calibrated microcopy ("Suggested", "Unverified") |
| **Fallback** | AI could not generate a useful response | Graceful degradation message + alternative path (search, contact, manual input) |
| **Overridden** | User has edited or rejected the AI output | UI acknowledges the override; does not re-apply AI output automatically |
| **Corrected** | User has provided feedback; system has acknowledged | Visual confirmation the feedback was received |

### Confidence Indicators
- High confidence: display result normally
- Medium confidence: "Suggested," "Likely," "Based on available information"
- Low confidence: "Could not verify," "Unconfirmed," "AI may be incorrect"; offer alternative path
- Do not use "AI-generated" as a label in isolation — pair it with a confidence signal
- If confidence falls below the BA's HITL trigger threshold, surface the human review path

### Transparency & Explainability Hooks
- "Why am I seeing this?" affordances for AI-driven recommendations
- Source citation and provenance displays for generative AI features
- Progressive disclosure: high-level result first, expand option for detailed reasoning
- EU AI Act Article 50 (live 2 August 2026): reusable `<AIDisclosureBanner>` component with EU-approved AI icon; disclosure must appear before or during the first meaningful interaction

### Human Override & Control Patterns
- **Preview-before-apply**: for AI actions with consequences, design a confirmation step showing the proposed action and its impact
- **Easy reversibility**: every AI-driven change must have a one-click undo, edit, or manual override
- **Mode switching**: explicit autonomy level controls ("Assisted mode" vs "Autopilot mode")
- **Feedback loops**: visible thumbs-up/down, edit, or "ask differently" mechanisms

### The "Red Path" — Design for When AI Is Wrong
- Treat AI errors as expected statistical events, not edge cases
- Design epistemic uncertainty UI: "I can't answer this, but I can help you [alternative]" is a better UX than a hallucinated answer delivered confidently
- Never design a dead-end state for AI uncertainty; always provide an alternative action path

---

## 11. GenUI Component Governance

When AI dynamically assembles UI in real-time, the designer's deliverable changes from fixed screens to **design bounds**: the rules that constrain what AI-assembled UI can look like.

### Component Palette Definition
- Define the allowed component set; unlisted components are not available to the AI assembler
- For each component in the palette: document allowed states, allowed content types, and prohibited combinations
- The palette is a design governance contract, not a suggestion — the frontend implementation must enforce it as a runtime constraint

### Assembly Rules
- Define relationship rules: which components can be composed together, in what order, with what spacing and layout constraints
- Define brand-safety constraints: prohibited color combinations, out-of-bounds typography pairings, disallowed imagery types
- Document semantic rules: which content types require which components

### GenUI Drift Detection
- After AI-generated UI is assembled and rendered, run design drift detection: verify no hardcoded values, no out-of-palette components, no prohibited combinations
- Treat design-system violations in AI-assembled UI with the same urgency as accessibility failures
- Define a fallback: when AI assembles a UI that violates the palette or assembly rules, what is the safe degraded rendering?

### MCP 2026-07-28 Protocol Alignment
The MCP specification revision makes the protocol core stateless (removing connection handshake, session, and server-initiated requests) — stateless HTTP is now the default. GenUI component registries that expose components to AI assemblers via MCP must align with this stateless transport model; document any stateful session assumptions as legacy requiring migration path.

---

## 12. Design System as Living Infrastructure

### W3C-Compliant Three-Tier Token Architecture
| Tier | Type | Example | Purpose |
|------|------|---------|---------|
| **Primitive (Core)** | Raw value | `#3B82F6`, `16px`, `500ms` | The raw palette; never used directly in components |
| **Semantic (Decision)** | Purpose-driven | `color-text-primary`, `spacing-component-gap` | Maps intent to primitive; the primary design-to-code contract |
| **Component** | Component-specific | `button-bg-primary-hover`, `card-border-radius` | Granular overrides for specific component states |

- Adopt W3C DTCG format with `$value` and `$type` syntax for all token definitions
- Semantic tokens are the primary handoff contract between design and Frontend; components must reference semantic tokens, not primitive values
- Document the purpose of each semantic token in the token definition, not only its value; AI tools need intent context, not just raw values

### Automated Design-to-Code Pipeline Discipline
- Token changes in the design source (Figma Variables or equivalent) must flow to code via an automated pipeline (Tokens Studio → PR → Style Dictionary); do not rely on manual exports or copy-paste
- Treat a token PR as a code review event: Frontend Developer must review token changes for implementation impact before merge
- Maintain the design system as the single source of truth; AI-generated code that hardcodes values instead of referencing tokens introduces drift and must be flagged as a defect
- **Dual-audience token documentation**: when design system serves AI agent interfaces, token definitions and component specs must be authored in strict Markdown hierarchy (H1→H2→H3) for LLM parse efficiency; coordinate with Technical Writer on `configure-llms-txt` and `write-documentation` skills

### AI Governance for Design System
- When AI tools generate UI code or components, they must reference the existing component library and token system — not generate from scratch
- Define and document the rules AI must follow when generating components: which tokens are in scope, which components are the building blocks, what customization is allowed
- Run design drift detection after AI-generated code is merged: verify that no hardcoded colors, spacing values, or typography values bypass the token system
- Treat design system constraint violations in AI-generated code with the same urgency as accessibility failures
