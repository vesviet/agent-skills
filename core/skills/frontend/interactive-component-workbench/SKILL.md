---
name: interactive-component-workbench
description: Use when building scratch-route component workbenches with search-param state switchers and multi-variant pickers for isolated multi-state UI testing.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Interactive Component Workbench

Construct isolated, scratch-route component workbenches featuring URL search-parameter state switchers and multi-variant design pickers to explore, stress-test, and document interactive UI components in isolation from application business logic.

## Core Rules

- **Scratch-Route Isolation Boundary**: Workbenches live exclusively on dedicated client-side scratch routes (e.g. `app/scratch/workbench/page.tsx` with `"use client"`). They must never contaminate production routes or bundle unnecessary test dependencies into production builds.
- **Production Code Immutability**: Production components must not be modified with artificial state flags or conditional branches solely to accommodate the workbench. All state injection must occur via component props or wrapped context providers.
- **Search Parameter State Protocol**:
  - State switcher: Driven via `?__state=<state-slug>`. Renders reachable lifecycle and interaction states: `default`, `loading`, `empty`, `error`, `disabled`, and `focused`.
  - Variant picker: Driven via `?__variant=<variant-slug>`. Renders exactly 3 purposeful design variants along one designated variation axis.
  - History preservation: Search parameter changes must use shallow URL state replacement to prevent polluting browser history during interactive exploration:
    ```ts
    const updateParam = (key: string, val: string) => {
      const url = new URL(window.location.href);
      url.searchParams.set(key, val);
      window.history.replaceState({}, '', url.toString());
    };
    ```
- **The 5 Permissible Variation Axes**:
  1. *Structure*: Layout organization, grouping hierarchies, flat list vs elevated cards, and single vs multi-column arrangement.
  2. *Density*: Spacing scale adjustments (compact vs comfortable vs spacious padding and margin tokens).
  3. *Emphasis*: Surface treatment and hierarchy (solid accent fill vs subtle tonal tint vs minimal neutral border).
  4. *Type*: Typographic hierarchy (prominent display type vs restrained caption scale; unitless line-height scaling).
  5. *Voice*: Copy style and phrasing (direct and functional vs warm and conversational; technical vs consumer).
- **Switcher Architecture & Styling**:
  - Appearance: Styled in a dark neutral overlay (`background: rgb(20 20 20 / 0.92); backdrop-filter: blur(8px); color: #f5f5f5; border: 1px solid rgba(255, 255, 255, 0.1);`) with a system font stack to prevent visual blending into the component under test.
  - Responsive Container Collapse: At viewport widths $\ge 876\text{px}$, render the switcher as a sticky vertical sidebar; below $876\text{px}$, automatically collapse into a floating neutral overlay `<select>`:
    ```css
    @container (max-width: 875px) {
      .workbench-sidebar { display: none; }
      .workbench-select-overlay { display: block; }
    }
    ```
  - Keyboard Shortcut standard: Pressing `ArrowUp` / `ArrowDown` cycles through states; pressing the `H` key toggles switcher visibility on and off to enable clean screenshot captures without UI noise:
    ```ts
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes((e.target as HTMLElement)?.tagName)) return;
    if (e.key === 'h' || e.key === 'H') setIsHidden((prev) => !prev);
    ```
- **Container Query Isolation**: The workbench preview canvas must declare `container-type: inline-size;` so component responsive rules respond to canvas boundaries rather than full browser windows.
- **State Transition Continuity**: Switching states dynamically must not trigger unhandled unmount exceptions, memory leaks, or cumulative layout shift ($\text{CLS} = 0$).
- **Inviolable Quality Floor**: All generated variants and mock states must clear the 13 escalation triggers before mounting in the picker:
  - Accessible name present on every interactive control.
  - Visible `:focus-visible` focus ring present on keyboard focus.
  - Minimum contrast maintained ($L_c \ge 75$ body, $L_c \ge 60$ headline).
  - Mobile touch targets $\ge 44 \times 44\text{px}$.
  - Support for `prefers-reduced-motion: reduce`.
- **Mock Fixture Discipline**: State fixtures must be realistic, immutable (`Object.freeze`), and self-contained within the scratch route. Never depend on live production APIs or mutable databases.

## Suggested Process

