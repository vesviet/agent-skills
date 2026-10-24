# Master Design Standard: UI/UX Anti-Slop Specification

This document establishes the unified **Master Design Standard** for all UI/UX design, frontend architecture, and component engineering across `agent-skills`. It consolidates and codifies the 9 S-Rank Design & UI/UX skills into an authoritative, enforceable design governance specification.

Every agent assuming the `@designer` (`ui-ux-designer`) or `@frontend` (`frontend-developer`) role MUST strictly comply with these rules.

---

## 1. S-Rank Design Skills Integration Matrix

The Master Design Standard synthesizes nine domain-leading design engineering methodologies into a singular cohesive framework:

| # | S-Rank Skill | Core Focus & Authority | Integrated Sections |
|---|--------------|------------------------|---------------------|
| 1 | **Taste Skill** | Aesthetic direction, 3-dial engine, archetype calibration, mandatory pre-code Design Read statement | §2 (Taste Engine), §3 (Design Read) |
| 2 | **Anthropic Frontend Design** | Layout family diversity, anti-center bias, hero viewport discipline, responsive grid orchestration | §4 (Layout & Composition), §10 (Copy & CTA) |
| 3 | **shadcn/ui (v4)** | Compound component composition, `FieldGroup` + `Field`, `InputGroup`, semantic tokens, Base UI vs Radix | §5 (Component Composition), §6 (Token System) |
| 4 | **Impeccable** | Micro-typography triad, perceptual contrast compliance, whitespace mathematics, visual polish | §3 (Design Read), §6 (Token System), §10 (Copy) |
| 5 | **Emil Design Engineering** | Tactile interactions, gesture feedback, physical state models, fluid component dynamics | §5 (Component Composition), §7 (Motion Physics) |
| 6 | **Animate** | Choreographed micro-interactions, transition curves, easing token governance, viewport reveals | §7 (Motion Physics & Skeletons) |
| 7 | **Emil Kowalski's Bundle** | Frequency-based animation budget (0ms Cmd+K, 150-250ms modals), harmonic oscillator spring physics | §7 (Motion Physics & Timing Table) |
| 8 | **Web Design Guidelines** | Bounded 2-pass QA protocol (Desktop 1280px+ & Mobile 375-430px simultaneously), single smooth-scroll engine | §7 (Smooth Scroll), §8 (Bounded Visual QA) |
| 9 | **Build Awwwards-Quality Sites** | Editorial typography, negative asset constraints (ban fake SVG logos / synthetic testimonials / ungrounded metrics) | §4 (Layout), §9 (Negative Asset Constraints) |

---

## 2. Taste Engine & Three-Dial Calibration

The Taste Engine governs design execution via three numeric dials on a 1–10 scale. Baseline default across all projects is **`8 / 6 / 4`**. These are global variables — cross-references must use these exact names, never aliases like `LAYOUT_VARIANCE` or `ANIM_LEVEL`.

```
                        TASTE ENGINE THREE DIALS
┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│     DESIGN_VARIANCE     │    MOTION_INTENSITY     │     VISUAL_DENSITY      │
│      (Default: 8)       │      (Default: 6)       │      (Default: 4)       │
├─────────────────────────┼─────────────────────────┼─────────────────────────┤
│ 1: Perfect Symmetry     │ 1: Static / No Motion   │ 1: Art Gallery / Ultra  │
│ 5: Balanced Bento Grid  │ 5: Snappy Micro-Springs │ 4: Modern SaaS Baseline │
│ 8: Bold Asymmetric Hero │ 6: Expressive Physics   │ 6: Productivity App     │
│ 10: Avant-Garde Chaos   │ 10: Cinematic Shader 3D │ 10: Cockpit / Telemetry │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

### 2.1 Detailed Dial Parameter Mapping

#### 1. `DESIGN_VARIANCE` (1–10, Baseline: 8)
- **Controls**: Degree of grid disruption, asymmetry, layout unpredictability, and compositional tension.
- **Level 1–3 (Symmetric & Predictable)**:
  - Rigid 12-column grid (`grid-cols-12`). Equal card spans (`col-span-4`, `col-span-6`).
  - Centered hero allowed if brief is manifesto/editorial. Symmetrical gutters (`gap-6`).
- **Level 4–6 (Structured Bento Grid)**:
  - Modern SaaS layout. Bento grids with mixed cell spans (`col-span-8` + `col-span-4`).
  - Subtle visual anchors, alternating content blocks with consistent rhythm.
- **Level 7–8 (Bold Editorial & Asymmetry — Default 8)**:
  - Asymmetric split hero (`60/40` or `65/35` desktop split).
  - Off-axis visual assets, staggered vertical card offsets (`translate-y-8`), overlapping container edges.
  - Section layout repetition strictly capped (minimum 4 distinct layout families per 8 sections).
- **Level 9–10 (Avant-Garde & Experimental)**:
  - Broken grids, extreme whitespace shifts, overlapping typography with background elements.
  - Diagonal borders, brutalist monospaced metadata callouts, horizontal scroll scrub tracks.

#### 2. `MOTION_INTENSITY` (1–10, Baseline: 6)
- **Controls**: Spring physics parameters, micro-interaction feedback, transition duration, and choreography.
- **Level 1–2 (Static / Subdued)**:
  - Zero decorative motion. Transitions limited to instantaneous or 100ms opacity fades (`transition-opacity duration-100`).
  - Strictly respects `prefers-reduced-motion`.
- **Level 3–4 (Functional & Restrained)**:
  - Standard modal/drawer transitions (150ms–200ms ease-out). Subtle hover feedback (`scale-[1.01]`).
  - Keyboard shortcuts and comboboxes: **0ms (zero animation)**.
- **Level 5–6 (Expressive Spring Physics — Default 6)**:
  - Emil Kowalski spring physics: Snappy interactive feedback (`stiffness: 300, damping: 30, mass: 0.8`).
  - Motion layout morphing (`layoutId`), fluid drawer drag gestures, scroll-triggered staggered reveals (`staggerChildren: 0.05`).
  - Off-thread GPU composited motion exclusively (`transform` and `opacity`).
- **Level 7–8 (Cinematic Choreography)**:
  - Pinned sticky card stacks (`pin: true, pinSpacing: false`), scrubbed horizontal pans, magnetic button triggers.
- **Level 9–10 (Immersive Experiential)**:
  - Continuous inertia scrolling (single smooth-scroll engine: Lenis OR Locomotive), canvas/shader motion sync.

#### 3. `VISUAL_DENSITY` (1–10, Baseline: 4)
- **Controls**: Container padding, whitespace volume, typographic scale ratio, and information density per viewport.
- **Level 1–2 (Airy / Art Gallery)**:
  - Massive whitespace (`py-32 md:py-48`, `gap-16`). Single focal element per viewport.
  - Hero typography `text-6xl md:text-8xl`. Body text `text-lg` with `leading-loose`.
- **Level 3–4 (Spacious Modern SaaS — Default 4)**:
  - Generous breathing room (`py-20 md:py-28`, `gap-8`). Container max width `max-w-6xl` or `max-w-7xl`.
  - Hero typography `text-4xl md:text-6xl`, body text `text-base md:text-lg` with `leading-relaxed` (1.75).
- **Level 5–6 (Balanced Productivity)**:
  - Application dashboard density (`p-6`, `gap-4`). Table rows `py-3 px-4`.
  - Headings `text-2xl md:text-3xl`, body text `text-sm`.
- **Level 7–8 (High-Density Professional)**:
  - Developer tools, IDE panels, analytics consoles (`p-3`, `gap-2`).
  - Table rows `py-1.5 px-2.5`, monospaced numerals, body text `text-xs`.
- **Level 9–10 (Cockpit / Telemetry)**:
  - Bloomberg terminal / DAW density. Zero decorative padding (`p-1`).
  - Font size `10px - 12px`, tabular monospace figures, compact status dots.

---

### 2.2 Dial Calibration Across Core Archetypes

| Archetype | VARIANCE | MOTION | DENSITY | Key Characteristics & Guidelines |
|:---|:---:|:---:|:---:|:---|
| **B2B Enterprise / Regulated / Gov** | **3** | **2** | **6** | Rigid 12-col grid, zero decorative whimsy, instantaneous transitions (0-150ms), high data density, WCAG AAA compliance. |
| **Modern Developer Tool (Linear/Supabase style)** | **6** | **5** | **5** | Dark-mode precision, monospace accents, keyboard shortcuts (0ms), structured bento grids, snappy Kowalski springs. |
| **Premium Consumer / Luxury Brand** | **7** | **6** | **3** | Cold luxury palette (slate/cobalt/monochrome), generous negative space, high-craft typography, tactile physical springs. |
| **Editorial / Creative Portfolio** | **8** | **6** | **3** | Asymmetrical split screens, oversized typography, curated editorial pacing, staggered reveals, high whitespace. |
| **Awwwards / Experiential Agency** | **9** | **8** | **3** | Broken grids, scroll-pinned sticky stacks, kinetic typography, magnetic interactions, bold expressive visual depth. |
| **Universal SaaS Marketing Baseline** | **8** | **6** | **4** | Default anti-slop baseline. Asymmetric split hero, fluid micro-interactions, generous breathing room, semantic tokens. |

### 2.3 Dial Clamping & Conflict Resolution Rules
When user briefs contain conflicting requirements (e.g., "We want an experimental Awwwards look, but for a Swiss private wealth management portal"):
- **Safety / Trust-First Clamp**: Regulatory, public-sector, and financial constraints strictly take precedence over aesthetic flair.
- `DESIGN_VARIANCE` is clamped to $\le 4$.
- `MOTION_INTENSITY` is clamped to $\le 3$.
- `VISUAL_DENSITY` is adjusted to $5 - 6$.
- Craft is expressed through subtle typographic hierarchy and immaculate spacing mathematics, never through chaotic layouts or disorienting animations.

---

## 3. Mandatory Pre-Code "Design Read" Statement

Before generating or modifying any JSX, TSX, CSS, or component markup, the agent **MUST emit a structured Design Read statement**. Authoring code without this prior declaration is a blocking defect.

### 3.1 Design Read Specification Format

```markdown
### Design Read
- **Mood & Intent**: [2–4 evocative adjectives, e.g. "Industrial Swiss Precision, Cold Monochrome, High-Signal Developer Tool"]
- **Dial Calibration**:
  - `DESIGN_VARIANCE`: [1–10] — [Layout rationale, e.g. "Level 8: Asymmetric 60/40 hero split, broken bento grid"]
  - `MOTION_INTENSITY`: [1–10] — [Physics rationale, e.g. "Level 6: Snappy Kowalski spring (k: 300, c: 30) on CTAs, 0ms on Cmd+K"]
  - `VISUAL_DENSITY`: [1–10] — [Whitespace rationale, e.g. "Level 4: Generous SaaS spacing (py-24, gap-8), text-5xl display headline"]
