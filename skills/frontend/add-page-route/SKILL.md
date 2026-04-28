---
name: add-page-route
description: Add or modify a page, screen, or route by following the repo's navigation, data-loading, layout, and auth patterns. Use when frontend work requires new route-level behavior or page wiring.
---

# Add Page Route

Use this skill when a frontend change needs a new page, screen, or route-level flow.

## Core Rules

- follow the repo's routing and layout pattern
- keep page-level orchestration separate from reusable component logic
- make loading, empty, error, and unauthorized states explicit
- preserve navigation and deep-link behavior
- update route-aware tests when the page contract changes

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
- [ ] tests added or updated

## Related Skills

- **add-ui-component**: Build reusable UI used by the page
- **integrate-api-client**: Load or mutate backend data from the route
- **frontend-testing**: Add route and screen coverage
- **navigate-service**: Understand existing frontend structure before wiring routes
- **commit-code**: Prepare the route change for delivery
