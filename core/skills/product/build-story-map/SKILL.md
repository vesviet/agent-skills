---
name: build-story-map
description: Structure and visualize product backlogs using Jeff Patton User Story Mapping, MoSCoW release swimlanes, and Critical Path Method (CPM) dependency scheduling. Use when organizing features into Epic-to-Story hierarchies, defining MVP walking skeletons, slicing releases, calculating float time on critical path tasks, or handing off scoped initiatives to engineering.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Build Story Map

Use this skill to structure product requirements into multidimensional User Story Maps, define MVP walking skeletons, slice releases into prioritized swimlanes, and schedule dependencies using the Critical Path Method (CPM).

## When to Use

- converting linear, overwhelming backlogs into structured 2D User Story Maps
- defining the minimum end-to-end viable product (**Walking Skeleton**) for early testing
- slicing feature releases into thematic swimlanes (MVP, Release 1.1, Release 2.0)
- conducting MoSCoW prioritization across release slices
- analyzing project schedule dependencies and calculating critical path float time (CPM)
- preparing structured, unambiguous delivery handoffs for engineering and business analysis

## Core Rules

- **Enforce Jeff Patton 2-Dimensional Story Map Structure**:
  - *Horizontal Axis (Narrative Flow / User Journey)*:
    - Top Level: **User Activities** (The Backbone; e.g. Discover, Onboard, Create, Checkout)
    - Mid Level: **User Tasks / Steps** (The Walking Skeleton; e.g. Select Plan, Enter Payment)
  - *Vertical Axis (Release Priority & Depth)*:
    - Slice down by sophistication: MVP (simplest functional end-to-end path) → Iteration 1 → Future Enhancements
- **Mandate the Walking Skeleton Concept**:
  - The MVP slice must be a complete end-to-end journey that works, even if crude or manual behind the scenes
  - Ban building disconnected silos (e.g. 100% of User Management built while Checkout remains non-functional)
- **Tag MoSCoW Priorities per Swimlane**:
  - *Must-Have (M)*: Non-negotiable for that specific release slice
  - *Should-Have (S)*: Important but not critical to initial go-live
  - *Could-Have (C)*: Desirable delighter if velocity permits
  - *Won't-Have this time (W)*: Explicitly excluded from the active swimlane
- **Apply Critical Path Method (CPM) Analysis**:
  - Map explicit dependency arrows between cross-functional delivery tasks
  - Calculate Early Start (ES), Early Finish (EF), Late Start (LS), and Late Finish (LF)
  - Identify the **Critical Path**: sequence of dependent tasks where $\text{Float} = \text{LS} - \text{ES} = 0$; any delay on this path directly delays project launch
- **Structured A2A Delivery Handoff**:
  - Every mapped story must be ready for export into `core/contracts/schemas/feature-ticket.json`
- Detailed worked examples, CPM calculations, and mermaid templates: [`references/story-mapping-and-cpm-scheduling.md`](references/story-mapping-and-cpm-scheduling.md)

## Suggested Process

### 1. Frame the User Persona & Problem Scenario
Identify the target actor and their primary end-to-end goal.

### 2. Map the Backbone (Activities & Tasks)
Write out the sequential user steps from left to right along the horizontal timeline. Group steps into major Activity clusters.

### 3. Brainstorm Stories & Details Vertically
Under each user step, brainstorm user stories representing variations, deeper functionality, and edge cases.

### 4. Slice into Release Swimlanes
Draw horizontal release slices. Carve out the Walking Skeleton (MVP) that provides the thinnest viable slice across all activities. Assign subsequent stories to Release 1.1 and Release 2.0.

### 5. Calculate Dependencies & Critical Path (CPM)
Convert the release swimlane into a task dependency network. Perform forward and backward passes to compute total float and highlight the Critical Path.

## Checklist

- [ ] horizontal backbone captures full chronological customer journey
- [ ] Walking Skeleton (MVP) connects all backbone activities end-to-end
- [ ] every story contains a clear user value statement (`As a... I want... So that...`)
- [ ] MoSCoW tags applied to all stories within the active release slice
- [ ] cross-team dependencies explicitly identified
- [ ] CPM analysis identifies critical path tasks with zero float
- [ ] stories prepared for handoff to BA and engineering via structured contracts

## Related Skills

- **define-product-strategy**: provide PR/FAQ and Opportunity Solution Tree context
- **prioritize-roadmap**: supply RICE scores and capacity timeboxes
- **write-product-brief**: generate formal product brief documents
- **write-use-cases**: expand complex story map steps into 13-field Use Case specifications
- **trace-requirements-impact**: track dependency blast radius when requirements change
