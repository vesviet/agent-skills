# frontend-developer.md - Year-Tagged Responsibilities (extracted)

These sections were extracted from `## Core Responsibilities` in the role file to keep the main file under a manageable size while preserving the full content.

---

### AI-Generated UI Governance (2025-2026)


In 2026, AI tools (Cursor, Copilot, v0) generate significant UI volume. The frontend developer's role shifts from writer to **architect, validator, and quality lead**:

**Tiered validation by risk level** — apply validation depth proportional to risk:
| Risk Tier | Example | Validation Required |
| --------- | ------- | ------------------- |
| **High** | Auth/permission UI, payment flows, form validation with business rules, role-conditional rendering | Full manual review: behavior correctness + accessibility + state machine correctness + security boundary check |
| **Medium** | Complex state flows, shared hooks/stores, API integration components | Review logic paths, all UI states, shared component impact |
| **Low** | Static layouts, presentational components, boilerplate scaffolding | Visual review + automated lint/a11y scan |

**Mandatory validation checklist for AI-generated UI code:**
- **Behavior correctness**: all UI states handled (loading, empty, error, disabled, stale, success); transitions are correct; derived state is computed correctly
- **Accessibility**: keyboard navigation, ARIA roles, focus management, screen reader compatibility; do not accept AI output that fails basic a11y checks
- **State management**: no unintended shared state mutations; no race conditions in async flows; optimistic updates have rollback paths
- **Rendering strategy**: SSR vs CSR vs partial hydration is intentional, not accidental; AI defaults may introduce unnecessary client-side JS or break SSR hydration
- **Security boundary**: UI permission checks are supplementary, not the primary security boundary; AI-generated role checks must not replace server-side authorization
- **Bundle impact**: check if AI-generated code added unnecessary dependencies or duplicated functionality already in the design system

**AI as collaborator, human as architect** — human engineer retains ownership of:
- rendering strategy selection: SSR / CSR / SSG / ISR / partial hydration / islands architecture
- state management boundaries: what is global state, what is local, what lives in the URL
- design system adherence: AI may not know your token system, component API, or naming conventions — verify
- performance budget decisions: AI-generated code may introduce bundle bloat that exceeds CI budget gates

**Visual regression testing** — for AI-generated UI changes:
- run visual diff against baseline screenshots for affected routes/components before merge
- use CI-integrated tools: **Playwright** (`toHaveScreenshot`), **Chromatic** (Storybook-based), or **Percy** for branch-diff visual comparison; baseline screenshots must be committed to the test repository
- flag unexpected layout shifts (CLS contributors) or rendering changes as defects, not style preferences
- treat visual regressions in auth flows, payment UI, or permission-conditional rendering as P1 blocking defects

**Agent Context Sharing (WebMCP):**
- implement Model Context Protocol (WebMCP) in the browser to share frontend state, DOM context, and UI events securely with autonomous AI Agents, allowing them to debug or interact with the client application natively



---

### AI Streaming UI & GenUI (2026)


In 2026, AI-powered UIs stream token responses and structured UI components in real time. Frontend developers own the streaming consumption layer:

**SSE-based AI token streaming:**
- use **Server-Sent Events (SSE)** as the primary protocol for streaming AI token responses — SSE is native to HTTP, works with CDNs and load balancers, and supports auto-reconnect; avoid WebSockets for unidirectional AI response streaming
- wire an `AbortController` to every SSE/streaming fetch request; cancel the stream in `useEffect` cleanup or on navigation away — missing `AbortController` creates stuck loading states and wasted token spend
- expose a visible stop/cancel button wired to `AbortController.abort()` for any streaming request that the user may want to interrupt mid-generation

**INP-safe streaming renders:**
- **AI token streaming is the #1 new INP risk in 2026**: token-by-token DOM updates block the main thread and cause INP failures; chunk streaming renders with `scheduler.yield()` or `requestIdleCallback` to release the main thread between batches
- wrap non-urgent streaming updates in `React.startTransition` to deprioritize them behind user interactions
- pre-size AI response containers with CSS min-height or aspect-ratio to prevent streaming text causing Cumulative Layout Shift (CLS); never allow containers to grow unconstrained as tokens arrive

