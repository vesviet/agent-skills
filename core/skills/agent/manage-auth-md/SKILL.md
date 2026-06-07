---
name: manage-auth-md
description: Use when creating, updating, or auditing the /auth.md file at the repository root to ensure agentic registration discovery compliance.
---

# Manage Auth.md

Use this skill when adding or updating the Agentic Registration Discovery file (`/auth.md`) to comply with WorkOS and `isitagentready.com` standards.

## Core Rules

- The file MUST begin exactly with the H1 heading `# Auth.md`. Do not use variations.
- The file MUST document the registration endpoints explicitly (e.g., `POST /agent/identity`).
- The phrase "agentic registration" should be present.
- It MUST be served from the root of the domain (`/auth.md`).

## Suggested Process
1. Create the `auth.md` file in the root workspace directory.
2. Formulate the header and intro text containing "agentic registration".
3. Write clear documentation for the registration and callback routes.
4. Verify link references to the oauth authorization metadata endpoints.
5. Deploy `auth.md` to ensure it is publicly served at `/auth.md`.

## Checklist

- [ ] File is named `auth.md`.
- [ ] First line is strictly `# Auth.md`.
- [ ] HTTP registration markers are clearly documented.
- [ ] Points to `/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server`.
- [ ] Contains the mandatory phrase "agentic registration".

## Related Skills

- **configure-oauth-metadata**: Set up the corresponding `agent_auth` blocks.
- **debug-workos-integration**: Troubleshoot scanner failures.
