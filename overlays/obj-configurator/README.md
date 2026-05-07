# OBJ 3D Configurator Overlay

Project-specific conventions for the 3D Product Configurator — an interactive WebGL application for customizing apparel products.

**Depends on:** `overlays/astro-cloudflare`

- **Repo:** `D:\regna\cloudflare\obj`
- **Live:** Cloudflare Workers (`obj.sweet-voice-f606.workers.dev`)

## Specifics

- Astro v5 host + React Three Fiber (R3F) interactive islands
- Three.js / R3F for 3D rendering, Redux Toolkit + Zustand for state
- Prisma ORM + SQLite for design persistence (`prisma/schema.prisma`)
- Express.js backend (`server.js`) for local dev API
- Design Hub legacy codebase in `src/design-hub/` (React class → hooks migration)

## Rules

- `rules/obj-project-rules.md` — 3D engine, state management, design-hub architecture
