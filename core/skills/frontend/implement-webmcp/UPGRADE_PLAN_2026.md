# implement-webmcp — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### WebMCP Evolution (2026)
- **Feature detection mandatory**: `'modelContext' in document` guards for SSR/polyfilled environments
- **State synchronization**: Critical app state (Redux/Zustand) exposed securely; sensitive fields stripped
- **Action allowlist (default deny)**: Explicit allowlist of browser actions (clicks, navigation, form fills); reject tools not on allowlist
- **Strict input schema validation**: Every tool declares explicit property types, enums, required fields; empty `{ type: "object" }` prohibited
- **Security context**: Agent operates within user's authenticated session; HttpOnly cookies not exposed to JS runtime
- **User consent gate (HITL)**: Non-idempotent/financial actions require explicit user confirmation; fail-safe on dismiss/timeout
- **Background sync**: Service Workers + Push API for async HITL callbacks
- **Structured error payloads**: `{ error: { code: 'OUT_OF_STOCK', message: '...' } }` — never raw stack traces

### MCP Ecosystem Integration (2026)
- **MCP Registry**: External tools via MCP Registry for developer workflows
- **Browser-side + backend MCP coordination**: `configure-mcp` skill for cross-environment coordination
- **WebMCP provider in root layout**: Global mount with SSR safety guards
- **Sanitized state mapping**: Reactive UI state (route, entity ID, filtered view) with sensitive field filtering

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| Feature detection mentioned | **Feature detection mandatory**: `'modelContext' in document` guards for SSR safety |
| State synchronization mentioned | **Sanitized state mapping**: Reactive UI state with sensitive field filtering before `provideContext()` |
| Action allowlist mentioned | **Default deny allowlist**: Explicit registration required; runtime broadening rejected |
| Input schema validation | **Strict schema mandatory**: Explicit property types, enums, required fields; empty object prohibited |
| Security context mentioned | **HttpOnly cookie isolation**: Auth tokens/cookies stay outside JS runtime WebMCP can read |
| HITL consent gate | **Mandatory for non-idempotent/financial**: Explicit confirmation modal; fail-safe on dismiss/timeout |
| Background sync mentioned | **Service Workers + Push API**: Async HITL callbacks for agent-user communication |
| Structured error payloads | **Error codes mandatory**: `{ error: { code, message } }`; raw stack traces prohibited |

### 2. New 2026 Patterns to Add
- **WebMCP Provider SSR Safety**: Mount in global root layout (`layout.tsx`, `Layout.astro`) with client-side execution guards
- **Reactive State Subscription**: Subscribe to route changes, active entity, filtered views; emit context on transitions
- **Action Allowlist Governance**: Allowlist as code (not config); every action requires security review
- **HITL Modal Component**: Reusable confirmation modal with timeout, dismiss handling, visual agent activity indicator
- **Service Worker HITL Bridge**: Push API for background agent callbacks; offline queue for confirmations
- **MCP Registry Coordination**: Backend MCP server cards registered; browser WebMCP discovers via registry
- **Permission Parity Enforcement**: Agent actions cannot bypass UI permission rules; same guards as UI

### 3. Checklist Additions
- [ ] WebMCP provider mounted in global root layout with SSR safety guards (`'modelContext' in document`)
- [ ] Sanitized application state mapped to agent context (no credentials, tokens, PII)
- [ ] Client-side actions and input schemas explicitly defined and registered (allowlist as code)
- [ ] Security boundaries and permission checks enforced on all action handlers
- [ ] HITL confirmation modal wired for destructive/financial actions (fail-safe on dismiss/timeout)
- [ ] Service Worker event listeners registered for push notifications/background sync
- [ ] Visual indicator when agent actively reading context or performing actions
- [ ] Component and integration tests for context emission and action execution
- [ ] MCP Registry coordination with backend server cards
- [ ] Permission parity: agent actions cannot bypass UI permission rules
- [ ] Structured error responses with codes (never raw stack traces)
- [ ] `implementation-result.json` emitted with action allowlist and validation run

### 4. Failure Mode Additions
- **SSR hydration breakage**: WebMCP provider runs server-side. Mitigation: Client-side execution guards; mount only in global root layout.
- **Action allowlist too broad**: Action added without security review. Mitigation: Default deny; explicit allowlist registration required.
- **Empty input schema**: Tool registered with `{ type: "object" }` no properties. Mitigation: Enforce explicit property types, enums, required fields.
- **Sensitive state exposed**: Passwords/tokens/PII in WebMCP context. Mitigation: Filter before `provideContext()`; never expose HttpOnly cookies.
- **No HITL gate on financial action**: Payment/account-modification runs without confirmation. Mitigation: Require HITL modal; fail-safe on dismiss/timeout.
- **Raw stack trace in error**: Server stack trace exposed. Mitigation: Structured JSON error responses with codes.
- **Browser feature not detected**: Assumes `'modelContext' in navigator` always true. Mitigation: Feature-detect with `in document`; polyfill bridge fallback.
- **Agent bypasses UI permissions**: Agent triggers transaction user couldn't via UI. Mitigation: Enforce same permission rules; reject bypassed paths.
- **Service Worker HITL failure**: Push notification not delivered. Mitigation: Fallback to in-app modal; offline queue for confirmations.

### 5. Output Contract Updates
- Update `contracts/schemas/implementation-result.json` with: action allowlist, sanitized state fields, HITL flow, WebMCP connection validation

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | WebMCP provider SSR safety guards (`'modelContext' in document`) | High |
| P0 | Default deny action allowlist with explicit registration | High |
| P0 | Strict input schema validation (explicit types, enums, required) | High |
| P0 | HITL confirmation gate for non-idempotent/financial actions | High |
| P1 | Sanitized reactive state mapping with sensitive field filtering | Medium |
| P1 | Service Worker + Push API for async HITL callbacks | Medium |
| P1 | MCP Registry coordination with backend cards | Medium |
| P1 | Permission parity enforcement (agent = UI permissions) | Medium |
| P1 | Structured error payloads with codes | Medium |
| P2 | Visual agent activity indicator | Low |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test WebMCP provider SSR safety (no hydration breakage)
- Verify action allowlist default deny blocks unregistered actions
- Test input schema validation rejects empty `{ type: "object" }`
- Test HITL modal blocks financial action without confirmation
- Test fail-safe on HITL dismiss/timeout
- Verify sensitive fields filtered from `provideContext()`
- Test Service Worker HITL bridge with push notifications
- Test MCP Registry discovery of backend cards
- Verify agent actions respect UI permission boundaries
- Verify structured error responses (no raw stack traces)