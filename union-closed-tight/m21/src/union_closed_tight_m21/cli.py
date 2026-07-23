"""Command line for the single fixed target."""

from __future__ import annotations

import argparse
from pathlib import Path

from union_closed_tight_m21.certificates import build_certificate, verify_certificate
from union_closed_tight_m21.encoding import build_cnf


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Order-eight, m=21 clean-tight gate")
    commands = root.add_subparsers(dest="command", required=True)

    generate = commands.add_parser("generate", help="write the deterministic target CNF")
    generate.add_argument("--output", type=Path, required=True)

    certify = commands.add_parser("certify", help="run the bounded DRAT/LRAT pipeline")
    certify.add_argument("--solver", required=True)
    certify.add_argument("--drat-checker", required=True)
    certify.add_argument("--lrat-checker", required=True)
    certify.add_argument("--manifest", type=Path, default=Path("certificates/manifest.json"))
    certify.add_argument("--work-directory", type=Path, default=Path(".work/certify"))
    certify.add_argument("--timeout-seconds", type=int, default=1800)

    verify = commands.add_parser("verify", help="regenerate CNF and replay retained proofs")
    verify.add_argument("--drat-checker", required=True)
    verify.add_argument("--lrat-checker", required=True)
    verify.add_argument("--manifest", type=Path, default=Path("certificates/manifest.json"))
    verify.add_argument("--work-directory", type=Path, default=Path(".work/verify"))
    verify.add_argument("--timeout-seconds", type=int, default=1800)
    return root


def main() -> None:
    arguments = parser().parse_args()
    if arguments.command == "generate":
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        build_cnf().to_file(arguments.output)
        return
    if arguments.command == "certify":
        build_certificate(
            arguments.solver,
            arguments.drat_checker,
            arguments.lrat_checker,
            arguments.manifest,
            arguments.work_directory,
            arguments.timeout_seconds,
        )
        print("order=8, m=21: DRAT+LRAT built and VERIFIED")
        return
    verify_certificate(
        arguments.manifest,
        arguments.drat_checker,
        arguments.lrat_checker,
        arguments.work_directory,
        arguments.timeout_seconds,
    )
    print("order=8, m=21: retained DRAT+LRAT VERIFIED")


if __name__ == "__main__":
    main()
