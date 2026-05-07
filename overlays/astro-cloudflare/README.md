# Astro Cloudflare Overlay

Generic, reusable conventions for any Astro v5 project deployed to Cloudflare Pages/Workers. This overlay is stack-specific but project-agnostic.

## Tech Stack Coverage

- **Framework:** Astro v5 (SSG/SSR)
- **Styling:** Tailwind CSS v3
- **Infrastructure:** Cloudflare Pages, Workers, R2, Wrangler
- **Email:** Resend API (optional)
- **Anti-Spam:** Cloudflare Turnstile (optional)
- **Linting:** ESLint + Prettier + astro-check

## Included

- `rules/astro-cloudflare-conventions.md` — Architecture, component patterns, deploy, Wrangler config

This overlay should be composed with the global core and optionally with project-specific overlays.