**GenUI (Generative UI via RSC streaming):**
- when using `streamUI` or equivalent (Vercel AI SDK), frontend devs must understand the RSC streaming lifecycle: the server streams hydrated React components (not just text tokens), requiring correct Suspense boundary placement and streaming-compatible layout
- do not allow agents to stream arbitrary JSX or HTML — use the Component Registry pattern (see below) to ensure only pre-approved, type-safe components are rendered

**AG-UI event rendering:**
- for agentic pipelines using the AG-UI protocol, implement discrete UI states for each event type: `THOUGHT` (show thinking indicator), `TOOL_CALL` (show tool execution progress), `RESULT` (render structured output), `ERROR` (show error state with retry option)
- do not render AG-UI events as raw text; each event type maps to a specific UI component with defined visual treatment



---

### AI Disclosure & Agent-Safe Components (2026)


EU AI Act Article 50 is live from **2 August 2026**. Frontend developers are the implementation layer for legal disclosure compliance:

**Article 50 disclosure UI (legal requirement):**
- every AI-powered feature that interacts with natural persons must display a clear, accessible, non-dismissable disclosure **before or during the first meaningful interaction** — not after the first AI message
- the disclosure must use plain, unambiguous language: "You are interacting with an AI system" — must not be buried in terms, tooltips, or sub-menus
- build a reusable `<AIDisclosureBanner>` component with the EU-approved AI icon for AI-generated content labels; use this component consistently across all AI-powered features — do not recreate disclosure UI per feature
- for systems live before 2 August 2026: machine-readable marking (C2PA content credentials or equivalent) for AI-generated images, audio, and video must be implemented by **2 December 2026**; include this as a scheduled engineering item in scope planning

**AI-generated content marking:**
- embed `data-ai-generated="true"` attributes on all AI-rendered text containers for machine-readable marking
- for AI-generated media (images, audio, video): integrate C2PA (Coalition for Content Provenance and Authenticity) content credentials or equivalent technical watermark metadata
- the EU AI icon must accompany any labelled AI-generated content display in EU-market products

**Agent-safe Component Registry pattern:**
- never allow AI agents to generate arbitrary JSX, HTML strings, or raw component trees for direct rendering; this is a critical security and quality boundary
- implement a typed Component Registry: agent sends structured JSON (`{ "type": "invoice", "props": {...} }`), the registry maps the type to a pre-approved, security-reviewed React component that renders the trusted UI
- all components in the registry must pass full security and accessibility review before registration; the registry is the trust boundary, not the agent

**HITL approval gates:**
- all agent-triggered mutations (payments, data deletion, form submission, external communications) must require an explicit `<AgentActionApprovalModal>` before execution — never allow agents to trigger irreversible actions without user confirmation
- wire HITL approval modals to `AbortController`; if the user cancels, abort the agent action and return to safe state
- the HITL gate must be rendered as a visible, keyboard-accessible modal — not a background confirmation; screen readers must announce the approval request

**Calling AI APIs — always via backend proxy:**
- never call AI provider APIs (OpenAI, Anthropic, Gemini) directly from frontend code; API keys must never be in browser-accessible code
- all LLM calls must route through a backend proxy layer that owns: API key management, rate limiting, cost attribution, token logging, and response caching
- the frontend consumes the proxy API via SSE or standard REST — it has no knowledge of which AI provider is used or what system prompt is sent



---

### WCAG 2.2 AA Legal Compliance (2026)


WCAG 2.2 AA is the mandatory legal baseline under EU EN 301 549, the UK Equality Act 2010, and ADA/Section 508. Frontend developers must implement all 9 new success criteria introduced in WCAG 2.2:

**WCAG 2.2 AA — new criteria (legally required):**
| Criterion | Level | Frontend Implementation |
|-----------|-------|------------------------|
| **2.4.11 Focus Not Obscured (Minimum)** | AA | Sticky headers, footers, overlays, and chat widgets must not fully cover a focused element; use scroll-margin-top / scroll-padding CSS properties on focusable elements beneath fixed bars |
| **2.5.7 Dragging Movements** | AA | All drag-and-drop interactions must have a single-pointer (click/tap) alternative — buttons to move, reorder, or resize items |
| **2.5.8 Target Size (Minimum)** | AA | Interactive targets must be ≥ 24×24 CSS pixels, or have sufficient spacing; critical for AI chat input areas, send buttons, and action chips |
| **3.2.6 Consistent Help** | A | Help mechanisms (support chat, FAQ links, contact) must appear in the same relative location across all pages in the site |
| **3.3.7 Redundant Entry** | A | Auto-populate previously entered data in multi-step flows; do not force users to re-enter information already provided in the same session |
| **3.3.8 Accessible Authentication (Minimum)** | AA | Authentication must not rely on cognitive function tests (puzzles, memorization, image recognition); directly impacts CAPTCHA choice — Turnstile (Cloudflare) or audio CAPTCHA is compliant; standard image CAPTCHAs are not |

**WCAG 2.2 for AI-powered UIs specifically:**
- **`aria-live="polite"` on streaming containers** is mandatory: screen readers cannot announce streaming AI tokens without an aria-live region; add `role="log"` + `aria-live="polite"` to all AI response containers
- **focus management after agent actions**: when an agent modifies the DOM, move focus to a meaningful element (e.g., the newly rendered result or a status notification); do not leave focus on a trigger element that no longer reflects current state
- **AI-generated content must be accessible**: validate any AI-generated HTML markup with axe-core before DOM insertion; AI tools frequently generate inaccessible markup (missing alt attributes, missing labels, incorrect ARIA roles)
- **WCAG 3.0** is in working draft — not yet required, but monitor for the new scoring model; design system tokens and component patterns adopted now will ease the transition



---

### Performance-as-a-Product (2025-2026)


Performance is a direct revenue driver. A 100ms improvement in response time can increase conversion by 1%; a poor INP score degrades perceived quality for all users. Enforce this at the engineering level:

**Core Web Vitals (CWV) — the 2026 standards:**
| Metric | What it measures | Target |
| ------ | ---------------- | ------ |
| **INP** (Interaction to Next Paint) | Overall session responsiveness (replaced FID in 2024) | <200ms |
| **LCP** (Largest Contentful Paint) | Perceived load speed | <2.5s |
| **CLS** (Cumulative Layout Shift) | Visual stability | <0.1 |

- **INP is the definitive responsiveness metric** in 2026: it measures every interaction throughout the session, not just the first (FID). A page that loads fast but stutters on interactions will still fail CWV.
- prioritize **field data (CrUX)** over lab data (Lighthouse scores): a 100/100 Lighthouse score on a fast dev machine does not represent real users on slow devices or mobile networks

**Performance budgets in CI/CD:**
- define and enforce JS bundle size budgets per route; fail CI if a change causes a bundle to exceed the budget
- define CWV budgets per page type and integrate CWV regression detection in CI (Lighthouse CI or equivalent)
- treat a CWV budget breach as a blocking defect, not a polish item

**Rendering strategy decision framework** — choose intentionally for each route:
| Strategy | Use when | Performance profile |
| -------- | -------- | ------------------- |
| **SSG** (Static Site Generation) | Content rarely changes, no user personalization | Fastest: CDN-cached HTML |
| **SSR** (Server-Side Rendering) | Personalized or frequently updated content | Fast TTFB, full HTML for SEO |
| **ISR** (Incremental Static Regeneration) | Content changes on a schedule | CDN cache + background revalidation |
| **CSR** (Client-Side Rendering) | Highly interactive, auth-gated dashboards | Worst for initial load; acceptable for app-shell after hydration |
| **Partial hydration / Islands** | Content-heavy pages with isolated interactive islands | Minimal JS: only interactive components hydrate |

**Optimization tactics for INP:**
- **break up long tasks**: any JS task >50ms on the main thread delays interaction response; use `scheduler.yield()` or task chunking
- **defer non-essential third-party scripts**: analytics, chat widgets, and ad scripts must not block interaction readiness
- **prioritize LCP elements**: use `fetchpriority="high"` on above-the-fold images and critical resources
- **adaptive hydration**: prioritize hydrating components based on user viewport position and device capability, not page order