- **Composition Archetype**: [Named layout family, e.g. "Asymmetrical Split Hero (60/40) + Bento Feature Matrix (5-cell)"]
- **Typography System**:
  - Display: [e.g. "Cabinet Grotesk" or "Geist Display" (sans, tracking-tight, leading-[1.08])]
  - Body: [e.g. "Geist Sans" (leading-relaxed, max-w-[65ch])]
  - Monospace: [e.g. "Geist Mono" for code snippets, metadata pills, and telemetry]
- **Palette & Semantic Tokens**:
  - Background: `bg-background` (OKLCH dark base, e.g. `oklch(0.14 0.01 260)`)
  - Surface/Card: `bg-card` / `bg-muted`
  - Accent: Single high-contrast accent hue, saturation < 80% (e.g. Emerald `oklch(0.78 0.15 150)`)
  - Text: `text-foreground` (high-contrast primary), `text-muted-foreground` (secondary)
  - Zero raw hex codes (`#...`) or ad-hoc `dark:` overrides allowed.
- **Negative Asset Commitments**:
  - [x] Prohibit fabricated SVG logos / fictional client emblems
  - [x] Prohibit synthetic testimonials and unverified persona metrics
  - [x] Prohibit em-dashes (`—`) in UI copy
  - [x] Single unified CTA intent across all page surfaces
```

### 3.2 Before vs After vs Why: Pre-Code Cognitive Anchoring

#### ❌ BEFORE (Unanchored Immediate Generation -> Generic AI Vibe-Slop)
```tsx
// ❌ SLOP: Generated immediately without Design Read.
// Sins: Pure black background, generic blue button, centered hero, em-dash in copy, hardcoded hex.
export default function Hero() {
  return (
    <div style={{ backgroundColor: '#000000' }} className="py-32 text-center text-white">
      <h1 className="text-5xl font-serif">Fast Cloud Orchestration — Made Simple</h1>
      <p className="text-gray-400 max-w-xl mx-auto mt-4">The #1 platform for high-velocity teams.</p>
      <button className="mt-8 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded">
        Start Free Trial
      </button>
    </div>
  );
}
```

#### ✅ AFTER (Design Read First -> Bound, Calibrated Implementation)
```markdown
### Design Read
- **Mood & Intent**: Utilitarian Monospace Precision, High-Signal Developer Tool
- **Dial Calibration**:
  - `DESIGN_VARIANCE`: 8 — Asymmetric 60/40 desktop split hero with terminal visual anchor
  - `MOTION_INTENSITY`: 6 — Tactile scale-[0.98] active spring on CTA; 0ms on keyboard shortcuts
  - `VISUAL_DENSITY`: 4 — Generous SaaS whitespace (min-h-[100dvh], py-24, gap-12)
- **Composition Archetype**: Asymmetrical Split Hero (60/40) with Live Interactive Preview
- **Typography System**: Display: Geist Sans (tracking-tight), Body: Geist Sans (leading-relaxed), Mono: Geist Mono
- **Palette & Semantic Tokens**: bg-background (oklch(0.14 0.01 260)), text-foreground (oklch(0.98 0 0)), accent: Emerald (oklch(0.78 0.15 150))
- **Negative Asset Commitments**:
  - [x] Prohibit fabricated SVG logos / fictional client emblems
  - [x] Prohibit synthetic testimonials and unverified persona metrics
  - [x] Prohibit em-dashes (—) in UI copy
  - [x] Single unified CTA intent across all page surfaces
```

```tsx
// ✅ IMPLEMENTATION: Perfectly matches the declared Design Read contract
import { Button } from "@/components/ui/button";

