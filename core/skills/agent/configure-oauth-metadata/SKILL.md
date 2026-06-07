---
name: configure-oauth-metadata
description: Use when configuring well-known OAuth and OpenID endpoints, particularly the agent_auth block for agentic registration.
---

# Configure OAuth Metadata

Use this skill when configuring `/.well-known/oauth-protected-resource`, `/.well-known/oauth-authorization-server`, or `/.well-known/openid-configuration`.

## Core Rules

- Ensure `authorization_servers` lists a fully resolvable, operational domain (do not use dummy subdomains like `auth.example.com` if they are not bound in DNS).
- The `agent_auth` block MUST exist in `oauth-authorization-server`.
- The `agent_auth` block MUST include a `"skill"` attribute pointing to the absolute URL of `auth.md`.
- For `agent_auth`, strictly use `"register_uri"` (not `identity_endpoint`) and `"claim_uri"` (not `claim_endpoint`).
- Define `credential_types_supported` nested inside the identity type blocks (e.g., `anonymous.credential_types_supported`), NOT at the root of `agent_auth`.

## Suggested Process
1. Locate or create the metadata JSON files for the auth server and protected resource.
2. Structure the `agent_auth` object payload with register and claim endpoints.
3. Validate domain names in DNS records to prevent connection/530 validation errors.
4. Mount metadata endpoints onto corresponding standard well-known routes.

## Checklist

- [ ] URLs are resolvable (avoid DNS/530 errors).
- [ ] `agent_auth.skill` points to `/auth.md`.
- [ ] `register_uri` and `claim_uri` are correctly named.
- [ ] `credential_types_supported` is nested correctly.
- [ ] Both `anonymous` and `identity_assertion` paths are documented if supported.

## Related Skills

- **manage-auth-md**: Manage the corresponding Auth.md discovery file.
- **debug-workos-integration**: Fix scanning errors.