---

### Accessibility-as-CI-Gate (2025-2026)


Accessibility review as a manual, pre-merge concern is insufficient at 2026 delivery pace. The production standard is **automated a11y enforcement baked into CI as a hard quality gate**, blocking merge on regression rather than relying on manual checklists:

**axe-core CI enforcement (hard gate):**
- integrate `@axe-core/playwright` into the CI test suite; run a11y scans on every PR against all affected routes and component states
- configure CI to **fail the build** on any new axe-core violation (do not allow existing violations to suppress new ones via a blanket ignore list; use targeted `rules: { 'rule-id': { enabled: false } }` for known exceptions with documented rationale)
- scan all user-facing states: not only the happy path render; include empty states, error states, and permission-limited states in the scan scope
- treat axe-core scan failures as P1 blocking defects, not style preferences; inaccessible controls are a legal liability under WCAG 2.2 AA (required by EU EN 301 549, ADA, and Section 508)

**Lighthouse CI continuous a11y tracking:**
- configure Lighthouse CI to track the Accessibility score alongside CWV metrics on every PR; publish score trends in the CI report
- set a minimum Lighthouse Accessibility score budget (e.g., 95+); score drops below budget trigger the same review process as CWV budget breaches
- use Lighthouse CI historical comparison to catch gradual score erosion across many small PRs that individually pass the axe-core hard gate

**A11Y enforcement in AI-generated UI:**
- AI tools (Cursor, Copilot, v0) frequently omit ARIA roles, focus management, and keyboard navigation; the axe-core CI gate catches these automatically
- for High-tier AI-generated UI (auth, payment, permission-conditional rendering): manual a11y review remains mandatory in addition to the automated gate
- the axe-core CI gate does not replace manual testing with VoiceOver/NVDA/JAWS for complex interactive components; it catches the systematic, automatable failures



---

### Edge-Side Rendering — React Server Components at CDN Edge (2025-2026)


The rendering strategy table covers SSR/CSR/SSG/ISR/Islands. A new architectural option in 2026 is **React Server Components (RSC) executing directly on the CDN edge** (Cloudflare Workers + Vite Cloudflare plugin), which is architecturally distinct from origin-server SSR and changes the performance profile and constraint set:

**Edge RSC vs. origin SSR — key distinctions:**
| Dimension | Origin SSR | Edge RSC (Cloudflare Workers) |
|-----------|-----------|-------------------------------|
| **TTFB** | 50–200ms typical (origin round-trip) | Near-zero (executed at nearest PoP) |
| **Runtime** | Node.js (full API) | V8 isolate (no Node.js APIs, no filesystem, no native modules) |
| **Streaming** | Node.js `ReadableStream` | `TransformStream` (Web Streams API only) |
| **State** | In-memory / Redis | Durable Objects (stateful coordination at edge) |
| **Cold starts** | Container warm-up (100ms–1s) | Isolate cold start (<5ms) |
| **Cost** | Per-second compute | Per-request microsecond billing |

**Edge-compatibility constraints — must validate before deploying RSC to edge:**
- **No Node.js APIs**: "fs", "path", "crypto" (Node version), "child_process", "Buffer" (non-Web), and any npm package that wraps them will fail at the edge; use Web APIs equivalents (`crypto.subtle`, `TextEncoder`, `URL`)
- **No native Node modules** (`.node` binaries): any npm package with native bindings cannot run in a V8 isolate; audit all RSC dependencies with `wrangler types` or the CF compatibility checker
- **Streaming is TransformStream-based**: RSC streaming uses Web Streams; libraries that pipe via Node.js "stream" require adaptation
- **Durable Objects for stateful edge**: if RSC needs per-user session state at the edge, use Durable Objects (WebSocket hibernation for long-lived connections); do not attempt to hold state in V8 isolate memory across requests
- **Bundle size limit**: Cloudflare Workers have a 10MB (compressed) script limit; monitor RSC bundle size; code splitting is required for large component trees

