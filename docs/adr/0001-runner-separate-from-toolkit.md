---
status: accepted
date: 2026-10-27
---

# The runner lives in its own repo, separate from the GC3 AI SAST Toolkit

The CLI workflow runner is developed as an installable Python package in its own repo, and is pointed at a copy of the GC3 AI SAST Toolkit at run time. It is not merged into the toolkit repo. We chose this because the runner's design will change rapidly while it is being learned and built, we intend to own it long-term, its early users are technical and can install it separately, and it depends on only a small, documented subset of the toolkit. Keeping it separate also keeps the toolkit documentation-only and avoids a clash between the toolkit's reviewer-facing `CLAUDE.md` / `AGENTS.md` and the instructions needed to develop the runner.

## Considered options

- **Merge into the toolkit repo (e.g. `3-runner/`).** Rejected for now. Benefits: one place for reviewers to find it, the toolkit's approved status, prompt and runner changes landing in one PR, and same-repo CI catching drift. Costs: every runner change waits on upstream review, the maintainers inherit Python code, and the root `CLAUDE.md` would govern development sessions as well as review sessions.
- **Vendor a copy of the toolkit into the runner repo.** Rejected: it drifts silently from upstream, and the toolkit has no licence, so redistributing its content is unclear.

## Consequences

- **How the runner gets the toolkit.** The toolkit is a git submodule pinned to a specific commit, used for development and integration tests. Unit tests use small fake fixtures. At run time the user supplies the toolkit location.
- **Recording the version.** Each run record holds a content hash of every toolkit file it used, plus the commit when available. Staleness checks compare hashes, not version labels, so they work with a submodule, a zip download or a department fork.
- **Release tags.** The toolkit currently has no releases, tags or version markers, although its reporting guide requires a prompt-pack version to be recorded. We will ask the maintainers whether they would tag releases. If they agree, we would suggest a release whenever the methodology changes (major for incompatible changes to stages, outputs or the report template; minor for additions; patch for wording fixes). If they tag releases: the submodule pins a release tag rather than a bare commit; each run record holds the release as the prompt-pack version alongside the content hashes, and warns if the files do not match the release they claim to be; the runner declares which toolkit versions it supports; and the drift check watches for new releases. Hashes stay the source of truth for staleness either way, and the runner must keep working from an untagged commit.
- **The manifest.** A manifest in the runner repo records the toolkit details the runner relies on, such as stage files and IDs, stage order, evidence labels, stable ID formats, the scope re-anchor line, the register's required fields and report template fields. These are recorded as structure, not quoted prompt text. The runner never parses or alters prompt text. Once the manifest has settled, it may be proposed upstream as a machine-readable file in the toolkit.
- **Catching drift.** A scheduled CI job (weekly, and runnable by hand) checks the toolkit's latest upstream version against the manifest and opens an issue if anything changed. Moving the pin to a newer toolkit version is always a reviewed change, never automatic.
- **Licence.** The runner package never includes toolkit content. The manifest holds only file paths, IDs and hashes, never copied prompt text. The runner's own code is MIT-licensed. We will ask the toolkit's maintainers to clarify its licence.
- **Instruction files.** The toolkit's root `CLAUDE.md` / `AGENTS.md` are reviewer instructions for whatever runs a stage, not instructions for agents working on the runner. The runner repo has its own developer `CLAUDE.md`.
- **What we ask of upstream.** Only four things: a README link to the runner, small PRs that make toolkit files easier for a program to parse (such as the manifest and stable stage IDs), versioned releases, and no runner code in their repo. Our fork of the toolkit is used only for those PRs, and its `CLAUDE.md` / `AGENTS.md` stay unchanged.
- **Hosting.** The runner repo lives on the author's personal GitHub account and can be transferred to a departmental or toolkit organisation later.

## When to revisit

Reopen this decision if any of the following happens:

- departments require the runner to ship inside the approved toolkit
- long-term ownership moves to the toolkit maintainers
- updating to a newer toolkit version keeps breaking the runner despite the manifest
