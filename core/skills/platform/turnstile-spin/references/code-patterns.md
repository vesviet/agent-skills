# Turnstile Spin — Code Patterns (Reference)

Code samples extracted from `SKILL.md` to keep the main file under 200 lines.
Load this file when implementing a siteverify Worker, wiring frontend token
handling, or reviewing the integration.

## Frontend Integration Example

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

## Backend siteverify Worker Implementation

Always verify the client token server-side via a secure endpoint. Never invoke siteverify directly from the web client.

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

      // Query Cloudflare validation endpoint
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

## Widget Modes Reference

- **`managed`**: The default and most robust challenge mode. Cloudflare analyzes user telemetry and behavior dynamically. If suspicious signals are present, it prompts the user with an interactive challenge. Ideal for checkout funnels, user login pages, and password resets.
- **`non-interactive`**: Invisible challenge using browser telemetry signals only. If the browser is heavily privacy-hardened or tracking protections are blocked, this challenge type may fail or fall back, so it should be used for medium-risk actions (e.g., search forms).
- **`invisible`**: Fully invisible CAPTCHA with no visual indicator. It presents the highest risk of false positives (legitimate users being blocked), so it must be selected carefully for low-risk checkpoints where seamless flow is prioritized.
- **Rule of Thumb**: Always select the least-intrusive mode that satisfies the site's security threat model.
