---
name: turnstile-spin
description: Implements end-to-end Cloudflare Turnstile CAPTCHA protection — widget creation, managed siteverify Worker deployment, and frontend integration — turning a "set up Turnstile" request into a validated, working integration. Use when adding bot protection to forms or gated flows in vanilla HTML, Next.js, Astro, SvelteKit, or Hugo projects.
---

# Turnstile Spin

Turns the prompt "set up Turnstile" into a working end-to-end integration: a widget, a deployed managed siteverify Worker, frontend snippets at every chosen insertion point, and a real validation pass before reporting success.

You are the agent. Run the wizard below by invoking the scripts under `scripts/` and branching on their JSON output. The scripts hold the deterministic logic (API calls, retry/error handling); your job is orchestration, codebase reading, confirmation, and the frontend edits.

Canonical instructions live at [`developers.cloudflare.com/turnstile/spin`](https://developers.cloudflare.com/turnstile/spin/). If the docs page and this file disagree, trust the docs page.

## Core Rules
- Do NOT write the Turnstile secret to disk. Only pass it via stdin to `wrangler secret put`.
- Do NOT skip validation (Step 11).
- Do NOT overwrite files without showing a diff.
- Do NOT deploy a Worker to a different account than the widget was created in.
- Do NOT call siteverify from the browser. Always: browser -> user's Worker -> siteverify.

## Suggested Process
1. Check credentials and account ID by running the auth-probe script.
2. Probe active domain settings, scans codebase layout, and present insertion plans.
3. Call api.cloudflare.com client endpoints to build the CAPTCHA widget.
4. Deploy siteverify Workers templates with wrangler.
5. Apply frontend changes and check responses via validate tool scripts.

## Checklist
- [ ] Account and API auth are verified.
- [ ] Target domain is registered for widget.
- [ ] Widget is created via Turnstile API.
- [ ] siteverify Worker is deployed.
- [ ] Frontend form submission gates on widget success.

## Related Skills
- **wrangler**: Manage deployment environments and bindings.
- **debug-workers-edge**: Troubleshoot execution at the edge.
