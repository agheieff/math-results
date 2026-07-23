"""Command-line entry point for exhaustive checks."""

import argparse
from collections.abc import Sequence

from tau_k_maximal.checker import exhaustive_check

DEFAULT_INSTANCES = ("2,4", "2,5", "2,6", "3,6")


def _instance(value: str) -> tuple[int, int]:
    try:
        raw_q, raw_order = value.split(",", maxsplit=1)
        return int(raw_q), int(raw_order)
    except ValueError as error:
        raise argparse.ArgumentTypeError("instance must have form Q,N") from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Exhaustively check small tau_k-maximal graph instances."
    )
    parser.add_argument(
        "instances",
        metavar="Q,N",
        nargs="*",
        type=_instance,
        help="q=k+1 and graph order (defaults to small feasible cases)",
    )
    parser.add_argument(
        "--max-ground-edges",
        type=int,
        default=18,
        help="refuse instances whose complete graph exceeds this many edges",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    instances = args.instances or [_instance(value) for value in DEFAULT_INSTANCES]
    for q, order in instances:
        result = exhaustive_check(q, order, max_ground_edges=args.max_ground_edges)
        status = "PASS" if result.maximal_edge_counts == (result.predicted_edge_count,) else "FAIL"
        print(
            f"{status} q={q} n={order}: {result.total_graphs} graphs, "
            f"{result.admissible_graphs} admissible, "
            f"{result.maximal_graphs} maximal, "
            f"maximal sizes={result.maximal_edge_counts}"
        )
