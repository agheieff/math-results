"""Build the eventual P(n,7) theorem certificate."""

from __future__ import annotations

from .graph import edges
from .minor import reduced_edges, residue_base
from .separator import native_source_digest, run_separator_dp, transcript_digest
from .upper import replay_schedule
from .witness import block_word, replay_block_witness

BASE_ORDERS = (50, 51, 52, 53, 54, 55, 56)
ISOLATED_ORDERS = (45, 46, 47, 48)
POSITIVE_CONTROLS = (44, 49)
ZERO_ORDERS = (*ISOLATED_ORDERS, *BASE_ORDERS)
EXPECTED_CLOSURES = (59, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 0)


def build_certificate() -> dict[str, object]:
    separator = run_separator_dp()
    if separator.closure_counts != EXPECTED_CLOSURES:
        raise AssertionError("balanced-separator closure counts changed")
    closure_exists = dict(
        zip(separator.orders, (count > 0 for count in separator.closure_counts), strict=True)
    )
    if any(not closure_exists[n] for n in POSITIVE_CONTROLS) or any(
        closure_exists[n] for n in ZERO_ORDERS
    ):
        raise AssertionError("balanced-separator results changed")

    for n in range(22, 155):
        if reduced_edges(n) != edges(n - 7):
            raise AssertionError(f"seven-column minor failed at n={n}")
    for n in range(50, 351):
        base = residue_base(n)
        if base not in BASE_ORDERS or base > n or (n - base) % 7:
            raise AssertionError("residue transfer failed")
    upper_replays = tuple(replay_schedule(n) for n in range(15, 203))
    selected, boundary = replay_block_witness(7)
    family_boundaries = [len(replay_block_witness(multiplier)[1]) for multiplier in range(3, 11)]

    return {
        "theorem": ("Z(P(n,7))=16 for 45<=n<=48 and for every integer n>=50"),
        "separator_certificate": {
            "semantics": (
                "exact outer-B-anchored balanced A/B/Y open-strip DP minimizing B with B<=15"
            ),
            "native_source_sha256": native_source_digest(),
            "transcript_sha256": transcript_digest(separator),
            "maximum_reduced_states": max(separator.layer_counts),
            "layer_counts": list(separator.layer_counts),
            "closures": separator.closure_records(),
            "isolated_exact_orders": list(ISOLATED_ORDERS),
            "pathwidth_base_orders": list(BASE_ORDERS),
        },
        "n49_half_boundary_witness": {
            "scope": "positive control only; it makes no claim about Z(P(49,7))",
            "column_word": list(block_word(7)),
            "selected_vertices": list(selected),
            "internal_boundary_vertices": list(boundary),
        },
        "multiple_of_seven_family": {
            "statement": "P(7m,7) has a half-set with exact internal boundary 2m",
            "replayed_multipliers": [3, 10],
            "boundary_sizes": family_boundaries,
        },
        "seven_column_minor": {
            "statement": "P(n-7,7) is a topological minor of P(n,7) for n>=22",
            "replayed_order_range": [22, 154],
            "base_orders": list(BASE_ORDERS),
        },
        "uniform_upper_bound": {
            "initial_size": 16,
            "replayed_order_range": [upper_replays[0].n, upper_replays[-1].n],
            "aggregate_force_count": sum(replay.force_count for replay in upper_replays),
        },
    }
