# CAD Projection Conventions

Drafting standards and mathematical specifications for vector technical drawings, isometric projections, and mechanical schematics authored in SVG.

## 1. Physical Unit Mapping & Sheet Grammar

1. **Millimeter Coordinate System**: All vector coordinates must be calibrated such that $1\text{ SVG unit} = 1\text{ mm}$ of physical paper dimensions. Unitless pixel scaling or non-metric ratios are prohibited.
2. **Standard Drawing Sheet**:
   - Primary format: ISO Landscape A3 sheet ($420\text{mm} \times 297\text{mm}$).
   - SVG root declaration: `viewBox="0 0 420 297"` with `xmlns="http://www.w3.org/2000/svg"`.
   - Drawing border margin: $12\text{mm}$ inset from sheet boundary (`x="12" y="12" width="396" height="273"`).
   - Title band: $24\text{mm}$ height across the bottom inner border (`y="261" height="24"`), reserving fields for project name, drawing number, scale ratio, author role, and revision date.

## 2. Four-Tier Stroke Weight Hierarchy (ISO 128 / ISO 5456)

All vector paths must adhere strictly to the 4-tier stroke hierarchy calibrated in millimeters:

| Tier | Stroke Width | Line Role | SVG Attribute Definition |
| :--- | :--- | :--- | :--- |
| **Tier 1 (Heavy)** | `0.35mm` | Outer silhouettes, cutting plane boundaries, primary assembly perimeters | `stroke-width="0.35" stroke="currentColor"` |
| **Tier 2 (Medium)** | `0.22mm` | Visible component edges, internal contours, surface intersections | `stroke-width="0.22" stroke="currentColor"` |
| **Tier 3 (Light)** | `0.16mm` | Dimension lines, extension lines, leader callouts, cross-section hatching | `stroke-width="0.16" stroke="currentColor"` |
| **Tier 4 (Fine)** | `0.13mm` | Centerlines, pitch circles, construction guides, assembly explode trails | `stroke-width="0.13" stroke="currentColor"` |

Specialized line styles:
- **Hidden Features**: `stroke-width="0.16"` with `stroke-dasharray="2 1"`.
- **Centerlines / Symmetry Axes**: `stroke-width="0.13"` with `stroke-dasharray="6 1 1 1"`.
- **Assembly Explode Trails**: `stroke-width="0.13"` with `stroke-dasharray="4 1.5 1 1.5"`.

## 3. Isometric Transformation Matrix

The isometric projection maps 3D Cartesian coordinates $(x, y, z)$ into the 2D projection plane $(x_{\text{proj}}, y_{\text{proj}})$ using a standard $\pm 30^\circ$ isometric projection:

$$\begin{bmatrix} x_{\text{proj}} \\ y_{\text{proj}} \end{bmatrix} = \begin{bmatrix} \text{ox} \\ \text{oy} \end{bmatrix} + \text{scale} \cdot \begin{bmatrix} \frac{\sqrt{3}}{2} & -\frac{\sqrt{3}}{2} & 0 \\ 0.5 & 0.5 & -1.0 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \end{bmatrix}$$

Coordinate axes convention:
- $+x$ axis (width): Projects down-right at an angle of $+30^\circ$ below horizontal ($x_{\text{proj}} \propto +\frac{\sqrt{3}}{2}$, $y_{\text{proj}} \propto +0.5$).
- $+y$ axis (depth): Projects down-left at an angle of $+30^\circ$ below horizontal ($x_{\text{proj}} \propto -\frac{\sqrt{3}}{2}$, $y_{\text{proj}} \propto +0.5$).
- $+z$ axis (height): Projects vertically upwards at $90^\circ$ ($x_{\text{proj}} \propto 0$, $y_{\text{proj}} \propto -1.0$).

## 4. Ellipse Projection Geometry

Circles in 3D space project onto isometric planes as ellipses with a canonical aspect ratio of $\sqrt{3} : 1 \approx 1.732 : 1$:
- **Top Plane ($xy$)**: Major axis is horizontal ($0^\circ$), minor axis is vertical ($90^\circ$). Major radius $r_{\text{maj}} = r \cdot \sqrt{2} \approx 1.414 r$, minor radius $r_{\text{min}} = r \cdot \sqrt{2/3} \approx 0.816 r$ (or normalized scale equivalent).
- **Right Plane ($xz$)**: Major axis is tilted at $+60^\circ$ to horizontal.
- **Left Plane ($yz$)**: Major axis is tilted at $-60^\circ$ ($120^\circ$) to horizontal.

## 5. Typography and Annotation Grammar

- Font family: Clean system sans-serif (`font-family="system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"`).
- Title block lettering: `3.5mm` capital height (`font-size="3.5"`), bold weight.
- Section / view identifiers: `2.5mm` capital height (`font-size="2.5"`), semibold weight.
- Dimension numbers and callout text: `1.8mm` height (`font-size="1.8"`), regular weight.
- Leader lines must originate with a $0.8\text{mm}$ filled dot or closed $30^\circ$ arrowhead and terminate in a horizontal shoulder before annotation text.

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-10-15
