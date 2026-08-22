---
name: turnstile-spin
description: Implements end-to-end Cloudflare Turnstile CAPTCHA protection — widget creation, managed siteverify Worker deployment, and frontend integration — turning a "set up Turnstile" request into a validated, working integration. Use when adding bot protection to forms or gated flows in vanilla HTML, Next.js, Astro, SvelteKit, or Hugo projects.
---

# Turnstile Spin

Turns the prompt "set up Turnstile" into a working end-to-end integration: a widget, a deployed managed siteverify Worker, frontend snippets at every chosen insertion point, and a real validation pass before reporting success.

You are the agent. Run the wizard below by invoking the scripts under `scripts/` and branching on their JSON output. The scripts hold the deterministic logic (API calls, retry/error handling); your job is orchestration, codebase reading, confirmation, and the frontend edits.

Canonical instructions live at [`developers.cloudflare.com/turnstile/spin`](https://developers.cloudflare.com/turnstile/spin/). If the docs page and this file disagree, trust the docs page.

## When to Use

- adding bot protection to a form or gated flow (login, signup, checkout)
- integrating Turnstile into vanilla HTML, Next.js, Astro, SvelteKit, or Hugo
- deploying a managed `siteverify` Worker and wiring server-side validation
- choosing the least-intrusive widget mode for a given risk level
- re-triggering the widget on token expiry or backend validation failure

## Core Rules
- Do NOT write the Turnstile secret to disk. Only pass it via stdin to `wrangler secret put`.
- Do NOT skip validation (Step 11).
- Do NOT overwrite files without showing a diff.
- Do NOT deploy a Worker to a different account than the widget was created in.
- Do NOT call siteverify from the browser. Always: browser -> user's Worker -> siteverify.
- Always choose the least-invasive widget mode (`non-interactive` or `invisible`) that maintains security requirements, falling back to `managed` for critical checkpoints.
- Ensure that tokens are never reused; they are single-use and expire within 300 seconds. Re-trigger the Turnstile widget on any failed form submission.
- **WIDGET-MODE-SELECTION**: `managed` for login/checkout/password-reset (shows interactive challenge if suspicious); `non-interactive` for medium-risk (browser telemetry only, may fail in privacy-hardened browsers); `invisible` for low-risk only (highest false-positive risk).
- **TOKEN-REUSE-PREVENTION**: On backend validation failure, frontend MUST call `turnstile.reset(widgetId)` — do NOT show a generic error; user must complete a fresh challenge.
- **CSP-TURNSTILE-DOMAINS**: Add Cloudflare Turnstile script domains to the site's Content Security Policy (`script-src` and `frame-src`) before deployment — missing CSP entries silently block the widget.

## Retrieval Sources

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| Turnstile docs | `https://developers.cloudflare.com/turnstile/` | Core API reference, script widget parameters |

## Suggested Process
1. Check credentials and account ID by running the auth-probe script.
2. Probe active domain settings, scans codebase layout, and present insertion plans.
3. Call api.cloudflare.com client endpoints to build the CAPTCHA widget.
4. Deploy siteverify Workers templates with wrangler.
5. Apply frontend changes and check responses via validate tool scripts.
6. Guide the integration by choosing the right widget mode and setting up token expiration handling.
7. Implement frontend listeners to reset and re-render the Turnstile widget upon backend validation failure or token expiry.

### Widget Modes, Token Handling, and Verification

#### Widget Modes Selection
- **`managed`**: The default and most robust challenge mode. Cloudflare analyzes user telemetry and behavior dynamically. If suspicious signals are present, it prompts the user with an interactive challenge. Ideal for checkout funnels, user login pages, and password resets.
- **`non-interactive`**: Invisible challenge using browser telemetry signals only. If the browser is heavily privacy-hardened or tracking protections are blocked, this challenge type may fail or fall back, so it should be used for medium-risk actions (e.g., search forms).
- **`invisible`**: Fully invisible CAPTCHA with no visual indicator. It presents the highest risk of false positives (legitimate users being blocked), so it must be selected carefully for low-risk checkpoints where seamless flow is prioritized.
- **Rule of Thumb**: Always select the least-intrusive mode that satisfies the site's security threat model.

#### Token Expiry & Reuse Prevention
Turnstile validation tokens are single-use to prevent replay attacks and remain valid for exactly 300 seconds (5 minutes).
If validation fails on the backend, the token becomes spent. The frontend must immediately reset the widget instance rather than showing a generic submission failure.

##### Frontend Integration Example:
```html
<form id="auth-form" action="/verify" method="POST">
  <input type="email" name="email" required placeholder="name@domain.com" />
  <!-- Turnstile widget placeholder container -->
  <div id="cf-turnstile-container" class="cf-turnstile" data-sitekey="1x00000000000000000000AA" data-callback="onTurnstileSuccess"></div>
  <button type="submit">Submit Verification</button>
</form>

<script>
  let cfToken = null;

  function onTurnstileSuccess(token) {
    cfToken = token;
  }

  document.getElementById('auth-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!cfToken) {
      alert('Verification required. Please wait for security check to complete.');
      return;
    }

    try {
      const resp = await fetch('/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: e.target.email.value,
          cf_token: cfToken
        })
      });

      if (!resp.ok) {
        // Reset the token state and refresh the Turnstile widget dynamically
        cfToken = null;
        if (typeof turnstile !== 'undefined') {
          turnstile.reset('#cf-turnstile-container');
        }
        alert('Validation failed. Security challenge has been reset. Please try again.');
      } else {
        alert('Validation successful!');
      }
    } catch (err) {
      cfToken = null;
      if (typeof turnstile !== 'undefined') {
        turnstile.reset('#cf-turnstile-container');
      }
      alert('A network error occurred. Challenge reset, please try again.');
    }
  });
</script>
```

#### Backend verify Worker Endpoint Pattern
Always verify the client token server-side via a secure endpoint. Never invoke siteverify directly from the web client.

##### siteverify Worker Implementation:
```typescript
interface Env {
  TURNSTILE_SECRET_KEY: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405 });
    }

    try {
      const { cf_token } = await request.json() as { cf_token?: string };
      if (!cf_token) {
        return new Response(JSON.stringify({ success: false, message: 'Missing challenge token.' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      // Query Cloudstile validation endpoint
      const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          secret: env.TURNSTILE_SECRET_KEY,
          response: cf_token,
          remoteip: request.headers.get('CF-Connecting-IP') || ''
        })
      });

      const outcome = await res.json() as {
        success: boolean;
        'error-codes'?: string[];
      };

      if (!outcome.success) {
        return new Response(JSON.stringify({
          success: false,
          message: 'Failed verification challenge',
          errors: outcome['error-codes']
        }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      return new Response(JSON.stringify({ success: true, message: 'Token verified successfully.' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    } catch (err) {
      return new Response(JSON.stringify({ success: false, message: 'Internal server verify error' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }
};
```

## Checklist
- [ ] Account and API auth are verified.
- [ ] Target domain is registered for widget.
- [ ] Widget is created via Turnstile API.
- [ ] siteverify Worker is deployed.
- [ ] Frontend form submission gates on widget success.
- [ ] Widget mode (`managed`, `non-interactive`, or `invisible`) is explicitly selected based on use case constraints.
- [ ] Token reuse is prevented by resetting the widget via `turnstile.reset()` on submission failure.
- [ ] Token expiry (300-second window) is handled gracefully with automatic widget re-triggering.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Related Skills
- **wrangler**: Manage deployment environments and bindings.
- **debug-workers-edge**: Troubleshoot execution at the edge.
