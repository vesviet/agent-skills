---
name: implement-webmcp
description: Exposes browser context, DOM state, and client-side actions to AI agents via WebMCP. Use when enabling in-browser AI agent interactions, DOM context sharing, or client-side action execution.
---

# Implement WebMCP

Use this skill to integrate WebMCP into a frontend application, allowing AI agents to read DOM state, execute browser-native actions, and synchronize context.

## Core Rules

- **State Synchronization**: Expose critical application state (Redux/Zustand stores) securely to the WebMCP context.
- **Action Scoping**: Define explicitly which browser actions (clicks, navigation, form fills) are exposed to the agent.
- **Security Context**: Ensure the agent operates strictly within the user's authenticated session boundaries without exposing secure, HttpOnly cookies to the JS runtime.
- **Background Sync**: Utilize Service Workers and the Push API for asynchronous HITL (Human-in-the-Loop) callbacks when the agent requires user confirmation.
- **Feature Detection**: Guard WebMCP invocations with feature detection (`typeof window !== 'undefined'` and check `navigator.modelContext`) to support SSR and polyfilled environments safely.

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

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output confirming the WebMCP connection initializes successfully.

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
