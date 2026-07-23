"""Build a deterministic finite regression certificate."""

from __future__ import annotations

import hashlib

from .forcing import replay_symbolic_schedule
from .graph import petersen_edges
from .minor import reduced_minor_edges, residue_base

MAX_K = 12
MAX_N = 120


def build_certificate() -> dict[str, object]:
    upper_digest = hashlib.sha256()
    upper_cases = 0
    for k in range(1, MAX_K + 1):
        for n in range(2 * k + 1, MAX_N + 1):
            replay = replay_symbolic_schedule(n, k)
            upper_digest.update(
                f"{k}:{n}:{replay.initial_size}:{replay.force_count}:"
                f"{replay.trace_sha256}|".encode()
            )
            upper_cases += 1

    minor_digest = hashlib.sha256()
    minor_cases = 0
    for k in range(1, MAX_K + 1):
        for n in range(3 * k + 1, MAX_N + 1):
            reduced = reduced_minor_edges(n, k)
            expected = petersen_edges(n - k, k)
            if reduced != expected:
                raise AssertionError(f"k-column minor mismatch at n={n}, k={k}")
            minor_digest.update(f"{k}:{n}:{len(reduced)}|".encode())
            minor_cases += 1

    transfer_digest = hashlib.sha256()
    transfer_cases = 0
    for k in range(1, MAX_K + 1):
        base_start = 2 * k + 1
        for n in range(base_start, MAX_N + 1):
            base = residue_base(n, k, base_start)
            if not base_start <= base < base_start + k or base > n or (n - base) % k:
                raise AssertionError("residue transfer failed")
            transfer_digest.update(f"{k}:{n}:{base}|".encode())
            transfer_cases += 1

    return {
        "theorems": [
            "Z(P(n,k))<=2k+2 for k>=1 and n>=2k+1",
            "P(n-k,k) is a topological minor of P(n,k) for k>=1 and n>=3k+1",
        ],
        "replay_grid": {"maximum_k": MAX_K, "maximum_n": MAX_N},
        "upper_witness": {
            "cases": upper_cases,
            "aggregate_sha256": upper_digest.hexdigest(),
        },
        "k_column_minor": {
            "cases": minor_cases,
            "aggregate_sha256": minor_digest.hexdigest(),
        },
        "residue_transfer": {
            "cases": transfer_cases,
            "aggregate_sha256": transfer_digest.hexdigest(),
        },
    }
