# Orval, TanStack Query v5, and Streaming API Specifications (2026)

## 1. OpenAPI Codegen Pipeline with Orval

### 1.1 Automated Type & Hook Generation
Manual API client writing introduces contract drift between backend protobuf/OpenAPI schemas and frontend client code:
- **Orval Automation**: Convert OpenAPI v3.1 / RFC 9727 specs into typed TanStack Query v5 hooks, MSW v2 mock handlers, and TypeScript types.
- **Drift Detection**: CI runs Orval verification to ensure committed client code strictly matches current API specifications:
  ```bash
  orval --config orval.config.ts --mode check
  ```

---

## 2. Centralized `queryOptions` Factories

### 2.1 Eliminating Magic String Query Keys
- All TanStack Query hooks must be configured using query option factories rather than scattered query key arrays:
  ```typescript
  import { queryOptions } from '@tanstack/react-query';

  export const userQueries = {
    all: () => ['users'] as const,
    detail: (userId: string) =>
      queryOptions({
        queryKey: [...userQueries.all(), userId],
        queryFn: () => fetchUser(userId),
        staleTime: 1000 * 60 * 5, // 5 minutes
      }),
  };
  ```

---

## 3. Optimistic Mutation Lifecycle

### 3.1 Three-Phase Rollback Pattern
Optimistic UI updates must guarantee atomic recovery on backend failures:
1. **`onMutate`**:
   - Cancel outstanding in-flight queries: `await queryClient.cancelQueries({ queryKey })`.
   - Capture current cache snapshot: `const previous = queryClient.getQueryData(queryKey)`.
   - Apply optimistic update using functional updater: `queryClient.setQueryData(queryKey, (old) => ...)`.
   - Return context containing previous snapshot.
2. **`onError`**:
   - Restore previous state from context: `queryClient.setQueryData(queryKey, context.previous)`.
3. **`onSettled`**:
   - Invalidate cache to reconcile with authoritative server state: `queryClient.invalidateQueries({ queryKey })`.

---

## 4. Streaming AI Responses (SSE & Chunked Fetch)

### 4.1 Token Chunking & State Batching
Streaming LLM completions must not trigger re-render storms:
- Pipe response body through `TextDecoderStream`.
- Process incoming Server-Sent Events (SSE) chunks via a `useReducer` action queue or batched `React.startTransition()` callbacks.
- Wire an `AbortController` signal to allow instantaneous user cancellation.
