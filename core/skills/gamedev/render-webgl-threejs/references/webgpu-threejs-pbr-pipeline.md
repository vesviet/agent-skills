# WebGPU & Three.js PBR Rendering Pipeline Specification (2026)

## 1. WebGPU / WebGL2 Dual Architecture

Modern browser 3D applications implement WebGPU as primary hardware abstraction with transparent WebGL2 fallback:

```
                      Device Initialization
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
       navigator.gpu exists?          Fall back to WebGL2
               │                               │
        WebGPURenderer                   WebGLRenderer
   (Compute shaders, BindGroups)   (VAOs, Multi-Draw indirect)
               │                               │
               └───────────────┬───────────────┘
                               ▼
                   SRGBColorSpace + ACESFilmic
                               ▼
                   DRACO / Meshopt + KTX2 VRAM
```

## 2. Asset Compression & VRAM Residency

1. **Geometry Compression**:
   - Draco: High compression ratio for static environment meshes.
   - Meshopt: Fast GPU-friendly decoding for dynamic, animated skeletal meshes.
2. **Texture Compression**:
   - KTX2 / Basis Universal: Transcoded on Web Workers directly into GPU-native formats (ASTC, BC7, ETC2).
   - Zero CPU decompression into uncompressed RGBA8 textures, slashing mobile VRAM usage by 75%.
3. **ORM Texture Packing**:
   - Single texture combining Occlusion (R), Roughness (G), Metalness (B) channels to eliminate redundant samplers.

## 3. Draw Call Optimization & Instancing

- **`THREE.InstancedMesh`**: Mandated for repetitive dynamic entities (projectiles, enemies, coins).
- **`THREE.BatchedMesh`**: Merges dissimilar static geometries with identical materials into single MultiDrawIndirect submissions.
- **Frustum & Occlusion Culling**: Compute-based hierarchical Z-buffer occlusion culling for complex scenes.

## 4. Deterministic GPU Resource Lifecycle

JavaScript garbage collection does not clean GPU allocations. The unmount protocol requires:
```typescript
function disposeHierarchy(node: THREE.Object3D) {
  if (node instanceof THREE.Mesh) {
    node.geometry.dispose();
    if (Array.isArray(node.material)) {
      node.material.forEach((m) => disposeMaterial(m));
    } else {
      disposeMaterial(node.material);
    }
  }
}
```
All texture maps, render targets, and compute pipelines must execute `.dispose()`.
