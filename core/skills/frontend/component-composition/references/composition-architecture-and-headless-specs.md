# Component Composition Architecture & Headless State Specifications

This reference provides architectural patterns, type definitions, and reference implementations for scalable component composition, Radix-style slot delegation (`asChild`), and headless state machine decomposition.

---

## 1. The Boolean Prop Proliferation Catalog

### 1.1 Combinatorial State Explosion ($2^N$)
When components attempt to handle visual or behavioral variants via boolean flags, internal state complexity explodes exponentially:

$$\text{State Combinations} = 2^N$$

Where $N$ is the number of boolean flags. A component with 7 booleans (`isCompact`, `hasIcon`, `isModal`, `withHeader`, `isHeader`, `isLoading`, `isHighlighted`) produces $2^7 = 128$ combinatorial states.

### 1.2 Pathologies of Boolean Proliferation
1. **Contradictory States**: The type system permits mutually incompatible flags simultaneously (e.g. `isCompact={true}` and `isExpanded={true}`).
2. **Conditional Spaghetti**: JSX renders nested ternaries and fragile logical operators.
3. **Inflexible Layouts**: Consumers cannot reorder, wrap, or inject custom siblings without introducing additional layout positioning props.
4. **Regression Fragility**: Modifying one boolean flag's CSS or logic risks cascading side-effects across all other $2^{N-1}$ states.

---

## 2. Compound Component Architecture

### 2.1 Context Interface Specification
Compound components decouple presentation from state by encapsulating shared logic inside a typed Context container with three distinct facets:

```tsx
export interface ComponentContextValue<TState, TActions, TMeta = Record<string, unknown>> {
  state: Readonly<TState>;
  actions: Readonly<TActions>;
  meta: Readonly<TMeta>;
}
```

### 2.2 Safe Context Hook Pattern
Always prevent silent null failures when subcomponents render outside their designated provider:

```tsx
import * as React from 'react';

export function createSafeContext<T>(contextName: string) {
  const Context = React.createContext<T | null>(null);

  function useSafeContext(): T {
    const value = React.use(Context);
    if (!value) {
      throw new Error(`useSafeContext: Component must be rendered within a <${contextName}.Provider>`);
    }
    return value;
  }

  return [Context, useSafeContext] as const;
}
```

---

## 3. Radix-Style Slot & Delegation Engine (`asChild`)

### 3.1 `composeRefs` Utility
Combines callback refs and object refs cleanly into a single callback ref:

```tsx
export function composeRefs<T>(...refs: (React.Ref<T> | undefined)[]) {
  return (node: T) => {
    refs.forEach((ref) => {
      if (!ref) return;
      if (typeof ref === 'function') {
        ref(node);
      } else {
        (ref as React.MutableRefObject<T | null>).current = node;
      }
    });
  };
}
```

### 3.2 `composeEventHandlers` Utility
Preserves consumer event listeners while executing component default actions unless `defaultPrevented`:

```tsx
export function composeEventHandlers<E extends React.SyntheticEvent>(
  originalHandler?: (event: E) => void,
  ourHandler?: (event: E) => void,
  { checkForDefaultPrevented = true } = {}
) {
  return (event: E) => {
    originalHandler?.(event);
    if (!checkForDefaultPrevented || !event.defaultPrevented) {
      ourHandler?.(event);
    }
  };
}
```

### 3.3 `Slot` Component Implementation
Delegates props, styles, event handlers, and refs to immediate children without adding extra DOM nodes:

```tsx
import * as React from 'react';

interface SlotProps extends React.HTMLAttributes<HTMLElement> {
  children?: React.ReactNode;
}

export const Slot = React.forwardRef<HTMLElement, SlotProps>((props, forwardedRef) => {
  const { children, ...slotProps } = props;

  if (React.isValidElement(children)) {
    const childRef = (children as any).ref;
    return React.cloneElement(children, {
      ...slotProps,
      ...children.props,
      className: [slotProps.className, children.props.className].filter(Boolean).join(' ') || undefined,
      onClick: composeEventHandlers(slotProps.onClick, children.props.onClick),
      ref: forwardedRef ? composeRefs(forwardedRef, childRef) : childRef,
    } as any);
  }

  return React.Children.count(children) > 1 ? React.Children.only(null) : null;
});
Slot.displayName = 'Slot';
```

