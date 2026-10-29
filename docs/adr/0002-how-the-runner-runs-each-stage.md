---
status: proposed
date: 2026-10-28
---

# How the runner runs each stage

## Summary

**Proposal.** Build the parts that record, check and report on stages first. On their own, these make up the **recorder**. Then add one of two ways for the runner to run stages itself:

- the **conductor**, which launches the department's approved coding agent
- the **runner-owned agent loop**, which calls the model directly

Which one comes first depends on what departments using the toolkit typically have approved, which the maintainers are asked.

**Status.** Proposed, not accepted. The details of how each approach is built will be added once the maintainers have answered the questions this decision [depends on](#depends-on-the-maintainers).

## Context

The runner needs a way to run each stage prompt against the scan copy. Two constraints shape the choice:

- **The prompts assume an agent that opens files as it goes**, not one that is handed a fixed set of files.
- **Departments approve different things.** Some have approved a coding agent such as Claude Code or Codex; some have approved direct model access such as Amazon Bedrock; some may have neither.

Whichever way runs a stage, the runner should give every run a consistent procedure, enforced permissions and an audit trail, without making methodological choices the toolkit does not define. The reviewer decides whether to run the next stage.

## Depends on the maintainers

This decision waits on the maintainers' answers to the [proposal](https://github.com/sumau/GC3-AI-SAST-Toolkit/issues/1#draft-proposal-to-post-upstream), which holds the questions. It depends on:

- whether they want a tool like this at all
- whether the runner should run stages, or only record and check stages the reviewer runs by hand
- what departments using the toolkit typically have approved: a coding agent, direct model access, or both
- whether stages share one agent session, and how stage 00 is applied. The toolkit's wording leans towards one session (`vendor/gc3-ai-sast-toolkit/1-prompts/README.md:9`, `vendor/gc3-ai-sast-toolkit/1-prompts/README.md:27`).

## Considered options

- **Recorder (built first; fallback).** The reviewer runs every stage by hand in their coding agent. The runner records versions, imports the agent's session transcript, checks outputs and drafts reports.
- **Conductor (candidate).** The runner launches the reviewer's coding agent, inside an isolated sandbox, with the stage prompt. The agent reads the scan copy and writes its outputs to a run folder. The runner holds no model credentials. This automates the setup the toolkit already describes (`vendor/gc3-ai-sast-toolkit/README.md:13-38`).
- **Runner-owned agent loop (candidate).** The runner gives the model its own tools (list, read and search within the scan copy; write within the run folder) and runs the tool-use loop itself, calling the model directly.
- **Single-call orchestrator (rejected).** The runner sends each stage prompt and a selection of files to a model in one call per stage.

```mermaid
---
config:
  layout: elk
---
flowchart LR
    subgraph rec ["Recorder (built first; fallback)"]
        direction TB
        r_scan@{ shape: docs, label: "Scan copy" }
        r_out@{ shape: docs, label: "Run folder" }
        r_rev(["👤 Reviewer"]) -- "decides the next stage<br/>and runs it by hand" --> r_agent["Coding agent"]
        r_rev -- "imports each stage" --> r_run["⚙️ Runner"]
        r_agent -- "opens files as it goes" --> r_scan
        r_agent -- "prompt and file contents" --> r_model("Model")
        r_model -- "tool requests" --> r_agent
        r_agent -- "writes outputs" --> r_out
        r_run -- "records and checks<br/>outputs and transcript" --> r_out
    end

    subgraph con ["Conductor (candidate)"]
        direction TB
        c_scan@{ shape: docs, label: "Scan copy" }
        c_out@{ shape: docs, label: "Run folder" }
        c_rev(["👤 Reviewer"]) -- "decides the next stage" --> c_run["⚙️ Runner"]
        c_run -- "launches each stage<br/>in an isolated sandbox" --> c_agent["Coding agent"]
        c_agent -- "opens files as it goes" --> c_scan
        c_agent -- "prompt and file contents" --> c_model("Model")
        c_model -- "tool requests" --> c_agent
        c_agent -- "writes outputs" --> c_out
        c_run -- "records and checks<br/>outputs and transcript" --> c_out
    end

    subgraph own ["Runner-owned agent loop (candidate)"]
        direction TB
        l_rev(["👤 Reviewer"])
        l_scan@{ shape: docs, label: "Scan copy" }
        l_out@{ shape: docs, label: "Run folder" }
        l_rev -- "decides the next stage" --> l_run["⚙️ Runner<br/>(own tools)"]
        l_run -- "prompt and tool results" --> l_model("Model")
        l_model -- "tool requests" --> l_run
        l_run -- "reads requested files<br/>and records each read" --> l_scan
        l_run -- "writes outputs" --> l_out

        l_agent["Coding agent<br/>(not used)"]
        l_rev ~~~ l_agent
        l_agent ~~~ l_scan
    end

    subgraph orc ["Single-call orchestrator (rejected)"]
        direction TB
        o_rev(["👤 Reviewer"])
        o_scan@{ shape: docs, label: "Scan copy" }
        o_out@{ shape: docs, label: "Run folder" }
        o_rev -- "approves at gates" --> o_run["⚙️ Runner"]
        o_run -- "chooses files" --> o_scan
        o_run -- "one call per stage:<br/>prompt and chosen files" --> o_model("Model")
        o_model -- "one response" --> o_run
        o_run -- "parses the response<br/>into artefacts" --> o_out

        o_agent["Coding agent<br/>(not used)"]
        o_rev ~~~ o_agent
        o_agent ~~~ o_model
    end

    rec ~~~ con ~~~ own ~~~ orc

    classDef unused stroke-dasharray: 5 5, color:#777
    class l_agent,o_agent unused
    classDef reviewer fill:#fde68a, stroke:#b45309, color:#000
    class r_rev,c_rev,l_rev,o_rev reviewer
```

## Trade-offs

**Conductor or runner-owned agent loop.** The deciding difference is which program sends the department's source code to the model. With the conductor, it is the coding agent the department has already approved. With the agent loop, it is the runner, which needs its own approval unless the department already trusts a direct model endpoint such as Amazon Bedrock.

On technical grounds, the agent loop is the better design: permissions hold by construction, the runner records every file read itself, and it can be tested deterministically. The conductor needs only an approved coding agent, at the cost of depending on agents the runner does not control and on a correctly set up sandbox. So the choice turns on what departments have approved, not on the design.

Building both roughly doubles the stage-running work, so only one is built first, behind an interface that leaves room for the other.

**Why not the recorder alone.** It leaves what the agent may do, which configuration loads and what happens when a stage stops early to each reviewer. It remains the fallback if the maintainers do not want stages run automatically.

**Why not the single-call orchestrator.** The runner would have to choose which files the model sees, which the methodology does not define and the prompts do not expect.

## Consequences

Whichever approach is built:

- The model can read the scan copy and write only to the run folder, with no shell and no network. So stage 02's optional local validation is not possible, and no result is `locally-validated`.
- The run record says which approach ran each stage, and stages that stop early are recorded as incomplete.
- The runner's checks confirm form, not correctness: it reports "form checks passed", never "verified".
- No test calls a real model.
- Issue #2 is reordered to match the build order above.

## When to decide or revisit

Decide which way of running stages to build first when the maintainers say what departments typically have approved, and fill in how it is built at that point.

Revisit this decision if:

- the maintainers prefer no automation (fall back to the recorder) or no tool at all (archive the runner)
- no supported agent can be held to the permissions above (rule out the conductor, and use the runner-owned agent loop where direct model access allows)
- departments that need the other approach start using the runner (build the second way of running stages)
