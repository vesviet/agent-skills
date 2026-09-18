# View Transitions & Motion Optimization Specifications

This reference provides production CSS recipes, React 19 / Next.js / Astro integration patterns, and Core Web Vitals optimization guidelines for the native CSS View Transitions API.

---

## 1. Production CSS Animation Recipes

### 1.1 Timing Variables and Easing
```css
:root {
  --duration-exit: 150ms;
  --duration-enter: 210ms;
  --duration-move: 380ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --ease-emphasized: cubic-bezier(0.05, 0.7, 0.1, 1);
}
```

### 1.2 Smooth Crossfade
```css
::view-transition-old(.fade-out) {
  animation: var(--duration-exit) var(--ease-standard) both fade-out;
}
::view-transition-new(.fade-in) {
  animation: var(--duration-enter) var(--ease-standard) both fade-in;
}

@keyframes fade-out {
  from { opacity: 1; }
  to { opacity: 0; }
}
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

### 1.3 Directional Navigation Slides
```css
/* Forward Navigation: Old slides left, New slides in from right */
::view-transition-old(.slide-to-left) {
  animation: var(--duration-exit) var(--ease-standard) both slide-left-out;
}
::view-transition-new(.slide-from-right) {
  animation: var(--duration-enter) var(--ease-emphasized) both slide-right-in;
}

/* Backward Navigation: Old slides right, New slides in from left */
::view-transition-old(.slide-to-right) {
  animation: var(--duration-exit) var(--ease-standard) both slide-right-out;
}
::view-transition-new(.slide-from-left) {
  animation: var(--duration-enter) var(--ease-emphasized) both slide-left-in;
}

