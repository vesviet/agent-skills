## Review Checklist

This reference checklist provides detailed engineering, validation, and security criteria for frontend development to meet 2027 Agentic SWE standards.

### UI Integrity
- user flow matches requirements, business logic, and expected roles
- bug fixes are verified against the original issue and nearby regression-prone flows
- loading, empty, error, success, disabled, stale, and retry states are explicit where relevant
- conditional rendering, derived state, and validation logic are correct for edge cases
- shared hooks, stores, utilities, or components affected by the fix have been re-checked
- accessibility, keyboard behavior, focus behavior, and responsive behavior are checked
- API contracts, caching, mutation side effects, and optimistic updates are handled intentionally
- tests or manual scenarios cover important interactions and impact radius
- user-facing copy, validation feedback, and error messaging are clear
- unverified risk is called out explicitly instead of implied away

### Red-Green TDD for UI
- **Behavioral Test Authoring First**: Component interaction tests (using Testing Library, user-event, or Playwright component testing) are authored prior to JSX or CSS implementation.
- **Verified Failing Assertion (Red)**: Tests initially fail with unambiguous expectation failures for unrendered states, missing handlers, or incomplete accessibility roles.
- **Minimal JSX/State Implementation (Green)**: Minimal component logic and styling are added to satisfy the behavioral tests without over-engineering or adding untested side logic.
- **Refactoring & Styling Isolation (Refactor)**: Component styles and layout are refined under active test coverage, ensuring visual enhancements do not break behavioral assertions.
- **State Machine Test Coverage**: Tests explicitly assert all state transitions (idle, pending, fulfilled, rejected) rather than testing only static visual snapshots.

### Execution Sandbox Isolation (OWASP ASI05)
- **Component Preview Sandboxing**: Dynamic previews of AI-generated components or third-party widgets execute inside sandboxed iframes (`sandbox="allow-scripts"` without `allow-same-origin`) to prevent access to session cookies, localStorage, or host DOM.
- **Third-Party Script Isolation**: External scripts, widgets, and dynamic WebMCP extensions run inside isolated Web Workers or partitioned iframe environments.
- **No Dynamic HTML/Code Evaluation**: Dynamic code execution (`eval()`, `new Function()`) is prohibited in frontend bundles; DOM injection of raw AI output without Trusted Types and DOMPurify is blocked.
- **Token & Storage Quarantine**: Sensitive authentication tokens, API keys, or personal data are never stored in client-side storage accessible to previewed or dynamic third-party scripts.

### Anti Vibe-Slop Verification
- **Functional Interactivity Verification**: Verify that every button, toggle, and input has an actual working handler wired to real state or APIs; reject mock `console.log` handlers or dead click targets.
- **Loading & Error State Parity**: Verify that loading skeletons, disabled states during async mutations, and granular error banners are fully functional, not omitted behind happy-path mocks.
- **Design System Conformance**: Reject hallucinated styling tokens, arbitrary hex values, or random utility classes; all styling must use verified design system tokens.
- **Visual vs Logic Parity**: Reject components that look visually polished but have broken tab order, missing aria attributes, or non-functional keyboard navigation.
- **Streaming & Hydration Robustness**: Verify that streaming AI chunks and async data hydrations do not trigger hydration mismatches, layout jumps, or race conditions between rapid user inputs.

### Deterministic UI State Machines
- **Finite State Modeling**: Complex async journeys (multi-step forms, streaming AI interactions, checkout flows) are modeled using explicit deterministic finite state machines.
- **Impossible State Elimination**: State models prevent invalid concurrent states (e.g., cannot be simultaneously `isLoading` and `isError`).
- **Deterministic Action Transitions**: Every user event or API response deterministically transitions the UI from one valid state to another with explicit error and retry states.
- **Cancellation & Backpressure**: Asynchronous requests and streaming token updates are bound to `AbortController` instances to cancel in-flight operations when transitions occur.

### AI-Generated UI Code Validation (when AI tools contributed to this change — mark N/A if code is entirely human-authored)
- risk tier classified: [high / medium / low]
- behavior correctness: all UI states handled including edge cases not in the prompt
- accessibility: keyboard navigation, ARIA, focus management verified; automated a11y scan passed
- state management: no shared state mutations; async race conditions and optimistic update rollbacks checked
- rendering strategy: SSR/CSR/hydration strategy is intentional, not an accidental AI default
- security boundary: UI permission checks supplement server-side auth; they are not the primary control
- bundle impact: no unnecessary dependencies; design system used instead of reinventing components
- visual regression: visual diff run against baseline for affected routes

