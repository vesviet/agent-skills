# React Native New Architecture & Offline-First Specifications

## 1. React Native New Architecture & Engine Invariants

### 1.1 Hermes Bytecode Compilation & Memory Architecture
The Hermes JavaScript engine is mandatory for production mobile applications. It replaces standard runtime JIT compilation with Ahead-Of-Time (AOT) bytecode generation:
- **AOT Bytecode Precompilation**: Hermes parses and compiles JavaScript source files into optimized bytecode (`.hbc`) during native build time (`hermesc`). This eliminates JS parsing and compilation latency during application startup, slashing cold-start Time-To-Interactive (TTI) to under 1.5 seconds on mid-tier mobile chipsets.
- **Garbage Collection (Hades GC)**: Hermes utilizes Hades, a generational, concurrent, segmented garbage collector. Hades executes background compaction cycles concurrently on a dedicated background thread, virtually eliminating "stop-the-world" GC pauses that cause 60/120 FPS UI stutter.
- **Memory Footprint Optimization**: Bytecode is mapped directly from disk into read-only virtual memory (`mmap`). This minimizes private dirty RAM allocations and dramatically reduces Out-Of-Memory (OOM) termination risks on resource-constrained devices.

### 1.2 TurboModules & JSI (JavaScript Interface) Zero-Bridge Overhead
- **Legacy Bridge Elimination**: The legacy React Native bridge relied on asynchronous, serialized JSON message queues over a shared C++ message bus. This introduced serialization bottlenecks, latency spikes with large payloads, and non-deterministic message delivery.
- **Direct Memory Invocation (JSI)**: JSI is a lightweight C++ interface layer enabling JavaScript to hold direct references to host C++ objects and native platform APIs without serialization.
- **TurboModules**: Native modules written as TurboModules register synchronous and asynchronous methods via JSI bindings. Native modules are initialized lazily on-demand rather than eagerly upon application boot, reducing startup overhead.
- **Fabric Renderer**: The Fabric concurrent rendering engine creates a C++ shadow tree directly in memory, reconciling layout mutations and delegating native view updates directly via JSI.

### 1.3 Bridgeless Mode
Bridgeless mode completely disables the initialization of the legacy bridge runtime:
- All module lookups resolve directly through the TurboModule Registry.
- Native logging, exception handling, and device event dispatching occur via C++ native event emitters.
- Native dependency validation: Verify that every third-party native package exports TurboModule/Fabric specifications. If a legacy module is detected, replace it or wrap it with an explicit C++ JSI TurboModule adapter.

```json
// app.json configuration
{
  "expo": {
    "jsEngine": "hermes",
    "newArchEnabled": true
  }
}
```

---

## 2. Shopify FlashList Recycling & Virtualization Architecture

### 2.1 Cell Recycling Mechanics vs. FlatList Limitations
- **FlatList Flaws**: React Native's legacy `FlatList` unmounts offscreen components and creates new native views upon scrolling. Under high-velocity fling gestures, view creation cannot keep pace with scroll speed, producing white/blank rectangular patches and garbage collector thrashing.
- **FlashList Cell Recycling**: `@shopify/flash-list` retains a fixed pool of native view instances. When an item scrolls offscreen, its underlying native view container is recycled and rebound to new data rather than destroyed and reallocated. This completely eliminates blank areas and preserves 60/120 FPS scroll velocity.

### 2.2 Calibration of `estimatedItemSize`
To guarantee seamless cell positioning before full layout measurement:
- Every `FlashList` instance must specify `estimatedItemSize` based on realistic rendering dimensions.
- **Empirical Calibration**: Compute the weighted average height (or width for horizontal lists) of rendered items across standard viewport widths.
- If items have variable heights, calibrate `estimatedItemSize` to the median item height:
```tsx
import { FlashList } from "@shopify/flash-list";
import React, { useCallback } from "react";
import { View, Text, StyleSheet } from "react-native";

interface FeedItem {
  id: string;
  title: string;
  body: string;
}

export const FeedList: React.FC<{ items: FeedItem[] }> = ({ items }) => {
  const renderItem = useCallback(({ item }: { item: FeedItem }) => (
    <View style={styles.card}>
      <Text style={styles.title}>{item.title}</Text>
      <Text style={styles.body}>{item.body}</Text>
    </View>
  ), []);

  return (
    <FlashList
      data={items}
      renderItem={renderItem}
      estimatedItemSize={112}
      keyExtractor={(item) => item.id}
      drawDistance={250}
    />
  );
};

const styles = StyleSheet.create({
  card: { padding: 16, borderBottomWidth: StyleSheet.hairlineWidth, borderColor: "#E5E7EB" },
  title: { fontSize: 16, fontWeight: "600" },
  body: { fontSize: 14, color: "#4B5563", marginTop: 4 }
});
```

### 2.3 Recycling Layout Safety Invariants
- **Stable Keys**: Use unique entity IDs (`item.id`) for `keyExtractor`. Never use list indices.
- **No Stateful Closures in Items**: Do not maintain local unmanaged state inside list items that depends on view identity; state must derive from the item data payload.
- **`overrideItemLayout`**: When rendering heterogeneous rows with distinct fixed heights (e.g. headers vs. standard items), implement `overrideItemLayout` to bypass measurement overhead entirely.

---

## 3. UI-Thread Animations via Reanimated Worklets

### 3.1 The `'worklet'` Directive & Native Driver Execution
- **React Native Reanimated**: Offloads animation and gesture handling loops from the single-threaded JavaScript runtime to the native UI thread (Render thread / CADisplayLink).
- **Worklet Architecture**: JavaScript functions annotated with `'worklet'` at the top of their body are compiled into standalone bytecode snippets by the Babel/Metro plugin. They are copied into a secondary Hermes JS runtime running directly on the native UI thread.
- **Shared Values (`useSharedValue`)**: Mutable pointers accessible synchronously from both the JS thread and the UI thread. Value updates trigger immediate UI thread layout updates without asynchronous serialization.

