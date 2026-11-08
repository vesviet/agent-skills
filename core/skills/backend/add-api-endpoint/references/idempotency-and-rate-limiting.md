# Idempotency, Rate Limiting & Deadline Propagation — Reference

This reference documents 2027 production standards for enterprise-grade API endpoints: IETF Idempotency-Key handling, distributed Redis atomic locking, sliding window rate limiting, and context deadline propagation.

---

## 1. IETF Idempotency-Key Specification & Replay Semantics

Idempotency ensures that executing an HTTP mutating operation (e.g., `POST /v1/payments`, `POST /v1/orders`) multiple times with the same key produces the identical side-effect and returns the identical response.

### 1.1 Protocol Invariants (IETF Draft `draft-ietf-httpapi-idempotency-key-header`)
1. **Header Identification**: Clients supply the `Idempotency-Key: <unique-token>` header (typically UUID v4 or ULID, 16–128 characters).
2. **Payload Fingerprinting**: Store a SHA-256 digest of the request method, URL path, and raw JSON request body alongside the key.
3. **State Transitions**:
   - `STARTED`: The request is currently processing. A concurrent request with the same key returns `409 Conflict` (or waits if lock acquisition with timeout is supported).
   - `COMPLETED`: The operation completed successfully. Replaying requests return the cached HTTP status code, headers, and response payload with an `Idempotent-Replayed: true` header.
   - `MISMATCH`: If a request arrives with an existing key but a differing payload SHA-256 digest, immediately reject with `422 Unprocessable Entity` or `400 Bad Request` (`Idempotency-Key collision with conflicting payload`).
4. **Time-To-Live (TTL)**: Keys persist for a configured retention window (minimum 24 hours).

### 1.2 Redis Distributed State Machine (Atomic Lua Script)

```lua
-- KEYS[1]: idemp:{key}
-- ARGV[1]: request_hash (SHA-256)
-- ARGV[2]: ttl_seconds (e.g., 86400)
local record = redis.call("HGETALL", KEYS[1])
if #record == 0 then
    -- Key not seen before: initialize state to STARTED
    redis.call("HSET", KEYS[1], "status", "STARTED", "hash", ARGV[1])
    redis.call("EXPIRE", KEYS[1], ARGV[2])
    return { "NEW" }
end

local status, stored_hash
for i = 1, #record, 2 do
    if record[i] == "status" then status = record[i+1] end
    if record[i] == "hash" then stored_hash = record[i+1] end
end

if stored_hash ~= ARGV[1] then
    return { "MISMATCH" }
end

if status == "STARTED" then
    return { "IN_PROGRESS" }
elseif status == "COMPLETED" then
    local response = redis.call("HGET", KEYS[1], "response")
    local status_code = redis.call("HGET", KEYS[1], "status_code")
    return { "CACHED", status_code, response }
end

return { "UNKNOWN" }
```

---

## 2. Sliding Window Rate Limiting

Rate limiting protects downstream services from Denial of Service (DoS) and noisy neighbor starvation while providing actionable backoff telemetry to clients.

### 2.1 Standard Telemetry Headers (IETF RFC 6585 / draft-ietf-httpapi-ratelimit-headers)
Every response (success or rejected) must include standard headers:
- `RateLimit-Limit`: Maximum requests permitted within window.
- `RateLimit-Remaining`: Requests remaining within active window.
- `RateLimit-Reset`: Seconds remaining until quota reset.
- `Retry-After`: Included on `429 Too Many Requests`, indicating wait time before retry.

### 2.2 Redis Sorted Set (ZSET) Sliding Log Algorithm
The sliding log algorithm eliminates the edge-burst vulnerability inherent in fixed-window counters:

```typescript
import { Redis } from "ioredis";

export async function checkSlidingRateLimit(
  redis: Redis,
  identifier: string,
  limit: number,
  windowSeconds: number
): Promise<{ allowed: boolean; remaining: number; resetAfter: number }> {
  const key = `ratelimit:${identifier}`;
  const now = Date.now();
  const windowStart = now - windowSeconds * 1000;

  const pipeline = redis.pipeline();
  pipeline.zremrangebyscore(key, 0, windowStart);    // Drop expired hits
  pipeline.zadd(key, now, `${now}-${Math.random()}`); // Record current request
  pipeline.zcard(key);                                // Total hits in window
  pipeline.expire(key, windowSeconds);                // Keep key alive

  const results = await pipeline.exec();
  const currentCount = (results?.[2]?.[1] as number) || 0;
  const allowed = currentCount <= limit;

  return {
    allowed,
    remaining: Math.max(0, limit - currentCount),
    resetAfter: windowSeconds
  };
}
```

---

## 3. Context Deadline Propagation & Cancellation Safety

Distributed API systems must prevent "zombie compute" where downstream databases and microservices continue working after the upstream client has timed out or disconnected.

### 3.1 Strict Timeout Hierarchy
1. **Client Gateway / Ingress Timeout**: e.g., 5.0 seconds.
2. **Service Route Handler Timeout**: Derived from request context, capped at Gateway - 500ms (e.g., 4.5 seconds).
3. **Database / RPC Downstream Timeout**: Capped at Route Handler - 500ms (e.g., 3.0 seconds).

### 3.2 Cancellation Rules
- **Context Propagation**: Always pass `ctx` (`context.Context` in Go, `AbortSignal` in TypeScript/Node.js) to every database query, RPC call, and HTTP client invocation.
- **Early Exit**: Inspect `ctx.Err()` or `signal.aborted` before starting CPU-intensive work or acquiring heavyweight mutexes.
- **Rollback Safety**: Ensure database transactions cleanly rollback when `context.Canceled` or `context.DeadlineExceeded` occurs. Never commit an uncompleted transaction.
