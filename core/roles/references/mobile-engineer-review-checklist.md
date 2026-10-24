## Review Checklist

This reference checklist provides detailed engineering, validation, and security criteria for mobile application engineering to meet 2027 Agentic SWE standards.

### New Architecture & Engine Invariants
- **Hermes Bytecode Ahead-Of-Time (AOT) Compilation**: Hermes engine is strictly enabled (`jsEngine: "hermes"`); JS source code is precompiled into Hermes bytecode (`.hbc`), ensuring cold-start Time-to-Interactive (TTI) < 1.5s on mid-tier Android devices.
- **Direct C++ JSI Pointer Invocations**: Native module calls execute directly via JavaScript Interface (JSI) memory bindings, eliminating the legacy asynchronous JSON bridge and serialization bottlenecks.
- **TurboModules Lazy Initialization**: Native dependencies export TurboModule specifications and load lazily on demand rather than eagerly during app initialization.
- **Bridgeless Mode Verification**: App runs with `newArchEnabled: true` and legacy bridge dependencies completely excised; all native event dispatching uses C++ event emitters.

### List Recycling & Virtualization Invariants
- **Mandatory FlashList Adoption**: All dynamic feeds and collections > 10 items use `@shopify/flash-list` instead of `FlatList` or unvirtualized `ScrollView`.
- **Calibrated `estimatedItemSize`**: Every `FlashList` instance declares an accurate `estimatedItemSize` based on median rendered row heights, preventing layout recalculation shifts.
- **Zero Blank Areas on Scroll Fling**: High-velocity scrolling flings maintain smooth 60/120 FPS frame rates with zero blank/white rectangular rendering lapses.
- **Stable Item Keys & Recycled Cell Safety**: Items use immutable entity IDs as keys (`keyExtractor`); items avoid local unmanaged state closures that corrupt state upon cell recycling.
- **`overrideItemLayout` Optimization**: Heterogeneous item rows with variable fixed heights implement `overrideItemLayout` to eliminate dynamic measurement overhead.

### Offline-First & State Invariants
- **Synchronous MMKV Key-Value Caching**: High-frequency preferences, session tokens, and feature flags use `react-native-mmkv` via direct JSI memory access; asynchronous `AsyncStorage` is eliminated.
- **Relational WatermelonDB SQLite Persistence**: Complex datasets (> 1,000 entities) are managed via WatermelonDB with observable RxJS queries, updating UI automatically on local record changes.
- **Network State Synchronization**: Connectivity listeners (`@react-native-community/netinfo`) are wired directly to TanStack Query's `onlineManager` to halt network polling when offline.
- **Optimistic Mutations with Atomic Rollbacks**: Offline user actions apply immediately to the local cache, persist in a durable mutation queue, and revert cleanly on unrecoverable 4xx API errors.
- **Background Sync Guardrails**: Background synchronization uses native schedulers (`BGTaskScheduler` on iOS, `WorkManager` on Android) with battery and metered network constraints.

### UI Thread Animation Invariants
- **Reanimated Worklet Thread Isolation**: Continuous gestures and layout animations execute on the native UI thread via React Native Reanimated worklets (`'worklet'`).
- **Zero JavaScript Thread Starvation**: JS thread utilization remains < 30% during gestures; frame render times stay within the 16.6ms (60 FPS) or 8.3ms (120 FPS) budget.
- **Shared Value Driven Animations**: Gesture handlers (`react-native-gesture-handler`) update `useSharedValue` pointers directly without roundtripping through JS state or React re-renders.
- **Physics-Based Transitions**: Layout changes use native springs (`withSpring`) or timing curves (`withTiming`) rather than manual setInterval or requestAnimationFrame loops.

### EAS Build & Signing Invariants
- **Environment Isolation in `eas.json`**: Build profiles (`development`, `preview`, `production`) maintain distinct native bundle identifiers (`com.company.app.dev` vs `com.company.app`) and isolated environment variables.
- **Zero Secrets in Version Control**: iOS Distribution Certificates, Provisioning Profiles, and Android Keystores are stored exclusively in EAS Credentials or encrypted vaults; `.keystore`, `.p12`, and `.jks` are in `.gitignore`.
- **Clean Reproducible Builds**: Cloud and local builds execute with deterministic lockfiles (`package-lock.json` or `yarn.lock`) and explicit Node/JDK toolchain pins.

### OTA Update Boundaries & Rollbacks
- **Cryptographic Fingerprint Runtime Versioning**: `runtimeVersion` policy is configured to `"fingerprint"`, preventing incompatible JS bundles from deploying to mismatched native binaries.
- **Strict Binary Barrier Enforcement**: OTA updates via EAS Update NEVER contain native module additions, permission changes, or native configuration updates; all native changes mandate full binary store builds.
- **Emergency Rollback Channel**: A documented rollback procedure exists to instantly republish a known-healthy update group or revert to embedded native code without store review delays.

### Apple App Store Guidelines Invariants
- **Guideline 4.3(b) Anti-Wrapper Differentiated Value**: App delivers tangible native platform functionality (device sensors, camera, biometrics, offline storage, widgets) beyond a basic web wrapper or raw LLM chat interface.
- **Guideline 1.2 AI User-Generated Content Moderation**: Apps generating AI content include an active in-app reporting button for every generated message, a blocking mechanism, a terms of service EULA, and a 24-hour review SLA.
- **Apple Privacy Manifest (`PrivacyInfo.xcprivacy`)**: Manifest accurately declares all accessed APIs (`NSPrivacyAccessedAPITypes` for UserDefaults, file timestamps) and tracking domains.

### Google Play Compliance Invariants
- **Generative AI Policy Disclosure**: Generative AI features are declared in the Google Play Console declaration form and accompanied by clear in-app user notifications.
- **Data Safety SDK Inventory**: All bundled third-party SDKs are audited for network transmission, user tracking, and data encryption practices matching the Google Play Data Safety form.
- **Zero AI-Generated Spam**: Store listings, app screenshots, icons, and descriptions are human-verified and free from deceptive AI-generated bulk artifacts.

### Crash & Symbolication Invariants
- **Hermes Bytecode De-obfuscation**: Hermes bytecode sourcemaps are uploaded to Sentry or Bugsnag during release builds to translate hexadecimal memory offsets into accurate TypeScript line numbers.
- **Native dSYM & ProGuard Mapping Upload**: iOS dSYM bundles and Android ProGuard/R8 `mapping.txt` files are archived and uploaded automatically during EAS post-build workflows.
- **Production Telemetry & Crash Alerting**: Crash reporting is initialized before the first UI render; breadcrumbs capture offline transition events and network status without logging PII.
