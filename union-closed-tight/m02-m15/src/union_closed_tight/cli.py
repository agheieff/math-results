"""Command-line interface."""

from __future__ import annotations

import argparse
from pathlib import Path

from union_closed_tight.certificates import build_manifest, verify_all
from union_closed_tight.encoding import Instance, build_cnf


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    commands = root.add_subparsers(dest="command", required=True)

    generate = commands.add_parser("generate")
    generate.add_argument("--order", type=int, default=8)
    generate.add_argument("--member-count", type=int, required=True)
    generate.add_argument("--output", type=Path, required=True)

    verify = commands.add_parser("verify")
    verify.add_argument("--manifest", type=Path, default=Path("certificates/manifest.json"))
    verify.add_argument("--checker", default="drat-trim")
    verify.add_argument("--lrat-checker")

    certify = commands.add_parser("certify")
    certify.add_argument("--order", type=int, default=8)
    certify.add_argument("--minimum", type=int, default=2)
    certify.add_argument("--maximum", type=int, default=15)
    certify.add_argument("--solver", default="cadical")
    certify.add_argument("--checker", default="drat-trim")
    certify.add_argument("--output", type=Path, default=Path("certificates/manifest.json"))
    return root


def main() -> None:
    arguments = parser().parse_args()
    if arguments.command == "generate":
        build_cnf(Instance(arguments.order, arguments.member_count)).to_file(arguments.output)
        return
    if arguments.command == "certify":
        build_manifest(
            arguments.order,
            arguments.minimum,
            arguments.maximum,
            arguments.solver,
            arguments.checker,
            arguments.output,
        )
        return
    verify_all(arguments.manifest, arguments.checker, arguments.lrat_checker)


if __name__ == "__main__":
    main()
