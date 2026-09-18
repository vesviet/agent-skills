---
name: develop-mobile-app
description: Architect high-performance mobile applications using React Native New Architecture, Hermes bytecode engine, TurboModules/JSI, Bridgeless mode, FlashList recycling, Reanimated worklets, and offline-first state persistence with MMKV and WatermelonDB. Use when building or optimizing React Native apps, virtualizing heavy lists, creating 60/120 FPS UI animations, or designing offline-first mobile sync architectures.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Develop Mobile App

Use this skill to design, implement, and optimize production-grade React Native and Expo applications utilizing New Architecture, off-thread UI animations, list recycling, and offline-first synchronization.

## When to Use

- configuring React Native New Architecture (Hermes engine, TurboModules, Fabric renderer, Bridgeless mode)
- replacing sluggish `FlatList` implementations with Shopify `FlashList` to eliminate blank scroll frames
- implementing non-blocking 60/120 FPS gesture-driven animations via Reanimated worklets
- establishing offline-first data persistence with MMKV key-value caching and WatermelonDB relational SQLite
- wiring network state detection (`NetInfo`) with TanStack Query offline cache and optimistic mutation queues
- profiling frame drops, cold-start time-to-interactive (TTI < 1.5s), and memory retain cycles

## Core Rules

- **Enforce React Native New Architecture & Bridgeless Mode**: mandate Hermes engine bytecode compilation, TurboModules with direct C++ JSI bindings (bypassing the legacy JSON bridge), and Fabric concurrent renderer; ban legacy asynchronous bridge dependencies
- **Mandate FlashList over FlatList for Virtualized Lists**: replace `FlatList` with `@shopify/flash-list` for data collections >10 items; require calibrated `estimatedItemSize`, recycling-safe component keys, and zero blank area renders
- **Execute Gestures & Animations on UI Thread**: continuous physics animations and gestures must run exclusively on the native UI thread using React Native Reanimated worklets (`'worklet'`); never drive frame animations across the JS thread
- **Tiered Offline-First Storage Hierarchy**: store synchronous auth tokens, preferences, and flags in `react-native-mmkv` via JSI (never async `AsyncStorage`); store complex relational entities (>1,000 records) in WatermelonDB SQLite with observable queries
- **Network-Aware Mutation Replay**: monitor connectivity via `@react-native-community/netinfo` bound to TanStack Query `onlineManager`; offline mutations must enqueue in persistent storage and replay deterministically upon reconnect
- **Optimistic UI Updates with Atomic Rollback**: user interactions must update UI immediately; failed mutations must roll back state cleanly and alert the user via non-blocking banners or haptics
- **Prevent Memory Leaks & Retain Cycles**: release native subscriptions, geolocation watches, timers, and image cache allocations during component unmount cleanup
- detailed architecture specs and recipes: [`references/react-native-new-architecture-and-offline-specs.md`](references/react-native-new-architecture-and-offline-specs.md)

## Suggested Process

### 1. Configure New Architecture Runtime
Verify Hermes compilation (`jsEngine: "hermes"`) and Bridgeless mode (`newArchEnabled: true`) in `app.json` or native build configs. Ensure all native module dependencies provide TurboModule/JSI specifications.

### 2. Implement Virtualized Lists with FlashList
Replace `FlatList` with `FlashList`. Calibrate `estimatedItemSize` based on average rendered item dimensions. Use stable item keys and avoid stateful closures inside `renderItem` that break item recycling.

### 3. Build UI-Thread Animations with Reanimated
Attach gesture handlers (`react-native-gesture-handler`) and define animated styles via `useAnimatedStyle`. Annotate native driver callbacks with `'worklet'` to ensure 60/120 FPS execution off the JS thread.

### 4. Implement Offline Storage & Cache Layer
Configure `react-native-mmkv` for instant synchronous key-value retrieval. Configure WatermelonDB schema and models for relational data. Hook TanStack Query persistence adapter to MMKV storage.

### 5. Wire Connectivity Listeners & Optimistic Queues
Connect `@react-native-community/netinfo` to query client online listeners. Wire optimistic mutation handlers with `onMutate` rollback snapshots and persistent background task replay.

### 6. Benchmark & Profile Performance
Measure TTI (< 1.5s cold start), JS thread frame drop rate (< 1%), and memory footprint under rapid scrolling. Verify offline interaction and clean reconnect synchronization.

## Checklist

- [ ] React Native New Architecture enabled (`newArchEnabled: true`) with Hermes bytecode compilation
- [ ] lists virtualized using `FlashList` with calibrated `estimatedItemSize` and verified zero blank frames
- [ ] animations and gestures execute on native UI thread using Reanimated worklets (`'worklet'`)
- [ ] synchronous key-value storage powered by MMKV via JSI; `AsyncStorage` eliminated
- [ ] relational entities persisted via WatermelonDB with observable database queries
- [ ] network connectivity monitored via `NetInfo` and synchronized with query cache `onlineManager`
- [ ] optimistic mutations provide instant UI feedback with reliable error rollback
- [ ] native event listeners, geolocation watchers, and timers cleaned up on unmount
- [ ] `contracts/schemas/implementation-result.json` emitted with performance benchmarks and test evidence

## Output Contracts

When completing a mobile implementation slice, emit:

- **`contracts/schemas/implementation-result.json`** — Declares modified files, component additions, performance benchmarks (TTI, FPS), and test results.

## Failure Modes

- **FlashList Blank Area Regression**: missing or inaccurate `estimatedItemSize` causes layout shifts and blank spaces during high-velocity fling scrolls. Mitigation: profile item heights across device screen sizes and set accurate `estimatedItemSize`.
- **JS Thread Frame Dropping**: complex computations or JSON parsing execute on the JS thread during user gestures. Mitigation: offload calculations to Web Workers / C++ JSI or chunk operations across frame cycles.
- **Offline Mutation Conflict**: stale cached data overwrites newer server changes during reconnect replay. Mitigation: implement vector clocks or server-wins timestamp resolution with client notification.
- **MMKV Multi-Process Crash**: accessing the same MMKV instance from background extensions without multi-process encryption locks. Mitigation: configure explicit MMKV instance IDs with encryption keys.

## Related Skills

- **add-ui-component**: Author and style mobile UI components conforming to Apple HIG and Material Design 3
- **deploy-mobile-app**: Configure EAS Build pipelines, code signing, OTA updates, and store compliance
- **performance-profiling**: Measure cold-start TTI, memory allocation, and frame render times
- **write-tests**: Author behavioral unit and integration test suites for mobile components and offline stores
- **integrate-api-client**: Connect mobile clients to backend REST, GraphQL, or gRPC endpoints
