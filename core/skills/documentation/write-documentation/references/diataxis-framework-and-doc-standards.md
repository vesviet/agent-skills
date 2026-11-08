# Diátaxis Framework & Modern Documentation Standards (2026)

## 1. The Diátaxis Documentation Architecture

The Diátaxis framework divides technical documentation into four distinct quadrants based on user needs and cognitive mode:

```
                  PRACTICAL (Action-oriented)
                              ▲
                              │
         TUTORIALS            │          HOW-TO GUIDES
    (Learning-oriented)       │       (Problem-oriented)
                              │
 ◄────────────────────────────┼────────────────────────────►
   THEORETICAL (Study)        │     PRACTICAL (Work)
                              │
        EXPLANATION           │           REFERENCE
    (Understanding-oriented)  │      (Information-oriented)
                              │
                              ▼
                 THEORETICAL (Cognition-oriented)
```

### 1.1 The Four Quadrants
1. **Tutorials (Learning-oriented)**:
   - *Goal*: Take a beginner by the hand through a concrete learning experience.
   - *Tone*: Welcoming, prescriptive, step-by-step.
   - *Anti-patterns*: Explaining deep architectural trade-offs; providing multiple alternative choices.
2. **How-To Guides (Problem-oriented)**:
   - *Goal*: Guide an experienced user through solving a real-world task.
   - *Tone*: Practical, recipe-based, outcome-focused.
   - *Anti-patterns*: Explaining fundamental concepts; open-ended teaching.
3. **Reference (Information-oriented)**:
   - *Goal*: Provide accurate, austere, authoritative technical facts (APIs, schemas, CLI flags).
   - *Rule*: Auto-generated from OpenAPI / AsyncAPI / Protobuf specs to prevent doc drift.
   - *Anti-patterns*: Conversational tone; tutorial instructions.
4. **Explanation (Understanding-oriented)**:
   - *Goal*: Clarify the big picture, architectural rationale, design trade-offs, and historical context.
   - *Tone*: Discursive, conceptual, analytical.
   - *Anti-patterns*: Command steps; copy-paste recipes.

## 2. Docs-as-Code & Dual-Audience Standards

Modern engineering documentation serves two concurrent audiences: human engineers and autonomous AI agents.

### 2.1 Frontmatter Invariant
Every documentation file must include semantic YAML frontmatter:
```yaml
---
title: "Service Architecture & Data Flow"
description: "Core microservice topology, event streaming semantics, and persistence boundaries."
category: "explanation" # tutorial | howto | reference | explanation
last_verified_version: "v2.12.0"
maintainer: "technical-lead"
---
```

### 2.2 Continuous Integration Gates
- `markdownlint`: Zero syntax or structural violations.
- `vale`: Strict enforcement of prose style guides (Google / Microsoft Developer Documentation Style).
- `lychee` / broken-link checker: 100% resolution of internal and external hyperlinks.
- Cloudflare Pages / Netlify Deploy Previews: Ephemeral preview deployments for every pull request.