export default function Hero() {
  return (
    <section className="relative min-h-[100dvh] flex items-center pt-20 pb-24 border-b border-border bg-background">
      <div className="container mx-auto px-6 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        {/* Left Column: 60% asymmetric copy stack */}
        <div className="lg:col-span-7 space-y-6 text-left">
          <div className="inline-flex items-center gap-2 rounded-full border border-border bg-muted/50 px-3 py-1 text-xs font-mono text-muted-foreground">
            <span className="h-1.5 w-1.5 rounded-full bg-primary" />
            <span>v2.8 Edge Runtime</span>
          </div>
          
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight text-foreground leading-[1.08]">
            Deterministic edge compute for distributed state
          </h1>
          
          <p className="max-w-[54ch] text-base sm:text-lg text-muted-foreground leading-relaxed">
            Execute stateful workers with sub-millisecond cold starts and automated replication across 35 global regions.
          </p>
          
          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Button size="lg" className="active:scale-[0.98] transition-transform">
              Deploy Cluster
            </Button>
            <Button variant="outline" size="lg">
              Read Specification
            </Button>
          </div>
        </div>

        {/* Right Column: 40% functional code terminal asset */}
        <div className="lg:col-span-5">
          <div className="rounded-lg border border-border bg-card shadow-sm overflow-hidden font-mono text-xs">
            <div className="flex items-center justify-between px-4 py-2.5 border-b border-border bg-muted/40">
              <span className="text-muted-foreground">worker.config.ts</span>
              <span className="text-[10px] text-muted-foreground/60 uppercase">TypeScript</span>
            </div>
            <pre className="p-4 text-card-foreground overflow-x-auto leading-relaxed">
              <code>{`export default defineCluster({\n  region: "auto",\n  replicas: 8,\n  storage: {\n    type: "replicated-sqlite",\n    sync: "immediate"\n  }\n});`}</code>
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
}
```

#### 💡 WHY
Pre-code commitments anchor the LLM to specific tokens, layout archetypes, and negative constraints before generating tokens. Without this anchor, code defaults to generic centered AI slop with pure black backgrounds and hardcoded hex colors.

---

## 4. Anti-Slop Layout & Composition Directives

### 4.1 Anti-Center Bias
Centered Hero / H1 sections are avoided when `DESIGN_VARIANCE > 4`. Use split screen (50/50, 60/40), left-aligned copy with right-aligned visual asset, asymmetric whitespace, or scroll-pinned compositions. Centered heroes are permitted only for manifesto/editorial launch pages.

### 4.2 Hero Viewport & Stack Discipline
- Hero content MUST fit in the initial viewport without scrolling on desktop (`min-h-[100dvh]` or clean fold clearance).
- Headline capped at **maximum 2 lines** on desktop.
- Subtext capped at **maximum 20 words** AND max 3–4 lines. If copy exceeds 20 words, cut copy or adjust hierarchy; never allow hero copy to push CTAs below the fold.
- Hero stack contains **at most 4 text elements**: (1) optional Eyebrow OR brand strip, (2) Headline, (3) Subtext, (4) CTAs (1 primary + max 1 secondary).
- Banned in hero: tiny tagline below CTAs, trust micro-strips, pricing teasers, feature bullets, avatar stacks. These belong in dedicated sections directly below the hero.
- Top padding capped at 6rem (`pt-24`) on desktop.

### 4.3 Section Layout Repetition Ban
Once a layout family is used for a section, that family may appear at most ONCE on the page. A page with 8 sections must use at least 4 distinct layout families (e.g. Asymmetric Split, Bento Grid, Pinned Sticky Stack, Horizontal Pan, Metric Ticker).

### 4.4 Zigzag Alternation Cap
Alternating left-image/right-text then left-text/right-image is capped at a maximum of 2 consecutive sections. The 3rd consecutive section must break the pattern.

### 4.5 Eyebrow Restraint (Strict Cap)
Uppercase wide-tracking label above headlines is capped at **maximum 1 eyebrow per 3 sections**. A 9-section page may have at most 3 eyebrows total. Drop eyebrows in favor of clear, confident headlines.

### 4.6 Bento Grid Cell Count & Diversity
Bento grids must have exactly as many cells as there is content (no empty filler tiles). At least 2–3 cells in any grid must have real visual variation (interactive previews, code snippets, visual graphics). Monochrome text-only bento grids are strictly banned.

### 4.7 Split-Header Ban
"Big left headline + floating right explainer paragraph" is banned by default. Sections must have one focused message; stack headline and explainer vertically with `max-w-[65ch]`.

### 4.8 Logo Wall Separation
"Used by / Trusted by" logo strip belongs strictly below the hero as an independent section. Apply the **Logo-Only rule**: logos must render with no category or industry subtitles underneath.

---

## 5. Modern Component Composition & Form Architecture

Modern component composition forbids monolithic, boolean-heavy wrappers in favor of composable compound primitives, decoupled form layouts, and safe polymorphic slots.

### 5.1 R1.1: Form Layouts — FieldGroup + Field (shadcn v4 vs Legacy v3)

#### Architectural Analysis
- **Legacy v3 Architecture**: Relied on `react-hook-form`'s `<Controller>` pattern wrapped across 6 distinct components: `<Form>`, `<FormField>`, `<FormItem>`, `<FormLabel>`, `<FormControl>`, and `<FormMessage>`.
  - *Pathology 1: Tight coupling*: Cannot use native Server Actions (`action={formAction}`), React 19 `useActionState()`, or TanStack Form without rewriting or bypassing the component.
  - *Pathology 2: Slot breakage*: `<FormControl>` clones its immediate child using Radix `Slot`. If a developer wraps an input in an extra `div` (e.g., for an icon or tooltip), the `id` and `aria-describedby` attach to the wrapper `div` instead of the actual `<input>`, destroying screen-reader accessibility.
  - *Pathology 3: Lack of layout primitive*: Grouping two inputs side-by-side (First Name, Last Name) required ad-hoc `div className="grid grid-cols-2 gap-4"`, leading to inconsistent spacing and margin collapse across forms.
- **shadcn v4 Architecture (`FieldGroup` + `Field`)**:
  - Decoupled from form state management. Operates purely on React 19 standard context and HTML accessibility primitives.
  - `<FieldGroup>` acts as the layout and semantic grouping authority (supporting `role="group"`, `<fieldset>`, `<legend>`, responsive grid columns, and cascaded disabled state).
  - `<Field>` provides atomic field context via `React.useId()`, linking `<FieldLabel>`, `<FieldDescription>`, `<FieldError>`, and any standard `<Input>` or custom control.

#### Before (Legacy v3 — Brittle, verbose, tightly coupled):
```tsx
// ❌ BEFORE (shadcn v3): 6 nested layers, tightly coupled to react-hook-form, breaks on custom wrappers
import { useForm } from "react-hook-form";
import { Form, FormField, FormItem, FormLabel, FormControl, FormDescription, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";

export function LegacyUserForm() {
  const form = useForm({ defaultValues: { username: "" } });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(console.log)} className="space-y-8">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                {/* Wrapping in a div breaks Radix Slot ARIA injection! */}
                <Input placeholder="shadcn" {...field} />
              </FormControl>
              <FormDescription>Your public display name.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
      </form>
    </Form>
  );
}
```

#### After (shadcn v4 — Clean, decoupled, framework-agnostic with FieldGroup):
```tsx
// ✅ AFTER (shadcn v4): Clean FieldGroup + Field compound composition; works with React 19 Server Actions or any state library
import * as React from "react";
import { FieldGroup, Field, FieldLabel, FieldDescription, FieldError } from "@/components/ui/field";
import { Input } from "@/components/ui/input";

