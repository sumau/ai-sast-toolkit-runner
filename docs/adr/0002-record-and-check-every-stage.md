---
status: accepted
date: 2026-10-29
---

# Record and check every stage, however it was run

## Summary

The runner records, checks and reports on every stage, whatever ran it. This is built first. On its own, it works with stages a reviewer runs by hand in their coding agent. How the runner itself might run stages is a separate decision, in [ADR 0003](0003-how-the-runner-runs-each-stage.md).

## Context

The toolkit asks for each run to record the model, prompt-pack version, prompt IDs and agent client (`vendor/gc3-ai-sast-toolkit/1-prompts/README.md:37-46`, `vendor/gc3-ai-sast-toolkit/CLAUDE.md:34-35`), and treats a machine-readable register as the source of truth (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:214-216`). Doing this by hand is where runs become inconsistent and hard to audit.

None of this depends on how a stage was run. Whether a reviewer runs it by hand or the runner runs it, the same things need recording and checking.

## Decision

For every stage, the runner:

- **records what was used:** the toolkit commit and content hashes (as in [ADR 0001](0001-runner-separate-from-toolkit.md)), the prompt IDs, and the model and agent client where known
- **captures what the stage produced:** its outputs in the run folder and, where available, the session transcript
- **checks what can be checked mechanically:** for example the scope re-anchor line, the evidence labels from stage 00, `file:line` citations that point at real lines in the scan copy, stable ID formats and the register's required fields
- **drafts reports** from the register, leaving human-only fields and missing evidence visibly empty

## Considered options

- **Build stage-running first.** Rejected. The checks are needed whichever way stages are run, they are useful with no automation at all, and how stages are run waits on the maintainers (ADR 0003).

## Consequences

- The checks confirm form, not correctness: the runner reports "form checks passed", never "verified".
- The run record says how each stage was run (by hand, or which approach in ADR 0003), and stages that stop early are recorded as incomplete.
- This part never calls a model, so it is tested with fixtures only.
- Issue #2 is reordered to build this first.

## When to revisit

- The maintainers do not want a tool like this at all (archive the runner).