---

## 4. Headless State Machine Hook Blueprint

Decouple behavioral and accessibility logic from visual presentation using headless hooks:

```tsx
export interface UseDialogOptions {
  defaultOpen?: boolean;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  id?: string;
}

export function useDialog({
  defaultOpen = false,
  open: controlledOpen,
  onOpenChange,
  id: customId,
}: UseDialogOptions = {}) {
  const [uncontrolledOpen, setUncontrolledOpen] = React.useState(defaultOpen);
  const isControlled = controlledOpen !== undefined;
  const isOpen = isControlled ? controlledOpen : uncontrolledOpen;

  const generatedId = React.useId();
  const id = customId || generatedId;
  const contentId = `${id}-content`;
  const titleId = `${id}-title`;

  const setOpen = React.useCallback(
    (next: boolean | ((prev: boolean) => boolean)) => {
      const resolved = typeof next === 'function' ? next(isOpen) : next;
      if (!isControlled) {
        setUncontrolledOpen(resolved);
      }
      onOpenChange?.(resolved);
    },
    [isControlled, isOpen, onOpenChange]
  );

  const open = React.useCallback(() => setOpen(true), [setOpen]);
  const close = React.useCallback(() => setOpen(false), [setOpen]);
  const toggle = React.useCallback(() => setOpen((prev) => !prev), [setOpen]);

  // Handle escape key
  React.useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') close();
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, close]);

  return {
    state: { isOpen },
    actions: { open, close, toggle, setOpen },
    triggerProps: {
      'aria-haspopup': 'dialog' as const,
      'aria-expanded': isOpen,
      'aria-controls': contentId,
      onClick: toggle,
    },
    contentProps: {
      id: contentId,
      role: 'dialog' as const,
      'aria-modal': true,
      'aria-labelledby': titleId,
    },
    titleProps: { id: titleId },
    closeProps: {
      onClick: close,
      'aria-label': 'Close',
    },
  };
}
```

---

## 5. React 19 Modernization Reference

| Pattern | React 18 Paradigm | React 19 Standard |
| :--- | :--- | :--- |
| **Ref Forwarding** | `React.forwardRef<HTMLElement, Props>((props, ref) => ...)` | Pass `ref` as standard prop: `function Component({ ref, ...props }: Props)` |
| **Context Consumption** | `const value = React.useContext(Context)` | `const value = React.use(Context)` (supports conditional calls) |
| **Context Provider** | `<Context.Provider value={value}>` | `<Context value={value}>` |
| **Server Actions** | Manual `fetch()` + `useTransition` boilerplate | `<form action={serverAction}>` + `useActionState` |

---

## 6. Anti-Patterns & Code Catalog

### 6.1 Bad: Boolean Prop Sprawl
```tsx
// Anti-Pattern: 12 props with boolean flags
<Modal
  isOpen={isOpen}
  hasBackdrop
  isScrollLocked
  withCloseButton
  isFullScreenOnMobile
  showConfirmButton
  confirmText="Save"
  onConfirm={handleSave}
/>
```

### 6.2 Good: Compound Composition with Slot Delegation
```tsx
// Compliant: Clear hierarchy and composability
<Dialog.Root open={isOpen} onOpenChange={setIsOpen}>
  <Dialog.Trigger asChild>
    <Button variant="primary">Edit Profile</Button>
  </Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay />
    <Dialog.Content>
      <Dialog.Title>Edit Profile</Dialog.Title>
      <ProfileForm />
      <Dialog.Close asChild>
        <Button variant="outline">Cancel</Button>
      </Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```
