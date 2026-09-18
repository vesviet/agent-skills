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
