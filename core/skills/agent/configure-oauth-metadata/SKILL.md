---
name: configure-oauth-metadata
description: Configures well-known OAuth 2.0 and OpenID Connect discovery endpoints (`oauth-protected-resource`, `oauth-authorization-server`, `openid-configuration`) including the `agent_auth` block required for agentic registration flows. Use when setting up or correcting OAuth metadata for AI agent authentication, WorkOS agentic registration, or any service that exposes agent-accessible authorization endpoints.
---

# Configure OAuth Metadata

Use this skill when configuring `/.well-known/oauth-protected-resource`, `/.well-known/oauth-authorization-server`, or `/.well-known/openid-configuration` — especially the `agent_auth` block that enables agentic client registration and claim flows.

## Core Rules

- Ensure `authorization_servers` lists a fully resolvable, operational domain — do not use dummy subdomains that are not bound in DNS; a 530 Origin DNS Error means the URL is unreachable.
- The `agent_auth` block MUST exist in the `oauth-authorization-server` metadata file.
- The `agent_auth` block MUST include a `"skill"` attribute pointing to the absolute URL of `auth.md`.
- Use `"register_uri"` (not `identity_endpoint`) and `"claim_uri"` (not `claim_endpoint`) — the field names are exact; any deviation will fail scanner validation.
- Define `credential_types_supported` nested inside the identity type blocks (e.g., `anonymous.credential_types_supported`), NOT at the root of `agent_auth`.
- Both `anonymous` and `identity_assertion` credential paths must be documented if the service supports them.
- All endpoints must be served with `Content-Type: application/json` and appropriate CORS headers.
- enforce PKCE (Proof Key for Code Exchange) as mandatory for all agent OAuth flows, asserting `code_challenge_methods_supported: ["S256"]` in authorization metadata
- support OpenID Connect (OIDC) Dynamic Client Registration by exposing a POST endpoint that accepts the Agent Card JSON as input
- bind issued access tokens cryptographically to agent identities using the `azp` and agent DID claims in the JWT payload
- validate that the `agent_auth` configuration complies with isitagentready.com and WorkOS requirements

## When to Use

- Setting up WorkOS Agentic Registration for the first time on a domain
- Correcting `agent_auth` field names after scanner validation failures
- Adding OAuth metadata endpoints to a Cloudflare Pages or Workers site
- Verifying that `isitagentready.com` or equivalent scanner passes the OAuth metadata checks
- Updating authorization server metadata after adding or changing credential types

## Suggested Process

1. **Locate or create metadata files**: Identify where `oauth-protected-resource.json` and `oauth-authorization-server.json` are served from. For Cloudflare Pages, these live under `public/.well-known/`. For Workers, serve them from dedicated route handlers.

2. **Structure the `oauth-authorization-server` payload**: Include the required top-level fields (`issuer`, `authorization_endpoint`, `token_endpoint`) and the `agent_auth` block:
   ```json
   {
     "issuer": "https://auth.yourdomain.com",
     "authorization_endpoint": "https://auth.yourdomain.com/authorize",
     "token_endpoint": "https://auth.yourdomain.com/token",
     "agent_auth": {
       "skill": "https://yourdomain.com/.well-known/auth.md",
       "register_uri": "https://auth.yourdomain.com/agent/register",
       "claim_uri": "https://auth.yourdomain.com/agent/claim",
       "anonymous": {
         "credential_types_supported": ["anonymous"]
       },
       "identity_assertion": {
         "credential_types_supported": ["jwt_bearer"]
       }
     }
   }
   ```

3. **Structure the `oauth-protected-resource` payload**: Include `resource` (the service URL) and `authorization_servers` (array of issuer URLs):
   ```json
   {
     "resource": "https://yourdomain.com",
     "authorization_servers": ["https://auth.yourdomain.com"]
   }
   ```

4. **Validate DNS**: Confirm every domain in `authorization_servers` resolves correctly in public DNS. A non-resolving domain causes 530 errors in scanners.

5. **Mount metadata endpoints**: Ensure each file is reachable at its standard path. Set `Content-Type: application/json` and CORS headers.

6. **Expose via Link headers**: Use `configure-agent-headers` to add Link headers pointing to both well-known files for passive agent discovery.

7. **Run scanner validation**: Test with `isitagentready.com` or the WorkOS scanner. Review the diagnostic output against specific rule names — e.g., "anonymous registration requires anonymous.credential_types_supported" maps to a specific nesting requirement.

### 2026: Mandatory PKCE and Token Binding

To secure machine-to-machine interactions and prevent authorization code interception, A2A OAuth flows require strict PKCE and cryptographic token binding:
- **Mandatory PKCE**: All client authorization requests must use PKCE with SHA-256 challenge. The authorization server metadata must declare `"code_challenge_methods_supported": ["S256"]`.
- **Authorized Presenter**: The token payload must contain the `azp` (Authorized Party) claim, which identifies the client agent that was issued the token.
- **DID Token Binding**: The token must bind the agent's DID. The JWT claims include the agent's public key identifier or DID URI in custom claims to ensure only the holder of the agent's private key can present the token.

### 2026: OIDC Dynamic Client Registration

Dynamic registration allows new worker agents to register as OAuth clients on-the-fly:
- **Registration Endpoint**: Expose a registration endpoint (`register_uri`) responding to POST requests.
- **Payload Schema**: The endpoint accepts OIDC Dynamic Client Registration payloads containing client metadata or directly accepting the worker's signed Agent Card JSON.
- **Client Credentials**: Upon validation of the Agent Card signature and capabilities, the server registers the client and returns a client identifier and registration access token.

## Checklist

- [ ] `authorization_servers` URLs are fully resolvable in public DNS (no 530 errors).
- [ ] `agent_auth` block exists in `oauth-authorization-server` metadata.
- [ ] `agent_auth.skill` points to the absolute URL of `auth.md`.
- [ ] Field names use `register_uri` and `claim_uri` (not `identity_endpoint`/`claim_endpoint`).
- [ ] `credential_types_supported` is nested inside credential type blocks, not at the `agent_auth` root.
- [ ] Both `anonymous` and `identity_assertion` paths are documented if supported.
- [ ] Metadata files are served with `Content-Type: application/json`.
- [ ] CORS headers allow agent clients to fetch the metadata cross-origin.
- [ ] Link headers via `configure-agent-headers` point to the well-known paths.
- [ ] Scanner validation passes without field-name or DNS errors.

## Related Skills

- **manage-auth-md**: Manage the `auth.md` discovery file that `agent_auth.skill` points to.
- **debug-identity-provider**: Diagnose and fix scanner validation failures after configuring metadata.
- **configure-agent-headers**: Expose OAuth metadata well-known paths via HTTP Link headers.
