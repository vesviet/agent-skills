# Topic Board Template & Operations

The `task-planner` and `seo-analyst` must maintain a rolling 7-day topic board to manage the Dual-Site Sprint cadence.

## 1. 7-Day Rolling Board

The board dictates exactly what will be drafted, audited, and published over the next 7 days across the two sites.

**Mandatory Guardrails for the Board:**
- Exactly 1 post per day for `Lease in Vietnam`.
- Exactly 1 post per day for `Máy Lạnh Treo Tường`.
- Ensure no Search Intent is repeated within a 7-day window on the same site (Anti-Cannibalization check).

## 2. Template Structure (`plan-YYYY-MM-DD.md`)

When creating the weekly topic board, use the following structure for each entry to ensure all AEO/GEO and Topical rules are met:

```markdown
### [Date: YYYY-MM-DD] - [Site Name]

- **Target Keyword:** ...
- **Search Intent:** ...
- **Pillar / Cluster:** [Pillar Name] -> [Cluster Name]
- **GEO/AEO Requirement:** Ensure Answer-first intro. Specify exact data for Fact Density.
- **E-E-A-T Target:** Identify the Experience Proof to inject (e.g., "Personal visit to the showroom", "Reviewing our internal 2026 sales data").
- **Assigned Writer:** ...
- **Status:** [Planned / Briefed / Drafting / Auditing / Published]
```

## 3. Workflow Handoff

1. **`task-planner`** initializes the board and sets the dates/cadence.
2. **`seo-analyst`** fills in the Keywords, Intents, Pillar/Cluster, and E-E-A-T targets.
3. The brief is generated (`seo-content-brief.json`) and handed off to the **`content-writer`**.
