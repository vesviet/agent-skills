---
name: add-page-route
description: Add or modify a page, screen, or route by following the repo's navigation, data-loading, layout, and auth patterns. Use when frontend work requires new route-level behavior or page wiring.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, run_dev_server, execute_command]
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
- for TanStack Router v2 or React Router v7 codebases: validate all URL search parameters with Zod `.catch()` fallbacks in `validateSearch` — raw URL parameters are user-controlled input and must not be used without validation
- hoist route data loading to loader functions — do not trigger primary data fetches in `useEffect` after mount (causes layout shift waterfalls)
- use type-safe navigation primitives (`<Link to="..." />`, `navigate({ to: '...' })`); never use untyped URL string concatenation (`navigate('/users/' + userId)`)
- for AI-generated routes: verify auth guard completeness (AI frequently omits auth wrappers), data loading pattern match, cache invalidation on mutations, and URL parameter validation before merging

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

## Failure Modes

- **Route added without SEO metadata**: a new page ships without title and description. **Mitigation:** require the SEO metadata at the route registration; reject pages without it.
- **Route added without authn/authz**: a new route is open to anonymous access. **Mitigation:** require an auth profile at the route registration; reject public exposure of non-public routes.
- **Layout drift from the design system**: a new page uses raw values instead of design tokens. **Mitigation:** enforce token-enforcement lint rules; reject pages that fail the lint.
- **A11y state missing**: a page omits one of the required UI states. **Mitigation:** enforce the state checklist on every page; reject pages that skip a state.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/implementation-result.json** — Required fields: change_summary, 
iles_touched[], and 
alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: route-level access control must follow least privilege; reject anonymous access to non-public routes.
- **ASI05 RCE Guard**: never construct route handlers or navigation logic from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the route contract is consumed by backend, design, and QA roles; emit a structured spec so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a route as "ready to ship" without the accessibility and performance checks; surface the residual risk.

## Related Skills

- **add-ui-component**: Build reusable UI used by the page
- **integrate-api-client**: Load or mutate backend data from the route
- **frontend-testing**: Add route and screen coverage
- **accessibility-review**: Check route-level a11y (focus management, navigation announcements)
- **navigate-service**: Understand existing frontend structure before wiring routes
- **commit-code**: Prepare the route change for delivery
