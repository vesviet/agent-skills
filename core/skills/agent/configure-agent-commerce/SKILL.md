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
- enforce fully programmatic A2A transactions using custom headers `X-Payment` and `X-Payment-Response`
- resolve agent customer identity through a cryptographically signed JWT with the `sub` claim set to the agent DID
- publish agent-readable commerce schemas at the standardized path `/.well-known/acp-manifest.json`
- do not bind the programmatic flow to human-centric checkout interfaces or Stripe-specific SDK redirects

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

### 2026: The x402 HTTP Payment Protocol

The x402 HTTP Payment Protocol defines a fully automated, programmatic agent-to-agent payment negotiation standard:
- **HTTP 402 Flow**: Paywalled endpoints respond with `402 Payment Required` to request a payment before serving the requested resource.
- **Protocol Headers**: The server sends the `X-Payment` request header containing payment instructions (currency, amount, destination address, and transaction identifier).
- **Payment Response**: The agent processes the payment autonomously (via local wallets or pre-approved limits) and submits proof in the `X-Payment-Response` header of a subsequent request.
- **A2A Programmatic Design**: The negotiation, authorization, and confirmation must be completely machine-to-machine, avoiding any dependency on interactive web views or human confirmation.
- **Header Structure and Content**:
  * The `X-Payment` request header contains a comma-separated list of key-value pairs specifying the billing parameters. These include `amount` (expressed in lowest denominator units, e.g., cents), `currency` (e.g., USD or USDC), `destination` (payment wallet or gateway address), and `memo` (a unique transaction UUID).
  * The `X-Payment-Response` header carries the corresponding transaction proof payload. It contains `txn_hash` (the cryptographic receipt or ledger transaction ID), `agent_did` (the agent's identifier), and `signature` (proving the agent signed the transaction hash).

### 2026: Stripe Machine Payments Protocol (MPP)

Stripe Machine Payments Protocol (MPP) enables automated billing and payment processing for machine clients:
- **MPP Client Setup**: Register agents with Stripe MPP to assign programmatic payment credentials and wallets.
- **Transaction Settlement**: The MPP gateway executes transfer requests and generates cryptographic proofs of payment immediately upon settlement.
- **Offline Verification**: The service provider validates the proof against Stripe's public ledger or API keys, eliminating synchronous external dependencies during path execution.
- **MPP Integration and Security**:
  * Establish Stripe MPP Webhook endpoints to handle asynchronous settlement events (such as `payment_intent.succeeded` with machine metadata).
  * Configure public key caching on the service provider to verify the cryptographic signatures on payment proofs without calling Stripe APIs on every request.
  * Utilize Stripe's delegated authorization flows to set limits and velocity controls (e.g., maximum $5.00 per transaction, $50.00 daily budget) for each machine credential.
- **Offline Ledger Settlement**:
  * For micro-transactions, agents can settle payments using an offline-first ledger, batching transaction confirmations to the main payment network once a specific threshold is reached.

### 2026: UCP and ACP Standards Integration

Standardizing the discovery and execution interfaces is critical for multi-agent interoperability:
- **ACP Manifest**: Publish the Agentic Commerce Protocol (ACP) configuration at the standardized endpoint `/.well-known/acp-manifest.json`.
- **Manifest Properties**: The manifest must declare supported payment protocols, accepted tokens, pricing tiers, and endpoint mappings.
- **User Context Protocol (UCP)**: Expose consumer context attributes to allow agents to retrieve user preferences, organizational policies, and billing limits safely.
- **ACP Manifest Structure**: The `/.well-known/acp-manifest.json` schema details the capabilities and payment rails supported by the endpoint. It registers the standard schemas (`acp_v1`), support for payment methods (e.g., `stripe_mpp` or `cryptographic_transfer`), metadata for discovery, and URI templates for payment verification.
- **User Context Protocol (UCP) Delegation**: When an user delegates commerce actions to an agent, the agent presents a delegation token (`delegation_token` in headers) to the UCP endpoint. This token specifies the user's spending allowances, shipping preference overrides, and authorized merchants, allowing the service to process the transaction with explicit bounds.

### 2026: Agent Customer Identity and DID Mapping

To track billing usage and enforce access control, the system maps agents to persistent customer records:
- **Decentralized Identifiers**: Every agent must possess a unique Decentralized Identifier (DID) representing its cryptographic identity.
- **Token Claims**: Authenticated requests must include a cryptographically signed JSON Web Token (JWT) where the `sub` claim maps directly to the agent's DID.
- **Identity Resolution**: Resolve the token signature against the agent's public keys discovered via its DID document.
- **DID and Customer Binding**:
  * Establish a database mapping layer between the agent's DID (`did:key:...` or `did:ion:...`) and a Stripe Customer ID or internal billing account.
  * Implement caching for DID documents to avoid network lookups during authentication, checking signatures against the cached public key.
  * Validate delegation chains using the JSON Web Token (`delegation` claim) to ensure the agent is authorized to act on behalf of the customer DID.

### 2026: Machine-to-Machine Payment Negotiation Flow

The dynamic negotiation between agent and service follows a strict programmatic sequence:
1. **Initial Access Attempt**: The agent requests a paywalled resource without credentials.
2. **Payment Required Challenge**: The service responds with HTTP 402, setting the `WWW-Authenticate: X-Payment-Required` header, and returns a JSON payload containing the payment manifest.
3. **Agent Decision & Transfer**: The agent verifies the amount against its local delegation limits, initiates payment via Stripe MPP or local crypto wallet, and retrieves a cryptographic payment proof.
4. **Resubmission with Proof**: The agent retries the original request, attaching the proof to the `X-Payment-Response` header.
5. **Validation and Delivery**: The service validates the payment proof asynchronously and delivers the resource with HTTP 200.
- **Idempotency and Deduplication**:
  * The agent must generate a unique UUID (`idempotency_key`) and include it in both the `X-Payment` negotiation phase and the final payment settlement.
  * The merchant's service tracks these keys in a transactional cache (e.g., Redis) to ensure duplicate request replays do not result in multiple ledger charges or credit deductions.

## Output Format

- `/.well-known/acp.json` — discovery metadata
- x402 payment manifest (inline in 402 response body)
- MPP handler endpoint returning `200 OK` on valid proof
- UCP endpoint returning consumer context object
- `/.well-known/acp-manifest.json` — agentic commerce schema manifest configuration

## Checklist

- [ ] x402 endpoints return `402 Payment Required` with correct `WWW-Authenticate` header.
- [ ] Payment manifest JSON includes accepted token types, amounts, and network IDs.
- [ ] MPP endpoint verifies payment proof server-side before granting access.
- [ ] User Context Protocol endpoint correctly resolves consumer preferences.
- [ ] ACP discovery file exists at the well-known path and passes schema validation.
- [ ] API responses use correct media types for agent consumption (`application/json`).
- [ ] Client validation rejects malformed or replayed payment proofs.
- [ ] Paywalled vs free endpoints are clearly separated and not crossable.
- [ ] Agent customer identity is verified via signed JWT using sub claim mapping.
- [ ] Custom X-Payment and X-Payment-Response headers are processed during request flow.

## Related Skills

- **configure-oauth-metadata**: Configure agentic authorization metadata — often prerequisite for UCP token validation.
- **manage-api-catalog**: Wire up linkset endpoints for commerce discovery alongside ACP.
- **configure-agent-headers**: Expose ACP well-known via HTTP Link headers for discovery.
