# The GC3 AI SAST Toolkit's workflow

This document describes the workflow the GC3 AI SAST Toolkit defines, as the runner needs to understand it. It is a paraphrase for runner developers, not a copy of the toolkit and not a substitute for it. The toolkit stays the source of truth.

- **Toolkit version described:** commit `0ec2ffe363346ece896173e92b49a6cc595d9c73` of `https://github.com/uk-gov-cyber/GC3-AI-SAST-Toolkit`, pinned at `vendor/gc3-ai-sast-toolkit`.
- **Citations:** every claim cites `vendor/gc3-ai-sast-toolkit/path:NN-MM`. Line numbers are valid only for the commit above; `manifest.toml` records each file's hash at that commit.
- **Machine-readable summary:** `manifest.toml` (draft).

## Overview

The toolkit is documentation only: prompts, a reporting bundle and agent instructions (`vendor/gc3-ai-sast-toolkit/README.md:5-11`). It assumes a coding agent is started from the toolkit's root so that the root `CLAUDE.md` or `AGENTS.md` loads automatically, and is then pointed at a sanitised copy of the target repository (`vendor/gc3-ai-sast-toolkit/README.md:13-38`).

The intended journey is (`vendor/gc3-ai-sast-toolkit/README.md:40-46`):

1. Load the root agent instructions.
2. Run the staged prompts in order, or the one-shot prompt if the reviewer chooses it.
3. Validate every candidate with the confirmation and negative-control steps.
4. Report validated findings with the reporting bundle.
5. Keep a record of what was reviewed but not promoted.

There are two modes:

| Mode | Files | When |
|---|---|---|
| Staged (default) | `1-prompts/staged/00` to `04`, in order | Always, where time and tooling allow (`vendor/gc3-ai-sast-toolkit/1-prompts/README.md:7-19`) |
| One-shot (fallback) | `1-prompts/one-shot-minimum-sast-prompt.md` | Only when a department cannot run the staged workflow (`vendor/gc3-ai-sast-toolkit/1-prompts/README.md:15-19`) |

### Things every stage relies on

