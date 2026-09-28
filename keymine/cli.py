from __future__ import annotations

import argparse
import sys

from .core import generate_key, generate_random_key, key_valid, mapping_lines


def print_mapping() -> None:
    print("Character mapping:")
    print()
    for line in mapping_lines():
        print(f"  {line}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "KeyMine GUI and CLI key generator for the supplied GameMaker key algorithm. "
            "Run without arguments to open the GUI."
        )
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--prefix",
        metavar="TEXT",
        help="generate a key from an exact 4-character A-Z/0-9 prefix",
    )
    mode.add_argument(
        "--validate",
        metavar="KEY",
        help="check whether an 8-character key passes the original validator",
    )
    mode.add_argument(
        "--show-mapping",
        action="store_true",
        help="display the complete mirror-character mapping",
    )
    mode.add_argument(
        "--count",
        type=int,
        metavar="N",
        help="generate N random keys in the terminal instead of launching the GUI",
    )

    return parser


def run_cli() -> int | None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.prefix is not None:
            print(generate_key(args.prefix))
            return 0

        if args.validate is not None:
            valid = key_valid(args.validate)
            print("VALID" if valid else "INVALID")
            return 0 if valid else 1

        if args.show_mapping:
            print_mapping()
            return 0

        if args.count is not None:
            if args.count < 1:
                parser.error("--count must be at least 1")

            for _ in range(args.count):
                print(generate_random_key())
            return 0

        return None

    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
