---
name: inspect-blender-rigs-motion
description: Diagnose and repair Blender armatures, bone roll alignment, animation retargeting hierarchies, and root motion trajectories before game engine import. Use when validating skeletal meshes, fixing bone twists, or extracting root motion for Godot, Unity, or Unreal.
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

# Inspect Blender Rigs Motion

Validate, repair, and normalize skeletal armatures, skinning weights, bone rolls, and root motion tracks in Blender via headless Python (`bpy`) scripts before importing into game engines.

## Core Rules

- **Applied Transforms Invariant**: Both the armature object and all skinned mesh objects must have unit scale `(1.0, 1.0, 1.0)`, zero rotation `(0, 0, 0)`, and aligned origins at the world origin `(0, 0, 0)` prior to export.
- **Consistent Bone Roll Alignment**: Enforce uniform primary and secondary bone axes across limb chains so quaternion interpolation and IK solvers do not twist joints during animation blending.
- **Root Motion Separation**: Dedicate a ground-projected `Root` bone at `(0, 0, 0)` parented above the `Hips`/`Pelvis` bone. Extract planar locomotion deltas onto the `Root` bone while keeping in-place vertical bounce on the pelvis.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` when completing rig diagnostics and motion pipeline fixes.

## Suggested Process

### 1. Headless Armature & Mesh Transform Audit
Execute a headless Blender inspection script (`blender --background asset.blend --python inspect_rig.py`) to verify:
- Unapplied object scales or negative scales that invert surface normals.
- Maximum vertex influence limits ($\le 4$ bone weights per vertex for real-time GPU skinning) and normalized weight sums ($\sum w_i = 1.0$).

### 2. Hierarchy & Bone Roll Normalization
Standardize the deform skeleton hierarchy:
- Separate deform bones (`DEF-*`) from control/IK rig bones (`CTRL-*`, `MCH-*`), exporting only deform bones to the target engine.
- Recalculate bone rolls in Edit Mode (`bpy.ops.armature.calculate_roll`) so limb hinge axes align cleanly with local $X$ or $Z$ axes.

### 3. Animation Retargeting Validation
Map source motion-capture or library animations onto the target humanoid skeleton:
- Verify rest pose (T-pose or A-pose) quaternion parity before baking action keyframes.
- Bake constrained IK/FK channels to explicit per-frame FK bone transforms with clean euler discontinuity filtering.

### 4. Root Motion Extraction & Export Verification
Project hip translation trajectories onto the ground plane (`Root` bone) for locomotion clips, zero out lateral drift on idle/in-place clips, and export deterministic `.glb` / `.fbx` binaries with tangents enabled.

## Output Contracts

When completing Blender rig and motion inspection, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Armature and skinned meshes have applied transforms with `(1.0, 1.0, 1.0)` scale at world origin
- [ ] Vertex skin weights are normalized and capped at 4 bone influences per vertex
- [ ] Deform bone hierarchy is cleanly isolated from IK/control rig helper bones
- [ ] Bone roll axes are consistent across symmetric left/right limb chains
- [ ] Root bone tracks planar locomotion cleanly without pelvis double-transform drift
- [ ] Exported glTF/FBX passes headless engine import without scale or quaternion warnings

## Related Skills

- **integrate-game-engine**: deterministic 3D glTF/FBX importer configurations and skeleton mapping
- **develop-gameplay-systems**: root motion integration with character controllers and state machines
