# ai-sast-toolkit-runner

> An unofficial, community runner for the GC3 AI SAST Toolkit. It is not produced or endorsed by the toolkit's maintainers.

A Python command-line tool that makes reviews using the GC3 AI SAST Toolkit's staged workflow easier to carry out and audit. It makes the procedure repeatable, although the model's output is not. It works with the toolkit's existing prompts, evidence model and reporting bundle. It does not replace or change the methodology.

Status: early development. Nothing here is usable for a real review yet.

## Relationship to the toolkit

The runner does not include any toolkit content. You supply a local copy of the GC3 AI SAST Toolkit, and the runner reads it from that path.

## Development

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12 or later.

```sh
uv sync
uv run pytest
uv run ai-sast-run --help
```

## Licence

The runner's own code is MIT-licensed; see [LICENSE](LICENSE). The GC3 AI SAST Toolkit is a separate work with its own terms.
