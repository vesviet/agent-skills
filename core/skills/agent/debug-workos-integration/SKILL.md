---
name: debug-workos-integration
description: Use when troubleshooting WorkOS Agentic Registration, Auth.md scanner errors, and SSO/Directory Sync issues.
---

# Debug WorkOS Integration

Use this skill to diagnose failures when `isitagentready.com` or another WorkOS validation scanner rejects your metadata or implementation.

## Core Rules

- Do NOT attempt to guess JSON schemas; always refer to the exact scanner logs (e.g., "anonymous registration requires anonymous.credential_types_supported").
- Validation scanners often enforce stable drafts over the latest experimental GitHub READMEs.
- `530 Origin DNS Error` from a scanner means the authorization server URL is dead or unreachable.

## Suggested Process
1. Run the target domain through the WorkOS agent readiness scanner tool.
2. Retrieve the diagnostic logs and identify the specific rule failures.
3. Compare the auth.md content and OAuth JSON schemas against the expected formats.
4. Correct DNS settings if a 530 error is returned.
5. Deploy corrections and re-run the validation scanner to verify.

## Checklist
- [ ] Scan output logs are retrieved and parsed.
- [ ] Header `# Auth.md` spelling and casing are verified.
- [ ] Schema structure for register_uri and claim_uri are corrected.
- [ ] Target domain is fully resolvable via public DNS.
- [ ] All registration endpoints are live and respond to POST requests.

## Related Skills

- **manage-auth-md**: Fix `auth.md` markers.
- **configure-oauth-metadata**: Fix JSON schema issues in the `agent_auth` block.
