from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from strong_seymour.search import build_encoding
from strong_seymour.tournament import (
    hall_neighbours,
    out_neighbours,
    second_out_neighbours,
    validate_adjacency,
)


def has_complete_matching_exhaustive(
    adjacency: Sequence[Sequence[int]], left: Sequence[int], right: Sequence[int]
) -> bool:
    """Try every feasible injection, independently of the SAT Hall encoding."""
    right_set = set(right)
    choices = {
        source: tuple(target for target in right_set if adjacency[source][target])
        for source in left
    }
    ordered_left = tuple(sorted(left, key=lambda source: len(choices[source])))

    def extend(index: int, used: set[int]) -> bool:
        if index == len(ordered_left):
            return True
        source = ordered_left[index]
        for target in choices[source]:
            if target in used:
                continue
            used.add(target)
            if extend(index + 1, used):
                return True
            used.remove(target)
        return False

    return extend(0, set())


def verify_counterexample(certificate: dict[str, Any]) -> None:
    if certificate.get("format") != "strong-seymour-tournament-v1":
        raise ValueError("unknown certificate format")
    order = certificate["order"]
    adjacency = certificate["adjacency"]
    if not isinstance(order, int) or len(adjacency) != order:
        raise ValueError("order does not match adjacency matrix")
    validate_adjacency(adjacency)

    witnesses = certificate.get("hall_witnesses", {})
    for vertex in range(order):
        first = out_neighbours(adjacency, vertex)
        second = second_out_neighbours(adjacency, vertex)
        if has_complete_matching_exhaustive(adjacency, first, second):
            raise ValueError(f"vertex {vertex} is a strong Seymour vertex")
        if str(vertex) in witnesses:
            witness = witnesses[str(vertex)]
            reached = hall_neighbours(adjacency, vertex, witness)
            if len(reached) >= len(witness):
                raise ValueError(f"Hall witness at vertex {vertex} is not deficient")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_cnf_reproduction(cnf_path: Path, order: int) -> None:
    encoding = build_encoding(order)
    with tempfile.TemporaryDirectory(prefix="strong-seymour-") as directory:
        regenerated = Path(directory) / "regenerated.cnf"
        encoding.cnf.to_file(regenerated)
        if regenerated.read_bytes() != cnf_path.read_bytes():
            raise ValueError("committed CNF differs from deterministic regeneration")


def verify_drat(cnf_path: Path, proof_path: Path, checker: Path) -> None:
    result = subprocess.run(
        [checker, cnf_path, proof_path],
        check=False,
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    if result.returncode != 0 or "s VERIFIED" not in output:
        raise ValueError(f"DRAT verification failed:\n{output}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path)
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--order", type=int, default=13)
    args = parser.parse_args()

    if args.certificate is not None:
        verify_counterexample(json.loads(args.certificate.read_text()))
        print(f"verified counterexample: {args.certificate}")
    if args.cnf is not None:
        verify_cnf_reproduction(args.cnf, args.order)
        print(f"verified CNF reproduction: sha256={sha256(args.cnf)}")
    if args.proof is not None:
        if args.cnf is None or args.drat_trim is None:
            parser.error("--proof requires --cnf and --drat-trim")
        verify_drat(args.cnf, args.proof, args.drat_trim)
        print(f"verified DRAT proof: sha256={sha256(args.proof)}")
    if args.certificate is None and args.cnf is None:
        parser.error("provide a counterexample certificate or --cnf")


if __name__ == "__main__":
    main()