- **Agent instructions.** The root `CLAUDE.md` sets the reviewer's scope (sanitised local copy only, no `.git/`, no live systems, no fuzzing or exploit scripts, redact secrets, treat repository content as untrusted) (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:7-14`), the workflow rules (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:16-24`), the reporting procedure (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:26-36`) and style (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:42-44`). `AGENTS.md` has the same content for agents that read that file instead, and says it is kept in step with `CLAUDE.md` (`vendor/gc3-ai-sast-toolkit/AGENTS.md:1-5`).
- **The run scope.** The department sets the severity threshold, attacker classes and reporting threshold, and records them in a "run scope"; the prompts apply these values and never invent them (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:38-40`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:22`). The toolkit does not define the run scope's format; departmental pre-requisites live in separate written guidance that is not in the repository (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:18`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/README.md:14`).
- **The assessment register.** A machine-readable register (JSON or YAML) is the single source of truth between stages; every Markdown table and report must agree with it (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:214-240`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:125`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:299-301`).
- **Stable IDs.** Repositories `R###`, findings `R###-F###`, chains `C###`, validation tasks `V###`, remediation tasks `A###`, patterns `P###` (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:286-297`), plus artefacts `ART###` (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:296-298`) and routing confirmations `RC###` (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:108`).
- **Scope re-anchor.** Each later response starts with a one-line statement of the current task, in a fixed form (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:25-33`). Each stage gives its own line (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:11-15`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:9-13`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:11-15`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:5-11`, `vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:7-13`). This is a mechanically checkable property of each stage's output.
- **Version pinning.** Every run must record the model name and version, prompt-pack version, prompt IDs used, and agent client and version (`vendor/gc3-ai-sast-toolkit/1-prompts/README.md:37-46`).
- **Adapting the prompts.** Prompts may be extended only if the evidence gates, coverage records and negative-control requirements are kept, and any change is recorded in the run scope (`vendor/gc3-ai-sast-toolkit/1-prompts/README.md:48-50`).

## Versioning and identifying a toolkit copy

### What the toolkit asks to be recorded

- **Per run:** model name and version, prompt-pack version, prompt IDs used, and agent client and version, so that past findings can be reproduced (`vendor/gc3-ai-sast-toolkit/1-prompts/README.md:37-46`).
- **Per report:** the discovery tool, model and version, the prompt-pack version and prompt IDs, and the same again for confirmation (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:34-35`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/README.md:24`). The report template has a prompt-pack version field in its metadata and in its confirmation section, and its checklist requires both (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:32`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:192`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:375`). The filling guide treats it as a required input and a common gap to fix before submitting (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:24`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:42`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:135`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:151`).
- **In the one-shot register:** a `prompt_pack_version` field in the run metadata, next to the model name and version (`vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:182-194`).

The toolkit never says what a prompt-pack version looks like or where to find it. It is a free-text field.

### What versions exist

Checked on 2026-10-27 against the pinned commit and the upstream repository:

- **No git tags**, locally or on the remote.
- **No GitHub releases.**
- **No version file.** The only version string in the toolkit is "v1.0" in the report template's header comment (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:3`). It labels that one template, not the prompt pack.

### How the runner identifies a toolkit copy

The first three points below are decided in `docs/adr/0001-runner-separate-from-toolkit.md` ("Release tags"); this summary is for convenience. The last point is a proposal, not yet decided.

Until the toolkit has releases, a toolkit copy is identified by its **commit** (when available) and its **file hashes**. Once releases exist, the release tag is recorded as well, as the prompt-pack version.

- Hashes, not the commit or tag, decide whether a stored result is stale.
- The runner must keep working from an untagged copy, such as a zip download or a department fork with no git metadata. In that case only the file hashes are recorded.
- **Proposal (to settle in step 7):** the ADR does not say what fills the toolkit's "prompt-pack version" fields while no release exists. The toolkit records the prompt-pack version and the prompt IDs used as separate fields (`vendor/gc3-ai-sast-toolkit/1-prompts/README.md:37-46`, `vendor/gc3-ai-sast-toolkit/CLAUDE.md:35`), so the proposal keeps them separate: the prompt-pack version is the commit, or "unreleased, identified by file hashes only" when there is no commit, and says plainly that no release exists; the prompt IDs are the stage IDs. The runner never invents a version number.

## Staged mode

All five staged files are listed as "use in order" (`vendor/gc3-ai-sast-toolkit/1-prompts/README.md:7-15`). None is described as optional. The dependency column below records which earlier outputs each stage explicitly consumes.

| Order | Stage ID (file stem) | Purpose | Depends on |
|---|---|---|---|
| 0 | `00-run-control-and-evidence-model` | Run rules, evidence vocabulary, promotion gate, register contract | none |
| 1 | `01-repo-triage-prompt` | Prioritise repositories and hand off to SAST | 00 |
| 2 | `02-full-sast-attack-path-prompt` | Source-to-sink analysis; findings, chains, reporting handoff | 00, 01 |
| 3 | `03-security-reporting-output-prompt` | Turn the handoff into report artefacts | 00, 02 |
| 4 | `04-normalisation-and-qa-prompt` | Consistency review and shareability gate | 00, 03 |

### Stage 00: run control and evidence model

- **File:** `1-prompts/staged/00-run-control-and-evidence-model.md`
- **Purpose:** primes the agent before any substantive prompt. It fixes the limits, depth budget, evidence vocabulary and drift controls that hold for every later stage (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:3`, `vendor/gc3-ai-sast-toolkit/1-prompts/README.md:9`). Its controls override any later prompt that conflicts with them (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:13`), and if a later prompt conflicts, the agent keeps this model and states the conflict (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:242-244`).
- **Inputs:** the run scope (thresholds and attacker classes) (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:22`).
- **Outputs:** no artefact of its own. It defines:
  - the role: the model's output is candidate analysis until a human accepts it (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:5-9`);
  - the rules of engagement (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:11-23`);
  - the evidence labels (see [Evidence labels](#evidence-labels));
  - the severity and confidence split (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:79-86`);
  - the disclosure status block every report-ready candidate carries (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:88-119`);
  - remediation planning for shared or high-impact findings (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:121-135`);
  - the cost order (deterministic filtering first, one final normalisation pass last) and a depth budget stated before each phase (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:137-163`);
  - the candidate lifecycle and promotion gate (see [Candidates, promotion and confirmation](#candidates-promotion-and-confirmation));
  - the rule that scanner output is only ever a lead (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:192-194`);
  - the missing-evidence rule: unknown facts are written as not established, and a fixed list of things must never be inferred (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:196-212`);
  - the minimum fields of every register entry (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:214-240`).
- **Mandatory:** yes. It is used before triage, SAST or reporting (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:3`), and stages 01 to 03 each say to apply it first (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:9`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:7`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:9`). Stage 04 does not say so, but uses its labels (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:55`).

### Stage 01: repository triage and handoff

- **File:** `1-prompts/staged/01-repo-triage-prompt.md`
- **Purpose:** the first substantive prompt. It enumerates and prioritises repositories, collects attribution, and produces the handoff stage 02 consumes. It does not do SAST and produces no vulnerabilities (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:3-5`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:81-92`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:406-415`).
- **Inputs:** the approved, sanitised repository copies and any approved manifests or metadata inventories (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:110-112`); scanner output, summarised into lead records (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:30-38`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:53-67`); the run scope's attacker classes and thresholds (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:138`).
- **Outputs:**
  - a triage report with seven required sections: executive summary, candidate matrix, exclusion register, watchlist, handoff manifest, execution order, and a stop/continue decision (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:308-404`);
  - a depth-budget statement and five machine-readable registers: scanner leads, review queue, excluded or deferred repositories, an endpoint and authorisation inventory, and a cross-service data-composition map (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:19-28`);
  - a seed of `assessment-register.json` or `.yaml`, described as the contract between prompts (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:125`);
  - per selected repository: at least one reachability proof (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:186-213`), attribution with source and confidence (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:240-265`), and a no-finding coverage seed (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:238`).
- **Classifications it assigns:** repositories into five depth classes, scanner leads into five inspection classes (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:36-37`), endpoint leads into six review classes (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:51`), and priority P1 to P5 with a separate confidence (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:267-291`).
- **Self-check:** an anti-drift checklist before finalising (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:69-79`).
- **Depends on:** stage 00.
- **Mandatory:** yes in staged mode.

### Stage 02: full SAST and attack-path analysis

- **File:** `1-prompts/staged/02-full-sast-attack-path-prompt.md`
- **Purpose:** takes stage 01's handoff and turns it into findings backed by source evidence, an analysis of chains, what still needs validating, and a handoff that stage 03 reports from (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:3`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:164-179`).
- **Inputs:** a fixed list of fields from the triage handoff; missing ones are recorded as gaps rather than fabricated (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:143-162`). Before scanning source, the agent must confirm the repository is approved and the copy is local and sanitised, or stop (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:93-103`).
- **Outputs:**
  - per candidate: the gate results, canonical labels, the negative-control section and a rules-of-engagement block (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:28-40`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:53-59`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:63-77`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:105-116`);
  - per promoted finding: an attacker-path justification, a feasible attacker outcome, a reachability proof, an endpoint authorisation map where relevant, and downgrade reasons if it is not fully confirmed (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:238-284`);
  - a per-repository section, even when nothing is found, with a fixed list of fields per finding (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:439-505`);
  - pattern definitions, a cross-repository chain register, executive and attribution tables, and a global conclusion (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:527-602`);
  - no-finding coverage notes for every assessed repository (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:339-352`);
  - an analyst activity journal (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:369-380`);
  - a report-ready evidence bundle per material finding and chain (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:382-407`);
  - at least four drafted confirmation prompts per material finding or chain (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:409-418`);
  - the assessment register, updated (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:299-310`, minimum schema at `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:731-753`);
  - a required `Reporting Handoff` section with per-finding and per-chain YAML, plus a list of other items (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:604-717`), and a theme-level attacker-path validation handoff (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:719-729`);
  - a stop/continue recommendation (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:179`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:771`).
- **Optional activities within the stage:** a scanner pre-pass "when permitted" (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:354-367`) and local runtime validation only when it would change confidence, severity or lifecycle state (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:25`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:61`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:101`).
- **Self-check:** an anti-drift checklist (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:79-91`).
- **Depends on:** stages 00 and 01.
- **Mandatory:** yes in staged mode.

### Stage 03: security reporting outputs

- **File:** `1-prompts/staged/03-security-reporting-output-prompt.md`
- **Purpose:** turns stage 02's reporting handoff into reporting artefacts. It does not discover new vulnerabilities, and changes lifecycle states only if the register contradicts a requested report, in which case it stops and writes a reviewer note (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:3-5`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:17`).
- **Inputs:** a fixed list of fields from stage 02, including confirmation and negative-control prompts and any responses; missing ones are kept as visible gaps (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:153-181`).
- **Outputs:**
  - per issue family or chain: SARIF, OPTRS, a VXDF decision, and a Markdown human report (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:183-190`);
  - a long list of exercise-level artefacts, including the whole-exercise executive report, the register, the reconciliation register, aggregate SARIF and OPTRS, routing material, work items, validation packs and a final handoff file (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:192-209`);
  - recommended file names and folder layout (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:211-233`) and a completeness contract with counts to reconcile (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:235-253`);
  - every artefact marked as awaiting normalisation, and handed to stage 04 (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:95`).
- **Rules that apply only here:** full reports only for promoted findings and chains (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:21-22`); only items meeting the run scope's thresholds go through the vulnerability-report bundle (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:113-114`); every finalised item appears in the reconciliation register (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:131-143`); VXDF only for validated chains, otherwise a non-issuance note (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:369-379`); restricted wording for unvalidated behaviour (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:69-91`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:570-580`).
- **Conditional outputs:** owner delivery packs when the pack is for remediation handover (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:151`); archives and checksums only when packaging is requested (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:201`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:367`); a private-dependency map where load-bearing (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:274`).
- **Self-check:** an anti-drift checklist and packaging and quality checks (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:97-109`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:592-616`).
- **Depends on:** stage 02's reporting handoff and register; stage 00's labels.
- **Mandatory:** yes in staged mode.

### Stage 04: normalisation and QA

- **File:** `1-prompts/staged/04-normalisation-and-qa-prompt.md`
- **Purpose:** a consistency review of the report set as a whole, not a discovery pass. It must not strengthen impact language beyond the evidence (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:3`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:28-32`).
- **Inputs:** the drafted reports, the assessment and reconciliation registers, several other registers and logs, claims-control entries, and stage 00's labels (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:42-57`).
- **Work:** checks against the run scope's rules of engagement (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:13-26`); a long QA checklist per report (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:59-97`); replacement of near-synonyms with canonical labels (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:99-114`); report-set and artefact-count reconciliation tables (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:116-145`).
- **Outputs:** nine required outputs, including a normalisation summary, QA findings, the register updated with a QA status, lists of reports safe to share and needing human review, and unresolved inconsistencies (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:147-159`); a closing one-line count summary (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:184-190`).
- **Shareability gate:** a report is safe to share only if every listed condition holds; otherwise it needs human review (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:161-182`). No report may be marked safe to share before this stage completes (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:95`).
- **Depends on:** stage 03's artefacts and registers; stage 00's labels.
- **Mandatory:** yes in staged mode.

### Branching and loops

The staged order is linear, but two stages end with a recommendation that may send the run elsewhere:

- Stage 01 ends with one of four decisions: continue broad triage, proceed to full SAST, narrow to a targeted pattern hunt, or pause SAST for validation (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/01-repo-triage-prompt.md:393-404`).
- Stage 02 ends with continue broad SAST, targeted pattern hunting, move to attacker-path validation, or stop (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:179`).
- Stage 03 states a recommended next phase (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:620-622`).
- After remediation, the relevant staged prompt is re-run against the fixed code (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/reporting-standards.md:158-160`).

The toolkit does not say how these recommendations map onto re-running stages. The question is tracked in [sumau/GC3-AI-SAST-Toolkit#1](https://github.com/sumau/GC3-AI-SAST-Toolkit/issues/1); how the runner handles these recommendations is under steps 2 and 5 in issue #2.

## One-shot mode

- **File:** `1-prompts/one-shot-minimum-sast-prompt.md`
- **Relationship to staged mode:** a fallback for teams that cannot run the staged workflow, not a replacement for it (`vendor/gc3-ai-sast-toolkit/1-prompts/README.md:15-19`, `vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:3-5`). The reviewer chooses it explicitly (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:19`, `vendor/gc3-ai-sast-toolkit/README.md:43`). It is a separate mode, not an extra stage: a run uses either the staged files or this one.
- **What it combines:** scope and depth budget, triage, source-to-sink review, promotion, recording what was not promoted, and a compact report pack with QA, in a single prompt (`vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:15-28`).
- **Self-contained:** it carries its own rules of engagement and its own copy of the evidence labels rather than referring to stage 00 (`vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:30-90`).
- **Default depth budget** if the reviewer gives none: one repository, up to 40 files, up to 25 scanner leads, at most 5 fully validated paths, at most 3 examples per pattern (`vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:103-122`).
- **Promotion gate:** the five core gates only, without stage 02's endpoint-authorisation and cross-service gates as separate gates (`vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:140-150`), although triage still covers those surfaces (`vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:135-136`).
- **Outputs:** seven files, written as files if the agent can, otherwise as sections of the response (`vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:168-291`):

| One-shot output | Nearest staged equivalent |
|---|---|
| `one-shot-sast-summary.md` | stage 01 executive summary and stage 02 global conclusion |
| `assessment-register.json` (with `run_metadata` including model and prompt-pack version) | the assessment register (stages 01 to 03) |
| `findings.md` (compact per-finding reports) | stage 03 human reports |
| `chains.md` | stage 02 chain register and stage 03 chain reports |
| `not-promoted-register.md` | stage 02 no-finding coverage notes |
| `validation-and-remediation.md` | stage 03 validation and remediation action registers |
| `normalisation-and-qa.md` (self-QA) | stage 04 |

The one-shot mode does not produce SARIF, OPTRS, VXDF, routing material or delivery packs. It ends with a fixed one-line count summary and a recommended next step, one of which is to re-run with the staged pack (`vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:306-314`).

## Evidence labels

The canonical labels are defined in stage 00 (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:35-77`). The root instructions say to use those definitions and preserve them in every artefact (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:22`). There are four families, each a closed set:

| Family | Values | Defined at |
|---|---|---|
| Source status | 4 values, from fully SAST-confirmed to source-disconfirmed | `vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:41-48` |
| Runtime status | 4 values: locally validated, deployed validated, not validated, not applicable | `vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:50-57` |
| Reachability status | 5 values, from source-visible to not established | `vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:59-67` |
| Exploitability status | 5 values: confirmed, hypothesis, config-dependent, private-dependent, disconfirmed | `vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:69-77` |

Related closed vocabularies:

- **Severity and confidence**, always kept separate: impact severity if exploitable (four levels or the department's scale) and evidence confidence (four levels) (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:79-86`).
- **Vulnerability disclosure status:** classification (6 values), evidence level (5), production impact (4), plus free-text safe/not-safe wording and handling fields (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:92-112`).
- **Lifecycle state:** 7 values (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:165-177`).

The same four families are restated, almost word for word, in the one-shot prompt (`vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:43-90`) and as the allowed values of the report template's evidence-status table (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:144-154`). Stage 03 requires them in an evidence classification table in every report (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:28-49`), and stage 04 normalises near-synonyms to them (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:99-114`).

Several other label sets appear elsewhere and do not map cleanly onto stage 00. How they map onto stage 00's labels is tracked in [sumau/GC3-AI-SAST-Toolkit#1](https://github.com/sumau/GC3-AI-SAST-Toolkit/issues/1).

## Candidates, promotion and confirmation

### Candidate lifecycle

Scanner output, including AI-generated candidate lists, is only ever a lead (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:192-194`). Every candidate ends in exactly one of seven lifecycle states, two promoted and five not, with a reason (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:165-177`). Not-promoted candidates must be kept in a coverage record, never dropped (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:24`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/reporting-standards.md:11`).

### Promotion gate

- **Stage 00** lists six things that must all be present before promotion; if any is missing, the candidate takes one of the five non-promoted states (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:179-190`).
- **Stage 02** turns this into five core gates (source, sink, path, control, consequence), each with `file:line` evidence, plus two conditional gates: endpoint authorisation for web, API and admin candidates, and data composition for cross-service candidates (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:28-40`). Analysis of a candidate stops as soon as a gate fails (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:21`).
- **Stage 02** also sets a promotion bar: a finding must have a credible path to one of eight attacker outcomes, and a list of things never counts on its own (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:211-236`). A finding whose reachability proof cannot name the attacker class, entry point, delivery mechanism and sink is not promoted (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:280`).
- **Chains** inherit the confidence of their weakest link and must cite findings or explicit assumptions (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:329-337`).

### Negative control

The negative control is mandatory and happens in two places:

1. **During analysis (stage 02 / one-shot).** Every candidate gets a section stating its strongest false-positive case (what would break it, where, whether evidence settles it, what would close it) and a decision afterwards: promoted, downgraded, disconfirmed or validation needed (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:63-77`, `vendor/gc3-ai-sast-toolkit/1-prompts/one-shot-minimum-sast-prompt.md:152-166`). Every promoted candidate must re-assess itself after this (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:103`). The prompting principles recommend this "argue both sides" pattern generally (`vendor/gc3-ai-sast-toolkit/1-prompts/README.md:31`).
2. **During confirmation (reporting).** The report template's negative-control prompt is mandatory (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:321-328`). If it finds a genuine reason the finding does not hold, the report is not filed (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:103`).

Stage 04 checks the negative-control result is present before a report can be shared (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:25`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/04-normalisation-and-qa-prompt.md:174`).

### Confirmation prompts

- **Drafted in stage 02:** at least four per material finding or chain (source-to-sink trace, sanitisation or authorisation check, reachability or configuration gate, negative control), with real file and line values filled in. Responses must not be fabricated (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:409-418`).
- **Reported in stage 03:** every material report has a confirmation section with the tool, model and version, each prompt and its response, and the submitter's assessment after the negative control. If no independent confirmation ran, the report says so and lists the unrun prompts as next steps (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:436-440`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:117`).
- **In the report template:** four generic prompts G1 to G4 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:201-229`), twelve type-specific prompts (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:231-319`), and the mandatory negative-control prompt (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:321-328`).
- **Independence:** ideally a different tool or model from discovery. Self-confirmation is allowed but must be flagged, and is a weaker signal (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:99`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:105`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:193-199`, `vendor/gc3-ai-sast-toolkit/CLAUDE.md:34`).
- **Gate on status:** confirmation, including the negative control, must run before a report moves from Draft to Submitted (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:33`).

The minimum number of confirmation prompts differs between files; which one is binding is tracked in [sumau/GC3-AI-SAST-Toolkit#1](https://github.com/sumau/GC3-AI-SAST-Toolkit/issues/1).

## The reporting bundle

### What it contains

- `reporting-standards.md`: the reporting model, including output layers, evidence states, claims control, SARIF, OPTRS, VXDF and routing (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/README.md:5-12`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/reporting-standards.md:1-160`).
- `review-checklist.md`: questions for people reviewing the method and outputs, and a feedback format (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/review-checklist.md:1-84`). It is for humans; the runner does not need it at run time.
- `templates/vulnerability-report.md`: a 17-section report template, labelled v1.0 in its header comment (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:1-18`).
- `templates/agent-filling-guide.md`: the procedure an agent follows to fill the template (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:1-5`).

### When the template is filled

When asked to report, escalate or file a finding, the agent reads the filling guide first, copies the template to an approved location outside the toolkit, fills every section, runs the confirmation prompts, records tool, model and prompt-pack versions, and does not commit the report to the toolkit (`vendor/gc3-ai-sast-toolkit/CLAUDE.md:26-36`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/README.md:16-27`). One report covers one finding. Only findings meeting the run scope's threshold get a report; the rest go to the not-promoted coverage register (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:9`, `vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:46-48`).

The guide needs five inputs before starting, and says to ask the human reviewer if any is missing (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:17-27`): the target repository and commit, the suspected finding, the team and reporter identity, the tool, model and prompt-pack identity, and the run scope.

### How each section is filled

The guide's sixteen steps work through the template in order, because later sections depend on evidence from earlier ones (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:29-139`). The "Source" column is where the runner would get the data; "human" means the toolkit expects a person to supply it.

| Template section | Filled by guide step | Source of data |
|---|---|---|
| 1. Report metadata (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:22-34`) | Step 2 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:37-44`) | Report ID scheme, reporter and team: human. Discovery tool, model and prompt-pack version: run metadata. Status starts as Draft. Tracking ID left blank for the receiving team. |
| (threshold check) | Step 3 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:46-48`) | Run scope. Stop and record as not promoted if below threshold. |
| 4. Affected locations (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:68-75`) | Step 4 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:50-64`) | Stage 02 handoff: file, lines, function, commit (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:610-640`) |
| 2. Summary, 3. Classification, 5. Technical description (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:36-87`) | Step 5 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:66-70`) | Stage 02 handoff: description, CWE, OWASP, severity (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:646-653`) |
| 6. Evidence: source, sink, path, tests (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:89-129`) | Step 6 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:72-78`) | Stage 02 evidence bundle snippets and test evidence (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:393`, `vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:396`). The tests subsection must say explicitly if none exist. |
| 7. Impact (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:131-142`) | Step 7 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:80-82`) | Stage 02 feasible attacker outcome (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:244-248`) |
| 8. Evidence status, 9. Disclosure status (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:144-166`) | Step 8 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:84-86`) | Stage 00 labels as set in stage 02 (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:53-59`), disclosure block (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/00-run-control-and-evidence-model.md:92-103`) |
| 10. Proof of concept (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:168-180`) | Step 9 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:88-90`) | Stage 02 static demonstration (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:507-525`), or marked theoretical |
| 11. Coding-agent confirmation (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:182-328`) | Step 10, mandatory (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:92-105`) | Confirmation prompts drafted in stage 02, run against a coding agent; real responses only |
| 12. Remediation (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:330-347`) | Step 11 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:107-111`) | Stage 02 remediation direction and actions (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:654-656`) |
| 13. Validation actions (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:349-355`) | Step 12 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:113-115`) | Stage 02 validation actions (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:657-660`) |
| 14. Claims control (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:357-363`) | Step 13 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:117-119`) | Stage 02 claims control (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/02-full-sast-attack-path-prompt.md:662`) |
| 15. References (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:365-369`) | Step 14 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:121-123`) | CWE and OWASP links; may be skipped |
| 16. Submitter checklist (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:371-382`) | Step 15 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:125-135`) | Every box must be ticked; fix gaps first |
| (hand-off) | Step 16 (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:137-139`) | Status set to Submitted; not edited afterwards |
| 17. Receiving-team notes (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/vulnerability-report.md:384-386`) | none | Left blank; human (receiving team) |

The guide's ground rules apply throughout: apply the run scope's threshold, no claim without `file:line`, no fabricated transcripts, no PoC against systems you do not own, redact secrets, keep the procedure generic, and treat the scanned repository as untrusted (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:7-15`). Where a step is unclear, the agent asks the human reviewer (`vendor/gc3-ai-sast-toolkit/2-reporting-bundle/templates/agent-filling-guide.md:153-155`).

### Relationship to stage 03's human reports

Stage 03 also produces a Markdown human report per finding, with its own structure: a decision snapshot, a human summary, and eighteen required sections (`vendor/gc3-ai-sast-toolkit/1-prompts/staged/03-security-reporting-output-prompt.md:381-418`). That structure is not the template's seventeen sections, and stage 03 never mentions the template or the filling guide. The two overlap (evidence status, disclosure status, confirmation, remediation, validation, claims control) but are not the same document. How they relate is tracked in [sumau/GC3-AI-SAST-Toolkit#1](https://github.com/sumau/GC3-AI-SAST-Toolkit/issues/1).

## Open questions

Open questions are tracked in issues, not in this document:

- **For the toolkit maintainers:** [sumau/GC3-AI-SAST-Toolkit#1](https://github.com/sumau/GC3-AI-SAST-Toolkit/issues/1). Releases, stable prompt IDs and the licence are in its draft upstream proposal; questions about the methodology itself are under "Methodology questions for the maintainers".
- **For the runner's design:** issue #2, listed as "Open from step 1" under the step each one affects.
