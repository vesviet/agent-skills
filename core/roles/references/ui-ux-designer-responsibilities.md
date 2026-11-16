# ui-ux-designer.md - Domain UX, AI Interaction & Living Design System Responsibilities

This reference supplements [`core/roles/ui-ux-designer.md`](../ui-ux-designer.md) with operational patterns for Product UX architecture, AI/Agentic UX, GenUI governance, and Two-Tier living design systems.

---

## 1. Product UI Architecture & Interaction Patterns (Mode A)

### 1.1 Surface Selection Matrix

| User Need | Recommended Surface | Key UX Invariant |
| :--- | :--- | :--- |
| Single field or inline status edit | **Inline edit** | Explicit save/cancel or optimistic update + undo toast; preserve scroll position |
| Quick filter, sort, or single contextual control | **Popover** | Non-modal or light-dismiss; never pack multi-step forms inside a popover |
| Secondary record inspection or multi-field edit from a list | **Drawer / Sheet** | Preserve parent list context; persist open ID in URL `?selected=` when shareable; `overscroll-behavior: contain` |
| Focused confirmation or short blocking decision | **Modal Dialog** | Focus trap, `Esc` to close, restore focus to triggering element on close, never nest modals |
| Deep workflow, multi-step wizard, or primary workspace | **Dedicated Route** | Clean URL state (`?tab=`, `?filter=`, `?page=`), browser back/forward safe, clear breadcrumb/exit |

### 1.2 Destructive Action & Feedback Matrix

| Reversibility / Blast Radius | Feedback Pattern | Requirement |
| :--- | :--- | :--- |
| **Low-risk reversible** (archive, reorder, toggle) | Optimistic UI + **Undo Toast** | Immediate visual feedback; single-click `Undo` window; no blocking modal |
| **Medium-risk scoped delete** (delete item, revoke token) | **Named Confirmation Dialog** | State exact object name & consequence; confirm button names action (`Delete Project`), never generic `OK`/`Yes`; default focus on safe action |
| **Irreversible / destructive tenant action** (drop workspace, billing cancel) | **Typed Confirmation + Consequence Summary** | Require typing resource slug; zero dark-pattern obstruction (DSA Art 25/26) |

### 1.3 Data-Dense & Table Ergonomics

- Numeric, currency, timestamp, and delta columns MUST specify `font-variant-numeric: tabular-nums`.
- Tables with vertical scroll MUST pin `thead` (`sticky top-0`) and reserve `scroll-margin-top` for anchor jumps.
- Truncated text (`text-ellipsis`) MUST provide a keyboard-accessible full-value reveal (tooltip, popover, or detail view).
- Filter/sort/tab states SHOULD serialize to URL query params (URL-as-state) so views survive refresh and sharing.

---

## 2. AI Interaction Design (Probabilistic Systems)

AI features produce non-deterministic, sometimes wrong outputs. Designing only the happy path is a specification failure.

### 2.1 Five Mandatory AI States

| State | Meaning | Design Requirement |
| :--- | :--- | :--- |
| **Generating / Thinking** | Model processing; output incomplete | Geometry-matched skeleton or streaming container; latency expectation; abort/stop control |
| **Uncertain** | Output produced with low/medium confidence | Confidence indicator + calibrated copy (`"Suggested"`, `"Likely"`, `"Unverified"`) |
| **Fallback (Red Path)** | AI failed, timed out, or refused | Factual degradation message (no `!`) + deterministic alternative (manual input, search, retry) |
| **Overridden** | User edited or rejected AI output | UI preserves human edit; never silently re-applies overwritten AI output |
| **Corrected** | User submitted feedback/correction | Subtle confirmation (`"Feedback recorded"`) |

### 2.2 Confidence, Transparency & Article 50

