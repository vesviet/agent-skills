# Two-Axis Review Playbook

Reference playbook for `review-code`. Loaded on demand — the SKILL.md body
summarizes the discipline; this file carries the full smell baseline and the
paste-ready sub-agent briefs.

Method provenance: two-axis (Standards / Spec) review adapted from the
`code-review` skill in `mattpocock/skills`; smell baseline from Fowler,
_Refactoring_, chapter 3.

---

## Fowler Smell Baseline

A fixed set of smells that applies to every diff even when the repo documents
no standards. Two binding rules:

- **The repo overrides.** A documented repo standard always wins; where it
  endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each hit is a labelled heuristic ("possible
  Feature Envy"), never a hard violation.

Each smell reads *what it is* → *how to fix*; match it against the diff:

| Smell | What it is | Fix |
| ----- | ---------- | --- |
| Mysterious Name | a function, variable, or type whose name doesn't reveal what it does or holds | rename it; if no honest name comes, the design's murky |
| Duplicated Code | the same logic shape appears in more than one hunk or file in the change | extract the shared shape, call it from both |
| Feature Envy | a method that reaches into another object's data more than its own | move the method onto the data it envies |
| Data Clumps | the same few fields or params keep travelling together (a type wanting to be born) | bundle them into one type, pass that |
| Primitive Obsession | a primitive or string standing in for a domain concept that deserves its own type | give the concept its own small type |
| Repeated Switches | the same switch/if-cascade on the same type recurs across the change | replace with polymorphism, or one map both sites share |
| Shotgun Surgery | one logical change forces scattered edits across many files in the diff | gather what changes together into one module |
| Divergent Change | one file or module is edited for several unrelated reasons | split so each module changes for one reason |
| Speculative Generality | abstraction, parameters, or hooks added for needs the spec doesn't have | delete it; inline back until a real need shows |
| Message Chains | long `a.b().c().d()` navigation the caller shouldn't depend on | hide the walk behind one method on the first object |
| Middle Man | a class or function that mostly just delegates onward | cut it, call the real target direct |
| Refused Bequest | a subclass or implementer that ignores or overrides most of what it inherits | drop the inheritance, use composition |

---

## Sub-Agent Briefs

Spawn the Standards and Spec reviews as parallel sub-agents so neither axis
pollutes the other's context. Both prompts are self-contained: the sub-agent
has no access to this file, so paste whatever it needs into the prompt.

### Standards sub-agent prompt must include

- the full diff command (`git diff <fixed-point>...HEAD`) and the commit list
- the list of standards-source files found in the repo
- **the smell baseline above, pasted in full**
- the brief:

> Report, per file/hunk where relevant, (a) every place the diff violates a
> documented standard: cite the standard (file + the rule); and (b) any
> baseline smell you spot: name it and quote the hunk. Distinguish hard
> violations from judgement calls: documented-standard breaches can be hard,
> but baseline smells are always judgement calls, and a documented repo
> standard overrides the baseline. Skip anything tooling enforces.
> Under 400 words.

### Spec sub-agent prompt must include

- the diff command and commit list
- the path or fetched contents of the spec
- the brief:

> Report: (a) requirements the spec asked for that are missing or partial;
> (b) behaviour in the diff that wasn't asked for (scope creep); (c)
> requirements that look implemented but where the implementation looks
> wrong. Quote the spec line for each finding. Under 400 words.

### Aggregation rules

- present both reports under `## Standards` and `## Spec`, verbatim or lightly cleaned
- do not merge findings and do not rerank across axes — the separation exists so one axis cannot mask the other
- end with one line per axis: total findings and the worst issue within that axis
