---
name: agent-panel-meeting
description: Orchestrate a 6-round, multi-role cross-examination panel meeting to debate architecture, code, or features and produce a final decision-ready JSON contract with trade-offs and residual risks. Use when rigorous cross-functional alignment is required before deciding, building, or shipping.
---

# Agent Panel Meeting

Use this skill to orchestrate an interactive, multi-round debate among multiple agent roles. This skill ensures that complex design decisions, architectures, or features are thoroughly vetted through cross-examination, rather than just collecting isolated opinions.

**Owner**: Agent Coordinator

## Role Categorization & Selection

To balance diverse perspectives while minimizing noise and token costs, panel selection must adhere to these rules:

1. **Panel Size**: Select a maximum of **3 to 4 Roles**. Do not exceed this limit.
2. **Categorization**: Classify available roles into three core groups:
   - **Builder**: Roles focused on creation and design (e.g., Developer, Architect).
   - **Defender**: Roles focused on safety, quality, and risk (e.g., Security, QA).
   - **Stakeholder**: Roles focused on business, users, and operations (e.g., Product, Ops).
3. **Mandatory Inclusion**: Every panel MUST include at least **1 Builder** and **1 Defender** to ensure structural balance between moving fast and staying safe.

## Prerequisite: Context Gathering (Phase 0)

To prevent token bloat and infinite reading loops, panel members must NOT read raw source code directly during the debate.
- **Action**: Before the meeting begins, the Agent Coordinator MUST run a context-gathering skill (such as `review-service` or `navigate-service`) to summarize the repository structure, conventions, and key files into a single context document.
- **Rule**: This context document serves as the sole initial input for the panel.

## Interaction Mechanism: The 6-Round Structure

Do not skip or merge rounds. Follow this exact 6-round iterative cross-examination process based on Collaborative Multi-Agent Debate (ColMAD):

### Round 1: Initial Thoughts (Isolated)
- **Action**: Each selected role provides their initial perspective, architecture recommendation, or analysis based purely on the user's requirements.
- **Rule**: Roles do not see each other's output yet.

### Round 2: Cross-Examination 1 (Rebuttal)
- **Action**: Reveal all Round 1 outputs to the panel. Each role must read the others' proposals, identify flaws, highlight risks, and provide rebuttals.
- **Rule**: Focus on breaking or challenging the assumptions made by the Builder roles.

### Round 3: Refinement
- **Action**: Based on the rebuttals from Round 2, each role updates, patches, or entirely pivots their proposed solution to address the highlighted risks.
- **Rule**: The updated proposals must explicitly reference the feedback that prompted the change.

### Round 4: Cross-Examination 2 (Edge Cases)
- **Action**: Reveal the refined Round 3 proposals. Roles perform a second, deeper cross-examination focusing strictly on edge cases, race conditions, integration points, or residual risks.
- **Rule**: No new foundational ideas; focus only on breaking the refined design.

### Round 5: Final Consensus Building
- **Action**: The roles attempt to reach a unified consensus using ColMAD non-zero-sum alignment. Each role must state their final position: "Agree", "Agree with reservations", or "Block".
- **Rule**: Do not force consensus if genuine disagreement remains. Capture the exact dissenting views and confidence scores.

### Round 6: Synthesis & HITL (Human-in-the-Loop)
- **Action**: The Agent Coordinator synthesizes the entire 5-round debate.
- **Rule**: 
  - Summarize the final trade-offs, stability convergence, and residual risks.
  - If there is a tie or a blocking objection, prepare a clear escalation to the user (HITL) to make the final call.

## Output Contracts

When the 6-round process completes, you MUST output the following two artifacts:

### 1. Structured JSON (A2A Contract)
Generate a JSON file conforming to `contracts/schemas/decision-record.json`. It must contain:
- The context and goal of the meeting.
- A summary of the arguments from each role.
- Identified trade-offs and residual risks.
- The final consensus or the specific decision requested from the user.

### 2. Human-Readable Summary (Markdown)
Generate a clear Markdown summary for the user to review. It must include:
- **The Panel**: Who participated and their category (Builder/Defender/Stakeholder).
- **The Debate**: Key pivots and rebuttals from the cross-examination rounds.
- **Trade-offs**: What we gain vs. what we lose.
- **HITL Decision Required**: A clear, actionable prompt asking the user to approve the recommendation or break a tie.

## Core Rules

- keep the panel size between 3 and 4 roles
- ensure at least 1 Builder and 1 Defender role participate in every meeting
- do not allow roles to read raw source code during debate; use Phase 0 context document only
- execute all 6 rounds sequentially without skipping or merging rounds
- apply Collaborative Multi-Agent Debate (ColMAD) non-zero-sum evaluation to avoid adversarial debate hacking
- require explicit Human-in-the-loop (HITL) sign-off for tie-breaking or unresolved blocking concerns
- emit both machine-readable `decision-record.json` and a human-readable Markdown summary

## Suggested Process

### 1. Phase 0: Context Gathering
Run `review-service` or `navigate-service` to produce a single context summary document of the target repo or component.

### 2. Panel Selection
Select 3-4 roles categorized into Builder (Dev/Architect), Defender (Security/QA), and Stakeholder (Product/Ops).

### 3. Execute 6-Round Debate
- **Round 1 (Initial Thoughts)**: Roles produce independent initial perspectives.
- **Round 2 (Rebuttal 1)**: Roles read all Round 1 outputs and cross-examine Builder assumptions.
- **Round 3 (Refinement)**: Roles update their proposals based on Round 2 feedback.
- **Round 4 (Rebuttal 2)**: Deep cross-examination targeting edge cases and residual risks.
- **Round 5 (Final Consensus)**: Roles state final vote (Agree / Agree with reservations / Block).
- **Round 6 (Synthesis & HITL)**: Agent Coordinator synthesizes trade-offs and escalates to HITL.

## Checklist

- [ ] Panel size is 3 to 4 roles maximum
- [ ] At least 1 Builder and 1 Defender included
- [ ] Phase 0 context document gathered before Round 1
- [ ] All 6 rounds completed in sequence
- [ ] `contracts/schemas/decision-record.json` generated
- [ ] Human-readable Markdown summary with HITL decision point generated
- [ ] ColMAD non-zero-sum consensus captured with explicit trade-offs

## Related Skills

- **meeting-review**: Single-response synthesis review for smaller proposals
- **agent-delegation**: Used to dispatch sub-tasks to panel members via A2A
- **review-service**: Context-gathering skill for Phase 0 repo reviews
- **navigate-service**: Codebase entry-point mapping for Phase 0 context

## Guardrails
- **Token Lock**: Do not allow the meeting to run into infinite loops. Halt strictly after Round 5 and synthesize in Round 6.
- **Theater Lock**: Do not invent fake disagreements. If the topic is trivial and all roles agree in Round 2, document the early consensus but ensure edge cases are still checked in Round 4.
- **Registry Lock**: Only invite roles that exist in the agent registry or repository.


