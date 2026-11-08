# Worked Example: Express + Zod + RFC 9457 Problem Details Endpoint

This worked example demonstrates an enterprise-grade `POST /v1/payments` endpoint in TypeScript/Express, enforcing schema-first contracts, Zod boundary validation, distributed idempotency, RFC 9457 error mapping, and MSW v2 network-isolated integration testing.

---

## 1. OpenAPI 3.1 Invariant Contract Snippet

```yaml
openapi: 3.1.0
paths:
  /v1/payments:
    post:
      summary: Process an authorized payment
      operationId: processPayment
      parameters:
        - name: Idempotency-Key
          in: header
          required: true
          schema:
            type: string
            minLength: 16
            maxLength: 128
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [amountCents, currency, recipientId]
              properties:
                amountCents:
                  type: integer
                  minimum: 100
                currency:
                  type: string
                  pattern: "^[A-Z]{3}$"
                recipientId:
                  type: string
                  format: uuid
      responses:
        "201":
          description: Payment processed successfully
        "400":
          description: RFC 9457 Validation Error
        "409":
          description: Concurrent request in progress
        "422":
          description: Idempotency key payload mismatch
```

---

## 2. Production TypeScript Implementation

### 2.1 Boundary Contract & Validation Schema (`schemas/payment.ts`)

```typescript
import { z } from "zod";

export const PaymentRequestSchema = z.object({
  amountCents: z.number().int().min(100, "Minimum payment amount is 100 cents ($1.00)"),
  currency: z.string().regex(/^[A-Z]{3}$/, "Currency must be an ISO 4217 3-letter code"),
  recipientId: z.string().uuid("Recipient ID must be a valid UUID v4")
}).strict();

export type PaymentRequest = z.infer<typeof PaymentRequestSchema>;

export interface PaymentResponse {
  paymentId: string;
  status: "AUTHORIZED" | "SETTLED";
  amountCents: number;
  currency: string;
  recipientId: string;
  createdAt: string;
}
```

### 2.2 Route Handler with RFC 9457 Error Middleware (`routes/payment.ts`)

```typescript
import { Router, Request, Response, NextFunction } from "express";
import crypto from "node:crypto";
import { PaymentRequestSchema, PaymentResponse } from "../schemas/payment";
import { IdempotencyStore } from "../services/idempotency";
import { PaymentGatewayClient } from "../services/gateway";

export class ProblemDetailsError extends Error {
  constructor(
    public status: number,
    public title: string,
    public detail: string,
    public type: string,
    public invalidParams?: Array<{ name: string; reason: string; code: string }>
  ) {
    super(detail);
  }
}

export function createPaymentRouter(
  idempStore: IdempotencyStore,
  gateway: PaymentGatewayClient
): Router {
  const router = Router();

  router.post("/v1/payments", async (req: Request, res: Response, next: NextFunction) => {
    const traceId = (req.headers["x-trace-id"] as string) || crypto.randomUUID();
    const idempKey = req.headers["idempotency-key"] as string;

    if (!idempKey || idempKey.length < 16 || idempKey.length > 128) {
      return next(new ProblemDetailsError(
        400,
        "Bad Request",
        "A valid 'Idempotency-Key' header (16-128 characters) is mandatory.",
        "https://api.example.com/errors/missing-idempotency-key"
      ));
    }

    // 1. Validate boundary schema with Zod
    const parseResult = PaymentRequestSchema.safeParse(req.body);
    if (!parseResult.success) {
      const invalidParams = parseResult.error.issues.map((issue) => ({
        name: issue.path.join("."),
        reason: issue.message,
        code: issue.code
      }));
      return next(new ProblemDetailsError(
        400,
        "Validation Failed",
        `Request body failed validation on ${invalidParams.length} field(s).`,
        "https://api.example.com/errors/validation-failed",
        invalidParams
      ));
    }

    const payload = parseResult.data;
    const payloadHash = crypto.createHash("sha256").update(JSON.stringify(payload)).digest("hex");

    try {
      // 2. Atomic Idempotency Check
      const lockState = await idempStore.acquireOrGet(idempKey, payloadHash);
      if (lockState.status === "MISMATCH") {
        return next(new ProblemDetailsError(
          422,
          "Unprocessable Entity",
          "Idempotency key was previously submitted with differing request parameters.",
          "https://api.example.com/errors/idempotency-mismatch"
        ));
      }
      if (lockState.status === "IN_PROGRESS") {
        return next(new ProblemDetailsError(
          409,
          "Conflict",
          "A transaction with this Idempotency-Key is actively being processed.",
          "https://api.example.com/errors/concurrent-mutation"
        ));
      }
      if (lockState.status === "CACHED") {
        res.setHeader("Idempotent-Replayed", "true");
        return res.status(lockState.statusCode).json(lockState.cachedResponse);
      }

      // 3. Execute downstream business logic
      const payment = await gateway.authorize(payload, traceId);

      // 4. Cache idempotency outcome
      await idempStore.saveSuccess(idempKey, 201, payment);

      return res.status(201).json(payment);
    } catch (err) {
      return next(err);
    }
  });

  return router;
}

// RFC 9457 Global Error Middleware
export function rfc9457ErrorHandler(
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
) {
  const traceId = (req.headers["x-trace-id"] as string) || crypto.randomUUID();

  if (err instanceof ProblemDetailsError) {
    return res.status(err.status).contentType("application/problem+json").json({
      type: err.type,
      title: err.title,
      status: err.status,
      detail: err.detail,
      instance: req.originalUrl,
      trace_id: traceId,
      ...(err.invalidParams ? { invalid_params: err.invalidParams } : {})
    });
  }

  // 5xx Security Rule: Mask raw internal errors from client
  return res.status(500).contentType("application/problem+json").json({
    type: "https://api.example.com/errors/internal-server-error",
    title: "Internal Server Error",
    status: 500,
    detail: "An unexpected error occurred while processing the transaction.",
    instance: req.originalUrl,
    trace_id: traceId
  });
}
```