@keyframes slide-left-out {
  to { transform: translateX(-25%); opacity: 0; }
}
@keyframes slide-right-in {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
@keyframes slide-right-out {
  to { transform: translateX(25%); opacity: 0; }
}
@keyframes slide-left-in {
  from { transform: translateX(-100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
```

### 1.4 Persistent App Shell Isolation
Prevent sticky headers and sidebars from animating during page transitions:
```css
::view-transition-group(site-header),
::view-transition-group(site-sidebar),
::view-transition-group(site-dock) {
  animation: none !important;
  z-index: 100;
}
```

### 1.5 Mandatory Reduced Motion Reset (WCAG 2.2 AA)
```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation: none !important;
    animation-duration: 0.01ms !important;
  }
}
```

---

## 2. React 19 & Next.js App Router Integration

### 2.1 DirectionalTransition Component
```tsx
import * as React from 'react';
import { ViewTransition } from 'react';

interface DirectionalTransitionProps {
  children: React.ReactNode;
  direction?: 'forward' | 'back' | 'none';
}

export function DirectionalTransition({
  children,
  direction = 'none',
}: DirectionalTransitionProps) {
  return (
    <ViewTransition
      default="none"
      enter={{
        'nav-forward': 'slide-from-right',
        'nav-back': 'slide-from-left',
        default: 'none',
      }}
      exit={{
        'nav-forward': 'slide-to-left',
        'nav-back': 'slide-to-right',
        default: 'none',
      }}
    >
      {children}
    </ViewTransition>
  );
}
```

### 2.2 Shared Element Morphing Example
```tsx
import { ViewTransition } from 'react';
import Link from 'next/link';

interface ProductCardProps {
  id: string;
  title: string;
  imageUrl: string;
}

export function ProductCard({ id, title, imageUrl }: ProductCardProps) {
  return (
    <div className="product-card">
      <Link href={`/products/${id}`}>
        <ViewTransition name={`product-hero-${id}`} share="morph" default="none">
          <img src={imageUrl} alt={title} className="product-thumb" />
        </ViewTransition>
        <h3>{title}</h3>
      </Link>
    </div>
  );
}
```

---

## 3. Astro v5 Multi-Page Navigation

### 3.1 Layout Root Setup
```astro
---
// src/layouts/BaseLayout.astro
import { ClientRouter } from 'astro:transitions';
---
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <ClientRouter />
  </head>
  <body>
    <slot />
  </body>
</html>
```

### 3.2 Astro Directives
- `transition:name="unique-id"`: Pair elements across routes for shared morphing.
- `transition:animate="morph" | "slide" | "fade"`: Define default route animation.
- `transition:persist`: Preserve state and DOM elements (video players, inputs) across navigations.

---

## 4. Core Web Vitals (INP < 200ms) Performance Budget

1. **Composited Properties Only**: Animate strictly `transform` and `opacity`. Never animate `width`, `height`, `top`, `left`, `margin`, or `padding`.
2. **Fast Mutation Callbacks**: Ensure DOM updates in `document.startViewTransition(fn)` complete in under 50ms.
3. **Data Pre-Fetching**: Always fetch route data or pre-cache images before initiating transitions. Never execute asynchronous I/O inside the synchronous transition callback.
4. **Main Thread Yielding**: For large DOM re-renders, chunk operations with `scheduler.yield()` or `requestIdleCallback()`.

---

## 5. Anti-Patterns & Pitfalls

### 5.1 Animating Layout Dimensions (Reflow Jank)
- **Bad**: Animating `height: 0 -> 400px` triggers reflow on every frame.
- **Good**: Animate `transform: scaleY(0) -> scaleY(1)` for GPU-accelerated compositing.

### 5.2 Non-Unique Shared Transition Name Collision
- **Bad**: Rendering multiple items with `name="item-hero"` throws `InvalidStateError`.
- **Good**: Scope names dynamically: `name={`item-hero-${item.id}`}`.

### 5.3 Omission of `default="none"`
- **Bad**: A `<ViewTransition>` without `default="none"` flashes a full crossfade on every background data revalidation.
- **Good**: Always declare `default="none"` to explicitly opt into intentional transitions only.

---

## 6. Frequency-Based Animation Budget (Emil Kowalski)

Animation latency must be inversely proportional to the frequency of user interaction.

| Tier | Interaction Category | Components / Triggers | Max Allowed Duration | Easing / Physics Curve | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 0** | **High-Frequency (Instant)** | Hotkey invocation (`Cmd+K`, `Ctrl+P`), Combobox filtering, Autocomplete suggestions, Tooltips on hover, Focus rings, Keyboard tab switching | **0ms (Instant)** | Linear / step-start (zero transition) | User expects instant responsiveness. Any spring or slide animation on hotkeys creates perceived lag and motion sickness. |
| **Tier 1** | **Micro-Interactions (Snappy)** | Button press/depress, Checkbox check, Switch toggle, Accordion single item toggle, Dropdown menu popover | **100ms – 150ms** | Snappy Spring: `stiffness: 450, damping: 35, mass: 1` (or `cubic-bezier(0.16, 1, 0.3, 1)`) | Provides tactile confirmation that input was registered without delaying subsequent user actions. |
| **Tier 2** | **Medium-Frequency Overlays (Strictly Bounded)** | Modal Dialogs, Slide-over Drawers / Sheets, Alert Dialogs, Toast Notifications | **150ms – 250ms** *(Strict ceiling: 250ms)* | Bounded Spring: `stiffness: 320, damping: 28, mass: 1` (or `cubic-bezier(0.32, 0.72, 0, 1)`) | Communicates spatial context (where overlay originated) while swiftly revealing actionable UI. Exceeding 250ms is anti-pattern slop. |
| **Tier 3** | **Low-Frequency Narrative (Expressive)** | Route / Page transitions, First-load Hero reveal, Milestone celebration modals, Onboarding walkthrough steps | **250ms – 400ms** *(Strict ceiling: 400ms)* | Gentle Spring: `stiffness: 220, damping: 24, mass: 1` | Storytelling and spatial orientation for infrequent events. Never exceed 400ms under any circumstance. |

---

## 7. Harmonic Oscillator Spring Physics Parameters

Physical UI motion is governed by the second-order harmonic oscillator equation:
$$m \frac{d^2 x}{dt^2} + c \frac{dx}{dt} + k x = 0$$

Where $m = 1.0$ (fixed mass), $k$ is spring tension (stiffness), and $c$ is friction (damping).
The damping ratio $\zeta = \frac{c}{2\sqrt{k \cdot m}}$ must remain in the **near-critically damped range ($\zeta \approx 0.75 - 0.85$)** to guarantee rapid arrival without amateurish cartoon bouncing.

| Profile Name | Target Use Cases | Mass ($m$) | Stiffness ($k$) | Damping ($c$) | Damping Ratio ($\zeta$) | Settling Time ($t_s$) | Perceived Feel |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Snappy Micro** | Checkbox check, Switch toggle, Button active press, Icon morph | `1.0` | `450` | `35` | $\approx 0.82$ | $\approx 120\text{ms}$ | Tactile, crisp, mechanical, immediate |
| **Bounded Overlay** | Modal Dialogs, Slide-over Sheet / Drawers, Context Menus | `1.0` | `320` | `28` | $\approx 0.78$ | $\approx 180\text{ms}$ | Fluid, responsive, polished, spatial |
| **Gentle Morph** | Accordion expansion, Shared element displacement, Card open | `1.0` | `220` | `24` | $\approx 0.81$ | $\approx 240\text{ms}$ | Smooth, readable, calm, elegant |
| **Immediate Rigid** | Hotkey palettes (`Cmd+K`), Combobox search dropdowns | `N/A` | `N/A` | `N/A` | `1.0` (Critical) | `0ms` | Instantaneous, zero latency |

### Banned Spring Configurations
- Cartoonish Bouncy Springs: $\zeta < 0.6$ (e.g. `stiffness: 500, damping: 10`), which oscillate 4+ times before settling.
- Heavy Sluggish Inertia: $m > 1.5$, which causes elements to feel slow and unresponsive.

---

## 8. Single Smooth-Scroll Engine Exclusivity Lock

### Architectural Exclusivity Rule
A repository must install and initialize **EXACTLY ONE** smooth-scroll coordinator across its entire tree:
- **Recommended**: `lenis` (`lenis/react`), which works on native scroll coordinates without translating the root element, preserving full accessibility and integrating cleanly with GSAP and Framer Motion.
- **Alternative**: Native CSS `html { scroll-behavior: smooth; }`.
- **Strict Prohibition**: Never install `@studio-freight/lenis` (or `lenis`) AND `locomotive-scroll` simultaneously. Dual `wheel` listeners fight for scroll coordinates, generating frame drops, micro-stuttering, cursor jumping, and breaking native keyboard navigation (`Tab`, `PageDown`).
- **Reduced Motion**: Always honor `prefers-reduced-motion: reduce` by disabling smooth scrolling and reverting to instant native navigation.