### 3.2 60/120 FPS Gesture Handling
Combine `react-native-gesture-handler` with Reanimated to build interactive physics-based gestures:
```tsx
import React from "react";
import { StyleSheet, View } from "react-native";
import { GestureDetector, Gesture } from "react-native-gesture-handler";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from "react-native-reanimated";

export const SwipeableCard: React.FC = () => {
  const translateX = useSharedValue(0);
  const contextX = useSharedValue(0);

  const panGesture = Gesture.Pan()
    .onStart(() => {
      'worklet';
      contextX.value = translateX.value;
    })
    .onUpdate((event) => {
      'worklet';
      translateX.value = contextX.value + event.translationX;
    })
    .onEnd(() => {
      'worklet';
      // Snap back or dismiss using physics spring
      translateX.value = withSpring(0, { damping: 15, stiffness: 120 });
    });

  const animatedStyle = useAnimatedStyle(() => {
    'worklet';
    return {
      transform: [{ translateX: translateX.value }],
    };
  });

  return (
    <GestureDetector gesture={panGesture}>
      <Animated.View style={[styles.box, animatedStyle]} />
    </GestureDetector>
  );
};

const styles = StyleSheet.create({
  box: { width: "100%", height: 100, backgroundColor: "#3B82F6", borderRadius: 12 },
});
```

---

## 4. Offline-First Architecture & State Persistence

### 4.1 Storage Tiering Strategy
Mobile applications require a tiered storage hierarchy:
1. **Synchronous Key-Value Layer (`react-native-mmkv`)**:
   - Backed by Tencent's MMKV memory-mapped key-value store using JSI.
   - Synchronous read/write operations without Promise overhead (~30x faster than `AsyncStorage`).
   - Use for auth tokens, feature flags, user preferences, and small JSON caches.
2. **Relational SQLite Layer (WatermelonDB)**:
   - Optimized for multi-thousand record datasets.
   - Separate SQLite process thread; lazy loading loads only visible attributes into memory.
   - Observable queries via RxJS: UI components automatically re-render when underlying records mutate.
3. **Query Cache Persistence (TanStack Query + MMKV)**:
   - Persistent client-side hydration for server-state queries.

### 4.2 Network Connectivity & NetInfo Integration
Monitor network connectivity via `@react-native-community/netinfo` and wire it directly to TanStack Query's `onlineManager`:
```typescript
import NetInfo from "@react-native-community/netinfo";
import { onlineManager } from "@tanstack/react-query";

export function initializeNetworkListener(): void {
  onlineManager.setEventListener((setOnline) => {
    return NetInfo.addEventListener((state) => {
      const isConnected = Boolean(state.isConnected && state.isInternetReachable);
      setOnline(isConnected);
    });
  });
}
```

### 4.3 Optimistic Mutations & Rollback Queue
Every offline write must:
1. Immediately apply the mutation to the client query cache.
2. Persist the pending mutation into an offline mutation queue stored in MMKV.
3. If the device is online, execute the network request immediately.
4. If the request fails or the device is offline, retain the queued action.
5. Replay pending mutations sequentially upon network reconnection.
6. If an unrecoverable 4xx error occurs, revert the cache snapshot and dispatch a user notification.

```typescript
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { MMKV } from "react-native-mmkv";

const storage = new MMKV({ id: "mutation-queue" });

export function useOptimisticUpdateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (updatedTodo: { id: string; text: string; completed: boolean }) => {
      const response = await fetch(`/api/todos/${updatedTodo.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedTodo),
      });
      if (!response.ok) throw new Error("Mutation rejected");
      return response.json();
    },
    onMutate: async (newTodo) => {
      await queryClient.cancelQueries({ queryKey: ["todos"] });
      const previousTodos = queryClient.getQueryData(["todos"]);
      queryClient.setQueryData(["todos"], (old: any) =>
        old ? old.map((t: any) => (t.id === newTodo.id ? { ...t, ...newTodo } : t)) : []
      );
      return { previousTodos };
    },
    onError: (err, newTodo, context) => {
      if (context?.previousTodos) {
        queryClient.setQueryData(["todos"], context.previousTodos);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });
}
```

### 4.4 Background Synchronization
- **iOS**: Register background refresh tasks using `BGTaskScheduler` (`BGAppRefreshTask`). Respect system battery, network constraints, and power budgets.
- **Android**: Schedule background sync via Android `WorkManager` with `Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build()`.
- Never execute long-running background sync loops on unmetered mobile data without user consent.

---

## 5. Performance Budgets & Production Telemetry

### 5.1 Hard Performance Thresholds
- **Cold Start Time-to-Interactive (TTI)**: < 1,500ms on 4GB RAM Android devices.
- **Frame Render Budget**: 16.6ms (60 FPS) / 8.3ms (120 FPS ProMotion / High Refresh Rate displays).
- **JS Thread Utilization**: < 30% sustained during continuous scroll fling.
- **App Startup Memory**: < 120MB baseline RSS.

### 5.2 Profiling Procedures
1. Profile JavaScript execution and flame charts using the React Native DevTools Performance Profiler.
2. Measure native frame rates and memory allocations using Xcode Instruments (Time Profiler, Allocations) on iOS and Android Studio Profiler (Systrace, CPU Profiler) on Android.
3. Validate that no bridge serialization messages appear in the React Native trace when interacting with TurboModules.
