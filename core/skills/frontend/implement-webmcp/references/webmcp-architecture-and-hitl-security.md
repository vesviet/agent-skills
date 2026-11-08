# WebMCP Architecture & Human-in-the-Loop (HITL) Security Standards (2026)

## 1. WebMCP Runtime Architecture & SSR Safety

### 1.1 In-Browser Model Context Protocol (WebMCP)
WebMCP bridges in-browser AI assistants directly to the Document Object Model (DOM), client-side store state, and registered browser action tools:
- **Feature Detection Guard**: Never access `document.modelContext` directly during server-side rendering or before DOM hydration:
  ```typescript
  export function isWebMcpAvailable(): boolean {
    return typeof window !== 'undefined' && 'modelContext' in document;
  }
  ```
- **Session Boundary Security**: WebMCP operates exclusively within the client execution sandbox. Secret tokens, refresh tokens, and authentication cookies must reside in `HttpOnly; Secure; SameSite=Strict` cookies, remaining completely inaccessible to client JavaScript.

---

## 2. Sanitized State Mapping & Context Injection

### 2.1 PII & Secret Scrubbing
Before synchronizing client application stores (Zustand, Redux, React Context) to the agent context buffer, execute deterministic field stripping:
- **Forbidden Context Fields**: `password`, `ssn`, `accessToken`, `refreshToken`, `apiKey`, `creditCard`, `cvv`.
- **Sanitized Projection**:
  ```typescript
  export function sanitizeStoreState(state: Record<string, unknown>): Record<string, unknown> {
    const sanitized = { ...state };
    const restrictedKeys = ['auth', 'session', 'tokens', 'billingSecret'];
    restrictedKeys.forEach((key) => delete sanitized[key]);
    return sanitized;
  }
  ```

---

## 3. Tool Registration & Default-Deny Allowlist

### 3.1 Strict Input Schema Declaration
Every registered client tool must declare concrete JSON Schema validation rules. Open `{ type: "object" }` declarations without explicit properties are rejected:
- Declare required fields, parameter ranges, and enum constraints.
- Tool handlers execute only after input parameters pass local validation.

---

## 4. Human-in-the-Loop (HITL) Approval Gate

### 4.1 Non-Idempotent & High-Risk Actions
Any action mutating persistent backend state, modifying billing details, or deleting data requires explicit user confirmation:
- **Fail-Safe Timeout**: If the user dismisses the approval dialog or fails to respond within 60 seconds ($T_{timeout} = 60\text{s}$), the action is automatically rejected with error code `USER_CONSENT_TIMEOUT`.
- **Visual Activity Beacon**: Display a persistent visual badge when an AI agent is reading DOM context or executing allowlisted actions.
