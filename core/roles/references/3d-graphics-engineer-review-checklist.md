## 3D Graphics Engineer Review Checklist

This reference checklist provides operational 3D graphics engineering, WebGPU rendering, shader optimization, and asset pipeline criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across WebGPU-first architecture with WebGL2 fallback, Draco and Meshopt geometry compression, complete VRAM resource disposal, generative 3D asset governance (Gaussian Splatting / NeRF), 60 FPS frame budgets, WGSL shader numerical stability, DPR clamping, and R3F canvas lifecycle integration.

### 1. WebGPU-First Modernization & Graceful WebGL2 Fallback (`WEBGPU-FALLBACK-LOCK`)
- **Next-Generation WebGPU Pipeline**:
  - rendering pipelines prioritize WebGPU (`navigator.gpu`) leveraging WGSL compute shaders, uniform buffer layouts, and asynchronous command encoding
  - runtime capability detection implements automated, graceful fallback to WebGL2 for unsupported browsers or restricted mobile GPUs:
    ```typescript
    async function initRenderer(): Promise<RendererContext> {
      if ('gpu' in navigator) {
        const adapter = await navigator.gpu.requestAdapter({ powerPreference: 'high-performance' });
        if (adapter) {
          const device = await adapter.requestDevice({
            requiredLimits: { maxBufferSize: 256 * 1024 * 1024 }
          });
          return new WebGPURendererContext(device);
        }
      }
      return new WebGL2RendererFallback();
    }
    ```
  - feature tiering cleanly disables heavy compute effects (e.g., screen-space ambient occlusion, volumetric fog, GPU particle sorting) under WebGL2 fallback without throwing unhandled exceptions

### 2. Draco & Meshopt Geometry Compression (`DRACO-MESHOPT-LOCK`)
- **Strict Asset Size Ceilings & Quantization**:
  - all glTF/GLB models must be compressed using Meshopt quantization (`EXT_meshopt_compression`) or Draco geometry compression; raw uncompressed `.obj` or unoptimized `.gltf` files are prohibited in production bundles
  - mobile 3D asset transfer budgets are strictly capped at $\le 2\text{MB}$ compressed payload per scene
  - textures encoded using KTX2 / Basis Universal (UASTC / ETC1S) for direct GPU VRAM transcoding (BC7 desktop, ASTC mobile, ETC2 fallback) without CPU decompression overhead:
    ```bash
    # Transcode and compress GLB assets using gltfpack with meshopt
    gltfpack -i scene_raw.gltf -o scene_optimized.glb -cc -tc -kn
    ```

### 3. VRAM Resource Lifecycle & Memory Leak Elimination (`MEMORY-DISPOSAL-LOCK`)
- **Comprehensive Scene Teardown & Disposal**:
  - all geometries, textures, materials, shaders, and render targets must explicitly execute `.dispose()` upon component unmount or scene transition
  - Three.js / R3F scenes audited with memory profiling tools to verify zero orphaned GPU VRAM allocations across page navigations:
    ```typescript
    function disposeSceneNode(node: THREE.Object3D): void {
      if ((node as THREE.Mesh).geometry) {
        (node as THREE.Mesh).geometry.dispose();
      }
      if ((node as THREE.Mesh).material) {
        const mat = (node as THREE.Mesh).material;
        if (Array.isArray(mat)) {
          mat.forEach(m => m.dispose());
        } else {
          mat.dispose();
        }
      }
    }
    ```

### 4. Generative 3D Asset & Gaussian Splatting (3DGS) Governance (`GEN-3D LOCK`)
- **Mathematical VRAM Allocation Bounds**:
  - 3D Gaussian Splatting scenes must enforce strict splat count ceilings ($\le 400\text{k}$ splats on mobile, $\le 1.2\text{M}$ on desktop) and adhere to the memory budget equation:
    $$VRAM_{\text{3DGS}} = N_{\text{splats}} \times (12 \times \text{sizeof(float32)} + 48 \times \text{sizeof(float16)}) \le 250\text{MB}$$
  - GPU texture memory consumption across all active mip levels must obey Little's Law VRAM bounds:
    $$VRAM_{\text{textures}} = \sum_{i=1}^M \left( W_i \times H_i \times Bpp_i \times 1.333 \right) \le 180\text{MB}$$