### Performance (Core Web Vitals)
- INP target: interactions respond within 200ms (no long tasks blocking main thread >50ms without yield)
- LCP target: largest contentful paint <2.5s; `fetchpriority="high"` on above-the-fold images
- CLS target: no layout shifts >0.1; no content popping in after load without reserved space
- JS bundle budget: per-route bundle sizes within defined limits; no accidental dependency bloat
- field data considered: CrUX data checked if available; Lighthouse score not the only signal
- third-party scripts: analytics, chat, and ad scripts deferred or loaded async
- rendering strategy documented: SSG / SSR / ISR / CSR / partial hydration / Edge RSC choice is explicit and justified

### Accessibility CI Gate
- axe-core/Playwright CI scan run for all affected routes and component states
- no new axe-core violations introduced (hard gate, not advisory)
- Lighthouse Accessibility score within defined budget
- manual a11y review completed for High-tier AI-generated auth/payment/permission UI (VoiceOver/NVDA)

### Edge RSC (when deploying RSC to CDN edge)
- No Node.js API usage in RSC dependency graph confirmed
- No native npm modules (.node binaries) in RSC bundle
- Streaming via Web Streams API (TransformStream), not Node.js stream
- Durable Objects used for stateful coordination (not in-isolate memory)
- Bundle size within Cloudflare Workers 10MB limit

### PWA & Service Workers (when SW-based agentic features are in scope)
- Service Worker does not execute LLM inference directly; inference delegated to cloud
- `postMessage` origin validated for all SW-to-app communication
- Background Sync / Periodic Background Sync used for task queuing and agent check-ins
- Push API configured for HITL callback delivery
- Service Worker scope declared explicitly and reviewed for overly broad coverage

### AI Streaming UI (when AI token streaming or GenUI is in scope)
- SSE used instead of WebSockets for unidirectional AI response streaming
- `AbortController` wired to every SSE/streaming fetch request; cancelled in `useEffect` cleanup
- Stop/cancel button visible and functional for all streaming requests
- Streaming renders chunked with `scheduler.yield()` / `requestIdleCallback`; no synchronous long tasks >50ms
- Non-urgent streaming updates wrapped in `React.startTransition`
- AI response containers pre-sized with CSS min-height or aspect-ratio to prevent CLS
- AG-UI events mapped to discrete UI component states (THOUGHT / TOOL_CALL / RESULT / ERROR); not rendered as raw text

### AI Disclosure & Agent-Safe Components (when AI features interact with natural persons)
- `<AIDisclosureBanner>` rendered before or during the first meaningful AI interaction (Article 50 legal requirement since 2 Aug 2026)
- Disclosure uses plain language ("You are interacting with an AI system"), not buried in terms
- `data-ai-generated="true"` attributes present on all AI-rendered text containers
- C2PA content credentials or equivalent machine-readable marking on AI-generated media
- No AI-generated content injected into DOM via `.innerHTML` or `dangerouslySetInnerHTML`; DOMPurify + Trusted Types sanitization applied
- Component Registry pattern used for any agent-rendered structured output; no arbitrary JSX/HTML from agents
- HITL `<AgentActionApprovalModal>` in place for all agent-triggered irreversible mutations
- AI provider APIs not called directly from frontend; all LLM calls routed through backend proxy

### WCAG 2.2 AA Compliance (when AI features or streaming UI is in scope)
- `aria-live="polite"` + `role="log"` on all streaming AI response containers
- Focus management implemented after agent-triggered DOM modifications
- Interactive targets (AI input areas, send buttons, action chips) ≥ 24×24px (WCAG 2.5.8)
- Sticky headers, overlays, and chat widgets do not fully cover focused elements; scroll-margin-top CSS property applied (WCAG 2.4.11)
- Drag-and-drop interactions have single-pointer alternative (WCAG 2.5.7)
- Multi-step flows auto-populate previously entered data (WCAG 3.3.7)
- Authentication does not require cognitive function tests; CAPTCHA choice is compliant (WCAG 3.3.8)