export function ModernUserForm({ action }: { action: (formData: FormData) => void }) {
  return (
    <form action={action}>
      <FieldGroup className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Field name="firstName">
          <FieldLabel>First Name</FieldLabel>
          <Input placeholder="Ada" required />
          <FieldDescription>Your legal given name.</FieldDescription>
          <FieldError />
        </Field>

        <Field name="lastName">
          <FieldLabel>Last Name</FieldLabel>
          <Input placeholder="Lovelace" required />
          <FieldError />
        </Field>
      </FieldGroup>
    </form>
  );
}
```

#### Why:
1. **50%+ Boilerplate Reduction**: Eliminates unnecessary `<Form>` and `<FormField render={...}>` controller wrappers for standard forms.
2. **Framework Freedom**: Works natively with React 19 Server Actions (`action={...}`), `useActionState()`, native HTML forms, TanStack Form, and `react-hook-form`.
3. **Bulletproof Accessibility**: `Field` uses React 19 `useId()` to guarantee deterministic `htmlFor`, `id`, `aria-describedby`, and `aria-errormessage` bindings regardless of internal DOM nesting depth.
4. **Layout Consistency**: `FieldGroup` enforces uniform grid gap and responsive flow across all form surfaces in the design system.

---

### 5.2 R1.2: Compound Inputs — InputGroup Architecture

#### Architectural Analysis
- **The Absolute Positioning Anti-Pattern**: Placing icons inside inputs via `relative` + `absolute left-3 top-1/2 -translate-y-1/2` forces hardcoded padding (`pl-10`) onto the `<Input />`.
  - When the icon size changes, or when prefix text (like `https://` or `+1`) is used instead of an icon, padding constants collide with input text.
  - Clicking on an absolute-positioned icon often fails to focus the input unless custom click-forwarding logic is manually attached.
  - Adding both a prefix icon and a suffix action button (e.g. Search icon on the left, "Clear" button on the right) requires messy, fragile utility combinations (`pl-10 pr-24`).
- **The Compound `InputGroup` Architecture**:
  - The outer `<InputGroup>` acts as the physical border and background box with `flex items-center`.
  - The outer container listens to `:focus-within` and renders the active ring (`focus-within:ring-2 focus-within:ring-ring focus-within:border-ring`).
  - Child elements `<InputGroupAddon>`, `<InputGroupInput>`, `<InputGroupButton>`, and `<InputGroupSelect>` render as natural flex siblings. The `<InputGroupInput>` has `border-0 shadow-none focus-visible:ring-0`, delegating its visual boundary to the parent.

#### Before (Fragile absolute positioning hack):
```tsx
// ❌ BEFORE: Absolute positioning hack, hardcoded padding, broken container focus state
import { Search, X } from "lucide-react";
import { Input } from "@/components/ui/input";

export function BadSearchInput() {
  return (
    <div className="relative w-full">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
      <Input
        type="text"
        placeholder="Search documents..."
        className="pl-10 pr-10 focus:ring-2 focus:ring-blue-500" 
      />
      <button 
        type="button" 
        className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
}
```

#### After (Compound InputGroup Primitives):
```tsx
// ✅ AFTER: Compound InputGroup with natural flex flow, unified focus-within, and modular addons
import * as React from "react";
import { Search, X } from "lucide-react";
import { InputGroup, InputGroupAddon, InputGroupInput, InputGroupButton } from "@/components/ui/input-group";

export function GoodSearchInput({ onClear }: { onClear?: () => void }) {
  return (
    <InputGroup className="w-full">
      <InputGroupAddon position="prefix">
        <Search className="h-4 w-4 text-muted-foreground" />
      </InputGroupAddon>
      <InputGroupInput 
        type="text" 
        placeholder="Search documents..." 
      />
      {onClear && (
        <InputGroupAddon position="suffix">
          <InputGroupButton 
            variant="ghost" 
            size="icon-xs" 
            onClick={onClear}
            aria-label="Clear search query"
          >
            <X className="h-3.5 w-3.5" />
          </InputGroupButton>
        </InputGroupAddon>
      )}
    </InputGroup>
  );
}
```

#### Why:
1. **Zero Padding Collisions**: Adornments and inputs participate in standard flex layout; widths adapt automatically to content (icons, text prefixes like `https://`, or country code dropdowns).
2. **Unified Focus State**: The entire container illuminates via `focus-within:ring-2 focus-within:ring-ring`, giving a cohesive, native appearance regardless of which internal element has focus.
3. **Accessibility**: Embedded buttons participate naturally in keyboard tab order; clicking any non-interactive addon transfers focus cleanly to the input.

---

### 5.3 R1.4: Composition Primitives — Base UI `render` Prop vs Radix Primitives `asChild`

#### Architectural Comparison Table

| Dimension | Radix Primitives `asChild` (`Slot`) | Base UI `render` Prop (`render={<Elem />}` or `render={(props, state) => ...}`) |
| :--- | :--- | :--- |
| **Mechanics** | Uses `React.cloneElement(children, mergedProps)` | Directly merges props and invokes render callback or clones element |
| **Child Cardinality** | Strictly **1** element (`React.Children.only`). Multiple children or text nodes throw fatal error | Flexible: supports element prop OR function with `(props, state) => ReactNode` |
| **State Injection** | **None**. Child cannot inspect internal state (`open`, `highlighted`) directly; must inspect DOM `data-*` attributes | **Full State Injection**. Render function receives `{ open, active, disabled, highlighted }` |
| **Ref Composition** | Reads `(children as any).ref`, deprecated in React 19; combines via `composeRefs` | Native React 19 `props.ref` alignment; safely composes refs without private property inspection |
| **Slot Bubbling Fragility** | High. Nesting `TooltipTrigger asChild` inside `DialogTrigger asChild` can swallow event cancellations | Low. Explicit prop merging handles event chains cleanly with full transparency |
| **Best Used When** | Maintaining existing Radix UI / shadcn v3 components with simple element replacement | Modern React 19 apps, Base UI primitives, or where child styling depends on internal headless state |

#### Before (Radix `asChild` — CloneElement limitations and state blindness):
```tsx
// ❌ BEFORE (Radix asChild): Cannot access internal state in JSX, crashes on multiple children, uses deprecated child.ref
import * as Dialog from "@radix-ui/react-dialog";
import { Button } from "@/components/ui/button";

export function RadixExample({ isOpen, onOpenChange }: { isOpen: boolean; onOpenChange: (open: boolean) => void }) {
  return (
    <Dialog.Root open={isOpen} onOpenChange={onOpenChange}>
      <Dialog.Trigger asChild>
        <Button variant="outline">Open Modal</Button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6">
          <Dialog.Title>Title</Dialog.Title>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

#### After (Base UI `render` Prop — Dynamic state injection and React 19 alignment):
```tsx
// ✅ AFTER (Base UI render prop): Exposes internal component state directly to child render prop callback
import { Dialog } from "@base-ui-components/react/dialog";
import { Button } from "@/components/ui/button";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

