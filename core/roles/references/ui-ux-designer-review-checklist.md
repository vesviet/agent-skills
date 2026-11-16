## UI/UX Designer Review Checklist

Operational verification gates for `@ui-ux-designer` deliverables (`DESIGN.md`, `ux-flow-spec.json`, `ui-component-spec.json`, `design-tokens-spec.json`).

---

### 1. Domain-Grounded Aesthetic & Anti-Slop Gate (`AESTHETIC-DIRECTION LOCK`)

- [ ] **Context-First Design Read**: 1-line Design Read explicitly states page/app kind, audience, committed aesthetic pole, and avoided cliché.
- [ ] **No AI Monoculture**: neither legacy AI slop (centered purple-glow dark mesh, `Fraunces`/`Instrument_Serif`, `Inter`/`Roboto`/`Space Grotesk` unprompted, warm-beige/brass cookware default) nor unprompted **Linear-dark-slate + `Geist` + Emerald** cloning when the domain calls for another visual voice.
- [ ] **Domain Archetype & Three Dials**: `DESIGN_VARIANCE`, `MOTION_INTENSITY`, and `VISUAL_DENSITY` (`1–10`) calibrated directly from the **Domain Archetype Matrix** in [`ui-ux-designer-anti-slop-standards.md`](ui-ux-designer-anti-slop-standards.md) (regulated/finance/public-sector clamped to `variance <= 4`, `motion <= 3`).
- [ ] **Palette & Shape Lock**: single dominant accent (`saturation < 80%`) unless domain explicitly requires multi-status semantics; consistent shape scale; no `#000000` pure black; tinted neutral off-black/off-white surfaces.

---

### 2. Mode A (Product UI) vs Mode B (Landing / Showcase) Gate

#### Mode A: In-App Product UI
- [ ] **IA & URL-as-State**: filters, tabs, pagination, and deep-linkable drawers specify URL search-param persistence.
- [ ] **Surface Selection**: Inline vs Popover vs Drawer vs Modal vs Route justified; modals specify focus trap, `Esc` close, focus restoration, and `overscroll-behavior: contain`.
- [ ] **Destructive & Async Ergonomics**: reversible actions use optimistic UI + Undo Toast; scoped deletes name the exact object; irreversible actions require typed confirmation.
- [ ] **Data-Dense Scannability**: numeric/monetary/live columns specify `tabular-nums`, sticky headers, `scroll-margin-top`, and accessible truncation disclosure.

#### Mode B: Landing & Showcase Surfaces
- [ ] **Hero Viewport Containment**: desktop (`>= 1280px`) hero fits within `100dvh` (`min-h-[100dvh]`), top padding `<= 6rem` (`pt-24`), headline `<= 2` lines, subtext `<= 20` words, primary CTA visible without scroll; anti-center bias respected when `DESIGN_VARIANCE > 4`.
- [ ] **Section & Eyebrow Discipline**: at most `1` uppercase tracking eyebrow per `3` sections; `>= 4` distinct layout families per `8` sections; max `2` consecutive zigzag blocks; no blank bento tiles; logo wall separated below hero (Logo-Only rule).

---

### 3. Component Anatomy, Copy & Web Micro-Craft Gate (`STATE-AND-SURFACE LOCK`)

- [ ] **Complete 5 Core States**: `Default`, `Loading` (geometry-matched skeleton, `CLS = 0`), `Empty` (clear copy + primary action), `Error` (factual diagnosis, zero `!`, actionable retry/recovery), and `Unauthorized` defined for every screen/widget.
- [ ] **Composition Anatomy (`vercel-composition-patterns`)**: `ui-component-spec.json` models compound subcomponents (`Root`, `Trigger`, `Content`), slot delegation, and explicit variants (`<= 2` stylistic booleans; zero layout-toggling boolean sprawl).
- [ ] **Copy & Punctuation Craft (`web-design-guidelines`)**:
  - True Unicode ellipsis (`…`) used on async states (`Loading…`) and triggers opening secondary flows (`Rename…`, `Export…`).
  - Unified CTA label per user intent across nav, hero, and footer; desktop CTAs fit on 1 line (`<= 3` words).
  - Zero em-dashes (`—`) in UI strings; zero ungrounded metrics (`92%`, `4.1×`), fake testimonials, or fabricated SVG brand swirls.
