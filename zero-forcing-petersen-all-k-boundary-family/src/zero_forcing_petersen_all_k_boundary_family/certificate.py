"""Build the all-k exact-boundary certificate."""

from __future__ import annotations

import hashlib

from .family import block, replay


def build_certificate() -> dict[str, object]:
    replays = tuple(replay(k, multiplier) for k in range(3, 41) for multiplier in range(3, 11))
    digest = hashlib.sha256()
    for result in replays:
        digest.update(
            (
                f"{result.k}:{result.multiplier}:{result.n}:{result.selected_size}:"
                f"{result.boundary_size}:{result.y_count}:{result.word_sha256}|"
            ).encode()
        )
    squares = tuple(replay(k, k) for k in range(6, 41))
    if any(result.n < 6 * result.k - 1 for result in squares):
        raise AssertionError("square order does not reach the proposed threshold")
    if any(result.boundary_size >= 2 * result.k + 2 for result in squares):
        raise AssertionError("square family does not refute the proposed boundary")

    return {
        "theorem": ("For all k,m>=3, P(km,k) has a half-set with exact internal boundary 2m"),
        "blocks": {
            "odd_k_2r_plus_1": "BA (YY)^r BY (AA)^(r-1)",
            "even_k_2r": "BA (YY)^r BA (AA)^(r-2)",
            "sample_k7": list(block(7)),
            "sample_k8": list(block(8)),
        },
        "finite_replay": {
            "k_range": [3, 40],
            "multiplier_range": [3, 10],
            "cases": len(replays),
            "aggregate_sha256": digest.hexdigest(),
        },
        "infinite_square_refutation": {
            "statement": ("For every k>=6, n=k^2>=6k-1 and a half-set has boundary 2k<2k+2"),
            "replayed_k_range": [6, 40],
            "boundary_gap": 2,
        },
    }
