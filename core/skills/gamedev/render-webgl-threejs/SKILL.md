---
name: render-webgl-threejs
description: Architect interactive WebGL2 and WebGPU 3D scenes using Three.js or React Three Fiber with compressed GLTF streaming, PBR materials, and post-processing pipelines. Use when building browser 3D games, WebGPU render loops, or EffectComposer pipelines.
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - create_file
  - search_code
  - run_build
  - run_tests
  - run_linter
  - execute_command
version: "1.0.0"
---

# Render WebGL Threejs

Build high-framerate WebGL2 and WebGPU interactive 3D scenes with compressed asset streaming, physically based rendering (PBR), merged post-processing passes, and deterministic VRAM lifecycle management.

## Core Rules

- **WebGPU with Graceful WebGL2 Fallback**: Initialize `WebGPURenderer` when navigator capabilities permit, while providing seamless automatic fallback to `WebGLRenderer` and handling `webglcontextlost` / `webglcontextrestored` events without crashing.
- **Compressed Asset Streaming**: Enforce Draco or Meshopt geometry compression alongside KTX2 / Basis Universal GPU-compressed textures so assets remain compressed in VRAM and decode off the main thread.
- **Explicit VRAM Disposal**: Never rely on JavaScript garbage collection for GPU resources. Explicitly call `.dispose()` on every `BufferGeometry`, `Material`, `Texture`, and `WebGLRenderTarget` when unmounting scenes or despawning entities.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing WebGL/Three.js rendering slices.

## Suggested Process

### 1. Renderer, Color Space & Pixel Ratio Setup
Configure the renderer for consistent cross-device fidelity and frame pacing:
- Set `renderer.outputColorSpace = THREE.SRGBColorSpace` and `renderer.toneMapping = THREE.ACESFilmicToneMapping`.
- Clamp device pixel ratio (`Math.min(window.devicePixelRatio, 2.0)`) to prevent fill-rate collapse on high-DPI mobile screens.

### 2. Asynchronous GLTF Streaming & Instancing
Load 3D scenes via `GLTFLoader` configured with `DRACOLoader`, `MeshoptDecoder`, and `KTX2Loader`:
- Convert repeated static props, foliage, and projectiles into `THREE.InstancedMesh` or `THREE.BatchedMesh` to collapse hundreds of draw calls into a single GPU submission.

### 3. PBR Material & Environment Lighting Calibration
Configure `MeshStandardMaterial` / `MeshPhysicalMaterial` using pre-filtered PMREM environment maps (`PMREMGenerator`):
- Pack metallic, roughness, and ambient occlusion into a single ORM texture (`roughnessMap` = G, `metalnessMap` = B, `aoMap` = R) to halve texture sampler lookups.

### 4. EffectComposer Post-Processing Consolidation
Combine bloom, vignette, and color grading into a merged `EffectComposer` pass (`pmndrs/postprocessing` `EffectPass`) rather than chaining multiple full-screen render-target blits.

## Output Contracts

When completing WebGL and Three.js rendering implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Renderer clamps DPR to at most 2.0 and handles WebGL context loss/restoration events
- [ ] GLTF pipeline uses Draco/Meshopt geometry compression and KTX2 GPU textures
- [ ] Repeated meshes use `InstancedMesh` or `BatchedMesh` to keep draw calls within budget
- [ ] PBR materials share ORM channel-packed textures and pre-filtered PMREM lighting
- [ ] Post-processing effects are merged into minimal full-screen render passes
- [ ] Geometries, materials, textures, and render targets execute `.dispose()` on unmount

## Related Skills

- **program-game-shaders**: custom GLSL vertex/fragment shaders and post-processing effects
- **profile-game-performance**: WebGL/WebGPU draw call batching and VRAM disposal profiling
