"""CaféLibro CLI entry point.

Each feature lives in its own module and exposes `register_parser(subparsers)`.
Add new features by importing the module and calling its register_parser below.
"""
import argparse
import sys

import loans


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cafelibro")
    subparsers = parser.add_subparsers(dest="command", required=True)

    loans.register_parser(subparsers)
    # When other features are added, register them here, e.g.:
    # members.register_parser(subparsers)
    # books.register_parser(subparsers)
    # returns.register_parser(subparsers)
    # holdings.register_parser(subparsers)
    # overdue.register_parser(subparsers)

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())