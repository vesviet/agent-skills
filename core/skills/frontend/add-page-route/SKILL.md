---
name: add-page-route
description: Add or modify a page, screen, or route by following the repo's navigation, data-loading, layout, and auth patterns. Use when frontend work requires new route-level behavior or page wiring.
---

# Add Page Route

Use this skill when a frontend change needs a new page, screen, or route-level flow.

## When to Use

- frontend work needs a new route/page
- modifying route-level data loading or layout
- wiring auth or navigation per repo pattern
- adding screen-level behavior

## Core Rules

- follow the repo's routing and layout pattern
- keep page-level orchestration separate from reusable component logic
- make loading, empty, error, and unauthorized states explicit
- preserve navigation and deep-link behavior
- update route-aware tests when the page contract changes
- if any code in this change was AI-generated, validate it per the risk tier defined in the frontend-developer role before accepting

### 2025-2026: AI-Generated Route Wiring Review

When AI tools generate page or route scaffolding, apply these additional checks before merging:

- **Auth guard completeness:** verify the generated route has the correct authentication and authorization guards — AI-generated routes frequently omit auth wrappers on sensitive pages or apply overly permissive default access.
- **Data loading correctness:** confirm the generated data-loading pattern (loader function, `useEffect`, SWR/React Query hook) matches the repo's established pattern and handles loading, error, and empty states explicitly — AI-generated loaders often assume happy-path only.
- **Stale data and cache invalidation:** check that generated mutations or navigations trigger appropriate cache invalidations — AI-generated code frequently omits `invalidateQueries` or router cache refresh after mutations.
- **Deep-link and URL parameter handling:** verify that AI-generated route parameter handling validates input (type coercion, missing param fallbacks) — raw URL parameters are user-controlled input and must not be used without validation.

## Suggested Process

### 1. Inspect Nearby Routes

Find a similar route and note:

- file placement
- route registration
- layout nesting
- data loading pattern
- auth or permission gating

### 2. Define The Route Responsibility

Clarify:

- what the page is for
- what URL or navigation entry reaches it
- what data it needs before render
- what actions a user can take there
- what state belongs at page level versus component level

### 3. Create The Route Wiring

Add or update:

- route definition or file-based route
- page component or screen entry
- navigation links or menu entries if needed
- layout or shell integration

### 4. Implement The Page Flow

Make page-level orchestration explicit:

- data loading
- access control
- view state branching
- mutations and success/failure feedback

### 5. Check Navigation Safety

Verify:

- direct URL access works if the app supports it
- back/forward navigation behaves correctly
- query params, path params, or search state are handled intentionally
- if the route is public-facing, verify SSR/SSG behavior and meta tag requirements (title, description, OG)

### 6. Add Tests

Use skill: `frontend-testing`

Cover:

- route render
- guard or auth behavior
- important page transitions
- failure and empty states

## Checklist

- [ ] local route pattern reviewed
- [ ] route responsibility defined
- [ ] layout and navigation wired correctly
- [ ] page-level states handled
- [ ] direct navigation checked
- [ ] SEO/SSR verified for public-facing routes (meta tags, OG, SSG behavior)
- [ ] tests added or updated

## Related Skills

- **add-ui-component**: Build reusable UI used by the page
- **integrate-api-client**: Load or mutate backend data from the route
- **frontend-testing**: Add route and screen coverage
- **accessibility-review**: Check route-level a11y (focus management, navigation announcements)
- **navigate-service**: Understand existing frontend structure before wiring routes
- **commit-code**: Prepare the route change for delivery
