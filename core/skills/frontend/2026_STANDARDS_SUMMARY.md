# 2026 Frontend Standards & Patterns — Consolidated Research Summary

## Overview
Deep research conducted September 2026 across React 19, TanStack ecosystem, CSS View Transitions, WebMCP, and AI-driven UI governance.

---

## 1. React 19 + RSC (Server Components) Architecture (2026)

### React 19.2 Stable (June 2026 with Expo SDK 56)
- **Server Components**: Render components ahead of time, separate environment from client
- **Full-stack React Architecture**: Libraries target React 19 with `react-server` export condition
- **Stable APIs**: RSC features stable, but bundler/framework APIs may break between minors

### New Hooks (2026)
| Hook | Purpose | Replaces |
|------|---------|----------|
| **`use()`** | Read promises directly in Server Components; RSC streaming + lazy data resolution | `useEffect` fetches in RSC |
| **`useActionState`** | Form actions with pending state, error handling, progressive enhancement | `useFormState` (deprecated) |
| **`useOptimistic`** | Optimistic updates for data mutations | Manual optimistic UI |
| **`useFormStatus`** | Form submission status in nested components | Manual form state |

### Form Actions (2026)
```tsx
// React 19 form actions - automatic form management
<form action={submitAction}>
  <input name="name" />
  <button disabled={isPending}>Save</button>
</form>

// useActionState for stateful forms
const [error, submitAction, isPending] = useActionState(
  async (prevState, formData) => { /* server action */ },
  initialState
);
```

---

## 2. Data Fetching Architecture (2026)

### RSC + TanStack Query Hybrid Pattern
```
┌─────────────────────────────────────────────────────┐
│  Server Components (RSC)                            │
│  ├── use() for initial data fetching                │
│   │   └── RSC streaming + lazy resolution           │
│  └── Server Functions (createServerFn) for data     │
└─────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────┐
│  Client Components ("use client")                   │
│  ├── TanStack Query v5 for interactivity            │
│  │   ├── Cache invalidation, background refetching  │
│  │   ├── Request deduplication                      │
│  │   └── Optimistic mutations                       │
│  └── useActionState for form mutations              │
└─────────────────────────────────────────────────────┘
```

### TanStack Query v5 Patterns (2026)
- **Centralized `queryOptions` factories**: No scattered magic string keys
- **`queryOptions` pattern**: Reusable, type-safe query configs across components
- **Optimistic mutations full lifecycle**: `onMutate` (cancel + snapshot + update), `onError` (rollback), `onSettled` (invalidate)
- **Functional updater syntax**: `setQueryData((old) => ...)` — no stale captures
- **Server state in query cache only**: Never duplicate in `useState`

### OpenAPI Codegen Pipeline: Orval (2026)
- **Single pipeline**: OpenAPI spec → TanStack Query v5 hooks + MSW v2 mocks + TypeScript types
- **Auto-updated MSW mocks** in test/dev environments
- **Generated types as source of truth**: No manual API contract types

---

## 3. Streaming AI Responses (2026)

```tsx
// Token-by-token UI updates without re-render storms
const [state, dispatch] = useReducer(reducer, initialState);

// ReadableStream + TextDecoderStream
const reader = response.body.getReader();
const decoder = new TextDecoderStream();
for await (const chunk of reader.pipeThrough(decoder)) {
  dispatch({ type: 'TOKEN', payload: chunk });
  // Batched via React.startTransition for non-urgent
}

// Cancellation hooks
const abortController = new AbortController();
<button onClick={() => abortController.abort()}>Stop</button>
```

---

## 4. CSS View Transitions API (2026)

### Native Browser Support
- **`::view-transition-old` / `::view-transition-new`** pseudo-elements
- **Composited motion only**: `transform` and `opacity` ONLY; never layout geometry (`width`, `height`, `top`, `left`, `margin`, `padding`)

### React 19 `<ViewTransition>` (2026)
```tsx
<ViewTransition name={`hero-${id}`} share="morph" default="none">
  <HeroImage src={image} />
</ViewTransition>
```

