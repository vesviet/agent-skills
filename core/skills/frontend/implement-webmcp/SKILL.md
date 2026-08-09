---
name: implement-webmcp
description: Set up WebMCP to expose browser context, DOM state, and client-side actions to AI agents.
---

# Implement WebMCP

Use this skill to integrate WebMCP into a frontend application, allowing AI agents to read DOM state, execute browser-native actions, and synchronize context.

## Core Rules
- **State Synchronization**: Expose critical application state (Redux/Zustand stores) securely to the WebMCP context.
- **Action Scoping**: Define explicitly which browser actions (clicks, navigation, form fills) are exposed to the agent.
- **Security Context**: Ensure the agent operates strictly within the user's authenticated session boundaries without exposing secure, HttpOnly cookies to the JS runtime.
- **Background Sync**: Utilize Service Workers and the Push API for asynchronous HITL (Human-in-the-Loop) callbacks when the agent requires user confirmation.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output confirming the WebMCP connection initializes successfully.

## Checklist
- [ ] WebMCP library integrated into the client bundle.
- [ ] Context synchronization configured for relevant UI state.
- [ ] Permitted actions strictly scoped and defined.
- [ ] Background sync configured for agent callbacks.
- [ ] `implementation-result.json` emitted.