- Pair any `"AI-generated"` label with a confidence signal or provenance hook (`"Why am I seeing this?"` + source citations via progressive disclosure).
- **Preview-before-apply**: consequential AI actions (send, pay, publish, delete, bulk-mutate) require explicit diff/action preview before execution.
- **EU AI Act Article 50 (live 2 August 2026)**: render a visible, accessible `<AIDisclosureBanner>` before or during the first meaningful interaction; specify C2PA content credentials for AI-generated media (2 December 2026).
- **AI Accessibility**: specify `aria-live="polite"` (or `role="log"`) for streaming text without stealing focus; provide context-aware alt-text rules for AI media.
- **HITL Reviewer Interface**: when BA specifies a confidence escalation trigger, design the reviewer surface (AI output, confidence, input context, audit preview, Confirm/Edit/Reject actions, and SLA-expiry state).

---

## 3. Agentic UX & Trust Ladder

| Tier | Autonomy Scope | Mandatory UX Requirement |
| :--- | :--- | :--- |
| **Suggest** | Agent proposes; human initiates | Full preview before side effect; one-click dismiss |
| **Verify** | Agent prepares; human confirms per action | Consequence preview + one-click confirm + visible undo |
| **Delegate** | Agent acts within bounds; human audits outcomes | Outcome summary + accessible audit trail + exception alerts |
| **Automate** | Agent runs autonomously; human monitors exceptions | Mandatory status surface + always-accessible pause/interrupt + exception notifications |

- Declare `agentic_autonomy.autonomy_tier` in `ux-flow-spec.json` and surface the active tier in the UI.
- Never ship `Automate` before `Suggest -> Verify` trust is earned (**Autopilot Trap**).
- Background agents MUST specify four async surfaces: **status surface**, **notification contract**, **async interrupt UX** (pause/redirect/cancel), and **completion handoff**.
- **Agents-as-Users (`agent_operability`)**: when browser agents operate the UI alongside humans, declare `agent_entry_points`, semantic ARIA affordances / WebMCP hooks (`implement-webmcp`), and `agent_courtesy_rules` (rate limits, idempotency).

---

## 4. GenUI Component Governance

When AI dynamically assembles UI at runtime:

- **Stateless MCP 2026-07-28 Alignment**: design component registries for stateless HTTP transport with externalized state (Redis, Durable Objects, D1), never assuming sticky in-memory MCP sessions.
- **Component Palette Allowlist**: explicitly list allowed design-system components, allowed states, and prohibited combinations.
- **Drift Detection & Deterministic Fallback**: validate assembled trees against the palette and semantic rules; render a deterministic safe fallback when assembly violates bounds.

---

## 5. Living Design System Infrastructure (`DESIGN.md` MASTER + Page Overrides)

### 5.1 Two-Tier Token Architecture (with Constrained Exceptions)

| Tier | Type | Example | Rule |
| :--- | :--- | :--- | :--- |
| **Tier 1: Primitive** | Raw OKLCH / scale value | `--slate-900`, `--space-4`, `--duration-150` | Palette definition only; **forbidden** directly in component specs |
| **Tier 2: Semantic** | Functional intent | `--surface-canvas`, `--text-primary`, `--border-subtle` | **Authoritative design-to-code contract** across light/dark/high-contrast themes |
| **Tier 3: Component** | Exception override | `--button-height-compact` | Strictly optional (`<= 3` per component); excess indicates missing semantic tokens |

### 5.2 Master + Page Override Pattern & DTCG 2025.10

- Author `DESIGN.md` (backed by `contracts/schemas/design-tokens-spec.json`) as the single **MASTER** token & visual contract for the project.
- When individual routes require contextual overrides (e.g., high-density telemetry view vs onboarding flow), document explicit **Page Overrides** layered on top of `MASTER` without forking primitive ramps or duplicating theme files.
- All token interchange uses **W3C DTCG Format Module 2025.10** (`$value` / `$type`), synced via automated pipeline (`DESIGN.md` / Figma Variables -> PR -> Style Dictionary v4 DTCG mode / Terrazzo) — never manual copy-paste.
- Author token docs in clean Markdown hierarchy (`H1 -> H2 -> H3`) for dual human/LLM consumption (`llms.txt` as doc scope map only, never as a search-ranking or WebMCP replacement).

Last updated: 2026-11-16