**When to choose Edge RSC over origin SSR:**
- choose Edge RSC when: TTFB is the primary bottleneck, the route has no Node.js-specific dependencies, personalization data is available at the edge (via KV, D1, or Durable Objects), and the component tree is within bundle limits
- choose origin SSR when: the route requires Node.js APIs, uses native npm modules, or needs large database queries that benefit from origin proximity
- **EDGE-RENDERING-COMPAT LOCK** applies: the decision to deploy RSC to the edge is an architectural choice that must be validated, not an automatic optimization



---

### PWA-Agent Bridge — Service Workers as Agentic Control-Plane (2025-2026)


In 2026, Service Workers are evolving beyond caching and offline support into **agentic orchestration infrastructure**: managing background AI task delegation, polling agent status, and bridging AI task completion back to the user interface:

**Service Worker as agentic control-plane:**
- use Service Workers to orchestrate background AI task delegation: the SW intercepts fetch requests to AI endpoints, queues tasks when offline, and retries with exponential backoff using `Periodic Background Sync`
- `Background Sync API`: when the device regains connectivity, the SW automatically retries queued AI tasks without requiring the user to re-submit; critical for mobile users on unreliable connections
- `Periodic Background Sync API`: for agent check-in patterns where the app periodically polls for completed agent tasks, updates, or model refreshes without requiring the user to open the app

**Web Push API as HITL callback bridge:**
- for Human-in-the-Loop AI workflows (agent tasks that require user approval or input), use the `Push API` to deliver HITL notifications: the backend sends a push event when the agent reaches a decision point requiring user input
- the Service Worker receives the push event and shows a notification (even when the app is closed); the user taps to open the app and complete the HITL step
- this enables truly async agentic workflows: the user initiates a task, the agent works in the background, and the push notification bridges the HITL callback

**Service Worker scope and security constraints:**
- Service Workers must not execute LLM inference directly; inference must be delegated to cloud AI agents or native app layers; the SW is a control-plane, not a compute engine
- validate message origin for all `postMessage` communication between SW and the app; do not process messages from untrusted origins
- Service Worker registration scope limits which routes the SW controls; scope must be declared explicitly and reviewed for overly broad coverage



---

### Browser-Native Module Federation (2025-2026)


For micro-frontend architectures or large frontend applications with independent team delivery, 2026 introduces a production-viable alternative to Webpack Module Federation: **Import Maps + ESM (Browser-Native Federation)**:

**Import Maps (<script type="importmap">):**
- Import Maps are a W3C standard (~94.5% browser coverage in 2026, with es-module-shims for compatibility fallback); they allow remapping bare module specifiers to URLs at the browser level without a bundler
- use Import Maps to share singleton dependencies (React, a design system library) across independently deployed micro-frontends without bundler coordination; each micro-frontend declares its own modules, and the Import Map enforces shared singleton versions
- Import Maps are a static JSON declaration served with the HTML shell; updates to the map require an HTML shell deployment, not a library rebuild

**Native Federation decision framework — when to use which approach:**
| Approach | Use when |
|----------|----------|
| **Import Maps + ESM** | Small to medium micro-frontend teams; bundler-agnostic requirement; singleton enforcement is the primary concern; no complex shared state across micro-frontends |
| **Module Federation 2.0** (Webpack/Rspack) | Large teams with complex dynamic loading requirements; runtime feature flags for shared modules; need for runtime version negotiation between independently deployed apps |
| **Single bundled app** | Team size <5 FE engineers; feature velocity over deployment independence; complexity cost of federation exceeds the benefit |

**Singleton management with Import Maps:**
- the primary risk of module federation (any approach) is **duplicate framework instances** (two React copies in the same page); this causes silent failures (hooks state isolation, context disappearing, event system splits)
- in Import Maps: pin React, ReactDOM, and all shared singletons in the Import Map with exact version URLs; micro-frontends must not bundle their own copy of pinned singletons
- verify singleton enforcement at runtime with `window.__REACT_DEVTOOLS_GLOBAL_HOOK__` or equivalent; if two React instances are present, the Import Map has a gap


---
