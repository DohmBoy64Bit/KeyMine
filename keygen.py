#!/usr/bin/env python3
"""KeyMine application entry point."""

from keymine.cli import run_cli


def main() -> int:
    exit_code = run_cli()
    if exit_code is not None:
        return exit_code

    from keymine.ui import launch_gui

    return launch_gui()


if __name__ == "__main__":
    raise SystemExit(main())