### Performance Budgets (2026)
| Interaction Type | Budget |
|------------------|--------|
| Hotkeys (`Cmd+K`) | 0ms (instant) |
| Micro-interactions | 100-150ms |
| Overlays/Drawers | 150-250ms |
| Route transitions | ≤ 400ms |
| **INP** | **< 200ms** (DOM mutation < 50ms) |

### Spring Physics (2026)
- **Mass**: m = 1.0
- **Damping**: ζ ≈ 0.75-0.85 (near-critical)
- **Forbidden**: Underdamped ζ < 0.6 (cartoonish bouncing)

### App Shell Isolation
- Persistent headers/sidebars: unique `viewTransitionName`, suppress animations
- **Single smooth-scroll engine**: Exactly one (Lenis or native CSS); no Lenis + Locomotive

### Reduced Motion (WCAG 2.2 AA)
- **Mandatory**: `@media (prefers-reduced-motion: reduce)` disables/instant-fades all animations

---

## 5. WebMCP (2026)

### Core Requirements
- **Feature detection**: `'modelContext' in document` guards for SSR/polyfill
- **State synchronization**: Sanitized app state (Redux/Zustand) → WebMCP context; sensitive fields stripped
- **Action allowlist (default deny)**: Explicit registration required; no runtime broadening
- **Strict input schema**: Every tool declares explicit property types, enums, required fields
- **Security context**: HttpOnly cookies stay outside JS runtime WebMCP can read
- **HITL gate**: Non-idempotent/financial actions require explicit user confirmation; fail-safe on dismiss/timeout
- **Background sync**: Service Workers + Push API for async HITL callbacks
- **Structured error payloads**: `{ error: { code: 'OUT_OF_STOCK', message: '...' } }` — never raw stack traces

### MCP Registry Integration
- Backend MCP server cards registered; browser WebMCP discovers via registry
- Permission parity: Agent actions cannot bypass UI permission rules

---

## 6. Component Architecture (2026)

### React 19 Idioms (Mandatory)
- **No `forwardRef`**: Pass `ref` as standard prop
- **`use(Context)`**: Instead of `useContext()`
- **`<Context value={...}>`**: Instead of `<Context.Provider>`
- **`useId()`**: Deterministic IDs for label/description/error linking (Server Actions compatible)

### shadcn v4 Form Architecture
- **`FieldGroup` + `Field`**: Replace legacy v3 `FormItem`/`FormControl` boilerplate
- **React 19 `useId()`**: Deterministic label, description, error linking
- **`InputGroup`**: Prefix/suffix addons, action buttons, dropdowns with `:focus-within` rings

### Compound Components & Slot Delegation
| Pattern | Use Case |
|---------|----------|
| **Base UI `render` prop** | Children need internal headless state injection or polymorphic tags |
| **Radix `asChild` (`Slot`)** | Single-child prop delegation without state projection |

### Headless Hooks (Standardized)
```tsx
const { state, actions, triggerProps, contentProps } = useDialog();
// Returns: keyboard bindings (Escape, Enter, Arrows) + ARIA attributes
```

### Anti-Boolean Prop Sprawl (2026)
- **Max 2 booleans for purely stylistic states**
- **Layout-altering booleans banned**: `isThread`, `hasBadge`, `isHeader`, `withIcon`, `isLoadingModal`
- **Replace with**: Compound components (`Component.Root`, `Component.Trigger`, `Component.Content`) or explicit pre-composed variants (`ThreadComposer`, `ChannelComposer`)

---

## 7. Design System & GenUI Governance (2026)

### Tailwind v4 CSS-First Configuration
- **`@theme` in CSS entrypoints**: Define all tokens inside `@theme` — NO `tailwind.config.js`
- **OKLCH perceptual color space**: Uniform contrast, predictable lightness across light/dark
- **CSS variable dark mode**: FORBID manual `dark:bg-*` / `dark:text-*` overrides; dark mode exclusively via `:root` / `.dark` CSS variable mapping

