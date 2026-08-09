---
name: implement-structured-outputs
description: Implements strict constrained decoding and validation for LLM responses. Use to replace brittle regex parsing with native JSON structured outputs.
---

# Implement Structured Outputs

Use this skill when integrating LLM responses into application code to guarantee schema adherence and eliminate parsing errors.

## Core Rules
- **No Regex Parsing**: Never use regex to extract JSON or structured data from raw LLM text blocks.
- **Constrained Decoding**: Use provider-native structured output features (e.g., OpenAI Structured Outputs, Gemini `responseSchema`, or vLLM XGrammar).
- **Dual Validation**: Define the schema once (e.g., in Zod/Pydantic). Use it both to constrain the LLM generation AND to validate the runtime response before passing it to business logic.
- **Fallback Logic**: Implement retry mechanisms with context injection when the LLM fails to adhere to the schema despite constraints.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output proving the schema validation handles both valid and invalid mock responses.

## Checklist
- [ ] Provider-native constrained decoding implemented.
- [ ] Shared schema defined (Zod/Pydantic).
- [ ] Runtime validation enforces the schema before business logic execution.
- [ ] Retry/fallback logic handles edge-case parsing failures.
- [ ] `implementation-result.json` emitted.
