"""Command-line entry point for ``ai-sast-run``."""

import argparse
from collections.abc import Sequence

from ai_sast_toolkit_runner import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-sast-run",
        description="Unofficial runner for the GC3 AI SAST Toolkit workflow.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
