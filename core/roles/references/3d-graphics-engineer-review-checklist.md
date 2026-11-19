## 3D Graphics Engineer Review Checklist

Operational verification gates for `@3d-graphics-engineer` deliverables across Three.js, React Three Fiber v9, WebGPU/WebGL2, shaders (TSL/WGSL/GLSL), and 3D asset pipelines.

---

### 1. Archetype Alignment & Backend Pairing (`RENDER-BACKEND-LOCK`)

- [ ] **Scene Archetype Classified**: explicitly tagged as `Product Configurator` (`frameloop="demand"`), `Spatial Showcase` (lazy-loaded + `MOTION_INTENSITY` synced), `Real-Time Game/Sim` (`frameloop="always"` + instancing), or `3DGS Scan Viewer`.
- [ ] **Clean Backend & Post-Processing Pairing**:
  - *WebGPU path*: `WebGPURenderer` + `MeshStandardNodeMaterial` / TSL + Three.js node `PostProcessing` + WGSL compute; inspected via **Chrome DevTools Shader Editor** (never WebGL-only `Spector.js`).
  - *WebGL2 fallback/path*: `WebGLRenderer` + `pmndrs/postprocessing` `EffectComposer` + `Spector.js` (dev-only, stripped in prod).
  - *R3F v9 alignment*: uses `useThree((s) => s.renderer)` instead of legacy `s.gl`.
- [ ] **Deterministic Context Recovery**: `webglcontextlost`/`webglcontextrestored` and WebGPU `device.lost` handlers reinitialize GPU resources without requiring full page reload.

---

### 2. Anti-AI-3D-Slop Visual & Mathematical Craft (`AI-3D-CRAFT-LOCK`)

- [ ] **Lighting & Tone Mapping**: calibrated PMREM HDRI environment lighting (`PMREMGenerator`) + intentional key/fill/rim hierarchy + `THREE.AgX` or `THREE.ACESFilmicToneMapping`; flat `ambientLight` + white `directionalLight` on `#000000` void rejected.
- [ ] **Camera Framing & Frustum**: product views use `fov 35–45` with bounding-sphere fit ($d = r / \sin(\text{fov}/2)$), tight `near`/`far` ratio to avoid Z-fighting, and damped `OrbitControls` with polar/distance clamps.
- [ ] **Grounding & Shadow Hygiene**: shadow bias calibrated (`bias` / `normalBias`) to prevent shadow acne and peter-panning; product scenes include contact grounding (`ContactShadows` or baked AO).
- [ ] **Texture Color-Space Invariant**:
  - `THREE.SRGBColorSpace` applied **only** to albedo/baseColor and emissive textures.
  - `THREE.NoColorSpace` (Linear) enforced on normal, roughness, metalness, AO, and packed ORM (`R=AO, G=Roughness, B=Metalness`) maps; `flipY = false` preserved for glTF assets.
- [ ] **Zero-Allocation Render Loop**: zero `new THREE.Vector3()`, `new THREE.Matrix4()`, `.clone()`, or React `setState()` inside `useFrame` / RAF loops; $\Delta t \le 0.1\text{s}$ clamped.

---

### 3. Complete VRAM Resource Lifecycle (`VRAM-DISPOSAL-LOCK`)

JavaScript GC does not release GPU buffers or textures, and `material.dispose()` in Three.js does **not** dispose attached `Texture` instances:

```typescript
const TEXTURE_KEYS = [
  'map', 'normalMap', 'roughnessMap', 'metalnessMap',
  'aoMap', 'emissiveMap', 'alphaMap', 'bumpMap', 'displacementMap', 'envMap',
] as const;

function disposeMaterialAndTextures(mat: THREE.Material): void {
  const record = mat as unknown as Record<string, unknown>;
  for (const key of TEXTURE_KEYS) {
    const tex = record[key];
    if (tex && typeof (tex as THREE.Texture).dispose === 'function') {
      (tex as THREE.Texture).dispose();
    }
  }
  mat.dispose();
}

function disposeSceneNode(node: THREE.Object3D): void {
  if ('geometry' in node && (node as THREE.Mesh).geometry) {
    (node as THREE.Mesh).geometry.dispose();
  }
  if ('material' in node && (node as THREE.Mesh).material) {
    const mat = (node as THREE.Mesh).material;
    if (Array.isArray(mat)) mat.forEach(disposeMaterialAndTextures);
    else disposeMaterialAndTextures(mat);
  }
}
```

- [ ] **Full Teardown Verified**: geometries, materials, **all attached texture maps**, `WebGLRenderTarget`s, and `PMREMGenerator`s disposed on unmount/scene switch.

---

### 4. Asset Budgets, Compression & LOD Hierarchy (`ASSET-BUDGET-AND-LOD-LOCK`)

- [ ] **Clear Per-Asset vs Per-Scene Ceilings**:
  - *Compressed GLB transfer*: `<= 2 MB` per scene on mobile (Draco or Meshopt quantization; raw `.obj`/uncompressed `.gltf` rejected).
  - *Per-prop interactive target*: `<= 10k` triangles for standard interactive props; meshes `> 50k` triangles require 3-tier LOD (`LOD0` / `LOD1` / `LOD2`).
  - *Per-scene mobile frame ceiling*: `<= 500k` rendered triangles, `<= 100` draw calls (`<= 250` desktop web), `<= 25` shadow-casting draw calls, `DPR <= 2.0`.
