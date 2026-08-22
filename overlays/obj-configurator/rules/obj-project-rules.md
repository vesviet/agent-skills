# OBJ 3D Configurator — Project Rules

Project-specific conventions for the 3D Product Configurator.

## Architecture

```
src/
├── components/          ← Astro host + React entry (ConfiguratorApp.tsx, ProductSelector.tsx)
├── design-hub/          ← Legacy 3D engine (being migrated to R3F)
│   ├── App.jsx          ← Main React app shell
│   ├── engine/          ← Three.js scene, loaders, renderers
│   ├── components/      ← UI panels (toolbar, color picker, text editor)
│   ├── redux-tool/      ← Redux Toolkit slices (product, decal, text, camera)
│   ├── store/           ← Zustand stores (migrating from Redux)
│   ├── hooks/           ← Custom React hooks
│   ├── common/          ← Shared utilities
│   └── constants/       ← Configuration constants
├── layouts/             ← Astro page layouts
├── lib/                 ← Shared TypeScript utilities
└── pages/               ← Astro routing
```

## 3D Engine Rules (Three.js r171+ / R3F v9)

- GLB format for all 3D models — no legacy OBJ/MTL in new work.
- Materials must use sRGB color space for consistency.
- Sprite-based preview during drag operations — never recalculate DecalGeometry per frame.
- Dispose Three.js resources (geometries, materials, textures) on component unmount.
- Cap canvas resolution with `devicePixelRatio` max of 2 on mobile.

### R3F v9 Breaking Change
```jsx
// ❌ v8 (old)
const { gl } = useThree()   // WebGLRenderer

// ✅ v9 (current)
const { renderer } = useThree()  // unified WebGL/WebGPU renderer
```

### WebGPU Adoption (2026)
```jsx
import { WebGPURenderer } from 'three/webgpu'

// Zero-config upgrade with automatic WebGL 2 fallback
<Canvas gl={(canvas) => new WebGPURenderer({ canvas, antialias: true })}>
```

For new 3D work in this project, prefer `WebGPURenderer` with built-in WebGL 2 fallback.

## State Management

- **Redux Toolkit** for product configuration state (slices in `src/design-hub/redux-tool/`).
- **Zustand** for new features — gradual migration from Redux.
- Debounce continuous transforms (scale/rotate) to 100ms before dispatching to store.
- Never mutate Three.js objects directly from React render — use `useFrame` or refs.
- High-frequency physics updates: sync via `useFrame` + refs, NOT React state.

## Database (Prisma + SQLite)

- Schema in `prisma/schema.prisma`.
- Local dev DB at `prisma/dev.db`.
- Migrations in `prisma/migrations/`.
- Express.js API (`server.js`) for design CRUD during local dev.

## Performance

- Memoize React sub-components (`React.memo`) to prevent re-renders during 3D interaction.
- Use `Suspense` boundaries for lazy-loaded 3D assets.
- Target 60fps during interaction — profile with Chrome DevTools Performance panel.
- Use **Spector.js** in development to capture/replay WebGL draw calls (disable in production).
- Use **Chrome DevTools Shader Editor** (Chrome 124+) for WebGPU pipeline inspection.

## Build & Deploy

- `npm run dev` — concurrent Astro frontend + Express backend.
- `npm run build` — Astro build only (backend not bundled).
- `npm run deploy` — build + Wrangler Workers deploy.
