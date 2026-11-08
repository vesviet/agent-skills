# React 19 RSC Routing & View Transitions Architecture (2026)

## 1. React Server Component (RSC) Leaf Architecture

### 1.1 Data Hoisting & Boundary Isolation
In React 19 and Next.js 15+ App Router, routes enforce strict separation between data fetching and interactive presentation:
- **Server Component Root**: All data fetching, auth verification, and database reads occur in async Server Components at the route root.
- **Client Leaf Boundary**: The `"use client"` directive must be pushed down to terminal UI leaves (buttons, interactive filter inputs, modals).
- **Waterfall Elimination**: Avoid fetching primary page data inside client-side `useEffect` hooks, which causes layout shift waterfalls and Cumulative Layout Shift (CLS) regressions.

---

## 2. Type-Safe Route Validation (TanStack Router & Next.js)

### 2.1 Untrusted Query Parameters
URL search parameters are user-controlled inputs subject to tampering:
- Every query parameter must be validated with Zod schemas.
- Use `.catch()` fallbacks to supply safe defaults instead of failing hard on malformed inputs:
  ```typescript
  import { z } from 'zod';

  export const searchSchema = z.object({
    page: z.coerce.number().int().positive().catch(1),
    filter: z.enum(['all', 'active', 'archived']).catch('all'),
    query: z.string().trim().max(100).catch(''),
  });
  ```

---

## 3. CSS View Transitions & React 19 `ViewTransition`

### 3.1 Off-Thread Composited Motion
Route animations must never trigger layout recalculation during transitions:
- Restrict animated CSS properties to `transform` and `opacity`.
- Target Interaction to Next Paint (INP) budget of `< 200ms` with DOM mutation callbacks `< 50ms`.
- Wrap route mutations in `React.startTransition()`:
  ```tsx
  import { startTransition } from 'react';

  function onNavigate(nextUrl: string) {
    if (!document.startViewTransition) {
      router.push(nextUrl);
      return;
    }
    document.startViewTransition(() => {
      startTransition(() => {
        router.push(nextUrl);
      });
    });
  }
  ```
- **Accessibility Invariant**:
  ```css
  @media (prefers-reduced-motion: reduce) {
    ::view-transition-group(*),
    ::view-transition-old(*),
    ::view-transition-new(*) {
      animation: none !important;
    }
  }
  ```

---

## 4. AI Route Audit Checklist

Before accepting AI-generated route code, verify:
- [ ] Auth guard completeness: Route wraps access control or verifies session before server reads.
- [ ] Loader hoisting: Data loading occurs at server root, not in client hooks.
- [ ] Cache revalidation: Mutating actions call `revalidatePath` or `router.invalidate()`.
- [ ] Safe parameters: Query/path parameters validated against Zod schemas with fallbacks.
