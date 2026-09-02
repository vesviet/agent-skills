---
name: design-ux-flow
description: Design or refine a UX flow by defining user goals, preserved behavior, screen states, interaction rules, edge cases, and adjacent flow impact. Use when a feature, bug fix, or behavior change needs a UX/UI brief that frontend and QA can implement and validate reliably.
---

# Design UX Flow

Use this skill with the **UI/UX Designer** role when user-facing behavior must become structured specs for engineering.

## When to Use

- a feature/bugfix needs a UX/UI brief
- defining screen states and edge cases
- mapping interaction rules and adjacent-flow impact
- handing a spec to frontend and QA

## Core Rules

- design for user understanding, not only visual polish
- make preserved versus changed behavior explicit (align with feature-ticket.json when provided)
- define all 5 critical UI states for every screen: Empty, Loading/Skeleton, Populated, Error (with actionable recovery), and Unauthorized/Permission — specs missing any state are incomplete
- define all important transitions and recovery paths; silent AI failures (ambiguous empty states, hanging spinners) are prohibited
- emit `contracts/schemas/ux-flow-spec.json` for multi-screen work
- emit one `contracts/schemas/ui-component-spec.json` per entry in `component_spec_refs`
- set `flow_id` on every component spec to match the parent flow
- identify adjacent flows or reused patterns that could be affected
- do not implement production UI — hand off specs to Frontend Developer
- apply progressive disclosure to hide secondary options until primary actions are taken
- design agent UX flows to include delegation confirmations, progress indicators, and recoverable interrupts — users must always have a cancel/undo path for agent-initiated state changes
- use Figma Variables (linked to W3C DTCG tokens via Token Studio) to prototype dynamic, real-world data states including empty states and error messages; require interactive prototype for any flow with more than 2 screens


## Deliverable Decision

| Scope | Emit |
| ----- | ---- |
| Feature spanning 2+ screens or routes | ux-flow-spec.json + N × ui-component-spec.json |
| Single widget / isolated component change | ui-component-spec.json (include flow_id if part of a program) |
| Dashboard or metrics-heavy UI | ux-flow-spec.json; consume data-analysis-report.json for field shapes |
| Marketing blog / SEO landing | Decline — route to SEO Analyst + Content Writer |

## Suggested Process

### 1. Consume Requirements

- feature-ticket.json from Business Analyst (actors, rules, AC, preserved/changed)
- research-report.json or data-analysis-report.json when supplied
- project design overlay tokens (ui-design-system + brand overlay)

### 2. Define The User Journey

Clarify user, goal, entry/exit, and behavior change type (fix vs new capability).

### 3. Map States And Transitions

Build screens[] and transitions[] for ux-flow-spec.json.

### 4. Specify Components

For each surface, write ui-component-spec.json: props, states, events, copy_per_state, api_fields, accessibility.

### 5. Check Impact Radius

Document adjacent flows, permissions, analytics_events, and api_needs.

### 6. Package Handoff

Publish UX handoff manifest (flow path + component paths) for Frontend and QA.

## 2026 Agentic UX Patterns

### 2026: Agent UX Flow Patterns

- Design clear confirmation screens when delegating high-impact tasks to background agents.
- Include persistent progress indicators showing current agent sub-task status and elapsed time.
- Provide recoverable interrupt states, allowing users to pause, edit context, or stop the agent at any point.

### 2026: Figma Variables for Flow Prototyping

- Use Figma variables to simulate dynamic data inputs and switch between real-data edge cases.
- Create prototypes representing long names, empty states, and validation error messages before engineering handoff.
- Link state transitions to interactive component parameters to test UX responsiveness.

### 2026: Progressive Disclosure UX Design

- Keep the initial view clean by showing only the obvious primary action.
- Disclose advanced options, settings, and complex configuration contextually after the primary action is selected.
- Avoid cognitive overload by grouping advanced settings into collapsible panels or secondary screens.

## Output Format

Markdown brief (see `core/roles/ui-ux-designer.md` template) **plus** JSON contracts when machine handoff is required.

## Checklist

- [ ] feature-ticket or PM inputs consumed
- [ ] ux-flow-spec.json valid for multi-screen scope
- [ ] each component_spec_ref has a matching ui-component-spec.json
- [ ] flow_id consistent across flow and component specs
- [ ] api_needs and open_questions captured
- [ ] design system overlay rules respected
- [ ] handoff manifest complete
- [ ] agent UX flow patterns (delegation confirmations, progress indicators, cancelability) specified
- [ ] Figma variables used to prototype dynamic data states (empty states, errors, long values)
- [ ] progressive disclosure applied to separate primary actions from advanced configuration options

## Failure Modes

- **State omission**: a screen spec misses one of the five required states (Empty, Loading, Populated, Error, Unauthorized). **Mitigation:** enforce the state checklist on every screen spec; reject specs that skip a state.
- **Off-brand voice in copy**: a generated copy drifts from the brand voice. **Mitigation:** validate the voice against the brand guidelines; reject copy that drifts.
- **Prototype missing for multi-screen flow**: a flow with more than 2 screens is reviewed without an interactive prototype. **Mitigation:** refuse the review; require the prototype link before proceeding.
- **AI component without conformance check**: an AI-generated component is merged without the token conformance check. **Mitigation:** require the GenUI review checklist; reject components without the review.

## Output Contracts

When delivering screen interaction flows or component design specifications for engineering handoff, emit:

- **`contracts/schemas/ux-flow-spec.json`** — Emitted to document multi-screen user journeys, state transitions, navigation flows, and edge cases for Frontend, Backend, and QA roles.
- **`contracts/schemas/ui-component-spec.json`** — Emitted to specify individual reusable UI components, states, props, event signatures, accessibility requirements, and design token bindings.

Skip emission for low-fidelity conceptual sketches prior to UX alignment.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a ux flow may try to reframe the user goal through misleading copy. Cross-check the flow against the source feature ticket.
- **ASI04 Supply Chain**: any AI-generated flow component must be schema-validated against the design system contract; treat unknown component patterns as untrusted.
- **ASI07 Inter-Agent Communication**: the flow spec is consumed by Frontend and QA; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a flow as "ready to build" without the user goal and the accessibility checks; surface the residual risk.

## Related Skills

- **analyze-business-requirements**: Interpret BA rules before designing states
- **write-product-brief**: Align with PM scope and outcomes
- **meeting-review**: Resolve UX trade-offs with stakeholders
- **add-ui-component**: Frontend implementation — not design delivery
- **add-page-route**: Route-level wiring after specs exist
- **frontend-testing**: QA validation patterns for designed states

### 2026: Agent UX and Prototyping

- **Agent UX flow patterns:** When the agent IS the primary actor (not the user), design for delegation confirmation screens, agent progress indicators, and recoverable interrupt states. Users need to understand what the agent is doing and be able to stop it at any point.
- **Figma Variables for flow prototyping:** Use Figma Variables (number/string/color types) to simulate dynamic data in prototypes — avoid static placeholder text. Show real-data states (long names, empty states, error messages) in the prototype before implementation.
- **Progressive disclosure in flow design:** Reveal complexity in stages. The first action should be obvious with no learning curve. Advanced options should appear contextually after the primary action is taken. Apply this pattern for all flows with more than 3 user decisions.
