# Authentication Flows, Session Specifications, and Multi-Tenant Isolation

This reference guide details production-grade architecture patterns, cryptographic protocols, data models, and runtime isolation techniques for modern backend systems.

---

## 1. OAuth2 PKCE Architecture (RFC 7636 / OAuth 2.1)

### 1.1 PKCE Handshake Mechanics

Standard Authorization Code grant flows are vulnerable to authorization code interception on public clients (single-page applications, mobile applications, native desktop clients) where client secrets cannot be securely stored. Proof Key for Code Exchange (PKCE) mitigates this by binding authorization code issuance to a dynamic, client-generated cryptographic secret.

```
+----------------+                      +--------------------+
|  Client (SPA/  |                      | Authorization      |
|  Mobile/Agent) |                      | Server (AS)        |
+----------------+                      +--------------------+
       |                                          |
       | 1. Generate code_verifier (43-128 chars) |
       | 2. Compute code_challenge = S256(verifier)
       |                                          |
       | 3. GET /authorize?code_challenge=...     |
       |    &code_challenge_method=S256           |
       |----------------------------------------->|
       |                                          | 4. User Authenticates & Consents
       |                                          | 5. Store code_challenge with code
       | 6. Redirect with authorization_code      |
       |<-----------------------------------------|
       |                                          |
       | 7. POST /oauth/v2/token                  |
       |    code=... & code_verifier=...          |
       |----------------------------------------->|
       |                                          | 8. Verify S256(verifier) == challenge
       |                                          | 9. Invalidate authorization_code
       | 10. Return Access Token & Refresh Token  |
       |<-----------------------------------------|
```

### 1.2 Cryptographic Invariants
1. **Code Verifier**:
   - High-entropy cryptographic string using unreserved URI characters: `[A-Z]`, `[a-z]`, `[0-9]`, `-`, `.`, `_`, `~`.
   - Length: Minimum 43 characters; maximum 128 characters ($\ge 256$ bits of entropy).
   - Generated using a cryptographically secure pseudorandom number generator (CSPRNG).
2. **Code Challenge**:
   - Transformed representation: `code_challenge = BASE64URL-ENCODE(SHA256(code_verifier))`.
   - The `code_challenge_method` MUST be set to `S256`. The legacy `plain` transformation is strictly prohibited.
3. **Single-Use Authorization Code & Replay Defense**:
   - An authorization code must expire within 60 seconds (recommended: 30 seconds).
   - Once presented, the authorization server must immediately invalidate the authorization code.
   - If an authorization code is presented more than once, the server MUST treat the event as an intrusion: reject the exchange and revoke all access and refresh tokens previously issued under that code.

---

## 2. Session Lifecycle & Multi-Device Management

### 2.1 Dual-Timeout Expiration Architecture

To balance user convenience with tight security bounds, user sessions must enforce two independent temporal limits:

1. **Sliding Inactivity Window (Idle Timeout)**:
   - Typical duration: 15 to 30 minutes.
   - Each authenticated user request extends the session's validity by the idle window:
     $$\text{expires\_at} = \min(\text{now}() + \text{idle\_timeout}, \text{created\_at} + \text{absolute\_timeout})$$
2. **Absolute Session Ceiling (Hard Timeout)**:
   - Typical duration: 8 to 24 hours.
   - Calculated strictly from `session.created_at`.
   - When $\text{now}() \ge \text{created\_at} + \text{absolute\_timeout}$, the session is terminated regardless of recent activity.

### 2.2 Relational Session Entity Schema

```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(64) NOT NULL,
    family_id UUID NOT NULL DEFAULT gen_random_uuid(),
    ip_address INET NOT NULL,
    user_agent TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    last_active_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    expires_at TIMESTAMPTZ NOT NULL,
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    revoked_reason VARCHAR(64)
);

CREATE INDEX idx_user_sessions_user_active ON user_sessions(user_id, expires_at) WHERE NOT revoked;
CREATE INDEX idx_user_sessions_family ON user_sessions(family_id);
```

### 2.3 Granular Revocation Controls
- **Session Revocation**: Mark single `user_sessions.id` as `revoked = true`.
- **Other Devices Revocation**: Revoke all sessions where `user_id = ? AND id != current_session_id`.
- **Global User Invalidation**: Triggered on password reset, role change, or security alert; revokes all user sessions and updates `user:revoked_epoch:{user_id}` in Redis.
- **Cookie Transport Security**:
  - Store session identifier in an HTTP cookie named with the `__Host-` prefix (`__Host-session_id`).
  - Required cookie attributes: `HttpOnly; Secure; SameSite=Lax; Path=/`.

---

## 3. JWT Rotation & Distributed Revocation

### 3.1 Token Lifespan & Refresh Token Rotation (RTR)

