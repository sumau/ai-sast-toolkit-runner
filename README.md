# ai-sast-toolkit-runner

> An unofficial, community runner for the GC3 AI SAST Toolkit. It is not produced or endorsed by the toolkit's maintainers.

A Python command-line tool that runs the GC3 AI SAST Toolkit's staged workflow as a repeatable, auditable process. It orchestrates the toolkit's existing prompts, evidence model and reporting bundle. It does not replace or change the methodology.

Status: early development. Nothing here is usable for a real review yet.

## Relationship to the toolkit

The runner does not include any toolkit content. You supply a local copy of the GC3 AI SAST Toolkit, and the runner reads it from that path. See [ADR 0001](docs/adr/0001-runner-separate-from-toolkit.md) for why the two are kept separate.

## Development

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12 or later.

```sh
uv sync
uv run pytest
uv run ai-sast-run --help
```

## Licence

The runner's own code is MIT-licensed; see [LICENSE](LICENSE). The GC3 AI SAST Toolkit is a separate work with its own terms.