1. **Scaffold Scratch Route**:
   - Create a scratch route file (e.g. `src/app/scratch/workbench/page.tsx`).
   - Import the component under test and wrap it in the project's root theme and styling provider.
   - Configure container queries on the preview canvas container (`container-type: inline-size`).
2. **Define Mock State Fixtures**:
   - Create comprehensive mock props covering every state: `default`, `loading`, `empty`, `error`, `disabled`.
   - Ensure error state includes recovery actions and empty state includes onboarding guidance.
3. **Configure the 5-Axis Variant Matrix**:
   - Select exactly one primary variation axis for exploration (e.g. Emphasis).
   - Author exactly 3 distinct variant fixtures demonstrating alternative token applications.
4. **Mount URL Search Param Switcher**:
   - Read `__state` and `__variant` parameters from the active URL search string.
   - Bind active state to the component props with immediate fallback to `default`.
5. **Attach Keyboard & Toggle Handlers**:
   - Register a `keydown` listener listening for `ArrowUp`, `ArrowDown`, and the `H` key.
   - Ensure keystrokes inside `<input>` or `<textarea>` do not inadvertently trigger workbench hotkeys.
6. **Verify Responsive Layout & Escalation Floor**:
   - Resize viewport below $876\text{px}$ to confirm overlay select collapse.
   - Audit all rendered states against the 13 escalation triggers.
7. **Document Findings & Handoff**:
   - Export approved component variants and verified prop configurations to implementation tickets.
   - Attach visual screenshots captured with switcher hidden (`H` hotkey).

## Anti-Patterns To Reject

- **Production Contamination**: Adding `if (process.env.NODE_ENV === 'test')` branches into production component files.
- **Unbounded Variation Axes**: Mixing structure, density, and emphasis simultaneously in a single variant review pass.
- **Unstyled Switcher Bleed**: Styling the workbench switcher with component tokens so it blends indistinguishably into the canvas.
- **Broken History Flooding**: Pushing hundreds of history entries via `router.push()` while arrowing through state permutations.
- **Accessibility Degradation**: Sacrificing focus indicators or contrast ratios in creative design variants.
- **Mutable Live Dependencies**: Connecting workbench mock states to mutable backend databases or live network endpoints.

## Switcher Specifications Table

| Element | Specification | Responsive Rule | Hotkey |
|---|---|---|---|
| Background | `rgb(20 20 20 / 0.92)` blur(8px) | Unaffected by theme tokens | — |
| Desktop Layout | Sticky vertical sidebar ($240\text{px}$) | Viewport width $\ge 876\text{px}$ | — |
| Mobile Layout | Floating neutral `<select>` overlay | Viewport width $< 876\text{px}$ | — |
| Visibility Toggle | Toggle DOM display / opacity | Preserved across state changes | Press `H` |
| State Cycle | Next / previous state navigation | Clamped to state array bounds | `ArrowUp` / `ArrowDown` |

## Output Contracts

- Emits `contracts/schemas/implementation-result.json` specifying verified component states, responsive breakpoints, and selected variant design tokens.

## Checklist

- [ ] Create an isolated scratch route under `app/scratch/` with `"use client"` directive.
- [ ] Implement search param state switcher reading `?__state=<slug>` with default fallback.
- [ ] Implement search param variant picker reading `?__variant=<slug>` along 1 variation axis.
- [ ] Provide mock fixtures for all reachable states (default, loading, empty, error, disabled).
- [ ] Style the switcher with dark neutral background (`rgb(20 20 20 / 0.92)`) and blur backdrop.
- [ ] Implement container query collapsing switcher to `<select>` overlay when width $< 876\text{px}$.
- [ ] Bind keyboard navigation: `ArrowUp`/`ArrowDown` for state cycling, `H` key for visibility toggle.
- [ ] Verify zero keyboard hotkey conflicts when focus is inside text input fields.
- [ ] Ensure all rendered states clear the 13 universal escalation triggers.
- [ ] Emit verified component results conforming to `contracts/schemas/implementation-result.json`.

## Related Skills

- **add-ui-component**: Implements production UI components tested on the workbench.
- **frontend-testing**: Automates multi-state assertions and screenshot regressions.
- **setup-design-system**: Configures tokens, spacing, and typography scales used on the workbench.
- **hostile-component-stress-testing**: Injects boundary stress inputs into workbench states.
