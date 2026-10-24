# 2026 Mobile Standards & Patterns — Consolidated Research Summary

## Overview
Deep research conducted September 2026 across React Native New Architecture, Hermes Engine, Expo SDK/EAS evolution, Apple/Google Store AI compliance, and mobile performance optimization.

---

## 1. React Native New Architecture (Mandatory 2026)

### Expo SDK Progression
| SDK | Release | New Architecture Status | Key Changes |
|-----|---------|------------------------|-------------|
| **SDK 52** (Nov 2024) | Default enabled for new projects | Opt-in for existing | `newArchEnabled: true` default; JSC removed; Hermes mandatory |
| **SDK 53** | Default enabled | Opt-out possible | Recommended for migration stability |
| **SDK 54** | Default enabled | Opt-out possible | Last SDK with opt-out capability |
| **SDK 55+** (RN 0.82+) | **Always enabled, cannot disable** | No opt-out | React Native 0.82 first to remove legacy bridge option |
| **SDK 56** (May 2026) | RN 0.85 + React 19.2 | Hermes bytecode diffing default | Expo UI production-ready; Widgets stable |
| **SDK 57** (Jun 2026) | RN 0.86 | Hermes V1 regressions fixed | 57.0.9 (memory), 57.0.17 (dev startup) |

### Three Pillars
1. **JSI (JavaScript Interface)**: Direct C++ binding, synchronous native calls, 40× faster bridge latency
2. **Fabric Renderer**: Concurrent, C++, synchronous layout, 55-60 fps scrolling vs 30-45 fps legacy
3. **TurboModules**: Lazy-loaded, typed, faster startup (200-400ms saved), strict TypeScript types
4. **Codegen**: Typed spec files (TS/Flow); native code generated from interfaces
5. **Bridgeless Mode**: Complete legacy Bridge thread disable, maximum memory savings

---

## 2. Hermes Engine Evolution (2026)

### Hermes V1 (SDK 56+)
- **Bytecode diffing enabled by default**
- **Chrome DevTools Protocol**: Debug via JavaScript Inspector (not Remote JS Debugging)

### Known Regressions & Fixes
| Issue | Symptoms | Fix |
|-------|----------|-----|
| **Memory regression** | Drastic memory increase with `react-native-worklets`/`reanimated` | Pin `expo@57.0.9+` (RN 0.86.2) |
| **Dev startup regression** | Increased startup time in development | Pin `expo@57.0.17+` (RN 0.86.3) |

---

## 3. Performance Optimization Priority (2026)

1. **New Architecture + Hermes V1** (mandatory baseline)
2. **FlashList over FlatList** for any list >10 items (recycling = native UICollectionView/RecyclerView)
3. **Eliminate unnecessary re-renders** with memoization
4. **Reanimated 4 worklets** for off-thread animations (60fps even with blocked JS thread)
5. **Metro tree-shaking** for bundle size reduction

### FlashList Migration Gains
- Typical: 2-3× smoother scrolling, zero blank frames on fling
- `estimatedItemSize` calibration critical per device screen size

### Reanimated 4+ (2026)
- **4.3.0+** (Mar 2026): CSS animations support SVG, `:hover` pseudo-selectors
- **4.4.0** (May 2026): Platform-backed CSS animation engine on iOS
- **4.5.0** (Jun 2026): CSS Core Animation gains shadow, background, border props
- **Shared Element Transitions** on New Architecture (feature flag since Dec 2025)

---

## 4. Expo Router Migration (2026)

- **File-based routing** replaces React Navigation
- **SDK 55+**: Expo Router drops React Navigation + new features
- **Nested layouts, route groups, `useLocalSearchParams`**
- **Brownfield**: More flexibility for embedded Expo apps

---

## 5. EAS Build & Update Evolution (2026)

### EAS Update Patterns
- **Channels/Branches/Runtime versions**: Mature deployment patterns
- **Runtime version policy**: `runtimeVersion: { policy: "appVersion" }` recommended
- **Emergency rollback channels**: Dedicated rollback branches for instant JS bundle revert
- **Auto-submit**: `eas build --auto-submit` manages native code signing automatically
- **EAS CLI 14+**: Required for latest features

---

## 6. Apple App Store Compliance (2026)

### Guideline 4.3(b) Anti-Wrapper
Must demonstrate differentiated native functionality:
- Device hardware access (camera, sensors, biometrics)
- Offline persistence (SQLite, MMKV, WatermelonDB)
- Rich interactive UI (Reanimated, native gestures)
- Widgets, App Clips, Live Activities

### Guideline 1.2 AI UGC Moderation
- Real-time content filtering for AI-generated content
- User reporting mechanisms
- Offensive content blocking
- AI content labeling mandatory