- **Procedural Geometry Collision Isolation**:
  - AI-generated procedural geometry or Gaussian splat point clouds must never be used directly as physical collision meshes; simplified collision primitives (AABB / OBB / BVH) must wrap procedural assets

### 5. Strict 60 FPS Frame Budget & Draw Call Caps (`FRAME-BUDGET-LOCK`)
- **Frame Timing & Render Complexity Limits**:
  - render loops must maintain steady 60 FPS ($16.6\text{ms}$ frame budget; $8.3\text{ms}$ for 120Hz displays) under standard device loads:
    $$\Delta t_{\text{frame}} \le 16.6\text{ms}, \quad \text{Jitter} \le \pm 2.0\text{ms}$$
  - draw calls strictly capped ($\le 100$ draw calls per frame on mobile, $\le 250$ on desktop) through material batching, texture atlasing, and geometry instancing (`InstancedMesh`)
  - dynamic resolution scaling (DRS) automatically engages if frame delta exceeds $22\text{ms}$ ($<45\text{ FPS}$) for $\ge 3$ consecutive seconds

### 6. WGSL Compute Shader Pipelines & Numerical Precision
- **Compute Shader Particle & Sorting Passes**:
  - high-concurrency particle systems and Gaussian splat depth sorting must execute in WGSL compute passes; CPU-blocking sort loops in the main thread are strictly prohibited:
  ```wgsl
  // POSITIVE: WGSL Workgroup Parallel Bitonic Sorting Step
  @group(0) @binding(0) var<storage, read_write> splatIndices: array<u32>;
  @compute @workgroup_size(64)
  fn bitonicSortStep(@builtin(global_invocation_id) global_id: vec3<u32>) {
    let index = global_id.x;
    if (index >= arrayLength(&splatIndices)) { return; }
    // Parallel sorting logic without thread blocking
  }
  ```
  - numerical precision specified explicitly (`precision highp float` vs `mediump`); division-by-zero guards must protect all vector normalizations

### 7. Responsive Viewport & Device Pixel Ratio (DPR) Clamping
- **Mobile Thermal & Power Preservation**:
  - Device Pixel Ratio (DPR) clamped to a maximum of `2.0` (`renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2.0))`) to prevent 4K/Retina rendering stalls and GPU thermal throttling on high-DPI mobile devices
  - animation delta time clamped ($\Delta t \le 0.1\text{s}$) to prevent physics tunneling or visual vertex exploding when tabs are backgrounded

### 8. Canvas / DOM Integration & Thread Synchronization
- **Non-Blocking UI Thread Isolation**:
  - heavy asset parsing, texture decompression, and physics computations offloaded to Web Workers via `OffscreenCanvas` or worker pools
  - 3D canvas events pass through smoothly to DOM overlay elements without input lag or gesture hijacking
  - canvas elements provide alternative text descriptions and ARIA labels for non-visual assistive technology

### 9. Context Loss Recovery & Lifecycle Management
- **Deterministic Context Restoration**:
  - WebGL `webglcontextlost` / `webglcontextrestored` and WebGPU `device.lost` listener lifecycles register automated asset rehydration without requiring full page reloads:
  ```typescript
  device.lost.then((info) => {
    console.warn(`WebGPU device lost: ${info.message}. Reason: ${info.reason}`);
    if (info.reason !== 'destroyed') {
      reinitializeWebGPUScene();
    }
  });
  ```

### 10. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Asset Size Ceiling** | Scene payload $\le 2\text{MB}$ | `gltf-transform inspect scene.glb` | Compressed transfer size $\le 2\text{MB}$ |
| **VRAM Splat Budget** | $VRAM_{\text{3DGS}} \le 250\text{MB}$ | Chrome DevTools Memory / WebGPU Tracer | Zero allocation breaches |
| **Frame Rate Floor** | $\Delta t_{\text{frame}} \le 16.6\text{ms}$ | Stats.js / `requestAnimationFrame` monitor | Steady 60 FPS ($\ge 95\%$ of frames) |
| **VRAM Teardown** | 0 retained textures/buffers | Automated Jest/Puppeteer disposal test | Zero lingering GPU buffers |
| **glTF Spec Validation** | 0 schema validation errors | `gltf-validator -i scene.glb` | 0 errors, 0 warnings |