### W3C DTCG Token Format
- **`{ "$value": ..., "$type": ... }` JSON** for Figma Variables, Style Dictionary, AI tools interop
- **Functional naming**: `primary-500`, `text-foreground`, `border-border` — NOT `light-blue`, `#...`

### GenUI Pipeline (Mandatory CI Gates)
1. **Token conformance check**: Consumes design tokens, forwards refs, includes ARIA, no duplicate classes
2. **axe-devtools scan**: Color contrast, screen reader labels, keyboard navigation
3. **CSS pollution prevention**: Strip custom/inline/non-repo CSS files and rules
4. **Chromatic/TurboSnap baseline**: Visual regression baseline required before merge
5. **Peer review mandatory**: All AI-generated components reviewed for code style and safety

### Storybook 8+ Requirements
- **`a11y` + `chromatic` addons**: Mandatory CI gates
- **TurboSnap**: Only re-tests changed component stories

---

## 8. Visual Regression (2026)

### Containerized Baselines (Mandatory)
- **Official Playwright Docker only**: `mcr.microsoft.com/playwright` matching CI environment
- Local macOS/Windows vs Linux CI = guaranteed false failures

### Technical Standards
- **Animation suppression**: `animations: 'disabled'`
- **Dynamic content masking**: `mask: [page.locator('...')]` for timestamps, avatars, IDs, ads
- **Explicit tolerance**: `maxDiffPixelRatio: 0.01`, `threshold: 0.2`
- **Component isolation**: Storybook + Chromatic TurboSnap + full-page Playwright
- **Cross-browser matrix**: Chromium, WebKit, Firefox at mobile/desktop
- **Hard CI gate**: Visual failures block merges unless `ui-ux-designer`/`frontend-developer` explicitly approves
- **Network mocking**: MSW for deterministic fixtures — live external API = non-deterministic

### Bounded Self-QA
- **Max 2 passes** post-authoring for agent self-QA
- Desktop + Mobile simultaneously
- Edits triggered by deterministic defects only (overflow, fold clipping, broken markup, `< 44x44px` touch targets, contrast failures)

### Negative Asset Constraints
- **Fabricated inline SVG logos prohibited**: "NovaCorp" style synthetic logos banned
- **Synthetic customer testimonials banned**: Unverified metrics prohibited
- **Authentic typography mandated**: System monograms, verified Simple Icons marks, honest structural placeholders

---

## 9. Frontend Testing (2026)

### Playwright v1.48+ (Mandatory)
- **Web-first auto-waiting**: `expect(locator).toBeVisible()`, `toBeEnabled()` — ban `sleep()`, `waitForTimeout()`
- **Trace Viewer**: `trace: 'retain-on-failure'` with console, network, DOM
- **HAR replay**: `page.routeFromHAR()` for deterministic external APIs
- **Component Testing**: `@playwright/experimental-ct-*` or Vitest Browser Mode

### MSW v2 Transport-Level
- **`setupServer` (Node/Vitest) / `setupWorker` (browser/Playwright)**
- **Typed `HttpResponse.json()`**: Standard fetch `http.*` methods
- **`onUnhandledRequest: 'error'`**: Catch unmocked requests, prevent live backend leakage
- **Network variation simulation**: Latency, 4xx/5xx, disconnection, malformed payloads

### WCAG 2.2 AA (Zero Violations CI Gate)
- **`@axe-core/playwright`**: `AxeBuilder.withTags(['wcag2a', 'wcag2aa', 'wcag22aa']).analyze()`
- **Keyboard focus containment**: Tab trapped in modals, flyouts, drawers
- **Focus restoration**: Escape dismisses overlay, restores focus to trigger
- **ARIA snapshots**: `expect(locator).toMatchAriaSnapshot()`

### AI/LLM UI Resilience Testing
- **Empty, truncated, streaming, malformed LLM responses**: Explicit test cases
- **Visual baselines before AI merge**: Catch missing active/hover/focus states
- **Axe-core on AI UI**: Catch syntactically valid but semantically broken ARIA