- **Access Token (AT)**: Stateless, short-lived (5 to 15 minutes). Signed using asymmetric keys (RS256, ES256, or EdDSA). Contains claims: `sub`, `tenant_id`, `jti`, `iat`, `exp`, `roles`.
- **Refresh Token (RT)**: Stateful or hashed reference, single-use, rotated on every token exchange.
- **Token Family Tracking & Reuse Detection**:
  ```
  Token Family (family_id: 9a2b...)
  [RT_1] ── exchanged ──> [RT_2] ── exchanged ──> [RT_3 (Active)]
     │
     └── Replay Attack: Attacker presents consumed [RT_1]
             │
             ▼
         BREACH DETECTED:
         1. Invalidate RT_3 immediately
         2. Set user_sessions.revoked = true for family_id
         3. Blacklist current active JTI in Redis
         4. Alert security monitoring
  ```

### 3.2 Redis Revocation Primitives

1. **JTI Denylist with Automatic Expiration**:
   When an access token is revoked before its natural expiration (e.g., explicit logout), store its `jti` in Redis with TTL equal to the token's remaining lifespan:
   ```
   TTL_SECONDS = max(0, jwt.exp - unix_timestamp_now())
   SET token:revoked:{jti} "1" EX TTL_SECONDS
   ```
   Once `exp` passes, Redis automatically evicts the key, preventing unbounded memory growth.
2. **User & Tenant Revocation Epochs**:
   For instant mass-revocation without storing millions of JTIs:
   ```
   SET user:revoked_epoch:{user_id} {current_timestamp}
   ```
   Verification logic:
   ```python
   revocation_epoch = redis.get(f"user:revoked_epoch:{jwt.sub}")
   if revocation_epoch and jwt.iat < int(revocation_epoch):
       raise UnauthorizedError("Token revoked via security epoch")
   ```

---

## 4. PostgreSQL Row-Level Security (RLS) Defense-in-Depth

Application-level filtering (`WHERE tenant_id = ...`) is susceptible to developer oversights and query builder bugs. Database Row-Level Security guarantees tenant boundary enforcement at the database storage engine.

### 4.1 RLS Setup Standard

```sql
-- 1. Enable and FORCE RLS (FORCE ensures table owner also obeys policies)
ALTER TABLE tenant_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE tenant_records FORCE ROW LEVEL SECURITY;

-- 2. Define Tenant Isolation Policy
CREATE POLICY tenant_isolation_policy ON tenant_records
    AS RESTRICTIVE
    FOR ALL
    TO app_user
    USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid)
    WITH CHECK (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid);
```

### 4.2 Connection Pool Transactional Context Injection

In pooled connection environments (Supavisor, PgBouncer), connections are shared across multiple HTTP requests. Session variables MUST be transaction-scoped:

```sql
BEGIN;
-- Third argument 'true' marks setting as local to the transaction
SELECT set_config('app.current_tenant_id', 'c38a2e37-9752-47d0-8f92-5645a27fa461', true);
SELECT set_config('app.current_user_id', 'a89c8362-e64e-4f0f-8c33-b248a31e89df', true);

-- Execute tenant queries safely
SELECT * FROM tenant_records;

COMMIT; -- Settings are automatically cleared on commit or rollback
```

**CRITICAL**: The application connection role (`app_user`) MUST NOT possess `SUPERUSER` or `BYPASSRLS` privileges.

---

## 5. Worker Runtime Memory & Multi-Tenant Isolation

High-throughput persistent worker runtimes (FrankenPHP, Laravel Octane, Python ASGI / Uvicorn) maintain memory across requests. Static variables, singleton service containers, and shared thread locals will cause catastrophic cross-tenant state bleed if not isolated.

### 5.1 Architecture Anti-Pattern vs. Safe Isolation

```
[UNSAFE: Static Singleton Bleed]
Request 1 (Tenant A) ──> Container::set('tenant_id', 'Tenant_A') ──> Process Request
                                                                          │ (Memory retained)
Request 2 (Tenant B) ──> Reads Container::get('tenant_id') [LEAK: sees Tenant A!]

[SAFE: Scoped Container & Reset Lifecycle]
Request 1 ──> RequestScope.create() ──> Set Tenant A ──> Process ──> Scope.destroy()
Request 2 ──> RequestScope.create() ──> Set Tenant B ──> Process ──> Scope.destroy()
```

### 5.2 Implementation Standards by Runtime

1. **PHP Octane & FrankenPHP**:
   - Register auth contexts strictly as request-scoped bindings.
   - Hook into request termination listeners to flush context:
     ```php
     Event::listen(RequestTerminated::class, function () {
         AuthContext::reset();
         TenantManager::clearCurrentTenant();
     });
     ```
2. **Python ASGI (FastAPI / Litestar)**:
   - Use `contextvars.ContextVar` for request-scoped security and tenant context:
     ```python
     from contextvars import ContextVar
     from uuid import UUID

     current_tenant_id: ContextVar[UUID | None] = ContextVar("current_tenant_id", default=None)

     # In middleware:
     token = current_tenant_id.set(tenant_id)
     try:
         await call_next(request)
     finally:
         current_tenant_id.reset(token)
     ```
3. **Automated Concurrency Testing**:
   Author integration tests executing interleaved, concurrent asynchronous requests across distinct tenants. Assert that under 100+ concurrent worker requests, no response payload contains foreign tenant identifiers.
