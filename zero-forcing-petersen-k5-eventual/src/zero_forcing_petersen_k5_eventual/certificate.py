"""Build the eventual P(n,5) theorem certificate."""

from __future__ import annotations

from .graph import edges
from .minor import reduced_edges, residue_base
from .separator import native_source_digest, run_separator_dp, transcript_digest
from .upper import replay_schedule
from .witness import N28_WORD, replay_n28_witness

BASE_ORDERS = (29, 30, 31, 32, 33)


def build_certificate() -> dict[str, object]:
    separator_results = run_separator_dp((28, *BASE_ORDERS))
    control, *bases = separator_results
    if not control.counterexample or any(result.counterexample for result in bases):
        raise AssertionError("balanced-separator base results changed")

    for n in range(16, 121):
        if reduced_edges(n) != edges(n - 5):
            raise AssertionError(f"five-column minor failed at n={n}")
    for n in range(29, 201):
        base = residue_base(n)
        if base not in BASE_ORDERS or base > n or (n - base) % 5:
            raise AssertionError("residue transfer failed")
    upper_replays = tuple(replay_schedule(n) for n in range(11, 201))
    selected, boundary = replay_n28_witness()

    return {
        "theorem": "Z(P(n,5))=12 for every integer n>=29",
        "separator_certificate": {
            "semantics": "exact balanced A/B/Y column DP with B<=11",
            "native_source_sha256": native_source_digest(),
            "transcript_sha256": transcript_digest(separator_results),
            "positive_control_n28": control.as_dict(),
            "pathwidth_base_orders": [result.as_dict() for result in bases],
        },
        "n28_half_boundary_witness": {
            "column_word": list(N28_WORD),
            "selected_vertices": list(selected),
            "internal_boundary_vertices": list(boundary),
        },
        "five_column_minor": {
            "statement": "P(n-5,5) is a topological minor of P(n,5) for n>=16",
            "replayed_order_range": [16, 120],
            "base_orders": list(BASE_ORDERS),
        },
        "uniform_upper_bound": {
            "initial_size": 12,
            "replayed_order_range": [upper_replays[0].n, upper_replays[-1].n],
            "aggregate_force_count": sum(replay.force_count for replay in upper_replays),
        },
    }
