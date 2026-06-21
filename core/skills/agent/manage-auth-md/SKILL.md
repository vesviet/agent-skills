---
name: manage-auth-md
description: Use when creating, updating, or auditing the /auth.md file at the repository or domain root to ensure agentic registration discovery compliance with WorkOS and isitagentready.com standards.
---

# Manage Auth.md

Use this skill when adding or updating the Agentic Registration Discovery file (`/auth.md`) to comply with WorkOS and `isitagentready.com` standards. The `auth.md` file is a human and machine-readable document that declares an application's agent registration endpoints, OAuth authorization metadata locations, and agentic compliance posture.

## Core Rules

- The file MUST begin exactly with the H1 heading `# Auth.md` on the first line of the document body. Do not use variations like `# Authentication`, `# auth`, or `## Auth.md`.
- The file MUST document the registration endpoints explicitly (e.g., `POST /agent/identity`).
- The phrase "agentic registration" MUST appear in the document body.
- The file MUST be served publicly at `/auth.md` from the domain root (e.g., `https://example.com/auth.md`).
- Link to the OAuth authorization metadata endpoints using exact URLs — do not use relative paths.
- Do not embed credentials, secrets, or tokens in `auth.md`. Only reference public endpoint paths.

## When to Use

- Setting up a new service for WorkOS agentic authentication integration
- Repairing a failing `isitagentready.com` scanner check for the Auth.md requirement
- Updating registration endpoint documentation after OAuth or agent identity changes
- Auditing an existing `auth.md` for spec compliance before submitting to a scanner or registrar

## Suggested Process

1. **Create the file**: Create `auth.md` in the root workspace directory (`public/auth.md` for static sites, root for Workers). Ensure it will be served publicly at `/auth.md`.

2. **Write the required header**: The first non-empty line MUST be exactly:
   ```
   # Auth.md
   ```
   Follow with a brief one-paragraph description of the service and its agentic registration support.

3. **Add the required phrase**: Include "agentic registration" in the first or second paragraph — for example: "This service supports agentic registration for AI agent clients."

4. **Document registration endpoints**: List each registration endpoint with its HTTP method, path, and description:
   ```
   ## Registration
   
   - `POST /agent/identity` — Register a new agent identity
   - `POST /agent/identity/callback` — Handle OAuth callback for agent sessions
   ```

5. **Link to OAuth metadata**: Add explicit links to the OAuth discovery endpoints:
   ```
   ## OAuth Metadata
   
   - Protected Resource: `/.well-known/oauth-protected-resource`
   - Authorization Server: `/.well-known/oauth-authorization-server`
   ```

6. **Deploy and verify**: Confirm the file is publicly accessible at `/auth.md` via `curl https://yourdomain.com/auth.md`. Check HTTP status `200 OK` and correct `Content-Type: text/markdown` or `text/plain`.

7. **Run scanner check**: Submit the domain to `isitagentready.com` and confirm the Auth.md check passes. Remediate any field failures reported by the scanner.

## Output Format

- `/auth.md` (or `public/auth.md`) — Markdown text file served publicly at `/auth.md`

## Checklist

- [ ] File is named `auth.md` (lowercase) and committed to the correct location.
- [ ] First line of the document body is exactly `# Auth.md`.
- [ ] Document contains the phrase "agentic registration".
- [ ] HTTP registration markers (`POST /agent/identity` etc.) are clearly documented.
- [ ] Points to `/.well-known/oauth-protected-resource` with explicit URL.
- [ ] Points to `/.well-known/oauth-authorization-server` with explicit URL.
- [ ] File is publicly accessible at `/auth.md` (verified via `curl`).
- [ ] Response status is `200 OK` with text content type.
- [ ] `isitagentready.com` Auth.md scanner check passes.

## Related Skills

- **configure-oauth-metadata**: Set up the `/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server` endpoints that `auth.md` references.
- **debug-workos-integration**: Troubleshoot WorkOS agent registration and scanner failures.
- **configure-agent-headers**: Expose `auth.md` presence via HTTP Link headers for passive discovery.
\n### 2026: Auth.md Enhancements

- **auth.md spec evolution (mid-2026):** The `## MCP Servers` section now requires a `transport` field (`streamable-http` or `sse`). The isitagentready.com scanner rejects auth.md files that reference SSE-only MCP servers without a `streamable-http` transport declaration.
- **Validation before publish:** Run `curl -s "https://isitagentready.com/check?url=YOUR_DOMAIN"` after every auth.md change to catch scanner errors before they affect agent registration flows. Do not rely on manual inspection alone.\n