- [ ] **KTX2 / Basis Universal Textures**: all textures `> 1024×1024` use KTX2 (UASTC/ETC1S) capped at `<= 1K` mobile / `<= 2K` desktop; total mipmapped texture VRAM obeys the **Geometric-Series Mipmap VRAM Bound**:
  $$VRAM_{\text{textures}} = \sum_{i=1}^M \left( W_i \times H_i \times Bpp_i \times 1.333 \right) \le 180\text{ MB}$$
- [ ] **Bundled WASM Decoders**: Draco, Meshopt, and KTX2 decoders served from pinned local package assets, never unverified external CDNs.

---

### 5. Generative 3D & Gaussian Splatting (3DGS) Governance (`GEN-3D-PROVENANCE-LOCK`)

- [ ] **Splat & VRAM Ceilings**: `<= 400k` splats on mobile (`<= 1.2M` desktop) and $VRAM_{\text{3DGS}} \le 250\text{ MB}$ (`N_splats * 32 bytes + radix_sort` or explicit covariance layout).
- [ ] **Mesh & License Validation**: AI-generated meshes (Meshy, Tripo, Rodin, NeRF bakes) pass `gltf-validator`, UV/normal checks, simplified AABB/OBB/BVH collision proxies, and commercial license provenance logging.

---

### 6. Raycasting, Instancing & Device-Tier Calibration

- [ ] **BVH-Accelerated Raycasting**: interactive meshes `> 10k` triangles use `three-mesh-bvh` (accelerated raycast bounds tree) or proxy collision meshes; raw per-triangle CPU raycasting inside `pointermove` is rejected.
- [ ] **Draw-Call Batching & Instancing**: repeated geometry uses `THREE.InstancedMesh` or `THREE.BatchedMesh` with frustum culling verified; material permutations and shader recompilations are minimized via shared `NodeMaterial` / uniform updates.
- [ ] **Shader Warm-Up & Pipeline Caching**: heavy custom shaders (TSL/WGSL/GLSL) pre-compile via `renderer.compileAsync(scene, camera)` behind a loading state so first interaction never stalls the main thread.
- [ ] **Adaptive Device-Tier Scaling**: `PerformanceMonitor` / GPU tier detection dynamically steps DPR (`[1, 1.5]` mobile, `[1, 2]` desktop), shadow map resolution (`512`–`2048`), and post-processing passes when frame time exceeds $16.6\text{ ms}$ (60 FPS) or $11.1\text{ ms}$ (90 FPS XR).
- [ ] **Decal & Z-Order Stability**: projected decals apply `polygonOffset` (`polygonOffsetFactor: -4`, `polygonOffsetUnits: -4`) and explicit `renderOrder` without Z-fighting against curved base geometry.

---

### 7. Accessibility, Host Dials & Verification Gates

- [ ] **A11y & Motion Compliance**: `prefers-reduced-motion` pauses/simplifies camera & particle motion; non-3D fallback (static render/image/summary) and canvas ARIA labels present; host `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY` honored.
- [ ] **Keyboard & Focus Navigation**: camera presets, hotspot selection, and configurator controls are reachable via keyboard without trapping focus inside the canvas element.

| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **glTF / Asset Integrity** | 0 schema/normal/UV errors; GLB `<= 2 MB` | `gltf-validator` & `gltf-transform inspect` | 0 errors; payload `<= 2 MB` |
| **Frame Pacing** | $\Delta t \le 16.6\text{ ms}$ (60 FPS); mobile draw calls `<= 100` | R3F DevTools / Chrome Performance / Stats.js | $\ge 95\%$ frames within budget on target tier |
| **Shader & Draw Call Trace** | Valid WGSL/TSL/GLSL & batched draws | Chrome DevTools Shader Editor (WebGPU) / `Spector.js` dev (WebGL2) | 0 compile errors; instancing/batching active |
| **VRAM Disposal** | 0 retained geometries/textures/targets | Chrome Memory / `renderer.info.memory` diff | Counts return to baseline after unmount |
| **Raycasting & Interaction** | Pointer hit-test `< 2 ms` on dense meshes | Chrome Performance / BVH profiler | Zero main-thread hitch during orbit/hover |
| **Delivery Contracts** | Schema-valid handoff | `python3 core/scripts/validate-contracts.py` | `implementation-result.json` (+ `performance-audit.json`) valid |

---

### 8. Pre-Release Sign-Off & Escalation Triggers

- [ ] **Escalation to `@frontend-developer` / `@ui-ux-designer`**: flag any DOM overlay Z-index collision, canvas pointer-event capture conflict, or missing `DESIGN.md` motion/density dial before merging.
- [ ] **Escalation to `@qa-engineer` / `@sre`**: require cross-GPU verification (Apple Silicon WebGPU, Intel/AMD Windows WebGL2, mid-tier mobile GPU) whenever custom shaders, KTX2 transcoding, or 3DGS renderers change.
- [ ] **Zero Production Debug Leaks**: verify `Stats.js`, `Spector.js`, `r3f-perf`, wireframe helpers, and `console.log` inside `useFrame` are stripped from production bundles.
