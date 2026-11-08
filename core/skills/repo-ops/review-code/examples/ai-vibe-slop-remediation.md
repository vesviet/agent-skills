# Worked Example: AI "Vibe Slop" Remediation Catalog

This catalog documents five canonical before-and-after remediations for insidious AI defect patterns ("vibe slop"), demonstrating how to replace cosmetic correctness with genuine software resilience.

---

## 1. Pattern 1: Phantom Validation vs. Verified Boundary Check

### Before (AI Vibe Slop)
Code appears to validate input, but the result is discarded, or regex evaluates truthy unconditionally:

```typescript
export async function registerAccount(req: Request, res: Response) {
  const { email, age } = req.body;

  // Phantom check: regex evaluated, return value discarded
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  // Faulty check: age string evaluates truthy regardless of number
  if (age && age > 18) {
    console.log("Adult verified");
  }

  await db.users.create({ email, age });
  res.status(201).json({ status: "created" });
}
```

### After (Genuine Boundary Verification)
Strict early-exit schema parsing before any business logic:

```typescript
import { z } from "zod";

const RegistrationSchema = z.object({
  email: z.string().email("Invalid email format"),
  age: z.number().int().min(18, "Registrant must be at least 18 years of age")
}).strict();

export async function registerAccount(req: Request, res: Response, next: NextFunction) {
  const parseResult = RegistrationSchema.safeParse(req.body);
  if (!parseResult.success) {
    return next(new ValidationError("Registration failed boundary check", parseResult.error.issues));
  }

  const { email, age } = parseResult.data;
  const user = await db.users.create({ email, age });
  return res.status(201).json({ id: user.id, email: user.email });
}
```

---

## 2. Pattern 2: Silent Error Swallowing vs. RFC 9457 Structured Details

### Before (AI Vibe Slop)
Indiscriminate catch block hides database corruption, network timeouts, or schema mismatches:

```typescript
export async function getBillingProfile(userId: string) {
  try {
    const profile = await stripeClient.customers.retrieve(userId);
    return profile;
  } catch (error) {
    // Slop: Swallows 401 Unauthorized, 404 Not Found, and 500 Network errors alike
    return null;
  }
}
```

### After (Explicit Error Domain Mapping)
Granular error handling mapping downstream status to RFC 9457 Problem Details:

```typescript
export async function getBillingProfile(userId: string, traceId: string) {
  try {
    return await stripeClient.customers.retrieve(userId);
  } catch (error: any) {
    if (error.statusCode === 404) {
      throw new ProblemDetailsError(
        404,
        "Customer Not Found",
        `No billing profile exists for customer ID '${userId}'.`,
        "https://api.example.com/errors/customer-not-found"
      );
    }

    logger.error("Downstream Stripe retrieval failed", { traceId, error, userId });
    throw new ProblemDetailsError(
      502,
      "Bad Gateway",
      "Billing provider temporarily unavailable. Please retry shortly.",
      "https://api.example.com/errors/billing-gateway-error"
    );
  }
}
```

---

## 3. Pattern 3: Mock Collusion vs. Contract-Driven Verification

### Before (AI Vibe Slop)
The test mocks both the dependency and the internal helper, tautologically asserting that the mock returned what was passed into it without testing real code logic:

```typescript
test("creates order successfully", async () => {
  const mockOrderService = {
    create: jest.fn().mockResolvedValue({ id: "ord_1", status: "PENDING" })
  };

  // Test does not exercise controller validation or serialization
  const res = await mockOrderService.create({ total: 100 });
  expect(res.id).toBe("ord_1");
  expect(mockOrderService.create).toHaveBeenCalledWith({ total: 100 });
});
```

### After (Contract-Driven Anti-Tautological Test)
Tests the real HTTP handler using actual validation parsers with downstream calls intercepted at the network layer via MSW v2:

```typescript
test("rejects order when total is below minimum merchant threshold", async () => {
  const app = createTestApp(); // Real Express app with real Zod middlewares

  const response = await request(app)
    .post("/v1/orders")
    .send({
      customerId: "a3b4c5d6-e7f8-4a9b-0c1d-2e3f4a5b6c7d",
      items: [{ productId: "p_1", quantity: 1, priceCents: 20 }] // Total 20 cents < min 100
    });

  expect(response.status).toBe(400);
  expect(response.body.title).toBe("Validation Failed");
  expect(response.body.invalid_params[0].reason).toContain("Minimum order total is 100 cents");
});
```

---

## 4. Pattern 4: Goroutine Leak vs. Managed Worker Pool with Context

### Before (AI Vibe Slop in Go)
Spawning unmanaged goroutines without cancellation listeners or termination channels:

```go
func (s *EventService) ProcessBatch(events []Event) {
    for _, ev := range events {
        // Slop: unmanaged goroutine; if processing blocks, leaks memory indefinitely
        go func(e Event) {
            s.externalClient.Send(e)
        }(ev)
    }
}
```

### After (Managed Worker Pool with `errgroup.Group`)
Bounded concurrency respecting context cancellation and propagating errors:

```go
func (s *EventService) ProcessBatch(ctx context.Context, events []Event) error {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(10) // Bound concurrency to 10 parallel workers

    for _, ev := range events {
        event := ev
        g.Go(func() error {
            // Respect context cancellation before starting work
            if err := ctx.Err(); err != nil {
                return err
            }
            return s.externalClient.SendWithContext(ctx, event)
        })
    }

    // Await completion or first cancellation
    return g.Wait()
}
```

---

## 5. Pattern 5: Destructive Column Drop vs. 3-Phase Expand/Contract

### Before (AI Vibe Slop Migration)
Single-step destructive schema migration executed while old application pods are running:

```sql
-- migration_004_rename_column.sql
ALTER TABLE accounts DROP COLUMN routing_code;
ALTER TABLE accounts ADD COLUMN iban VARCHAR(34) NOT NULL;
```
*Result*: Live application pods running version N fail immediately on incoming requests because `routing_code` is missing and `iban` has no default.

### After (3-Phase Expand / Contract Migration)

**Step 1: Expand (Deployable with App v1)**
```sql
-- Phase 1 Migration: Add nullable new column
ALTER TABLE accounts ADD COLUMN iban VARCHAR(34) DEFAULT NULL;
CREATE INDEX CONCURRENTLY idx_accounts_iban ON accounts(iban);
```

**Step 2: Dual-Write & Async Backfill (Deploy App v2)**
App v2 writes to both `routing_code` and `iban`. Background worker backfills historical records:
```sql
-- Keyset-paginated backfill
UPDATE accounts
SET iban = generate_iban_from_routing(routing_code, account_number)
WHERE id > :cursor AND iban IS NULL
ORDER BY id ASC
LIMIT 500;
```

**Step 3: Contract (Deploy App v3, then run cleanup)**
App v3 reads and writes exclusively to `iban`. Run final migration:
```sql
-- Phase 3 Migration: Drop deprecated column
ALTER TABLE accounts DROP COLUMN routing_code;
```
