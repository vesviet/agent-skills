---
name: configure-agent-commerce
description: Implements agentic commerce standards (x402 HTTP payment protocol, MPP, UCP, ACP) to enable transactional checkout flows in agent-driven applications — making a service billiable and discoverable by AI agents. Use when adding agent-to-agent payment, user context resolution, or agentic commerce directory registration to a web service.
---

# Configure Agent Commerce

Use this skill when integrating agent-driven checkout and commerce discovery flows using agentic standards: the x402 HTTP payment protocol, Merchant Payment Protocol (MPP), User Context Protocol (UCP), and Agentic Commerce Protocol (ACP).

## Core Rules

- Adhere strictly to the x402 and Merchant Payment Protocol (MPP) metadata requirements.
- Expose the User Context Protocol (UCP) endpoint at the documented path for consumer preference resolution.
- Maintain up-to-date `.well-known` endpoints for Agentic Commerce Protocol (ACP) discovery.
- Never expose payment credentials or secret keys — only reference identifiers and public metadata.
- x402 responses must return HTTP 402 with a `WWW-Authenticate: X-Payment-Required` header and a JSON payment manifest.

## When to Use

- Adding paywall or metered access for AI agents (agent-to-agent billing via x402)
- Integrating agent payment flows with crypto or programmable payment rails (MPP)
- Exposing user context (preferences, identity, tier) to trusted agents via UCP
- Making a service discoverable in agentic commerce directories via ACP

## Suggested Process

1. **Define commerce scope**: Identify which endpoints require payment, which are free, and which require UCP context before serving.
2. **Set up x402 paywall**: Implement the `402 Payment Required` response for paywalled endpoints — include a valid payment manifest with accepted tokens, amounts, and network identifiers.
3. **Implement MPP endpoint**: Mount the Merchant Payment Protocol handler to receive and verify token payment proofs from agent clients.
4. **Mount UCP endpoint**: Expose the User Context Protocol endpoint (`/ucp` or per spec path) to resolve consumer preferences for authenticated agent sessions.
5. **Expose ACP well-known**: Create `/.well-known/acp.json` (or per ACP spec path) so agent commerce directories can auto-discover supported payment methods and scopes.
6. **Validate agent-side flow**: Test the full payment cycle — agent sends 402 request → receives manifest → pays → retries with proof → receives resource.
7. **Review security posture**: Confirm payment proof validation is server-side, not bypassable client-side. Confirm UCP tokens are scoped and non-transferable.

## Output Format

- `/.well-known/acp.json` — discovery metadata
- x402 payment manifest (inline in 402 response body)
- MPP handler endpoint returning `200 OK` on valid proof
- UCP endpoint returning consumer context object

## Checklist

- [ ] x402 endpoints return `402 Payment Required` with correct `WWW-Authenticate` header.
- [ ] Payment manifest JSON includes accepted token types, amounts, and network IDs.
- [ ] MPP endpoint verifies payment proof server-side before granting access.
- [ ] User Context Protocol endpoint correctly resolves consumer preferences.
- [ ] ACP discovery file exists at the well-known path and passes schema validation.
- [ ] API responses use correct media types for agent consumption (`application/json`).
- [ ] Client validation rejects malformed or replayed payment proofs.
- [ ] Paywalled vs free endpoints are clearly separated and not crossable.

## Related Skills

- **configure-oauth-metadata**: Configure agentic authorization metadata — often prerequisite for UCP token validation.
- **manage-api-catalog**: Wire up linkset endpoints for commerce discovery alongside ACP.
- **configure-agent-headers**: Expose ACP well-known via HTTP Link headers for discovery.
