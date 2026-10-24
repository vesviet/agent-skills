## UI/UX Designer Review Checklist

This reference checklist provides operational design governance, anti-slop aesthetic restraint, AI interaction design, accessibility compliance, and design-system token criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across anti-slop visual restraint (The Three Dials), eyebrow label rationing, hero section viewport fitting, unified call-to-action intent, comprehensive AI state design, European Accessibility Act (EAA) compliance, Generative UI (GenUI) palette governance, and automated design token export pipelines.

### 1. Anti-Slop Aesthetic Restraint & The Three Dials (`ANTI-SLOP-DESIGN LOCK`)
- **Mandatory 1-Line Design Read**:
  - every design specification begins with an explicit 1-line Design Read articulating page kind, target audience, brand tone, and visual family
  - generic AI clichés strictly rejected fail-closed: centered heroes on dark mesh gradients, oversaturated neon purple/blue glows, three identical feature cards with generic icons, and unbranded rounded cards
- **Quantitative Calibration of The Three Dials**:
  - design specifications explicitly calibrate the three aesthetic parameters:
    1. `DESIGN_VARIANCE` (1–10, recommended 3–6): degree of layout divergence from standard grid conventions
    2. `MOTION_INTENSITY` (1–10, recommended 2–5): animation velocity, spring stiffness, and transition frequency; animations must strictly obey `prefers-reduced-motion`
    3. `VISUAL_DENSITY` (1–10, recommended 5–8): information density, typography scale ratio, and whitespace rationing
  - accent saturation capped ($< 80\%$ HSL saturation) with a single dominant accent hue; multi-color neon palettes prohibited

### 2. Eyebrow Label Rationing & Restraint (`EYEBROW-RESTRAINT LOCK`)
- **Strict Eyebrow Label Frequency Cap**:
  - uppercase, wide-tracking eyebrow badges/labels restricted to at most 1 out of every 3 page sections (e.g. a 9-section landing page may possess at most 3 eyebrows total, with hero counting as 1)
  - redundant or decorative category tags eliminated in favor of clean, self-explanatory section headlines

### 3. Hero Section Viewport Fitting & Typography Limits (`HERO-VIEWPORT LOCK`)
- **Initial Viewport Accessibility**:
  - hero section on desktop viewports ($\ge 1280\text{px}$) must fit entirely within the initial viewport fold ($100\text{vh}$) without requiring user scroll
  - headline strictly capped at 2 lines maximum; subtext capped at 20 words across 3–4 lines; top container padding capped at `6rem` (`pt-24`)
- **Above-the-Fold Actionability**:
  - primary call-to-action (CTA) buttons must be immediately visible and clickable above the fold on all standard display resolutions

### 4. Call-to-Action (CTA) Intent Unification (`CTA-INTENT LOCK`)
- **Single Label Per User Intent**:
  - buttons driving the same conversion action across the page must use an identical, unified label (e.g. consistently "Start Free Trial", not alternating between "Try Now", "Get Started", and "Sign Up Free")
  - desktop button text fits on a single line (maximum 3 words); ambiguous or jargon-heavy labels prohibited

### 5. Comprehensive AI State Design (`AI-STATE LOCK` / `TRUST-DESIGN LOCK`)
- **Five AI-Specific Component States**:
  - every AI-powered interface component specifies explicit visual treatments for all five non-standard states:
    ```tsx
    // POSITIVE: Five Mandatory States in Component Specification
    export function AIActionContainer({ state, output, confidence, onOverride }: AIActionProps) {
      switch (state) {
        case 'generating':  return <SkeletonStreamingIndicator text="Synthesizing plan..." />;
        case 'uncertain':   return <UncertaintyBanner confidence={confidence} explain="Model flagged boundary case" />;
        case 'fallback':    return <DeterministicManualInputForm error="AI service unavailable" />;
        case 'overridden':  return <UserOverrideDiffView original={output} onRevert={onOverride} />;
        case 'corrected':   return <FeedbackSavedToast message="Calibration recorded for future runs" />;
        default:            return <VerifiedOutputCard data={output} />;
      }
    }
    ```
  - probabilistic outputs never presented as absolute facts; confidence ranges and "Why am I seeing this?" explanatory hooks provided for automated recommendations

