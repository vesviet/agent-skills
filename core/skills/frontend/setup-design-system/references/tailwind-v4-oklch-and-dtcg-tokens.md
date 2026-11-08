# Tailwind v4, OKLCH Perceptual Tokens, and W3C DTCG Standards (2026)

## 1. Tailwind v4 CSS-First Architecture (`@theme`)

### 1.1 Complete Elimination of `tailwind.config.js`
Tailwind CSS v4 replaces JavaScript configuration files with native CSS `@theme` directives located directly inside CSS entrypoints:
- All design tokens, breakpoints, font families, and container metrics are declared as CSS custom properties within `@theme`.
- Zero configuration overhead; instantaneous compilation via the Lightning CSS engine.

---

## 2. OKLCH Perceptual Color Space

### 2.1 Perceptual Uniformity Across Themes
RGB and HSL color spaces exhibit severe non-linear perceived brightness shifts across different hues (e.g., pure yellow appears vastly brighter than pure blue at 50% lightness).
- **OKLCH Uniformity**: OKLCH separates perceived Lightness ($L$), Chroma ($C$), and Hue angle ($H$).
- Maintaining uniform $L$ across hues ensures identical contrast ratios against background surfaces:
  $$\text{Contrast Ratio}(\text{Surface}, \text{Text}) \ge 4.5:1 \quad (\text{WCAG 2.2 AA})$$

### 2.2 Pure CSS Variable Dark Mode
- Never pollute component JSX with ad-hoc `dark:bg-slate-900` or `dark:text-white` utility classes.
- Dark mode must be achieved exclusively by swapping CSS variable values in `:root` and `.dark`:
  ```css
  :root {
    --background: oklch(0.985 0.002 247);
    --foreground: oklch(0.145 0.005 247);
    --primary: oklch(0.488 0.243 264.376);
  }

  .dark {
    --background: oklch(0.145 0.005 247);
    --foreground: oklch(0.985 0.002 247);
    --primary: oklch(0.627 0.265 264.376);
  }
  ```

---

## 3. W3C Design Tokens Community Group (DTCG) Specification

### 3.1 Token Portability Contract
Design systems must export tokens in standardized W3C DTCG format for bidirectional synchronization with Figma Variables, Style Dictionary, and AI code generation tools:
```json
{
  "color": {
    "brand": {
      "primary": {
        "$type": "color",
        "$value": "oklch(0.488 0.243 264.376)",
        "$description": "Core interactive brand color meeting WCAG 2.2 AA contrast"
      }
    }
  },
  "spacing": {
    "base": {
      "$type": "dimension",
      "$value": "0.25rem"
    }
  }
}
```
