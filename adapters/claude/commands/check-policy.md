---
description: "Verify active role permissions and action boundaries against core/policies/action-boundaries.yaml before executing state-changing operations."
---

# Policy Check Command

Run this command to audit planned operations against the pack's Policy-as-Code rules:

1. Identify the current active role (e.g., `backend-developer`, `content-writer`, `agent-coordinator`).
2. Identify the target operation or tool action from `core/policies/mcp-tool-map.yaml`.
3. Check `core/policies/action-boundaries.yaml` to confirm the action is `allowed`, `requires_approval`, or `denied`.
4. If the action is `requires_approval`, summarize the command and ask for explicit human confirmation before proceeding.
5. If the action is `denied`, halt immediately and explain the policy boundary to the user.

Arguments: $ARGUMENTS