### 6. Accessibility Compliance (WCAG 2.2 Level AA / EAA 2025 / EN 301 549)
- **Mathematical Contrast Ratio Formulation**:
  - all text and interactive UI elements must satisfy the relative luminance contrast ratio invariant:
    $$CR = \frac{L_1 + 0.05}{L_2 + 0.05} \ge 4.5:1 \text{ (normal text)}, \ge 3.0:1 \text{ (large text / UI controls)}$$
    where relative luminance $L$ is calculated per sRGB definition:
    $$L = 0.2126 \cdot R + 0.7152 \cdot G + 0.0722 \cdot B$$
  - dark mode and light mode palettes tested independently across all surface elevation tokens
- **Touch Target & Keyboard Navigation**:
  - touch targets enforce minimum $24\times 24\text{px}$ bounding box with $\ge 8\text{px}$ spacing (or minimum $44 \times 44\text{px}$ without spacing)
  - keyboard focus indicators must be explicitly styled (`outline: 2px solid var(--color-focus-ring)`); CSS rules removing outline (`outline: none`) without custom focus styles are strictly rejected

### 7. Generative UI (GenUI) Component Governance (`GENUI-GOVERNANCE LOCK`)
- **Strict Component Palette Boundaries**:
  - AI-assembled dynamic interfaces restricted to an approved allowlist of design system components; unapproved raw HTML or rogue layout combinations rejected fail-closed:
    ```json
    {
      "allowed_components": [
        "Card", "MetricCard", "TimeSeriesChart", "DataTable", "AlertBanner"
      ],
      "forbidden_combinations": [
        ["AlertBanner", "HeroHeadline"]
      ],
      "max_dynamic_depth": 3
    }
    ```
  - deterministic fallback UI renders immediately if generative assembly violates layout constraints or fails client validation

### 8. Automated Design Token Export Pipeline (`TOKEN-EXPORT LOCK`)
- **Single Source of Truth via Style Dictionary**:
  - design tokens (colors, typography, spacing, shadows, radii) exported through an automated build pipeline (Figma Tokens / Style Dictionary $\rightarrow$ CSS/Tailwind variables):
    ```css
    :root {
      --color-primary-500: #1a56db;
      --color-surface-base: #ffffff;
      --color-text-primary: #111827;
      --color-focus-ring: #3b82f6;
      --spacing-grid-base: 4px;
      --radius-interactive: 8px;
    }
    ```
  - manual hardcoding of hex values or arbitrary pixel margins into component styles is strictly prohibited

### 9. Interaction Performance & Frame Budgets
- **Web Vitals & Interaction Latency**:
  - Interaction to Next Paint (INP) targeted at $\le 200\text{ms}$; visual feedback on click/tap rendered within $\le 100\text{ms}$
  - CSS transitions and animations constrained to GPU-accelerated properties (`transform`, `opacity`); layout-triggering animations (`width`, `height`, `top`) prohibited in hover/active states

### 10. Operational Failure Modes & Escalation Protocols
- **Layout Shift Prevention**:
  - skeleton loaders and image containers must reserve explicit aspect ratios (`aspect-ratio: 16/9`) to maintain Cumulative Layout Shift ($CLS \le 0.1$)
- **Streaming UI Stalls**:
  - client timeouts detected if SSE token stream drops for $> 5\text{s}$; fallback banner with retry button presented

### 11. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Three Dials Setting** | Dials within calibrated bounds | Design spec review | Explicit ratings 1–10 declared |
| **Contrast Ratio** | $CR \ge 4.5:1$ (normal text) | Axe / Lighthouse Accessibility | 0 WCAG 2.2 AA contrast violations |
| **Eyebrow Ratio** | $\le 1 \text{ eyebrow} / 3 \text{ sections}$ | Section count audit | Cap strictly respected |
| **Hero Viewport** | Height $\le 100\text{vh}$ on desktop | Viewport inspector at 1280px | 0 scroll required for CTA |
| **Focus Indicator** | Visible outline on focus | Keyboard tab traversal test | Non-zero visible focus ring |
| **Touch Target Size** | Size $\ge 24\text{px}$ + $8\text{px}$ margin| Chrome DevTools Elements audit | 0 sub-size tap targets |
| **Design Tokens** | 0 hardcoded hex codes | `rg -i "#[0-9a-f]{3,6}" src/components/` | 0 direct hex codes |
| **UI Spec Contract** | Valid `ui-spec.json` | `python3 core/scripts/validate-contracts.py` | 100% schema compliant |
