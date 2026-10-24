---
name: generate-game-assets-pipeline
description: Automate procedural and AI-assisted game asset pipelines including pixel sprite sheets, texture atlas packing, and PBR channel packing. Use when generating game art pipelines, packing sprite atlases, or normalizing textures and meshes for engine import.
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

# Generate Game Assets Pipeline

Build deterministic, automated asset generation and processing pipelines that transform raw procedural or AI-generated art into packed sprite sheets, trimmed texture atlases, and channel-packed PBR materials.

## Core Rules

- **Provenance & Budget Gate**: Every AI-assisted or procedurally generated asset must pass automated resolution, polycount, and palette validation before entering the engine repository, with generation parameters recorded in a manifest.
- **Extruded Texture Atlases**: Pack 2D sprites and UI icons into power-of-two (POT) texture atlases with at least $2\text{px}$ edge extrusion and padding to eliminate texture bleeding during mipmapping and bilinear filtering.
- **Linear PBR Channel Packing**: Pack single-channel grayscale maps (Ambient Occlusion in Red, Roughness in Green, Metallic in Blue) into a single linear-color-space ORM texture to save 66% of sampler bandwidth and VRAM.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` when completing asset pipeline tooling and batch processing.

## Suggested Process

### 1. Sprite Sheet & Pixel Art Normalization
Standardize 2D character and VFX frames via headless CLI scripts (Aseprite CLI, ImageMagick, or Python Pillow):
- Enforce uniform pivot anchors, indexed color palettes, and clean alpha thresholds (zero stray semi-transparent pixels on pixel-art silhouettes).
- Export structured JSON/XML frame metadata alongside the packed sprite sheet PNG/KTX2.

### 2. Texture Atlas Bin-Packing
Run deterministic rectangle bin-packing (MaxRects algorithm) to consolidate individual sprites by scene or lifecycle scope:
- Group co-loaded assets into shared atlases ($\le 2048 \times 2048$ mobile, $\le 4096 \times 4096$ desktop) with $2\text{px}$ border extrusion so sprite batches render in a single draw call.

### 3. PBR ORM Channel Packing & Mipmap Generation
Combine material maps programmatically in linear space (`sRGB = false`):
- Map `R = Ambient Occlusion`, `G = Roughness`, `B = Metallic`, `A = Height/Smoothness`.
- Validate normal maps use the target engine's handedness convention (OpenGL $+Y$ vs DirectX $-Y$) and re-normalize mipmap vectors.

### 4. Automated CLI Pipeline Verification
Wire asset validation into CI pre-commit or build scripts to reject non-POT textures, missing mipmaps, or uncompressed raw files before engine packaging.

## Output Contracts

When completing game asset pipeline automation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Sprite sheets and texture atlases include $2\text{px}$ edge extrusion to prevent UV seam bleeding
- [ ] PBR metallic, roughness, and occlusion maps are channel-packed into linear ORM textures
- [ ] Normal map green-channel orientation ($+Y$ OpenGL vs $-Y$ DirectX) matches the target engine
- [ ] All 3D/mipmapped textures conform to power-of-two (POT) or block-compression multiples of 4
- [ ] Procedural and AI-generated assets record generation seeds and pass polycount/VRAM gates
- [ ] Batch processing CLI scripts run deterministically in headless CI environments

## Related Skills

- **integrate-game-engine**: automated engine asset import presets and texture compression
- **program-game-shaders**: PBR channel-packed texture sampling and material shaders
