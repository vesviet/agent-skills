# setup-visual-regression — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### Containerized Baselines (Mandatory 2026)
- **Official Playwright Docker only**: `mcr.microsoft.com/playwright` matching CI environment — local macOS/Windows vs Linux CI = guaranteed false failures
- **Baseline generation in CI container**: Canonical reference snapshots generated in project's official Docker image

### Bounded Self-QA (2026)
- **Hard maximum 2 passes** post-authoring for agent self-QA
- **Desktop + Mobile simultaneously**: `>= 1280px` and `375px - 430px` viewports
- **Edits triggered by deterministic defects only**: horizontal overflow, fold clipping, broken markup, `< 44x44px` touch targets, contrast failures
- **Prevent infinite refinement loops**: Strict defect-driven edits only

### Negative Asset Constraints (2026)
- **Fabricated inline SVG logos prohibited**: "NovaCorp" style synthetic logos banned
- **Synthetic customer testimonials banned**: Unverified metrics prohibited
- **Authentic typography mandated**: System monograms, verified Simple Icons marks, honest structural placeholders

### Technical Standards (2026)
- **Animation suppression**: All CSS animations, transitions, cursor blinks disabled (`animations: 'disabled'`)
- **Dynamic content masking**: Dates, avatars, random IDs, ads masked via `mask: [page.locator('...')]`
- **Explicit tolerance thresholds**: `maxDiffPixelRatio: 0.01`, `threshold: 0.2` — unconfigured defaults too loose
- **Component isolation**: Storybook + Chromatic with TurboSnap for design system components + full-page Playwright
- **Cross-browser matrix**: Chromium, WebKit, Firefox at mobile/desktop viewports
- **Hard CI gate**: Visual regression failures block merges unless `ui-ux-designer` or `frontend-developer` explicitly approves
- **Network mocking**: MSW for deterministic visual fixtures — live external API = non-deterministic

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| Containerized baselines mentioned | **Official Playwright Docker mandatory**: `mcr.microsoft.com/playwright` matching CI; local vs Linux = false failures |
| Self-QA bounds mentioned | **Max 2 passes post-authoring**: Desktop + Mobile simultaneously; defect-driven edits only |
| Negative asset constraints | **Fabricated SVGs/testimonials prohibited**: Authentic typography, Simple Icons, honest placeholders only |
| Animation suppression | **All animations/transitions/cursor blinks disabled**: `animations: 'disabled'` before snapshots |
| Dynamic content masking | **Mask dates/avatars/IDs/ads**: `mask: [page.locator('...')]` before capture |
| Tolerance thresholds | **Explicit `maxDiffPixelRatio: 0.01`, `threshold: 0.2`**: Defaults too loose |
| Component isolation | **Storybook + Chromatic TurboSnap + Playwright full-page**: Both isolation levels |
| Cross-browser matrix | **Chromium, WebKit, Firefox at mobile/desktop**: Required matrix |
| Hard CI gate | **Visual failures block merges**: Only `ui-ux-designer`/`frontend-developer` can approve |
| Network mocking | **MSW mandatory**: Deterministic fixtures; live external API = non-deterministic |

### 2. New 2026 Patterns to Add
- **Playwright Docker CI Pipeline**: Baseline capture in `mcr.microsoft.com/playwright` container matching CI runner
- **Bounded Self-QA Protocol**: 2-pass limit, dual viewport, defect-driven edits, loop prevention
- **Authentic Asset Pipeline**: System monograms, Simple Icons verification, placeholder honesty check
- **TurboSnap Integration**: Chromatic only re-tests changed component stories; faster CI
- **Visual Regression Dashboard**: PR-linked diff summaries, baseline approval workflow, drift detection
- **MSW Visual Fixtures**: Record once, replay deterministically for all visual tests