### PrivacyInfo.xcprivacy (Mandatory)
- Required reason API declarations (UserDefaults, File timestamps)
- Tracking domain declarations
- All AI SDKs declared with required reason APIs

### iPad Testing
- Test on iPad simulator even if `ios.supportsTablet: false`
- Apple may reject if elements don't render properly on iPad

---

## 7. Google Play Compliance (2026)

### Target API 36 (Android 16)
- **Mandatory from August 31, 2026** for new apps/updates
- Wear OS/TV/Automotive: Target API 35 (Android 15)
- Existing apps: Target API 35 to remain available to new users
- Extension to November 1, 2026 available via Play Console

### AI Disclosure Mandate
- Declare generative AI features in Play Console declaration form
- Display prominent in-app notices
- Review restricted-content safeguards, in-app reporting, moderation

### Data Safety
- Document every third-party SDK's data collection, transmission, encryption
- Keep Data Safety synchronized with build (SDK inventory)
- Reconcile form and build — reject if they disagree

### Sensitive Categories
- **AI-generated content**: safeguards, reporting, moderation, honest capability description
- **Financial features**: exact product type, country requirements, licenses, disclosures, data handling

### Release Gate Requirements
1. Data safety: Code/SDK inventory reconciled to declarations
2. Store listing: Approved copy/assets matching current functionality
3. Reviewer access: Working credentials, complete instructions

---

## 8. Crash Reporting & Symbolication (2026)

- **Hermes sourcemaps**: Automated upload in EAS post-build hook
- **Native dSYMs**: iOS debug symbols uploaded to Sentry/Bugsnag
- **Android ProGuard/R8 mappings**: Uploaded for crash symbolication
- **Hermes bytecode diffing**: Enabled by default in SDK 56+

---

## 9. Offline-First Architecture (2026)

### Tiered Storage Hierarchy
| Tier | Technology | Use Case | Access Pattern |
|------|------------|----------|----------------|
| **L1** | `react-native-mmkv` (JSI) | Auth tokens, prefs, flags | Synchronous, instant |
| **L2** | WatermelonDB (SQLite) | Relational entities >1K records | Observable queries |
| **L3** | TanStack Query v5 | Server state cache | Background sync, dedup |

### Network-Aware Mutation Replay
- `@react-native-community/netinfo` → TanStack Query `onlineManager`
- Offline mutations enqueued in persistent storage
- Deterministic replay on reconnect with vector clocks/server-wins timestamp
- Optimistic UI updates with atomic rollback (`onMutate`/`onError`/`onSettled`)

### Memory Leak Prevention
- Release native subscriptions, geolocation, timers, image caches on unmount
- Explicit MMKV instance IDs with encryption keys for multi-process safety

---

## 10. Cross-Skill Integration: Mobile → Backend → Frontend

```
develop-mobile-app
├── New Architecture mandatory (SDK 55+)
├── FlashList virtualization
├── Reanimated 4 worklets + CSS Core Animation
├── Tiered offline: MMKV + WatermelonDB + TanStack Query v5
├── Expo Router file-based routing
├── Codegen TypeScript specs for TurboModules
└── Performance profiling (Expo inspector, flame graphs)
    ↓
deploy-mobile-app
├── EAS Build multi-env profiles
├── EAS Update channels + rollback
├── Apple 4.3(b) + 1.2 AI compliance
├── Google Play Target API 36 + AI disclosure
├── PrivacyInfo.xcprivacy + Data Safety
├── Hermes sourcemaps + dSYMs + ProGuard upload
└── Expo SDK 55+ / EAS CLI 14+
    ↓
integrate-api-client (frontend) / backend APIs
├── Orval OpenAPI → TanStack Query v5 + MSW v2
├── React 19 use() for RSC + TanStack Query client
├── useActionState for forms + useMutation for complex
└── Streaming AI responses with useReducer
```

---

## 11. Key References

- **Expo New Architecture**: https://docs.expo.dev/guides/new-architecture
- **Expo SDK 56/57 Changelog**: https://expo.dev/changelog
- **React Native New Architecture**: https://reactnative.dev/blog/2026/06/11/react-native-0.86
- **Reanimated Changelog**: https://swmansion.com/changelog/react-native-reanimated
- **Hermes Engine**: https://docs.expo.dev/guides/using-hermes
- **EAS Update**: https://docs.expo.dev/eas-update/deployment
- **Apple Guidelines**: App Store Review Guidelines 4.3(b), 1.2
- **Google Play Target API**: https://playstore.solutions/blog/google-play-policy-changes-2025
- **FlashList**: https://shopify.github.io/flash-list
- **Expo Router**: https://docs.expo.dev/router/introduction