---

## 3. MSW v2 Level 0 Sandbox Integration Test

This test suite executes inside an air-gapped container (`--network=none`):

```typescript
import { test, describe, before, after, afterEach } from "node:test";
import assert from "node:assert/strict";
import express from "express";
import request from "supertest";
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import { createPaymentRouter, rfc9457ErrorHandler } from "../routes/payment";

const server = setupServer(
  http.post("https://payment-vault.internal/v1/charge", async ({ request: req }) => {
    const body = (await req.json()) as { amountCents: number; currency: string; recipientId: string };
    if (body.recipientId === "00000000-0000-0000-0000-000000000000") {
      return new HttpResponse(null, { status: 500 });
    }
    return HttpResponse.json({
      paymentId: "pay_test_98765",
      status: "AUTHORIZED",
      amountCents: body.amountCents,
      currency: body.currency,
      recipientId: body.recipientId,
      createdAt: new Date().toISOString()
    }, { status: 200 });
  })
);

describe("POST /v1/payments Endpoint Invariants", () => {
  before(() => server.listen({ onUnhandledRequest: "error" }));
  after(() => server.close());
  afterEach(() => server.resetHandlers());

  const mockStore = {
    records: new Map(),
    async acquireOrGet(key: string, hash: string) {
      if (!this.records.has(key)) {
        this.records.set(key, { status: "STARTED", hash });
        return { status: "NEW" };
      }
      const existing = this.records.get(key);
      if (existing.hash !== hash) return { status: "MISMATCH" };
      if (existing.status === "STARTED") return { status: "IN_PROGRESS" };
      return { status: "CACHED", statusCode: existing.statusCode, cachedResponse: existing.response };
    },
    async saveSuccess(key: string, statusCode: number, response: unknown) {
      const existing = this.records.get(key);
      this.records.set(key, { ...existing, status: "COMPLETED", statusCode, response });
    }
  };

  const app = express();
  app.use(express.json());
  app.use(createPaymentRouter(mockStore as any, {
    async authorize(req: any) {
      const res = await fetch("https://payment-vault.internal/v1/charge", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(req)
      });
      if (!res.ok) throw new Error("Vault error");
      return res.json();
    }
  }));
  app.use(rfc9457ErrorHandler);

  test("returns 201 and valid payload on valid request", async () => {
    const res = await request(app)
      .post("/v1/payments")
      .set("Idempotency-Key", "idemp-test-uuid-0001")
      .send({
        amountCents: 5000,
        currency: "USD",
        recipientId: "e2c91c3d-9f4a-4b96-857e-63f533a1e2f1"
      });

    assert.equal(res.status, 201);
    assert.equal(res.body.status, "AUTHORIZED");
    assert.equal(res.body.amountCents, 5000);
  });

  test("returns RFC 9457 Problem Details on invalid input", async () => {
    const res = await request(app)
      .post("/v1/payments")
      .set("Idempotency-Key", "idemp-test-uuid-0002")
      .send({
        amountCents: 50, // Below min 100
        currency: "INVALID",
        recipientId: "not-a-uuid"
      });

    assert.equal(res.status, 400);
    assert.equal(res.headers["content-type"], "application/problem+json; charset=utf-8");
    assert.equal(res.body.title, "Validation Failed");
    assert.equal(res.body.invalid_params.length, 3);
  });

  test("replays cached response on identical idempotency key", async () => {
    const key = "idemp-test-uuid-0003";
    const payload = {
      amountCents: 2500,
      currency: "EUR",
      recipientId: "e2c91c3d-9f4a-4b96-857e-63f533a1e2f1"
    };

    const first = await request(app).post("/v1/payments").set("Idempotency-Key", key).send(payload);
    assert.equal(first.status, 201);

    const second = await request(app).post("/v1/payments").set("Idempotency-Key", key).send(payload);
    assert.equal(second.status, 201);
    assert.equal(second.headers["idempotent-replayed"], "true");
    assert.deepEqual(first.body, second.body);
  });
});
```
