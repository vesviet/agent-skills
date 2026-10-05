## UI/UX Designer Review Checklist

This reference checklist provides operational design governance, anti-slop aesthetic restraint, AI interaction design, accessibility compliance, and design-system token criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across anti-slop visual restraint (The Three Dials), eyebrow label rationing, hero section viewport fitting, unified call-to-action intent, comprehensive AI state design, European Accessibility Act (EAA) compliance, Generative UI (GenUI) palette governance, and automated design token export pipelines.

### 1. Anti-Slop Aesthetic Restraint & The Three Dials (`ANTI-SLOP-DESIGN LOCK`)
- **Mandatory 1-Line Design Read**:
  - every design specification begins with an explicit 1-line Design Read articulating page kind, audience, tone, and design system aesthetic family
  - generic AI clichés strictly rejected: centered heroes on dark mesh gradients, oversaturated neon purple/blue glows, three identical feature cards, and clichéd typography pairings
- **Calibration of The Three Dials**:
  - design specifications explicitly calibrate the three aesthetic parameters:
    1. `DESIGN_VARIANCE` (1–10): degree of layout divergence from convention
    2. `MOTION_INTENSITY` (1–10): animation velocity, spring stiffness, and transition frequency
    3. `VISUAL_DENSITY` (1–10): information density and whitespace rationing
  - accent saturation capped ($<80\%$ HSL saturation) with a single dominant accent hue

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
    1. **Generating / Thinking**: skeleton loaders, progress steppers, or non-blocking streaming indicators
    2. **Uncertain**: visual indicator reflecting low model confidence with calibrated microcopy
    3. **Fallback**: graceful degradation to deterministic form or manual input when AI fails
    4. **Overridden**: clean visual feedback when a user edits, rejects, or reverts AI-suggested content
    5. **Corrected**: explicit confirmation when user feedback is submitted to the system
- **Anti-Overconfidence & Transparency Hooks (`AI-OVERCONFIDENCE LOCK`)**:
  - probabilistic outputs never presented as absolute facts; confidence ranges and "Why am I seeing this?" explanatory hooks provided for automated recommendations

### 6. Accessibility Compliance (WCAG 2.2 AA / EAA 2025 / EN 301 549)
- **Legal Accessibility Standard Conformance (`ACCESSIBILITY-COMPLIANCE LOCK`)**:
  - all interactive components achieve WCAG 2.2 AA conformance as mandated by the European Accessibility Act (EAA):
    - minimum 4.5:1 contrast ratio for normal text; 3:1 for large text and UI components
    - minimum $24\times 24\text{px}$ touch target size for interactive controls
    - full keyboard navigation support with visible, non-obscured focus indicators
    - ARIA live regions configured for dynamic streaming updates and status messages

### 7. Generative UI (GenUI) Component Governance (`GENUI-GOVERNANCE LOCK`)
- **Strict Component Palette Boundaries**:
  - AI-assembled dynamic interfaces restricted to an approved allowlist of design system components; unapproved raw HTML or rogue layout combinations rejected fail-closed
  - deterministic fallback UI renders immediately if generative assembly violates layout constraints or fails client validation

### 8. Automated Design Token Export Pipeline (`TOKEN-EXPORT LOCK`)
- **Single Source of Truth via Style Dictionary**:
  - design tokens (colors, typography, spacing, shadows, radii) exported through an automated build pipeline (Figma Tokens / Style Dictionary $\rightarrow$ CSS/Tailwind variables)
  - manual hardcoding or copy-pasting of hex values, pixel sizes, or magic numbers into component styles strictly prohibited