### Pairwise & Systematic Testing
- **`combinatorial-testing`**: Pairwise covering arrays across viewports × permissions × states
- **`systematic-debugging`**: 4-phase isolation (Reproduce → Isolate → Diagnose → Verify)
- **Mutation testing**: Stryker ≥ 75-80% for critical UI logic

---

## 10. Cross-Skill Integration: Frontend → Backend → Mobile

```
add-page-route
├── RSC leaf pattern ("use client" depth)
├── Loader pattern mandatory (no useEffect fetches)
├── Zod validateSearch with .catch() fallbacks
├── AI route audit (auth, loader, cache, URL)
├── CSS View Transitions integration
    ↓
add-ui-component
├── RSC/client boundary classification
├── React 19 useActionState + useOptimistic
├── Anti-slop mechanics (min-h-[100dvh], motion/react, :active, CTA no-wrap, approved icons)
├── AI governance (token, axe, CSS strip, review, baseline)
├── Lit v3 @lit/react wrapper
├── shadcn v4 FieldGroup/Field + useId()
    ↓
component-composition
├── React 19 idioms (no forwardRef, use(Context), useId())
├── shadcn v4 FieldGroup/Field + useId()
├── Base UI render prop vs Radix asChild decision
├── Headless hooks (useDialog, useDropdown)
├── Anti-boolean prop sprawl (max 2 stylistic)
    ↓
integrate-api-client
├── Orval: OpenAPI → TanStack Query v5 + MSW v2 + TS types
├── queryOptions factories (no magic string keys)
├── React 19 use() for RSC + TanStack Query client
├── useActionState for forms + useMutation for complex
├── Streaming: ReadableStream + useReducer + cancellation
    ↓
frontend-testing
├── Playwright v1.48+ web-first + Trace Viewer + HAR
├── MSW v2 transport-level + onUnhandledRequest: 'error'
├── WCAG 2.2 AA zero-violations CI gate
├── Font-stabilized visual regression in containerized Linux
├── Playwright Component Testing / Vitest Browser Mode
├── ARIA snapshots + AI LLM response matrix
├── Pairwise combinatorial + systematic debugging 4-phase
├── Mutation score ≥ 75-80% (Stryker)
    ↓
implement-view-transitions
├── Composited motion only (transform/opacity)
├── Frequency-based animation budget
├── React 19 ViewTransition with default="none"
├── Shared element morphing (dynamic unique names)
├── INP < 200ms with 50ms DOM mutation limit
    ↓
implement-webmcp
├── Feature detection ('modelContext' in document)
├── Default deny action allowlist
├── Strict input schema validation
├── HITL gate for non-idempotent/financial
├── Service Worker + Push API for async HITL
├── MCP Registry coordination
├── Permission parity (agent = UI permissions)
```

---

## 11. Key References

- **React 19**: https://react.dev/blog/2024/12/05/react-19
- **TanStack Query v5**: https://tanstack.com/query/v5/docs
- **TanStack Start RSC**: https://tanstack.com/blog/react-server-components
- **Orval**: https://orval.dev
- **CSS View Transitions**: https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API
- **React 19 ViewTransition**: https://react.dev/reference/react/ViewTransition
- **WebMCP**: https://webmcp.dev
- **Playwright v1.48+**: https://playwright.dev/docs/release-notes
- **MSW v2**: https://mswjs.io/docs/getting-started
- **axe-core/playwright**: https://github.com/dequelabs/axe-core-npm
- **Storybook 8**: https://storybook.js.org/blog/storybook-8
- **Tailwind v4**: https://tailwindcss.com/blog/tailwindcss-v4
- **OKLCH**: https://oklch.com
- **W3C DTCG**: https://design-tokens.github.io/community-group/format
- **shadcn/ui v4**: https://ui.shadcn.com
- **Reanimated 4**: https://docs.swmansion.com/react-native-reanimated
- **FlashList**: https://shopify.github.io/flash-list
- **Expo Router**: https://docs.expo.dev/router/introduction