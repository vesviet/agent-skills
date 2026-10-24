# develop-mobile-app — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### React Native New Architecture (Mandatory 2026)
- **SDK 52+**: New Architecture enabled by default for new projects
- **SDK 55+ (React Native 0.82+)**: New Architecture **always enabled, cannot be disabled**
- **Three Pillars**:
  - **JSI (JavaScript Interface)**: Direct C++ binding, synchronous native calls, 40× faster bridge latency
  - **Fabric Renderer**: Concurrent, C++, synchronous layout, 55-60 fps scrolling
  - **TurboModules**: Lazy-loaded, typed, faster startup (200-400ms saved), strict TypeScript types
- **Bridgeless Mode**: Complete legacy Bridge thread disable, maximum memory savings
- **Codegen**: Typed spec files (TypeScript/Flow); native code generated from TS interfaces

### Hermes Engine Evolution (2026)
- **Hermes V1** (SDK 56+): Bytecode diffing enabled by default
- **Memory regression**: Increased memory with `react-native-worklets`/`reanimated` — fixed in `expo@57.0.9+` (RN 0.86.2)
- **Dev startup regression**: Increased startup time in development — fixed in `expo@57.0.17+` (RN 0.86.3)
- **Chrome DevTools Protocol**: Hermes apps debug via JavaScript Inspector (not Remote JS Debugging)

### Expo SDK 56/57 Features (2026)
- **SDK 56** (May 2026): React Native 0.85 + React 19.2, Hermes bytecode diffing default, Expo UI production-ready, Widgets stable
- **SDK 57** (June 2026): React Native 0.86, prebuilt artifacts for major libraries, build time statistics
- **Expo Modules API**: All modules support New Architecture by default
- **Expo Router**: File-based routing replaces React Navigation

### Performance Optimization Priority (2026)
1. **New Architecture + Hermes V1** (mandatory baseline)
2. **FlashList over FlatList** for any list beyond a screen (recycling = native UICollectionView/RecyclerView)
3. **Eliminate unnecessary re-renders** with memoization
4. **Reanimated 4 worklets** for off-thread animations (60fps even with blocked JS thread)
5. **Metro tree-shaking** for bundle size reduction

### Reanimated 4+ (2026)
- **4.3.0+** (Mar 2026): CSS animations support SVG components, `:hover` pseudo-selectors
- **4.4.0** (May 2026): Platform-backed CSS animation engine on iOS
- **4.5.0** (Jun 2026): CSS Core Animation gains shadow, background, border props
- **Shared Element Transitions** on New Architecture (feature flag since Dec 2025)
- **Worklets 0.11+** compatibility required

### Offline-First Architecture (2026)
- **MMKV** via JSI: Synchronous key-value (never async `AsyncStorage`)
- **WatermelonDB**: Relational SQLite with observable queries for >1,000 records
- **TanStack Query v5**: Persistence adapter to MMKV, `onlineManager` via `NetInfo`
- **Optimistic mutations**: Full lifecycle (`onMutate` snapshot + `onError` rollback + `onSettled` invalidate)
- **Vector clocks / server-wins timestamp**: Conflict resolution for offline mutation replay

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| New Architecture recommended | **New Architecture mandatory**: SDK 55+ cannot disable; Bridgeless mode required for production |
| Hermes optional | **Hermes V1 mandatory**: Default engine, bytecode diffing, Chrome DevTools debugging |
| FlashList recommended | **FlashList mandatory for >10 items**: Calibrated `estimatedItemSize`, recycling-safe keys |
| Reanimated worklets | **Reanimated 4+ CSS Core Animation**: Platform-backed iOS engine, SVG support, pseudo-selectors |
| Offline storage basic | **Tiered hierarchy**: MMKV (sync, JSI) for tokens/prefs; WatermelonDB (SQLite) for relational >1K records |
| TanStack Query basic | **TanStack Query v5**: `queryOptions` factories, `useActionState` for forms, persistence to MMKV |
| NetInfo basic | **`onlineManager` integration**: Deterministic offline mutation queue with persistent replay |

### 2. New 2026 Patterns to Add
- **Expo SDK Version Requirements**: Minimum SDK 53 for New Architecture stability; SDK 55+ for production
- **Codegen TypeScript Specs**: TurboModule interfaces defined in TS, native code generated
- **React Native 0.85+ / React 19.2**: Concurrent features, `use()` hook, `useActionState`, `useOptimistic`
- **Expo Router File-Based Routing**: Replaces React Navigation; nested layouts, route groups
- **Performance Profiling Workflow**: Expo built-in inspector, flame graphs, Metro bundle analyzer
- **Hermes V1 Regression Management**: Pin `expo@57.0.9+` for memory, `expo@57.0.17+` for dev startup
- **Shared Element Transitions**: Reanimated 4 feature flag for New Architecture transitions
- **Metro Tree-Shaking**: Bundle size optimization for production

