# Ousterhout Deep Modules, Seams & Interface-First Testing Reference

Use these structural design heuristics (synthesized from John Ousterhout's *A Philosophy of Software Design*, Michael Feathers' *Working Effectively with Legacy Code*, and `mattpocock/skills`) when architecting new services, boundaries, or TypeScript/backend modules.

---

## 1. Core Design Vocabulary

- **Module:** Any cohesive unit with an exported interface and a hidden implementation (package, service, microservice client, domain class).
- **Deep Module vs Shallow Module:**
  - **Deep Module:** Exposes a small, intuitive interface hiding substantial implementation complexity. Maximizes **Leverage** (callers learn very little to accomplish a lot) and **Locality** (behavior changes require editing one module, not ten).
  - **Shallow Module (Reject):** Exposes a large or mirror-image interface whose body only forwards calls or adds boilerplate wrapper indirection, inflating context window overhead.
- **Seam:** A boundary point where system behavior can be altered or substituted without editing source code at the call site — the exact boundary where a module's public interface sits.
- **Adapter:** A concrete implementation satisfying the contract at a seam.

---

## 2. Architectural Guardrails

### 2.1 The Two-Adapter Rule ("Two Adapters Prove a Seam")
- Creating an abstract interface or repository wrapper around **one** concrete implementation proves only a *hypothetical seam* (speculative generality / Middle Man smell).
- Require **two or more concrete adapters** (e.g. primary database/provider plus fake/in-memory adapter or multiple carrier APIs) before introducing an abstraction seam.

### 2.2 The Deletion Test
Evaluate every intermediate wrapper, helper, or facade with a thought experiment:
- *If deleting the module causes complexity to simply disappear without touching callers* $\rightarrow$ it was a useless shallow pass-through wrapper; inline and delete it.
- *If deleting the module forces complex invariants and branching to fragment across $N$ call sites* $\rightarrow$ it is a justified Deep Module protecting callers.

### 2.3 Design It Twice
Before locking a new cross-module contract or service interface, sketch **two genuinely different structural designs** (not cosmetic renamings) and compare caller ergonomics, seam testability, and blast radius before picking the cleaner boundary.

---

## 3. Interface Is The Test Surface (Seam-Based TDD)
- Both production callers and automated tests must traverse the **same public interface seam**.
- Prohibit unit tests that reach past the interface seam to assert private fields, internal helper invocation counts, or tautological mock behavior mirroring the implementation.
- Prefer real in-memory adapters or sandbox containers behind clean ports over deep mock trees.

---

## 4. TypeScript Deep Module Conventions (Node / Astro / Next.js / Workers)
- **Root Entrypoint Enforcement (`dependency-cruiser`):** Configure architectural lint rules (`check:deps`) forbidding cross-module imports into internal subpaths (`src/modules/<mod>/internal/**`), allowing imports solely through each module's public root entrypoint while avoiding indiscriminate barrel re-export chains that trigger circular imports or bundle bloat.
- **Type-Safe Test Builders (`fromPartial()` over `as any`):** Replace unsafe `as any` or bare type assertions in test fixtures with strongly typed partial builders (e.g. `fromPartial(...)` via `@total-typescript/shoehorn` or strict helper factories) so interface evolutions surface compile-time breaks immediately.
