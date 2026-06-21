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
- Always choose the least-invasive widget mode (`non-interactive` or `invisible`) that maintains security requirements, falling back to `managed` for critical checkpoints.
- Ensure that tokens are never reused; they are single-use and expire within 300 seconds. Re-trigger the Turnstile widget on any failed form submission.

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

### 2026: Widget Modes, Token Handling, and Verification

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

## Related Skills
- **wrangler**: Manage deployment environments and bindings.
- **debug-workers-edge**: Troubleshoot execution at the edge.
\n### 2026: Turnstile Modes and Reuse

- **Turnstile mode documentation:** There are three widget modes. The `managed` mode (automatic challenge, shows spinner if needed) is the default. The `non-interactive` mode (invisible, uses browser signals only) may fail in privacy-hardened browsers. The `invisible` mode (fully invisible) has the highest risk of false positives. Choose `managed` for checkout/login flows, and `non-interactive` only for low-value actions where friction must be zero.
- **Enterprise Turnstile token reuse:** Turnstile tokens are single-use and expire in 300 seconds. If your siteverify call fails due to token reuse, the client must re-execute the widget. Design the UX to re-trigger the widget on a failed submission rather than showing a generic error.
- **Content Security Policy (CSP) Updates:** Ensure CSP directives allow the loading of the Turnstile script and the execution of necessary background checks. Turnstile requires access to specific domains; keeping CSP updated is critical.
- **React and Framework Wrappers:** Use official or community-supported React components (such as `@marsidev/react-turnstile`) to ensure smooth lifecycle management of the widget. Unmounting and remounting widgets requires proper cleanup to avoid memory leaks.
- **Logging and Monitoring:** Track Turnstile solve rates and fallback occurrences in your application analytics. Unexpected spikes in challenges may indicate a configuration issue or a targeted attack.
- **Graceful Fallbacks:** If the Turnstile API is unreachable, your backend should be configured to gracefully fallback depending on the risk tolerance. Do not completely lock out users during an API outage if it can be avoided.
- **Testing Challenges:** Use Cloudflare's provided test sitekeys (e.g., `1x00000000000000000000AA`) to simulate passing, failing, and interactive challenges in your automated testing suite to verify the UI behaves appropriately in all scenarios.
- **Accessibility Integration:** The Turnstile widget is designed to be accessible, but ensure the surrounding container does not trap focus improperly. Verify that screen readers announce the widget state correctly.\n