### 3. Checklist Additions
- [ ] Playwright/Chromatic installed and configured
- [ ] Viewport matrix: Mobile (375x667), Tablet (768x1024), Desktop (1280x800)
- [ ] Cross-browser: Chromium, WebKit, Firefox
- [ ] Color scheme variants: light mode, dark mode
- [ ] Dynamic content masking: timestamps, avatars, numeric feeds masked
- [ ] Animation disabling: `animations: 'disabled'` during test runs
- [ ] Network mocks: MSW for deterministic state rendering
- [ ] Baseline capture in official Playwright Docker container (`mcr.microsoft.com/playwright`)
- [ ] Baseline quality verified: image quality, cropping, full-page layout coverage
- [ ] Baseline committed to repo or artifact registry per policy
- [ ] CI visual regression step on PRs touching frontend assets
- [ ] Visual diff artifact uploads on failure for PR review
- [ ] Failure reporting links to visual comparison summaries
- [ ] Baseline update CLI documented (`npm run test:visual -- -u`)
- [ ] Mandatory reviewer sign-off: `ui-ux-designer` or `frontend-developer` before baseline update
- [ ] `maxDiffPixelRatio: 0.01`, `threshold: 0.2` configured
- [ ] Component isolation: Storybook + Chromatic TurboSnap + Playwright full-page
- [ ] Negative asset check: no fabricated SVGs, no synthetic testimonials
- [ ] Bounded self-QA: max 2 passes, dual viewport, defect-driven only
- [ ] `implementation-result.json` emitted with visual baseline generation proof

### 4. Failure Mode Additions
- **Local vs CI baseline mismatch**: macOS/Windows snapshots vs Linux CI. Mitigation: Official Playwright Docker container for ALL baseline generation.
- **Unbounded self-QA refinement**: Agent iterates infinitely on visual tweaks. Mitigation: Hard 2-pass limit; only deterministic defect edits allowed.
- **Fabricated asset compliance failure**: Synthetic logos/testimonials in baselines. Mitigation: Negative asset constraint check in pipeline; reject non-authentic assets.
- **Threshold too loose**: Real regressions below threshold allowed. Mitigation: `maxDiffPixelRatio: 0.01`, `threshold: 0.2`; per-component category thresholds.
- **Driver version drift**: Chromatic/Percy updated without re-baselining. Mitigation: Re-baseline all components on driver upgrades; CI surfaces missing re-baseline.
- **Live API non-determinism**: External API changes visual output between runs. Mitigation: MSW mocks for all visual tests; deterministic fixtures.
- **TurboSnap missed changes**: Changed component not re-tested. Mitigation: Verify TurboSnap dependency graph; manual trigger for global changes.

### 5. Output Contract Updates
- Update `contracts/schemas/implementation-result.json` with: visual framework, viewport/browser matrix, baseline container, tolerance thresholds, CI gate status, self-QA pass count

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Official Playwright Docker container for baseline generation | High |
| P0 | Bounded self-QA protocol (2 passes, dual viewport, defect-only) | High |
| P0 | Negative asset constraints (no fabricated SVGs/testimonials) | High |
| P0 | Explicit tolerance thresholds (`maxDiffPixelRatio: 0.01`) | High |
| P0 | Hard CI gate with `ui-ux-designer`/`frontend-developer` approval | High |
| P1 | MSW network mocking for deterministic fixtures | Medium |
| P1 | Component isolation: Storybook + Chromatic TurboSnap + Playwright | Medium |
| P1 | Cross-browser matrix (Chromium/WebKit/Firefox) | Medium |
| P1 | Baseline update workflow with mandatory sign-off | Medium |
| P2 | Visual regression dashboard with PR-linked diffs | Low |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test baseline generation in `mcr.microsoft.com/playwright` Docker container
- Verify self-QA stops at 2 passes with defect-driven edits only
- Verify negative asset check rejects fabricated SVGs/testimonials
- Test `maxDiffPixelRatio: 0.01` catches real regressions
- Verify CI gate blocks merge without `ui-ux-designer`/`frontend-developer` approval
- Test MSW mocks provide deterministic visual fixtures
- Verify TurboSnap only re-tests changed component stories
- Verify baseline re-generation on driver version upgrade