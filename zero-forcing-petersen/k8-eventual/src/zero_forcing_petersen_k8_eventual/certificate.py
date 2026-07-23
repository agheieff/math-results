"""Build the eventual P(n,8) theorem certificate."""

from __future__ import annotations

from .graph import edges
from .minor import reduced_edges, residue_base
from .separator import (
    SeparatorRun,
    frozen_separator_run,
    frozen_transcript_file_digest,
    native_source_digest,
    run_separator_dp,
    transcript_digest,
)
from .upper import replay_schedule
from .witness import replay_n64_witness

BASE_ORDERS = (65, 66, 67, 68, 69, 70, 71, 72)
POSITIVE_CONTROL = 64
EXPECTED_CLOSURES = (97, 0, 0, 0, 0, 0, 0, 0, 0)
EXPECTED_TRANSCRIPT_SHA256 = "9f53f1601eac5cd136a949829955d361caa9240a63e8f7e64dbd3b210237701d"
FIRST_RUN_BINARY_SHA256 = "ab3c4cff63b95e4faf81f283aa7f53ee85dc9ac1ca62bf0410b8a30305ea552b"
K7_CONTROL_BINARY_SHA256 = "e78cd07ccb17bdf416fc755fb3387da8c886d9071a533c048aaf9e82056fdc14"


def build_certificate(separator: SeparatorRun | None = None) -> dict[str, object]:
    frozen = frozen_separator_run()
    result = run_separator_dp() if separator is None else separator
    if result != frozen:
        raise AssertionError("exact separator transcript changed")
    if result.closure_counts != EXPECTED_CLOSURES:
        raise AssertionError("balanced-separator closure counts changed")
    if transcript_digest(result) != EXPECTED_TRANSCRIPT_SHA256:
        raise AssertionError("balanced-separator transcript digest changed")

    closure_exists = dict(
        zip(result.orders, (count > 0 for count in result.closure_counts), strict=True)
    )
    if not closure_exists[POSITIVE_CONTROL] or any(closure_exists[n] for n in BASE_ORDERS):
        raise AssertionError("balanced-separator control or base result changed")

    for n in range(25, 177):
        if reduced_edges(n) != edges(n - 8):
            raise AssertionError(f"eight-column minor failed at n={n}")
    for n in range(65, 401):
        base = residue_base(n)
        if base not in BASE_ORDERS or base > n or (n - base) % 8:
            raise AssertionError("residue transfer failed")
    upper_replays = tuple(replay_schedule(n) for n in range(17, 221))
    witness = replay_n64_witness()

    return {
        "status": "PASS",
        "theorem": "Z(P(n,8))=18 for every integer n>=65",
        "separator_certificate": {
            "semantics": (
                "exact outer-B-anchored balanced A/B/Y DP with B<=17, "
                "partitioned by the first eight inner colors"
            ),
            "partition_count": 6561,
            "native_source_sha256": native_source_digest(),
            "first_run_binary_sha256": FIRST_RUN_BINARY_SHA256,
            "transcript_sha256": transcript_digest(result),
            "transcript_file_sha256": frozen_transcript_file_digest(),
            "maximum_aggregate_reduced_states": max(result.layer_counts),
            "layer_counts": list(result.layer_counts),
            "closures": result.closure_records(),
            "positive_control_order": POSITIVE_CONTROL,
            "pathwidth_base_orders": list(BASE_ORDERS),
        },
        "k7_partition_cross_check": {
            "statement": (
                "the partitioned verifier reproduced every frozen k=7 layer count "
                "and transcript fingerprint"
            ),
            "orders": [44, 56],
            "closure_counts": [59, 0, 0, 0, 0, 92, 0, 0, 0, 0, 0, 0, 0],
            "closure_xor_at_positive_controls": [
                "88298d16f88edf2d",
                "3d0b2c1015298c12",
            ],
            "closure_sum_at_positive_controls": [
                "fea6f72ed18adae9",
                "7cc711e54967840",
            ],
            "frozen_transcript_sha256": (
                "4a85f75724dc7c70a2503feba361c93c151b77275877d43dbdda7ce09fc392a5"
            ),
            "control_binary_sha256": K7_CONTROL_BINARY_SHA256,
        },
        "n64_half_boundary_control": {
            "scope": "positive separator control only; no claim about Z(P(64,8))",
            "column_word": list(witness.word),
            "selected_vertices": list(witness.selected),
            "internal_boundary_vertices": list(witness.boundary),
            "word_sha256": witness.word_sha256,
        },
        "eight_column_minor": {
            "statement": "P(n-8,8) is a topological minor of P(n,8) for n>=25",
            "replayed_order_range": [25, 176],
            "base_orders": list(BASE_ORDERS),
        },
        "uniform_upper_bound": {
            "initial_size": 18,
            "replayed_order_range": [upper_replays[0].n, upper_replays[-1].n],
            "aggregate_force_count": sum(replay.force_count for replay in upper_replays),
        },
    }