export function BaseUIExample() {
  return (
    <Dialog.Root>
      <Dialog.Trigger
        render={(props, state) => (
          <Button 
            {...props} 
            variant="outline" 
            className={cn("gap-2", state.open && "border-primary ring-2 ring-primary/20")}
          >
            Preferences
            <ChevronDown className={cn("h-4 w-4 transition-transform duration-150", state.open && "rotate-180")} />
          </Button>
        )}
      />
      <Dialog.Portal>
        <Dialog.Backdrop className="fixed inset-0 bg-black/50 backdrop-blur-xs" />
        <Dialog.Popup className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-card text-card-foreground p-6 rounded-lg border border-border shadow-lg">
          <Dialog.Title className="text-lg font-semibold">User Preferences</Dialog.Title>
        </Dialog.Popup>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

#### Why:
1. **Dynamic State-Driven Styling**: The render function receives internal state variables (`state.open`, `state.highlighted`), allowing child components to animate icons or alter classes without writing complex CSS `data-[state=open]:` selector gymnastics.
2. **React 19 Ref Safety**: Base UI does not inspect `element.ref` directly, preserving strict compatibility with React 19's unified `props.ref` standard.
3. **No Slot Crashes**: If conditions require rendering an alternative element or null, Base UI handles it predictably without throwing `React.Children.only` fatal errors.

---

## 6. Token Architecture & Color Discipline

### 6.1 Semantic OKLCH Tokens vs Raw Hex & Manual `dark:` Overrides

#### Architectural Analysis
- **The Dark Utility Proliferation Anti-Pattern**:
  - Writing `bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-50 border-zinc-200 dark:border-zinc-800` pollutes markup with duplicate styling.
  - If a team introduces a secondary theme (e.g. `midnight`, `oled-black`, or high-contrast accessible theme), `dark:` utilities cannot adapt because they are hardcoded to a single dark palette.
  - Raw hex values (e.g. `bg-[#0f172a]`) completely bypass the design token pipeline and break automated accessibility/contrast auditing.
- **The OKLCH Semantic Token Architecture**:
  - In Tailwind v4 and modern CSS, tokens are declared once in `@theme` using the OKLCH color space (`oklch(L C H)`).
  - OKLCH is perceptually uniform: lightness values are consistent across hues. A lightness of $0.98$ is equally bright in blue, green, or neutral grey.
  - Component code strictly consumes semantic tokens: `bg-card text-card-foreground border-border`. When switching between light and dark modes, only the underlying CSS variable changes. Component markup contains **zero** `dark:` color utilities for core theme surfaces!

#### Before (Hardcoded hex, manual dark overrides, theme fragmentation):
```tsx
// ❌ BEFORE: Raw hex values and manual dark: overrides polluting markup and breaking theme portability
export function BadCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="bg-white dark:bg-[#18181b] border border-[#e4e4e7] dark:border-[#27272a] p-6 rounded-lg shadow-sm">
      <h3 className="text-xl font-semibold text-[#09090b] dark:text-[#fafafa]">
        {title}
      </h3>
      <p className="mt-2 text-sm text-[#71717a] dark:text-[#a1a1aa]">
        {description}
      </p>
      <button className="mt-4 bg-[#18181b] dark:bg-[#fafafa] text-white dark:text-black px-4 py-2 rounded-md hover:bg-[#27272a] dark:hover:bg-[#e4e4e7]">
        Action
      </button>
    </div>
  );
}
```

#### After (Strict semantic tokens in OKLCH, zero component dark: overrides):
```css
/* ✅ In globals.css (Tailwind v4 CSS-first theme) */
@theme {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.145 0 0);
  --color-card: oklch(1 0 0);
  --color-card-foreground: oklch(0.145 0 0);
  --color-primary: oklch(0.205 0 0);
  --color-primary-foreground: oklch(0.985 0 0);
  --color-muted: oklch(0.97 0 0);
  --color-muted-foreground: oklch(0.556 0 0);
  --color-border: oklch(0.922 0 0);
  --color-ring: oklch(0.708 0 0);
}

.dark {
  --color-background: oklch(0.145 0 0);
  --color-foreground: oklch(0.985 0 0);
  --color-card: oklch(0.17 0 0);
  --color-card-foreground: oklch(0.985 0 0);
  --color-primary: oklch(0.985 0 0);
  --color-primary-foreground: oklch(0.205 0 0);
  --color-muted: oklch(0.269 0 0);
  --color-muted-foreground: oklch(0.708 0 0);
  --color-border: oklch(0.269 0 0);
  --color-ring: oklch(0.439 0 0);
}
```

```tsx
// ✅ AFTER: Pure semantic tokens — zero hex codes, zero manual dark: overrides in component markup
export function GoodCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="bg-card text-card-foreground border border-border p-6 rounded-lg shadow-xs">
      <h3 className="text-xl font-semibold tracking-tight">
        {title}
      </h3>
      <p className="mt-2 text-sm text-muted-foreground">
        {description}
      </p>
      <button className="mt-4 bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md transition-colors">
        Action
      </button>
    </div>
  );
}
```

#### Why:
1. **Zero Manual Dark Mode Debt**: Components adapt automatically to dark mode, OLED black mode, or custom brand themes without touching component JSX.
2. **Perceptual Contrast Uniformity**: OKLCH ensures mathematically consistent perceived contrast across light and dark palettes, guaranteeing WCAG AA compliance.
3. **Clean Codebases**: Eliminates repetitive `dark:*` class strings, reducing CSS bundle size and developer cognitive load.

### 6.2 Typography & Color Discipline Rules
- **Serif Discipline**: Serif display fonts are banned as the default for creative or premium briefs. Default to high-craft sans display (`Geist Display`, `Cabinet Grotesk`, `Satoshi`, `Outfit`). Specifically banned default serifs: `Fraunces` and `Instrument_Serif`.
- **Word Emphasis**: Word emphasis in display type must use bold or italic of the **same font family**; never inject a foreign serif word into a sans headline.
- **Color Discipline & Lila Ban**: Maximum 1 accent color with saturation < 80%. Ban generic AI-purple/blue glow gradients on dark buttons and backgrounds. Use neutral bases with singular high-contrast accents.
- **Palette Rotation**: Ban the default reach for warm-beige (`#f5f1ea`), brass/clay, and espresso text. Rotate to cold luxury, forest green, terracotta+slate, cobalt+cream, or sharp monochrome.
- **Shape Consistency Lock**: Enforce a single corner-radius scale across the page (all-sharp, all-soft 12-16px, or documented pill buttons + soft cards).

---

## 7. Motion Physics & Animation Frequency Budget

### 7.1 Frequency-Based Animation Timing Table (Emil Kowalski)

Animation latency must be inversely proportional to the frequency of user interaction.

| Tier | Interaction Category | Components / Triggers | Max Allowed Duration | Easing / Physics Curve | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 0** | **High-Frequency (Instant)** | Hotkey invocation (`Cmd+K`, `Ctrl+P`), Combobox filtering, Autocomplete suggestions, Tooltips on hover (after delay), Focus ring outlines, Keyboard tab switching | **0ms (Instant)** | Linear / step-start (zero transition) | User expects instant system responsiveness. Any spring or slide animation creates perceived lag and motion sickness. |
| **Tier 1** | **Micro-Interactions (Snappy)** | Button press/depress, Checkbox check, Switch toggle, Accordion single item toggle, Dropdown menu popover | **100ms – 150ms** | Snappy Spring: `stiffness: 450, damping: 35, mass: 1` (or `cubic-bezier(0.16, 1, 0.3, 1)`) | Provides tactile confirmation that input was registered without delaying subsequent user actions. |
| **Tier 2** | **Medium-Frequency Overlays (Strictly Bounded)** | Modal Dialogs, Slide-over Drawers / Sheets, Alert Dialogs, Toast Notifications | **150ms – 250ms** *(Strict ceiling: 250ms)* | Bounded Spring: `stiffness: 320, damping: 28, mass: 1` (or `cubic-bezier(0.32, 0.72, 0, 1)`) | Communicates spatial context (where overlay originated) while swiftly revealing actionable UI. Exceeding 250ms is anti-pattern slop. |
| **Tier 3** | **Low-Frequency Narrative (Expressive)** | Route / Page transitions, First-load Hero reveal, Milestone celebration modals, Onboarding walkthrough steps | **250ms – 400ms** *(Strict ceiling: 400ms)* | Gentle Spring: `stiffness: 220, damping: 24, mass: 1` | Storytelling and spatial orientation for infrequent events. Never exceed 400ms under any circumstance. |

### 7.2 Harmonic Oscillator Spring Physics Presets

The behavior of a physical UI spring is governed by the second-order differential equation:
$$m \frac{d^2 x}{dt^2} + c \frac{dx}{dt} + k x = 0$$

Where $m = 1.0$ (mass), $k$ is stiffness, $c$ is damping, and $\zeta = \frac{c}{2\sqrt{k \cdot m}}$ is the damping ratio.
Near-critical damping ($\zeta \approx 0.75 - 0.85$) yields a fast, fluid arrival with zero cartoon bounce.

| Profile Name | Target Use Cases | Mass ($m$) | Stiffness ($k$) | Damping ($c$) | Damping Ratio ($\zeta$) | Settling Time ($t_s$) | Perceived Feel |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Snappy Micro** | Checkbox check, Switch toggle, Button active press, Icon morph, Segmented control tab indicator | `1.0` | `450` | `35` | $\approx 0.82$ | $\approx 120\text{ms}$ | Tactile, crisp, mechanical, immediate |
| **Bounded Overlay** | Modal Dialogs, Slide-over Sheet / Drawers, Context Menus, Tooltip pop | `1.0` | `320` | `28` | $\approx 0.78$ | $\approx 180\text{ms}$ | Fluid, responsive, polished, spatial |
| **Gentle Morph** | Accordion content expansion, Shared element layout displacement, Card open | `1.0` | `220` | `24` | $\approx 0.81$ | $\approx 240\text{ms}$ | Smooth, readable, calm, elegant |
| **Immediate Rigid** | Hotkey palettes (`Cmd+K`), Combobox search dropdowns, Tab key highlights | `N/A` | `N/A` | `N/A` | `1.0` (Critical) | `0ms` | Instantaneous, zero latency |

#### Banned Spring Configurations:
- Underdamped cartoonish bouncing ($\zeta < 0.6$, e.g. `stiffness: 500, damping: 10`).
- Heavy sluggish inertia ($m > 1.5$).
- Overdamped muddy settling ($\zeta > 1.3$, takes > 500ms to arrive).

### 7.3 Single Smooth-Scroll Engine Constraint

- **Strict Exclusivity Rule**: A project must select **EXACTLY ONE** smooth-scroll engine across the entire codebase.
  - **Option A (Recommended for modern React/Next.js)**: `lenis` (`lenis/react`). It runs on native scroll coordinates without translating the DOM root, preserving accessibility and integrating cleanly with GSAP `ScrollTrigger` and Framer Motion.
  - **Option B**: Native CSS smooth scrolling (`html { scroll-behavior: smooth; }`).
- **Prohibition**: Installing `lenis` AND `locomotive-scroll` in the same repository or initializing both in layout files is strictly forbidden. Dual virtual scroll listeners fight over coordinates, causing compositor frame drops, cursor stuttering, trackpad lag, and breaking keyboard navigation (`Tab`, `PageDown`).

### 7.4 Canonical Motion Skeletons
- **Sticky-Stack**: `start: "top top"`, every card except the last is pinned (`pin: true, pinSpacing: false`), previous card shrinks (`scale: 0.92, opacity: 0.55`) driven by next card's trigger.
- **Horizontal-Pan**: Wrapper pinned, inner track slides horizontally (`start: "top top", end: "+=${distance}"`, `scrub: 1`).
- **Reveal-Stagger**: Motion `whileInView` with `viewport={{ once: true, amount: 0.3 }}`, stagger via `delay: i * 0.06`.
- **Forbidden Patterns**: `window.addEventListener("scroll", ...)` (runs every frame, jank-prone), custom `window.scrollY` in React state, `requestAnimationFrame` touching React state, unmotivated motion, and horizontal marquees exceeding 1 per page.

### 7.5 Before vs After vs Why: Frequency Budget & Smooth Scroll

#### Before (Sluggish 350ms Cmd+K & Dual Scroll Engines):
```tsx
// ❌ BEFORE: 350ms animation on hotkey palette + duplicate scroll engines destroying frame pacing
import { motion, AnimatePresence } from "framer-motion";
import Lenis from "lenis";
import LocomotiveScroll from "locomotive-scroll";

// Problem 1: Dual scroll engines fight over wheel events
export function BrokenScrollSetup() {
  React.useEffect(() => {
    const lenis = new Lenis();
    const loco = new LocomotiveScroll();
    return () => { lenis.destroy(); loco.destroy(); };
  }, []);
  return null;
}

// Problem 2: 350ms transition on Cmd+K hotkey
export function BadPalette({ isOpen }: { isOpen: boolean }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ duration: 0.35 }} // ❌ Sluggish 350ms delay on hotkey!
          className="fixed top-24 left-1/2 -translate-x-1/2 w-[500px] bg-card p-4"
        >
          <input placeholder="Search..." autoFocus />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

#### After (Enforcing 0ms Hotkey Tier, 180ms Bounded Drawer, and Single Lenis Engine):
```tsx
// ✅ AFTER: Tier 0 (0ms) Cmd+K, Tier 2 (180ms) Bounded Drawer, and single clean Lenis provider
import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ReactLenis } from "lenis/react";

// 1. Single Smooth-Scroll Engine with WCAG reduced-motion check
export function CleanScrollProvider({ children }: { children: React.ReactNode }) {
  const [prefersReduced, setPrefersReduced] = React.useState(false);
  React.useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReduced(mq.matches);
  }, []);

  if (prefersReduced) return <>{children}</>;

  return (
    <ReactLenis root options={{ duration: 1.0, smoothWheel: true }}>
      {children}
    </ReactLenis>
  );
}

