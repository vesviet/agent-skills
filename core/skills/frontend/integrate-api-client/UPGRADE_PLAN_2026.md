# integrate-api-client — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### OpenAPI Codegen Pipeline (2026)
- **Orval as standard**: Automatically converts OpenAPI specs → TanStack Query v5 queries, MSW v2 mocks, TypeScript types
- **`queryOptions` factories**: Reusable, type-safe query configurations across components
- **MSW mocks auto-updated**: In test and dev environments when schemas change
- **Generated types as source of truth**: No manual type definitions for API contracts

### React 19 Data Fetching (2026)
- **`use()` hook for RSC**: Read promises directly in Server-rendered components; facilitates RSC streaming and lazy data resolution
- **TanStack Query for client-side**: Interactive operations requiring cache invalidation, background refetching, request deduplication
- **Avoid nesting client query hooks**: When RSC streaming resolves initial page load data
- **Server Components + TanStack Query hybrid**: RSC for initial data, TanStack Query for interactivity

### React 19 Mutations (2026)
- **`useActionState` for forms**: Straightforward form actions and state updates with pending state, error handling
- **`useMutation` (TanStack Query) for complex**: Advanced cache manipulation, pagination updates, optimistic UI
- **Validation error binding**: Action errors correctly bound back to UI inputs

### Streaming AI Responses (2026)
- **`ReadableStream` + `TextDecoderStream`**: Parse chunked responses token-by-token
- **`useReducer` pattern**: Avoid unnecessary re-renders during rapid stream updates
- **Cancellation hooks**: Allow users to abort active stream requests

### TanStack Query v5 Patterns (2026)
- **Centralized `queryOptions` factories**: Scattered magic string query keys are anti-pattern
- **Optimistic mutations full lifecycle**: `onMutate` (cancel + snapshot + update), `onError` (rollback), `onSettled` (invalidate) — no rollback handlers = prohibited
- **Functional updater syntax**: `setQueryData((old) => ...)` to prevent stale state captures
- **Server state in query cache only**: Never duplicate in local `useState`

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| OpenAPI codegen mentioned | **Orval pipeline mandatory**: OpenAPI → TanStack Query v5 + MSW v2 + TS types; `queryOptions` factories |
| React 19 `use()` mentioned | **`use()` for RSC streaming**: Read promises in Server Components; TanStack Query for client interactivity |
| React 19 `useActionState` mentioned | **`useActionState` for forms**: Pending state, error handling, progressive enhancement |
| `useMutation` for complex | **`useMutation` only for complex**: Cache manipulation, pagination, optimistic UI; simple forms → `useActionState` |
| Streaming AI responses | **`ReadableStream` + `useReducer`**: Token-by-token updates, cancellation hooks |
| TanStack Query v5 `queryOptions` | **Centralized factories mandatory**: No scattered magic string keys |

### 2. New 2026 Patterns to Add
- **Orval Configuration**: OpenAPI spec → TanStack Query v5 hooks + MSW v2 handlers + TS types in single pipeline
- **`queryOptions` Factory Pattern**: Reusable query configs with `queryKey`, `queryFn`, `staleTime`, `gcTime`
- **RSC + TanStack Query Hybrid**: Server Components for initial data (`use()`), client components for interactivity
- **React 19 `useActionState` Form Pattern**: `<form action={submitAction}>`, automatic reset, progressive enhancement
- **Streaming Response Handler**: `ReadableStream` → `TextDecoderStream` → `useReducer` for token-by-token UI
- **Cancellation Infrastructure**: `AbortController` integration for stream cancellation
- **Optimistic Mutation Guard**: Lint rule requiring `onError` rollback for every `useMutation`

### 3. Checklist Additions
- [ ] Orval configured for OpenAPI → TanStack Query v5 + MSW v2 + TS types
- [ ] `queryOptions` factories used for all query configurations (no magic string keys)
- [ ] React 19 `use()` used in Server Components for initial data fetching
- [ ] TanStack Query v5 used for client-side interactivity (cache invalidation, refetching, deduplication)
- [ ] Simple form mutations use `useActionState` with `<form action={submitAction}>`
- [ ] Complex mutations use `useMutation` with full optimistic lifecycle (`onMutate`/`onError`/`onSettled`)
- [ ] Functional updater syntax: `setQueryData((old) => ...)` — no stale captures
- [ ] Server state stays in query cache; no `useState` duplication
- [ ] Streaming AI responses: `ReadableStream` + `TextDecoderStream` + `useReducer`
- [ ] Cancellation hooks for active streams (`AbortController`)
- [ ] Validation errors from actions bound to UI inputs
- [ ] MSW v2 mocks auto-generated and updated with Orval pipeline
- [ ] Idempotency keys on every non-idempotent mutation (POST/DELETE)
- [ ] Explicit error code handling (4xx vs 5xx differentiated)
- [ ] `implementation-result.json` emitted

### 4. Failure Mode Additions
- **Orval spec drift**: OpenAPI spec changes but generated code not updated. Mitigation: CI step running Orval; fail if generated code differs from committed.
- **RSC/TanStack Query boundary confusion**: Client query hooks nested in Server Components. Mitigation: Lint rule banning `useQuery` in `"use client"` components that are RSC children; use `use()` in RSC.
- **`useActionState` for complex mutations**: Simple form hook used for paginated cache updates. Mitigation: Lint rule: `useActionState` only for forms; `useMutation` for cache manipulation.
- **Streaming re-render storm**: `useState` updated per token. Mitigation: `useReducer` pattern; batch updates; `React.startTransition` for non-urgent.
- **Missing cancellation**: User cannot abort slow AI stream. Mitigation: `AbortController` wired to cancel button; cleanup on unmount.
- **Stale state capture**: `setQueryData(newData)` captures stale closure. Mitigation: Functional updater `setQueryData((old) => ...)` mandatory.
- **MSW mock divergence**: Mocks not updated with schema changes. Mitigation: Orval generates MSW handlers; CI verifies mocks match spec.

### 5. Output Contract Updates
- Update `contracts/schemas/implementation-result.json` with: Orval config, `queryOptions` factories, RSC/Client boundary, streaming handler, cancellation infrastructure

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Orval pipeline: OpenAPI → TanStack Query v5 + MSW v2 + TS types | High |
| P0 | Centralized `queryOptions` factories (no magic string keys) | High |
| P0 | React 19 `use()` in RSC for initial data | High |
| P0 | `useActionState` for forms + `useMutation` for complex | High |
| P0 | Streaming AI responses: `ReadableStream` + `useReducer` + cancellation | High |
| P1 | Functional updater syntax enforcement (`setQueryData((old) => ...)`) | Medium |
| P1 | Optimistic mutation full lifecycle guard (lint rule) | Medium |
| P1 | RSC + TanStack Query hybrid pattern documentation | Medium |
| P2 | Idempotency keys on non-idempotent mutations | Low |
| P2 | Explicit error code handling (4xx vs 5xx) | Low |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test Orval generates identical code on CI (fail on drift)
- Verify `queryOptions` factories used (grep for magic string query keys)
- Test React 19 `use()` in Server Component with streaming data
- Test `useActionState` form with Server Function (progressive enhancement)
- Test streaming AI response with `useReducer` — no re-render storm
- Test cancellation via `AbortController` on active stream
- Verify functional updater syntax (no stale captures)
- Test MSW v2 mocks match OpenAPI spec
- Verify idempotency keys on POST/DELETE mutations