### 3. Checklist Additions
- [ ] Expo SDK >= 53 (55+ recommended for production — New Architecture mandatory)
- [ ] `newArchEnabled: true` and `jsEngine: "hermes"` in `app.json` (Bridgeless mode for production)
- [ ] All native dependencies provide TurboModule/JSI specifications (verified via `expo doctor`)
- [ ] `FlatList` completely replaced with `@shopify/flash-list` for all virtualized lists
- [ ] `estimatedItemSize` calibrated per device screen size; zero blank frames verified
- [ ] All animations/gestures on UI thread via Reanimated 4 worklets (`'worklet'` annotated)
- [ ] Reanimated 4.4+ CSS Core Animation used for iOS platform-backed animations
- [ ] Shared Element Transitions enabled (feature flag) for New Architecture transitions
- [ ] `react-native-mmkv` via JSI for synchronous key-value (auth tokens, prefs, flags)
- [ ] WatermelonDB schema/models for relational entities (>1,000 records) with observable queries
- [ ] TanStack Query v5 `queryOptions` factories for centralized query keys/fetchers
- [ ] TanStack Query persistence adapter connected to MMKV storage
- [ ] `@react-native-community/netinfo` bound to `onlineManager` for connectivity detection
- [ ] Optimistic mutations: `onMutate` snapshot + `onError` rollback + `onSettled` invalidate
- [ ] Vector clocks or server-wins timestamp resolution for offline mutation conflicts
- [ ] Native subscriptions, geolocation, timers, image caches cleaned up on unmount
- [ ] Cold-start TTI < 1.5s, JS thread frame drop < 1%, memory footprint under rapid scroll
- [ ] Expo Router file-based routing implemented; React Navigation removed
- [ ] `contracts/schemas/implementation-result.json` emitted with performance benchmarks

### 4. Failure Mode Additions
- **New Architecture migration blockers**: Third-party library lacks TurboModule support. Mitigation: `expo doctor` audit; migrate to Expo Modules API alternatives; prebuilt artifacts in SDK 56+.
- **FlashList blank frames on fling scroll**: Inaccurate `estimatedItemSize`. Mitigation: Profile item heights across device sizes; set accurate `estimatedItemSize`.
- **JS thread frame drops during gestures**: Complex computations on JS thread. Mitigation: Offload to Web Workers / C++ JSI; chunk operations across frame cycles.
- **Offline mutation conflict on reconnect**: Stale cache overwrites server changes. Mitigation: Vector clocks or server-wins timestamp with client notification.
- **MMKV multi-process crash**: Background extension access without encryption locks. Mitigation: Explicit MMKV instance IDs with encryption keys.
- **Hermes V1 memory regression**: `expo@57.0.0-57.0.8` memory spike with worklets/reanimated. Mitigation: Pin `expo@57.0.9+`.
- **Hermes V1 dev startup regression**: `expo@57.0.0-57.0.16` slow dev startup. Mitigation: Pin `expo@57.0.17+`.
- **Reanimated legacy proxy crashes**: Stale animated values after app pause. Mitigation: Update to Reanimated 4.5.3+ (Jul 2026).
- **Metro bundle bloat**: Unused code in production bundle. Mitigation: Metro tree-shaking; analyze with `expo export --analyze`.

### 5. Output Contract Updates
- Update `contracts/schemas/implementation-result.json` with: Expo SDK version, New Architecture status, Hermes version, Reanimated version, FlashList migration status, performance benchmarks (TTI, FPS, memory)

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Expo SDK 55+ New Architecture mandatory enforcement | High |
| P0 | Hermes V1 with bytecode diffing + regression pinning | High |
| P0 | FlashList mandatory replacement for all virtualized lists | High |
| P0 | Reanimated 4+ worklets + CSS Core Animation on iOS | High |
| P1 | Tiered offline storage: MMKV (JSI) + WatermelonDB (SQLite) | High |
| P1 | TanStack Query v5: `queryOptions` factories + MMKV persistence | Medium |
| P1 | Optimistic mutations full lifecycle + conflict resolution | Medium |
| P1 | Expo Router file-based routing migration | Medium |
| P1 | Performance profiling workflow (Expo inspector, flame graphs) | Medium |
| P2 | Shared Element Transitions (feature flag) | Low |
| P2 | Metro tree-shaking bundle optimization | Low |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test `expo doctor` passes with all dependencies New Architecture compatible
- Verify FlashList zero blank frames under high-velocity fling scroll
- Verify Reanimated worklets execute 60fps with blocked JS thread
- Verify MMKV synchronous reads + WatermelonDB observable queries
- Verify TanStack Query v5 `queryOptions` pattern + MMKV persistence
- Verify optimistic mutation rollback on network error
- Verify Expo Router navigation works with New Architecture
- Benchmark cold-start TTI < 1.5s, frame drop < 1%