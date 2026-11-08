# React 19 Component Standards & Anti-Slop Mechanics (2026)

## 1. React 19 Form Actions & Optimistic State

### 1.1 Progressive Form Actions
Modern component architectures utilize native React 19 form actions and hooks, completely eliminating client-side `onSubmit` boilerplate:
- **`useActionState`**: Manages server action execution, returning pending status, errors, and updated form state.
- **`useOptimistic`**: Instantaneous UI updates rendering anticipated state while network action resolves in the background:
  ```tsx
  const [optimisticState, setOptimisticState] = useOptimistic(
    currentState,
    (state, update) => ({ ...state, ...update })
  );
  ```

---

## 2. Anti-Slop Finish Standards

To prevent unpolished "AI slop" in component interfaces, enforce the following five rules:
1. **Dynamic Viewport Units**: Use `min-h-[100dvh]` rather than `100vh` on full-screen containers to avoid mobile address bar jumps.
2. **Continuous Motion Isolation**: Never bind scroll, drag, or pointer movements to React `useState`. Use `motion/react` primitives (`useMotionValue`, `useTransform`) to update DOM nodes directly off the main thread.
3. **Tactile Feedback**: Interactive buttons and card triggers must provide physical feedback via active transform scaling: `active:scale-[0.98]`.
4. **CTA Text Stability**: Primary Call-To-Action buttons on desktop must include `whitespace-nowrap` to prevent awkward line breaks on localized strings.
5. **Icon Ecosystem Discipline**: Never inject raw, inline SVG markup. Only import vetted, accessible icon packages (`@radix-ui/react-icons`, `@phosphor-icons/react`, `hugeicons-react`).

---

## 3. Compound Component Architecture & Slot Delegation

### 3.1 Eliminating Boolean Prop Sprawl
Do not pass dozens of boolean flags (`isModal`, `hasHeader`, `withCloseIcon`, `isElevated`). Instead, structure components into compound primitives with Radix-style `asChild` slot delegation:
```tsx
<Dialog.Root open={isOpen} onOpenChange={setIsOpen}>
  <Dialog.Trigger asChild>
    <Button>Open Dialog</Button>
  </Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm" />
    <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
      <Dialog.Title>Settings</Dialog.Title>
      {children}
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

---

## 4. GenUI Automated Quality Gates

Every component authored or modified by AI agents must pass three automated pre-commit gates:
- **Design Token Conformance**: Zero hardcoded hex colors (`#ffffff`) or pixel spacing (`padding: 14px`). All tokens must map to Tailwind v4 CSS variables.
- **axe-core Accessibility Audit**: Zero automated WCAG 2.2 Level AA violations.
- **CSS Pollution Sweep**: Strip non-standard inline `style={{ ... }}` objects and rogue stylesheet imports.
