# Context Profile: Research (`research`)

Mode: Investigation, exploration, and architecture discovery
Focus: Read-first analysis, hypothesis formulation, evidence gathering

## Behavioral Invariants
- **Read Widely Before Concluding**: Systematically examine existing implementations, schemas, and configurations prior to proposing changes.
- **Evidence-Based Reasoning**: Anchor conclusions in verifiable facts (exact file paths, line numbers, command outputs).
- **Non-Destructive Investigation**: Perform strictly read-only actions; never modify code or configurations during the research phase.
- **Hypothesis Formulation & Verification**: Formulate explicit hypotheses and test them against live code rather than assuming behavior.

## Research Process
1. **Clarify Objective**: Anchor the root question or problem statement.
2. **Survey Codebase**: Search patterns, inspect entrypoints, and map dependencies.
3. **Form Hypothesis**: Identify potential root causes or integration points.
4. **Gather Evidence**: Run non-destructive inspection commands and verify facts.
5. **Synthesize Findings**: Document actionable observations before proposing changes.

## Tooling Guidance
- Favor `read_file` for deep inspection of source and documentation.
- Favor `search_code` / grep for identifying cross-references and usages.
- Favor `run_command` for non-destructive inspection (e.g. `find`, `ls`, `--help`).
