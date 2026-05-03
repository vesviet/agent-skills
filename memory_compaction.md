## Compact Working State

Current goal:
- Perform the 69-case full regression pass defined in `obj_regression_test_plan.md` to ensure the massive legacy cleanup didn't introduce UI/UX regressions.

Recent Achievements:
- **Polo Shirt 3D Orientation FIXED**: Diagnosed that the rendering engine had been migrated to React Three Fiber (`ProductModel.jsx`). Applied a dynamic rotation `[-Math.PI / 16, 0, 0]` directly to the R3F `<group>` node specifically for GLB/GLTF models. This 11.25-degree forward pitch exactly counteracts the model's native backward tilt, making it stand perfectly upright and face the camera.
- **Legacy Cleanup COMPLETE (Phase 1-4)**: The legacy codebase has been fully modernized. 
- Zero custom `window.*` globals remain.
- Zero `ObservableValue` / `toolbarActive` usages (fully migrated to Redux `toolSlice` single source of truth).
- Dead code (`tab.js`, `control.js`, `copyText.js`, `window.patternScale`) completely purged.
- Over 40+ legacy `console.log` debug statements removed.
- Over 40+ dead `window.*` function probes purged from `textUtils.js`.
- Class components refactored to functional components with Hooks (`LogoPattern.jsx`).

Architecture state:
- The design-hub now strictly uses `bridge/engineBridge.js` and Redux Toolkit for state.
- `webGL.js` is a "headless" logic layer for legacy interactions; it no longer appends WebGL rendering to the DOM.
- Visual 3D rendering is now declarative via `@react-three/fiber` inside `SceneManager.jsx` and `ProductModel.jsx`.

Next action:
- Run a manual or automated verification of the regression test cases.
