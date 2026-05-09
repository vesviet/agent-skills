# 🚀 Agent-Skills v2.0: The Complete User Guide

Welcome to the **Agent-Skills v2.0** ecosystem. This system transforms standard AI coding assistants into an **Autonomous Swarm Environment**. Instead of having one general AI try to do everything, you now have a team of highly specialized, policy-driven "Virtual Employees" that can talk to each other using strict Data Contracts.

---

## 1. Core Concepts of v2.0

- **Policy-as-Code:** Agents cannot run destructive commands (like dropping databases or pushing to production) without explicit permission. This is governed by `core/policies/action-boundaries.yaml`.
- **A2A Delegation:** Agents can spin up sub-agents to do specialized work (e.g., a Backend Developer asking a Data Engineer to write a complex SQL migration).
- **Structured Contracts:** Agents no longer pass information via messy text. Handoffs between roles (e.g., UX Designer → Frontend Developer) are done via strict **JSON Schemas** (Data Contracts).

---

## 2. How to Trigger an Agent

To get the best results, you must explicitly invoke the agent by its **Role Name** and provide the necessary context.

### The "Golden" Prompt Structure:
> *"Act as the `@<role-name>`. [State your objective]. Ensure you follow your v2.0 role guidelines and output the necessary JSON contract if applicable."*

### ✅ Example 1: Creating a UI Component
> *"Act as the `@ui-ux-designer`. I need a new Product Card for the E-commerce site. Please generate the `ui-component-spec.json` contract for this component."*
>
> *(After the UX agent replies with the JSON)*
> 
> *"Now act as the `@frontend-developer`. Read the `ui-component-spec.json` generated above and implement the React component."*

### ✅ Example 2: Backend Development
> *"Act as the `@backend-developer`. We need a new endpoint to fetch User Orders. Please define the API contract using `api-contract-spec.json`, then implement the Express route."*

### ✅ Example 3: Bug Fixing with Agent Coordinator (Auto-delegation)
When a QA Agent finds a bug (e.g., `test-report.json` says "failed"), you don't need to fix it manually. Wake up the Coordinator to manage the fix end-to-end:
> *"Act as the `@agent-coordinator`. Read `test-report.json`. Use A2A to call `@backend-developer` to fix the Prisma error, then call `@qa-engineer` to re-test. Do not stop until the report status is 'passed'."*

---

## 3. A2A Delegation (Agent-to-Agent)

In v2.0, you don't need to micromanage everything. Agents know when a task is out of their depth and can delegate it.

**How it works:**
If you ask the `@reviewer` to audit a large Pull Request containing a tricky authentication flow, the Reviewer will:
1. Review the general code quality.
2. Realize auth is involved and trigger an **A2A Task**.
3. Delegate the auth snippet to the `@security-engineer`.
4. The Security Engineer returns a `security-audit.json`.
5. The Reviewer merges the findings and presents the final report to you.

*Tip: You can force an agent to delegate by saying: "Act as `@technical-lead`. Plan this feature and delegate the slices to the frontend and backend agents."*

---

## 4. The JSON Contracts

Whenever an agent finishes a major phase of work, it should generate a JSON contract to ensure the next agent in the pipeline understands exactly what to do.

Here are the core contracts available in `core/contracts/schemas/`:

| Contract File | Used By | Purpose |
|---------------|---------|---------|
| `feature-ticket.json` | PM / BA | Defines business rules and acceptance criteria for Devs. |
| `ui-component-spec.json`| UX Designer | Defines UI states and props for Frontend Devs. |
| `api-contract-spec.json`| Backend Dev | Defines REST/gRPC endpoints for Frontend consumption. |
| `schema-migration.json` | Data Engineer | Defines DB changes and rollback scripts safely. |
| `test-report.json` | QA Engineer | Logs test results, bugs, and release recommendations. |
| `performance-audit.json`| 3D / Frontend | Logs FPS, memory, and bundle size metrics. |
| `security-audit.json` | Security Eng | Logs vulnerabilities and assigns CVE mitigation tasks. |
| `deployment-plan.json` | DevOps | Defines environment rollout and rollback strategy. |
| `incident-report.json` | SRE | Logs post-mortem findings and action items. |
| `adr-spec.json` | Architect | Records why a technical decision was made. |

---

## 5. Security & Action Boundaries

You are protected by `core/policies/action-boundaries.yaml`.

- **Frontend & UX Agents:** Can read/write files and run dev servers. They are **DENIED** from modifying secrets or running DB migrations.
- **Backend & Data Agents:** Can run migrations (with user approval), but are **DENIED** from pushing directly to production.
- **Content Writers:** Are **DENIED** from running builds or installing dependencies.

*If an agent tries to execute a denied tool, the system will automatically block it and ask you for manual override permission.*

---

## 6. Pro-Tips for Daily Usage

1. **Don't let them skip the JSON:** If an agent gives you a wall of text instead of a JSON contract, tell it: *"Please output this as a valid `[name-of-contract].json`."*
2. **Combine Packs:** If you are working on the Go Microservices, tell the agent: *"Use the `ecommerce-team` pack and the `go-microservices` overlay."*
3. **Use the Planner:** If you have a massive idea but don't know where to start, say: *"Act as `@task-planner`. Break this idea down into a step-by-step Execution Plan."*
