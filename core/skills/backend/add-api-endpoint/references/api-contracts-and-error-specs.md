# API Contracts, RFC 9457 Problem Details & Sandbox Readiness — Reference

This reference provides 2027 standards for schema-first invariant contract binding (OpenAPI 3.1 / JSON Schema), structured RFC 9457 error handling, and sandbox execution readiness.

---

## 1. Schema-First Invariant Contract Binding

In 2027 Agentic SWE, endpoints must never be implemented from informal descriptions. The machine-readable contract is the invariant boundary:

### 1.1 OpenAPI 3.1 & JSON Schema Specifications
- **Schema Authority**: The OpenAPI 3.1 specification or JSON Schema document (`contracts/schemas/api-contract-spec.json`) must be authored and meta-validated before writing route handlers.
- **Contract Invariance**: Handlers must bind strictly to the declared schema. Field types, constraints (`minLength`, `pattern`, `minimum`), and mandatory properties cannot deviate from the spec.
- **Runtime Validation**: Use high-performance schema validators at the HTTP boundary (Zod, Pydantic, TypeBox). Parsing must reject unknown or extra properties when strict mode is enabled.

### 1.2 Boundary Implementation Pattern (TypeScript / Express & Zod)

```typescript
import { Router, Request, Response, NextFunction } from "express";
import { z } from "zod";

export const CreateOrderSchema = z.object({
  customerId: z.string().uuid(),
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number().int().positive(),
    price: z.number().positive()
  })).min(1),
  idempotencyKey: z.string().min(16).max(128)
});

export type CreateOrderInput = z.infer<typeof CreateOrderSchema>;

export function createOrderRouter(orderService: OrderService): Router {
  const router = Router();

  router.post(
    "/v1/orders",
    requireAuth,                               // Enforce default-deny authz
    validateBody(CreateOrderSchema),           // Boundary validation against invariant schema
    async (req: Request, res: Response, next: NextFunction) => {
      try {
        const order = await orderService.createOrder(req.user.id, req.body);
        res.status(201).json(order);
      } catch (err) {
        next(err);                             // Forward to RFC 9457 error handler
      }
    }
  );

  return router;
}
```

---

## 2. RFC 9457 Structured Problem Details Standard

All error responses across HTTP APIs must adhere strictly to RFC 9457 (Problem Details for HTTP APIs). Ad-hoc error envelopes (e.g. `{ "error": "something went wrong" }`) are prohibited.

### 2.1 Standard Problem Details Envelope

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 400,
  "detail": "The request body failed schema validation on 2 fields.",
  "instance": "/v1/orders",
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "invalid_params": [
    {
      "name": "customerId",
      "reason": "Must be a valid UUID v4",
      "code": "invalid_format"
    },
    {
      "name": "items[0].quantity",
      "reason": "Quantity must be an integer greater than zero",
      "code": "greater_than"
    }
  ]
}
```

### 2.2 Core Specification Rules
1. **`type` (URI)**: Absolute or relative URI referencing documentation for the error type.
2. **`title` (string)**: Short summary of the error type. It must not change between occurrences of the same status/type.
3. **`status` (integer)**: Matches the HTTP status code returned in the HTTP header.
4. **`detail` (string)**: Specific explanation of why this individual invocation failed.
5. **`instance` (URI)**: The resource URI on which the error occurred.
6. **Extension Fields**: Machine-readable extensions like `invalid_params` array (`name`, `reason`, `code`) or `retry_after_ms`.
7. **5xx Security Rule**: Responses with 5xx status codes must **NEVER** expose stack traces, database query fragments, filesystem paths, or internal hostnames. Map unexpected exceptions to a generic `Internal Server Error` envelope containing only a correlateable `trace_id`.

---

## 3. Execution Sandbox Readiness & Isolation

Endpoints and their test suites must be built to operate cleanly within isolated container environments per `core/policies/execution-sandbox.md`:

### 3.1 Network Isolation (Level 0 Air-Gap)
- Integration test suites for endpoints must pass with `--network=none`.
- Endpoints must not make outbound network calls to ambient internet services during testing.

### 3.2 Downstream Mocking with MSW v2
All external HTTP dependencies called by the endpoint handler must be intercepted using Mock Service Worker (MSW v2) at the network layer:

```typescript
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

export const handlers = [
  http.post("https://payment.gateway.internal/charges", async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      chargeId: "chg_test_123",
      status: "succeeded"
    }, { status: 200 });
  })
];

export const server = setupServer(...handlers);
```

### 3.3 Zero Ambient Credentials
- Endpoints must not depend on ambient AWS/GCP/Azure credentials on developer laptops.
- Inject explicit, validated test environment variables or ephemeral credentials in container configurations.
