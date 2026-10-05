## 3D Graphics Engineer Review Checklist

This reference checklist provides operational 3D graphics engineering, WebGPU rendering, shader optimization, and asset pipeline criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across WebGPU-first architecture with WebGL2 fallback, Draco and Meshopt geometry compression, complete VRAM resource disposal, generative 3D asset governance (Gaussian Splatting / NeRF), 60 FPS frame budgets, WGSL shader numerical stability, DPR clamping, and R3F canvas lifecycle integration.

### 1. WebGPU-First Modernization & Graceful WebGL2 Fallback (`WEBGPU-FALLBACK-LOCK`)
- **Next-Generation WebGPU Pipeline**:
  - rendering pipelines prioritize WebGPU (`navigator.gpu`) leveraging compute shaders, uniform buffer layouts, and multi-threaded command encoding
  - runtime capability detection implemented with automated graceful fallback to WebGL2 for unsupported legacy browsers or restricted mobile GPUs
  - feature tiering cleanly disables heavy compute effects (e.g. screen-space ambient occlusion, volumetric fog) under WebGL2 fallback

### 2. Draco & Meshopt Geometry Compression (`DRACO-MESHOPT-LOCK`)
- **Strict Asset Size Ceilings & Quantization**:
  - all glTF/GLB models compressed using Draco geometry compression or Meshopt quantization; raw uncompressed `.obj` or unoptimized `.gltf` files prohibited in production bundles
  - mobile 3D asset transfer budgets strictly capped ($\le 2\text{MB}$ compressed payload per scene); textures encoded using KTX2 / Basis Universal (UASTC / ETC1S) for direct GPU VRAM transcoding without CPU decompression overhead

### 3. VRAM Resource Lifecycle & Memory Leak Elimination (`MEMORY-DISPOSAL-LOCK`)
- **Comprehensive Scene Teardown & Disposal**:
  - all geometries, textures, materials, shaders, and render targets must explicitly call `.dispose()` upon component unmount or scene transition
  - Three.js / R3F scenes audited with memory profiling tools to verify zero orphaned GPU VRAM allocations or lingering animation loop listeners across page navigations

### 4. Generative 3D Asset & Gaussian Splatting (3DGS) Governance (`GEN-3D LOCK`)
- **Memory Footprint Profiling & LOD Generation**:
  - AI-generated 3D assets (3D Gaussian Splats, NeRF bakes, generative meshes) must undergo automated polygon reduction and Level of Detail (LOD) generation before merging
  - 3D Gaussian Splatting scenes enforce strict splat count ceilings ($\le 500\text{k}$ splats on mobile, $\le 2\text{M}$ on desktop) with frustum culling and distance-based point discarding

### 5. Strict 60 FPS Frame Budget & Draw Call Caps (`FRAME-BUDGET-LOCK`)
- **Frame Timing & Render Complexity Limits**:
  - render loops must maintain steady 60 FPS ($16.6\text{ms}$ frame budget; $8.3\text{ms}$ for 120Hz displays) under standard device loads
  - draw calls strictly capped ($\le 100$ draw calls per frame on mobile) through material batching, texture atlases, and geometry instancing (`InstancedMesh`)
  - total polygon budget bounded ($\le 500\text{k}$ triangles on mobile viewports)

### 6. WGSL & Custom Shader Numerical Precision
- **Shader Math & Branching Optimization**:
  - custom WGSL and GLSL fragment/vertex shaders optimized: expensive dependent texture reads and dynamic divergent branching inside fragment loops eliminated
  - numerical precision specified explicitly (`precision highp float` vs `mediump`); division-by-zero checks guard all normalization and vector math operations

### 7. Responsive Viewport & Device Pixel Ratio (DPR) Clamping
- **Mobile Thermal & Power Preservation**:
  - Device Pixel Ratio (DPR) clamped to a maximum of `2.0` (`gl.setPixelRatio(Math.min(window.devicePixelRatio, 2))`) to prevent 4K/Retina rendering stalls and thermal throttling on high-DPI mobile devices
  - render resolution dynamically throttles down (dynamic resolution scaling) if frame rate drops below 45 FPS for $>2$ consecutive seconds

### 8. Canvas / DOM Integration & Thread Synchronization
- **Non-Blocking UI Thread Isolation**:
  - heavy asset parsing, texture decompression, and physics computations offloaded to Web Workers via OffscreenCanvas or worker pools
  - 3D canvas events pass through smoothly to DOM overlay elements without input lag or gesture hijacking
- **Accessibility & Screen Reader Alternatives**:
  - canvas elements provide alternative text descriptions and ARIA labels for non-visual assistive technology

### 9. Production Asset Pipeline & Artifact Delivery (`ASSET-PIPELINE LOCK`)
- **Automated Validation in CI/CD**:
  - 3D asset pipeline verifies glTF schema compliance via glTF-Validator in automated build jobs; zero errors allowed
  - asset delivery manifests produce valid, schema-compliant `contracts/schemas/3d-scene-spec.json` or `contracts/schemas/implementation-result.json`
- **PBR Texture Map Standards**:
  - roughness, metalness, and ambient occlusion packed into single combined ORM texture channels to minimize sampler count

### 10. Operational Failure Modes & Real-Time Profiling
- **Context Loss Recovery**:
  - `webglcontextlost` and `gpudevicefound` event handlers register automatic scene restoration without requiring full page reloads
- **Thermal Throttling Protection**:
  - frame delta monitors detect sustained mobile GPU throttling; downgrade shadow map resolution and disable post-processing passes automatically
- **Fallback Glitch Prevention**:
  - WebGL2 fallbacks verified to render without black screen artifacts or missing material shaders when WebGPU context creation fails
