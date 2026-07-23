"""Build the eventual P(n,6) theorem certificate."""

from __future__ import annotations

from .graph import edges
from .minor import reduced_edges, residue_base
from .separator import native_source_digest, run_separator_dp, transcript_digest
from .upper import replay_schedule
from .witness import N36_WORD, replay_n36_witness

BASE_ORDERS = (37, 38, 39, 40, 41, 42)
ISOLATED_ORDER = 35
EXPECTED_CLOSURES = (40, 0, 124, 0, 0, 0, 0, 0, 0)


def build_certificate() -> dict[str, object]:
    separator = run_separator_dp()
    if separator.closure_counts != EXPECTED_CLOSURES:
        raise AssertionError("balanced-separator results changed")

    for n in range(19, 133):
        if reduced_edges(n) != edges(n - 6):
            raise AssertionError(f"six-column minor failed at n={n}")
    for n in range(37, 301):
        base = residue_base(n)
        if base not in BASE_ORDERS or base > n or (n - base) % 6:
            raise AssertionError("residue transfer failed")
    upper_replays = tuple(replay_schedule(n) for n in range(13, 202))
    selected, boundary = replay_n36_witness()

    return {
        "theorem": "Z(P(35,6))=14 and Z(P(n,6))=14 for every integer n>=37",
        "separator_certificate": {
            "semantics": "exact balanced A/B/Y open-strip DP minimizing B with B<=13",
            "native_source_sha256": native_source_digest(),
            "transcript_sha256": transcript_digest(separator),
            "maximum_reduced_states": max(separator.layer_counts),
            "layer_counts": list(separator.layer_counts),
            "closures": separator.closure_records(),
            "isolated_exact_order": ISOLATED_ORDER,
            "pathwidth_base_orders": list(BASE_ORDERS),
        },
        "n36_half_boundary_witness": {
            "scope": "positive control only; it makes no claim about Z(P(36,6))",
            "column_word": list(N36_WORD),
            "selected_vertices": list(selected),
            "internal_boundary_vertices": list(boundary),
        },
        "six_column_minor": {
            "statement": "P(n-6,6) is a topological minor of P(n,6) for n>=19",
            "replayed_order_range": [19, 132],
            "base_orders": list(BASE_ORDERS),
        },
        "uniform_upper_bound": {
            "initial_size": 14,
            "replayed_order_range": [upper_replays[0].n, upper_replays[-1].n],
            "aggregate_force_count": sum(replay.force_count for replay in upper_replays),
        },
    }