// 2. Tier 0 Hotkey Command Palette (0ms duration, instant feedback)
export function GoodCommandPalette({ isOpen }: { isOpen: boolean }) {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-24 bg-black/40 backdrop-blur-xs">
      <div className="w-full max-w-lg bg-card text-card-foreground border border-border p-4 rounded-xl shadow-2xl">
        <input 
          className="w-full bg-transparent border-b border-border pb-2 text-sm outline-none placeholder:text-muted-foreground" 
          placeholder="Type a command or search..." 
          autoFocus 
        />
      </div>
    </div>
  );
}

// 3. Tier 2 Bounded Drawer (settles in 180ms with calibrated spring)
export function GoodDrawer({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/40 z-40 backdrop-blur-xs"
          />
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", stiffness: 320, damping: 28, mass: 1.0 }}
            className="fixed right-0 top-0 bottom-0 w-80 bg-card border-l border-border p-6 z-50 shadow-xl"
          >
            <h2 className="text-lg font-semibold">Settings</h2>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

#### Why:
1. **Respects User Velocity**: Keyboard power users invoking `Cmd+K` are not blocked by transition delays; the input cursor is immediately ready to accept keystrokes.
2. **Rock-Solid 60/120fps Rendering**: Eliminates event listener race conditions and coordinate collisions on the compositor thread caused by duplicate scroll engines.
3. **Bound Predictability**: Drawers provide spatial context within 180ms, well below human perceptual frustration thresholds (250ms).

---

## 8. Bounded Visual Verification & Self-QA Protocol

### 8.1 Bounded Self-QA Passes (Maximum 2 Passes)

Autonomous agents generating frontend code must strictly avoid infinite aesthetic refinement loops:
1. **Pass Budget Cap**: The agent is allocated a hard maximum of **two (2) self-QA passes** after initial code generation (Pass 0: Authoring).
   - `qa_pass_count = 0`: Initial implementation.
   - `qa_pass_count = 1`: Pass 1 (Structural & Responsive Verification).
   - `qa_pass_count = 2`: Pass 2 (Polish, Contrast & Regression Verification).
   - Hard Stop: When `qa_pass_count == 2`, the loop **strictly terminates**. Zero further code edits are permitted under the self-QA cycle.
2. **Simultaneous Multi-Viewport Verification**:
   Every verification pass must inspect **both viewports simultaneously**:
   - **Desktop Viewport**: Width `>= 1280px` (baseline: `1280 x 800` or `1440 x 900`).
   - **Mobile Viewport**: Width `375px - 430px` (baseline: `390 x 844` or `375 x 667`).
3. **Deterministic Defect Criteria (Binary Trigger Rule)**:
   Code modifications during Pass 1 and Pass 2 are triggered **only** by objective, measurable defects:
   - **Horizontal Overflow**: `document.documentElement.scrollWidth > window.innerWidth` (horizontal scrollbars on mobile or desktop).
   - **Text / Container Clipping**: Hero headline, subtext, or CTA pushed below `100dvh` fold on desktop, or text clipped by overflow hidden without ellipsis.
   - **Broken Markup / Template Artifacts**: Raw `{template}` brackets, unescaped entities, or unrendered variables visible in the DOM.
   - **Touch Target Violations**: Interactive buttons, links, or inputs measuring `< 44 x 44px` on mobile viewport.
   - **Contrast Ratio Failures**: WCAG 2.2 AA violations (`< 4.5:1` for body text, `< 3:1` for large text/icons and form borders).
   - **CTA Wrapping Defect**: Desktop primary CTA button text wrapping onto multiple lines.
4. **Suppression of Subjective Aesthetic Re-Critique**:
   Subjective impressions ("the spacing feels slightly airy", "maybe a warmer shadow") are **strictly prohibited** from triggering code edits during QA passes. Residual cosmetic observations are logged to `handoff.md` as non-blocking design debt.
5. **Anti-Oscillation Guard**:
   If Pass 2 flags an issue on a property modified in Pass 1 (e.g. changing `p-6` back to `p-4`), the edit is blocked, and the Pass 1 state is preserved.

### 8.2 Before vs After vs Why: Bounded QA Protocol

#### ❌ BEFORE (Unbounded Hallucinated Inspection Loop):
```text
Agent Pass 1: "I notice the hero section padding is pt-24. Let me reduce it to pt-16 to make it tighter."
[Agent edits code]
Agent Pass 2: "Now the subtitle text seems to wrap awkwardly on mobile. Let me reduce font size from text-lg to text-base."
[Agent edits code]
Agent Pass 3: "Now the CTA button looks slightly too prominent compared to the headline. Let me change button padding."
[Agent edits code]
Agent Pass 4: "Actually, the top of the hero feels cramped now. Let me change pt-16 back to pt-20."
[Agent edits code]
Agent Pass 5: "Checking again... Maybe the card shadow could be 2% softer..."
Result: 52,000 tokens burned, 5 code churn cycles, zero objective defects resolved, mobile layout regressed.
```

#### ✅ AFTER (Bounded 2-Pass Protocol):
```text
Agent Pass 0: Author initial component code with Desktop (1280px) and Mobile (390px) responsive classes.
Agent Pass 1 (Structural & Responsive Verification):
  - Desktop (1280px): Hero stack fits in 100dvh fold; headline 2 lines; CTA single line. OK.
  - Mobile (390px): DETECTED DEFECT: Horizontal overflow (document.scrollWidth 420px > window.innerWidth 390px) caused by fixed width `w-[400px]` on code preview card.
  - Fix: Update `w-[400px]` to `w-full max-w-[400px]`.
Agent Pass 2 (Polish & Regression Verification):
  - Desktop (1280px): Re-verified fold clearance and contrast (Button: 5.2:1 contrast ratio against bg-background). OK.
  - Mobile (390px): Re-verified horizontal scroll: scrollWidth = 390px (0px overflow). Tap targets >= 44px. OK.
  - PASS LIMIT REACHED: qa_pass_count = 2. Hard termination triggered.
  - Residual Note recorded in handoff.md: "Minor: Consider adding subtle border highlight on code card in future polish iteration."
Result: 2 deterministic passes, exactly 1 objective defect fixed, zero token blowup, verified mobile+desktop stability.
```

#### 💡 WHY
Unbounded LLM loops suffer from subjective drift and oscillation. Capping QA to 2 passes with binary defect triggers guarantees rapid convergence, prevents token exhaustion, and eliminates hallucinated visual nitpicks.

---

## 9. Asset Integrity & Negative Constraints

AI-generated interfaces frequently suffer from recognizable "vibe-slop" visual assets. The following negative constraints are strictly enforced:

### 9.1 The Strict Negative Constraints
1. **Absolute Ban on Fabricated SVG Logos**:
   - Strictly prohibit authoring inline SVG paths representing invented company logos, client emblems, or abstract polyhedra swirls ("NovaPulse AI", "ApexFlow", "NexusCore").
   - Prohibit fictitious customer brand walls.
2. **Absolute Ban on Synthetic Testimonial Text & Avatars**:
   - Strictly prohibit generating fictional quotes, fake executive personas ("Jane Doe, VP at TechScale"), invented customer titles, or unverified statistical claims (`342.8% boost`).
   - Prohibit linking to generic external headshot photos pretending to be real clients.

### 9.2 Mandatory Authentic Alternatives
1. **Authentic Typography & Wordmarks**: Represent brand identity through clean typography using active typographic tokens or monograms in an accessible badge:
   ```tsx
   <div className="flex h-7 w-7 items-center justify-center rounded-md bg-primary text-primary-foreground font-mono text-xs font-semibold">
     NP
   </div>
   <span className="font-semibold tracking-tight text-foreground text-base">
     NovaPulse
   </span>
   ```
2. **Generic Functional Iconography**: Icons must be drawn strictly from approved packages (`lucide-react`, `@phosphor-icons/react`, `@radix-ui/react-icons`) and represent **functional UI actions** (`<Terminal />`, `<Database />`, `<ChevronRight />`), NEVER masquerading as corporate brand marks.
3. **Verified Social Proof Marks**: When real brand integration is required, use verified official monochrome marks via Simple Icons (`https://cdn.simpleicons.org/{slug}`) with the Logo-Only rule.
4. **Factual Structural Placeholders**: If customer logos or testimonials are requested but real assets are not provided, render honest structural placeholders (`[Client Logo Slot: Monochrome SVG]`).
5. **Verifiable Technical Highlights**: Replace fake testimonials with factual architecture benchmarks (latency measurements, uptime SLA, concurrent connection benchmarks).

### 9.3 Before vs After vs Why: Asset Integrity

#### ❌ BEFORE (Slop: Invented SVG Swirl & Synthetic Testimonial Quote):
```tsx
// ❌ SLOP: Hallucinated SVG logo and fabricated executive testimonial
export function BadAssets() {
  return (
    <div>
      {/* Fake SVG swirl */}
      <svg className="h-8 w-8 text-indigo-500" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" stroke="url(#g)" strokeWidth="8" fill="none" />
        <defs><linearGradient id="g"><stop stopColor="#6366f1"/><stop offset="1" stopColor="#a855f7"/></linearGradient></defs>
      </svg>
      {/* Fake testimonial */}
      <blockquote>
        "NovaPulse doubled our engineering velocity by 340% in 14 days!"
        <footer>Sarah Miller, VP of Cloud at HyperScale</footer>
      </blockquote>
    </div>
  );
}
```

#### ✅ AFTER (Authentic: Typographic Wordmark & Factual Benchmark):
```tsx
// ✅ AUTHENTIC: Clean typographic wordmark & verifiable architecture benchmark
export function GoodAssets() {
  return (
    <div className="space-y-8">
      {/* Authentic wordmark */}
      <div className="flex items-center gap-2.5">
        <div className="flex h-7 w-7 items-center justify-center rounded-md bg-primary text-primary-foreground font-mono text-xs font-semibold">
          NP
        </div>
        <span className="text-base font-semibold tracking-tight text-foreground">
          NovaPulse
        </span>
      </div>

      {/* Verifiable Technical Benchmark */}
      <div className="rounded-xl border border-border bg-card p-6">
        <div className="flex items-center justify-between pb-4 border-b border-border">
          <h4 className="text-xs font-mono font-semibold uppercase text-muted-foreground">
            Verified Engine Benchmark
          </h4>
          <span className="text-xs font-mono text-primary bg-primary/10 px-2 py-0.5 rounded-full">
            p99 &lt; 28ms
          </span>
        </div>
        <div className="grid grid-cols-2 gap-4 pt-4 text-left">
          <div>
            <div className="text-2xl font-mono font-semibold text-foreground">100k+</div>
            <div className="text-xs text-muted-foreground mt-0.5">Concurrent Connections</div>
          </div>
          <div>
            <div className="text-2xl font-mono font-semibold text-foreground">0.02%</div>
            <div className="text-xs text-muted-foreground mt-0.5">Edge Cold-Start Revalidation</div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

#### 💡 WHY
Fabricated SVG artwork and invented executive testimonials undermine product credibility and generate brittle, unmaintainable code. Clean typographic wordmarks and verifiable technical metrics convey genuine technical authority.

---

## 10. Copy Self-Audit & CTA Intent Unification

### 10.1 Copy Self-Audit
Audit all visible UI strings before handoff. Reject:
- Grammatically broken phrases or ungrounded claims.
- Cute-but-wrong AI wordplay ("free on its past").
- Em-dashes (`—`) in UI headings and button copy.
- Fake-precision numbers (`92%`, `4.1×`, `5.8 mm`) that do not originate from verified business metrics or are not explicitly labeled as mock.
- When in doubt, replace with a plain functional sentence — clear, direct language always trumps AI-generated cute copy.

### 10.2 CTA Intent Unification
- Each page intent (contact, signup, view work) must use a single unified label across navigation, hero, and footer.
- Do not mix "Get in touch", "Contact us", and "Let's talk" on one page.
- Primary CTA labels must never wrap to multiple lines on desktop (maximum 3 words, ideally 1–2 words).

---

## 11. Design System Selection Map & Living Infrastructure

### 11.1 Official Package Selection
When the design read points to a known system, reach for the official package — do not recreate its CSS by hand:

| Brief reads as… | Reach for | Why |
|-----------------|-----------|-----|
| Microsoft / enterprise SaaS / dashboards | `@fluentui/react-components` | Official Fluent UI, accessibility done |
| Google-ish UI, Material-flavored product | `@material/web` + Material 3 tokens | Official, theme-able via Material Theming |
| IBM-style B2B / enterprise analytics | `@carbon/react` + `@carbon/styles` | Official Carbon, mature data-density patterns |
| Shopify app surfaces | `polaris.js` / Polaris React | Required for Shopify admin UI |
| Atlassian / Jira-style product | `@atlaskit/*` + `@atlaskit/tokens` | Official Atlassian DS |
| GitHub-style devtool / community page | `@primer/react-brand` | Official Primer Brand |
| Modern accessible React foundation | `@radix-ui/themes` or `@base-ui-components/react` | Primitives + polished accessibility |
| Modern SaaS where you own components | shadcn/ui (`npx shadcn@latest add …`) | Full ownership, compound composition |
| Modern SaaS / AI marketing | Tailwind v4 utilities + CSS `@theme` | CSS-first token configuration |

- **One system per project**: Do not mix Fluent with Carbon in the same tree.
- When the brief is an aesthetic (glassmorphism, bento, brutalism, dark tech), build with native CSS + Tailwind + maintained primitives, clearly documenting approximations.

### 11.2 Living Infrastructure & Dual-Audience Documentation
- **W3C DTCG Token Architecture**: Primitive -> Semantic -> Component. Components reference semantic tokens exclusively.
- **Automated Pipeline**: Tokens Studio -> PR -> Style Dictionary.
- **Dual-Audience Token Documentation**: When design systems serve AI agents, token definitions and specs must be authored in strict Markdown hierarchy (H1->H2->H3) for LLM parse efficiency.

---

## 12. Agentic UX, Trust Ladder & AI Interaction States

### 12.1 Trust Ladder Governance
| Tier | What it means | UX requirement |
|------|--------------|---------------|
| **Suggest** | Agent proposes; user always initiates the action | Full preview before any effect; easy dismiss |
| **Verify** | Agent proposes and prepares; user confirms once per action | One-click confirm with consequence preview; undo always visible |
| **Delegate** | Agent acts within a defined scope; user reviews outcomes | Outcome summary required; audit trail accessible; exception alerts visible |
| **Automate** | Agent acts fully autonomously; user monitors exceptions only | Status surface mandatory; interrupt/pause control always accessible; exception alerts |

- Every agentic feature must declare its Trust Ladder tier in `ux-flow-spec.json` under `autonomy_tier`.
- Do not ship Automate before Suggest -> Verify trust is earned (avoid the Autopilot Trap).

### 12.2 AI Interaction States & The Red Path
AI features are probabilistic. UI must design for the full 5-state model:
1. **Generating / Thinking**: Skeleton or progress indicator; latency expectation.
2. **Uncertain**: Calibrated microcopy ("Suggested", "Unverified"); confidence indicator.
3. **Fallback**: Graceful degradation + alternative action path.
4. **Overridden**: Acknowledges user override; does not re-apply AI output.
5. **Corrected**: Visual confirmation that user feedback was recorded.
- **The Red Path**: Treat AI errors as expected statistical events. Always design an alternative action path, never a dead-end state.
- **EU AI Act Article 50 (live August 2026)**: Disclose AI interaction before or during the first meaningful interaction.
