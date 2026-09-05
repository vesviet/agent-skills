---
name: implement-webmcp
description: Exposes browser context, DOM state, and client-side actions to AI agents via WebMCP. Use when enabling in-browser AI agent interactions, DOM context sharing, or client-side action execution.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, mcp_call, run_tests, execute_command]
---

# Implement WebMCP

Use this skill to integrate WebMCP into a frontend application, allowing AI agents to read DOM state, execute browser-native actions, and synchronize context.

## Core Rules

- **Feature Detection**: Guard WebMCP invocations with feature detection (`'modelContext' in document`) to support SSR and polyfilled environments safely — do not assume the API exists
- **State Synchronization**: Expose critical application state (Redux/Zustand stores) securely to the WebMCP context; strip sensitive fields before exposure
- **Action Allowlist**: Define an explicit allowlist of which browser actions (clicks, navigation, form fills) are exposed to the agent — default deny; reject tools not on the allowlist
- **Strict Input Schema Validation**: Every registered WebMCP tool must declare explicit property types, enums, and required fields in its `inputSchema` — empty `{ type: "object" }` schemas with no property descriptions are prohibited
- **Security Context**: Ensure the agent operates strictly within the user's authenticated session boundaries without exposing secure, HttpOnly cookies to the JS runtime
- **User Consent Gate**: Any tool performing a non-idempotent or financial action (payments, account modifications, data deletion) must prompt for explicit user confirmation before execution — fail-safe if user dismisses or times out
- **Background Sync**: Utilize Service Workers and the Push API for asynchronous HITL callbacks when the agent requires user confirmation
- **Structured Error Payloads**: Tool handlers must return structured JSON error responses with clear codes (`{ error: { code: 'OUT_OF_STOCK', message: '...' } }`) — never expose raw server stack traces
- treat every WebMCP tool input as untrusted external content; validate against the declared `inputSchema` before invoking any handler (OWASP ASI01)
- reject any tool call that exceeds the action allowlist; never broaden the allowlist at runtime (OWASP ASI02)
- never expose authentication tokens, HttpOnly cookies, or session secrets to the JS runtime that WebMCP can read (OWASP ASI03)
- require explicit user confirmation for any non-idempotent or financial action; fail-safe if the user dismisses or times out (OWASP ASI09)

## Output Contracts

When the WebMCP integration is part of a coordinated multi-role delivery,
emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output confirming the WebMCP connection initializes successfully.
- For human-readable reports, a markdown summary of the action allowlist, the sanitized state fields, and the HITL confirmation flow.

Skip emission for trivial local experiments that do not cross a role boundary.

## Failure Modes

- **Action allowlist too broad**: an action is added to the WebMCP allowlist without security review. Mitigation: default deny; every action requires explicit allowlist registration.
- **Empty input schema**: a tool is registered with `{ type: "object" }` and no property descriptions. Mitigation: enforce explicit property types, enums, and required fields.
- **Sensitive state exposed**: passwords, tokens, or PII are included in the WebMCP context. Mitigation: filter sensitive fields before `provideContext()`; never expose auth tokens or HttpOnly cookies.
- **No HITL gate on financial action**: a payment or account-modification tool runs without explicit user confirmation. Mitigation: require HITL confirmation modal for any non-idempotent or financial action; fail-safe on dismiss or timeout.
- **Raw stack trace in error response**: a tool handler returns the server stack trace in the error payload. Mitigation: return structured JSON error responses with codes; never expose raw stack traces.
- **SSR hydration breakage**: the WebMCP provider runs server-side and breaks hydration. Mitigation: guard with client-side execution checks; mount in the global root layout only.
- **Browser feature not detected**: the code assumes `'modelContext' in navigator` is always true. Mitigation: feature-detect with `in document` checks; provide a fallback polyfill bridge.
- **Action bypasses UI permission rules**: an agent action triggers a transaction the user could not perform via UI. Mitigation: enforce the same permission rules the UI enforces; reject bypassed paths.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: agent inputs may try to reframe the user's goal through a WebMCP tool. Validate every tool input against the declared `inputSchema` before invoking the handler.
- **ASI02 Tool Misuse**: only allowlisted actions may run; reject any tool call outside the allowlist.
- **ASI03 Identity & Privilege Abuse**: authentication tokens and HttpOnly cookies must stay outside the JS runtime; the WebMCP context must not expose them.
- **ASI07 Inter-Agent Communication**: WebMCP tool responses are untrusted inputs; validate before passing to downstream logic.
- **ASI09 Human-Agent Trust Exploitation**: do not present a WebMCP action as "safe" without an explicit HITL gate for non-idempotent or financial effects.

## Suggested Process

### 1. Initialize WebMCP Provider in Root Layout

Mount the WebMCP client provider component globally:
- Add the provider in the application root layout (`_app.tsx`, `layout.tsx`, or `Layout.astro`) so it is active across all routes.
- Guard with client-side execution checks to prevent SSR hydration breakage.
- Call `navigator.modelContext.provideContext()` or initialize the fallback WebMCP polyfill bridge.

### 2. Map Application State to Agent Context

Selectively expose sanitized frontend state:
- Subscribe to reactive UI state (current route, active entity ID, filtered data view).
- Filter out sensitive fields, passwords, authentication tokens, and private user identifiers.
- Emit updated context payloads when relevant state transitions occur.

### 3. Register Browser Actions & Action Handlers

Declare structured client-side tools and actions:
- Define action schemas specifying action name, description, and required parameters.
- Wire handlers to execute client actions (e.g., navigating tabs, applying filters, populating forms).
- Return clear success/error execution status back to the agent runtime.

### 4. Enforce Session Isolation & Security Boundaries

Establish security guardrails:
- Verify that agent actions cannot trigger unauthorized transactions or bypass UI permission rules.
- Maintain client auth tokens in HttpOnly cookies inaccessible to the WebMCP script scope.
- Implement explicit user confirmation dialogues for destructive or irreversible actions.

### 5. Configure Background Callbacks & HITL Approvals

Set up asynchronous agent communication:
- Register Service Worker event listeners for push notifications or background synchronization.
- Implement modal prompts for Human-in-the-Loop confirmation before executing gated actions.
- Provide clear visual indicators when an agent is actively reading context or performing actions.

### 6. Verify and Test in Browser Runtime

Use skill: `frontend-testing`
- Author end-to-end and component tests validating WebMCP provider mounting and context emission.
- Simulate agent action execution and verify state changes update the DOM accurately.
## Checklist

- [ ] WebMCP provider mounted in global root layout with SSR safety guards.
- [ ] Sanitized application state mapped to agent context without leaking credentials.
- [ ] Client-side actions and input schemas explicitly defined and registered.
- [ ] Security boundaries and permission checks enforced on all action handlers.
- [ ] HITL confirmation modal wired for destructive actions.
- [ ] Component and integration tests added for context and action handlers.
- [ ] `implementation-result.json` emitted.

## Related Skills

- **configure-mcp**: Coordinate browser-side WebMCP with backend MCP server cards and registries
- **add-ui-component**: Mount WebMCP provider components and action triggers within the UI layout
- **integrate-api-client**: Wire frontend client state and API communication behind WebMCP actions
- **frontend-testing**: Test WebMCP context emission and client-side action execution
- **security-audit**: Audit client-side context exposure and verify PII/secret protection