- [ ] **Touch, Input & Dark Mode Polish**: mobile inputs `>= 16px` (prevent iOS Safari zoom); touch targets `>= 44×44px` (`>= 24×24px` WCAG 2.2 AA minimum with spacing); `:active` unified at `scale-[0.96]` (150ms `ease-out`, disabled excluded); hover guarded in `@media (hover: hover)`; `color-scheme: dark` declared on dark themes.

---

### 4. Tokens, Accessibility & Legal Compliance Gate

- [ ] **Two-Tier DTCG 2025.10 Tokens**: `DESIGN.md` (`MASTER` + page overrides) uses Two-Tier tokens (`Primitive -> Semantic`, max `<= 3` component exceptions) in `$value`/`$type` syntax; zero raw hex/px values or manual `dark:` surface overrides in component specs.
- [ ] **Contrast Dual Gate**:
  - *Legal Floor (WCAG 2.2 AA)*: $CR \ge 4.5:1$ normal text, $\ge 3.0:1$ large text and UI controls/focus rings.
  - *Perceptual Target (APCA)*: $L_c \ge 75$ body text, $L_c \ge 60$ headlines/controls, verified in both light and dark modes.
- [ ] **Accessibility & Regulatory Scope**: EAA (`WCAG 2.2 AA / EN 301 549`) and US ADA Title II (`WCAG 2.1 AA`, `2027-04-26` / `2028-04-26` / HHS May 2026) targets flagged when in scope; focus ring visible (`>= 2px` offset, 2.4.11 Focus Not Obscured); WCAG 3.0 never claimed as conformance target.
- [ ] **Dark-Pattern Review**: `dark_pattern_review` recorded in `ux-flow-spec.json` checking all 6 classes (nagging, obstruction, sneaking, forced action, confirmshaming, trick questions) per DSA Art 25/26 & FTC.

---

### 5. AI, Agentic UX & GenUI Gate (when in scope)

- [ ] **5 AI States & Red Path**: `Generating`, `Uncertain`, `Fallback`, `Overridden`, `Corrected` specified; calibrated microcopy + `"Why am I seeing this?"` provenance + preview-before-apply + primary undo.
- [ ] **EU AI Act Article 50**: upfront `<AIDisclosureBanner>` before first meaningful interaction (live 2 Aug 2026) and C2PA metadata spec for AI media (2 Dec 2026).
- [ ] **Trust Ladder & Background UX**: `agentic_autonomy.autonomy_tier` declared (`<=` earned user trust); status surface, notification contract, async interrupt, and completion handoff specified for background agents.
- [ ] **GenUI & Dual-Audience**: component allowlist + forbidden combinations + deterministic fallback defined on stateless MCP 2026-07-28; `agent_operability` declared when browser agents operate the UI (WebMCP).

---

### 6. Machine Verification Gate Table

| Gate | Invariant | Verification Method / Tool | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Design Contracts** | Schema valid & `flow_id` linked | `python3 core/scripts/validate-contracts.py` | 100% pass across `ux-flow-spec`, `ui-component-spec`, `design-tokens-spec` |
| **Token Hygiene** | Zero raw hex or Tier-1 leakage | `rg -i "#[0-9a-f]{3,6}" src/components/` | 0 hardcoded hex in component markup |
| **WCAG 2.2 AA + APCA** | Legal contrast + perceptual $L_c$ | Axe / Lighthouse / APCA check | 0 WCAG 2.2 AA violations; $L_c \ge 75 / 60$ |
| **Composition Hygiene** | `<= 2` stylistic booleans | Prop surface & `composition_anatomy` audit | Compound subcomponents used for multi-region UI |
| **Multi-Viewport & INP** | Zero overflow at `320px`, INP `<= 200ms` | Bounded 2-pass visual QA (`1280px` & `390px`) | 0 horizontal overflow, `CLS <= 0.1`, `INP <= 200ms` |
| **Prototype / Workbench** | Multi-screen (`> 2`) flow exercised | Figma prototype or `interactive-component-workbench` | All transitions + 5/6 states verified |
