# Policies

This directory contains machine-readable policies that define action boundaries, data classification, and governance rules for agent operations.

## Why Policies Exist

Text-based rules in `core/rules/code.md` are advisory. Policies in this directory are structured YAML definitions that can be checked programmatically at runtime.

Policies answer: "Is this agent, in this role, allowed to perform this action on this data?"

## Policy Types

### Action Boundaries

`action-boundaries.yaml` defines what each of the 26 delivery roles is allowed, requires approval for, or denied from doing.

### Data Classification

`data-classification.yaml` defines sensitivity levels for different data types to prevent accidental exposure.

### MCP Tool Mapping

`mcp-tool-map.yaml` maps IDE/MCP tool names to policy action ids for `agent-tool-orchestration` and Cursor hooks.

## Usage

Skills should reference policies when making decisions about state-changing actions:

1. identify the current role
2. identify the action being attempted
3. check the action against `action-boundaries.yaml`
4. if the action involves data, check sensitivity against `data-classification.yaml`
5. proceed, request approval, or deny based on the policy result

## Relationship To Rules

`core/rules/code.md` remains the human-readable always-on rules. Policies provide the structured, machine-checkable complement. When both exist, policies take precedence for enforcement.
