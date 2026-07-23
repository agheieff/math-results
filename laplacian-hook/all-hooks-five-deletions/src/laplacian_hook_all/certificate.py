"""Finite symbolic certificate for the corrected all-hook theorem."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from itertools import combinations

from .characters import scaled_character_numerators
from .graphs import ComplementType, complement_types
from .statistics import (
    ComplementInvariants,
    complement_invariants,
    graph_statistics,
)

Signature = tuple[tuple[int, int], ...]
SignaturePair = tuple[Signature, Signature]

EXPECTED_TYPE_COUNTS = {0: 1, 1: 1, 2: 2, 3: 5, 4: 11, 5: 26}
EXPECTED_PATTERN_COUNTS = {
    (-12, 1): 2,
    (-6, 0): 6,
    (-6, 1): 5,
    (0, -1): 2,
    (0, 0): 6,
    (0, 1): 6,
    (6, -1): 1,
    (6, 0): 5,
    (6, 1): 1,
    (12, 0): 1,
    (18, -1): 1,
    (18, 0): 1,
}
EXPECTED_CLASS_COUNTS = {"q1": 644, "q2": 354, "q3": 30, "endpoint": 1, "q4": 6}
EXPECTED_SHA256 = "8519991111d6428962c7ac5513e542ecd44e36b689aaf0c00a01d38cb6de2ee0"

P_PAIRS: dict[SignaturePair, int] = {
    (((2, 1), (4, 13)), ((3, 3), (3, 3))): -1,
    (((2, 1), (2, 1), (4, 13)), ((2, 1), (3, 3), (3, 3))): -1,
    (((2, 1), (5, 29)), ((3, 3), (4, 7))): -2,
    (((2, 1), (5, 58)), ((3, 3), (4, 13))): -1,
    (((6, 122),), ((6, 659),)): 1,
}
Q_PAIRS: dict[SignaturePair, int] = {
    (((2, 1), (4, 30)), ((6, 692),)): -1,
}
ENDPOINT_PAIR: SignaturePair = (
    ((2, 1), (4, 15)),
    ((5, 220),),
)


@dataclass(frozen=True)
class Certificate:
    graphs: tuple[ComplementType, ...]
    invariants: tuple[ComplementInvariants, ...]
    type_counts: dict[int, int]
    pattern_counts: dict[tuple[int, int], int]
    class_counts: dict[str, int]
    sha256: str

    def summary(self) -> dict[str, object]:
        return {
            "types": len(self.graphs),
            "type_counts": self.type_counts,
            "pairs": len(self.graphs) * (len(self.graphs) - 1) // 2,
            "class_counts": self.class_counts,
            "sha256": self.sha256,
        }


def _p_polynomial(order: int, hook_parameter: int) -> int:
    n, k = order, hook_parameter
    return 8 * k**3 - 48 * k**2 - 2 * k * n**2 + 10 * k * n + 76 * k + n**3 - 4 * n**2 + n - 42


def _q_polynomial(order: int, hook_parameter: int) -> int:
    n, k = order, hook_parameter
    return 12 * k**2 - 10 * k * n - 16 * k + 3 * n**2 + n + 10


def _scaled_q4_difference(
    left: ComplementType,
    right: ComplementType,
    order: int,
    hook_parameter: int,
) -> int:
    left_stats = graph_statistics(left, order)
    right_stats = graph_statistics(right, order)
    if left_stats.two_matching_count != right_stats.two_matching_count:
        raise AssertionError("two-matching term did not cancel")
    transposition, three_cycle, four_cycle = scaled_character_numerators(order, hook_parameter)
    denominator = (order - 1) * (order - 2) * (order - 3)
    return (
        denominator * (left_stats.elementary[3] - right_stats.elementary[3])
        + transposition
        * (order - 2)
        * (order - 3)
        * (left_stats.edge_outside_e2_sum - right_stats.edge_outside_e2_sum)
        - three_cycle
        * (order - 3)
        * (left_stats.triangle_outside_degree_sum - right_stats.triangle_outside_degree_sum)
        + four_cycle * (left_stats.four_cycle_count - right_stats.four_cycle_count)
    )


def _pair_class(left: ComplementInvariants, right: ComplementInvariants) -> str:
    if left.edge_count != right.edge_count:
        return "q1"
    if left.degree_square_sum != right.degree_square_sum:
        return "q2"
    pattern = (
        left.degree_cube_sum - right.degree_cube_sum,
        left.triangle_count - right.triangle_count,
    )
    if pattern == (0, 0):
        return "q4"
    if pattern == (6, 1):
        return "endpoint"
    return "q3"


def _verify_deep_identities(
    graph_by_signature: dict[Signature, ComplementType],
) -> None:
    checks: dict[SignaturePair, tuple[str, int]] = {
        **{pair: ("p", multiplier) for pair, multiplier in P_PAIRS.items()},
        **{pair: ("q", multiplier) for pair, multiplier in Q_PAIRS.items()},
    }
    if len(checks) != 6:
        raise AssertionError("wrong deep-pair count")
    for pair, (kind, multiplier) in checks.items():
        left, right = (graph_by_signature[signature] for signature in pair)
        for order in range(20, 32):
            for hook_parameter in range(4):
                expected = multiplier * (
                    _p_polynomial(order, hook_parameter)
                    if kind == "p"
                    else (order - 3) * _q_polynomial(order, hook_parameter)
                )
                if _scaled_q4_difference(left, right, order, hook_parameter) != expected:
                    raise AssertionError("deep q4 polynomial identity changed")

    left, right = (graph_by_signature[signature] for signature in ENDPOINT_PAIR)
    for order in range(20, 32):
        denominator = (order - 1) * (order - 2) * (order - 3)
        for hook_parameter in (1, order):
            if _scaled_q4_difference(left, right, order, hook_parameter) != -denominator:
                raise AssertionError("endpoint q4 identity changed")


def _payload(
    invariants: tuple[ComplementInvariants, ...],
    classes: tuple[tuple[int, int, str], ...],
) -> dict[str, object]:
    return {
        "invariants": [
            {
                "signature": item.signature,
                "edges": item.edge_count,
                "s2": item.degree_square_sum,
                "s3": item.degree_cube_sum,
                "triangles": item.triangle_count,
            }
            for item in invariants
        ],
        "pairs": classes,
    }


def build_certificate() -> Certificate:
    graphs = complement_types()
    invariants = tuple(complement_invariants(graph) for graph in graphs)
    type_counts = dict(sorted(Counter(item.edge_count for item in invariants).items()))
    patterns: Counter[tuple[int, int]] = Counter()
    classes = []
    deep_pairs: set[SignaturePair] = set()
    endpoint_pairs: set[SignaturePair] = set()
    for left, right in combinations(range(len(graphs)), 2):
        left_invariant, right_invariant = invariants[left], invariants[right]
        pair_class = _pair_class(left_invariant, right_invariant)
        classes.append((left, right, pair_class))
        signature_pair = (left_invariant.signature, right_invariant.signature)
        if pair_class == "q4":
            deep_pairs.add(signature_pair)
        elif pair_class == "endpoint":
            endpoint_pairs.add(signature_pair)
        if pair_class in {"q3", "q4", "endpoint"}:
            patterns[
                (
                    left_invariant.degree_cube_sum - right_invariant.degree_cube_sum,
                    left_invariant.triangle_count - right_invariant.triangle_count,
                )
            ] += 1
    if deep_pairs != P_PAIRS.keys() | Q_PAIRS.keys():
        raise AssertionError("deep-pair identities do not cover the q4 class")
    if endpoint_pairs != {ENDPOINT_PAIR}:
        raise AssertionError("wrong endpoint pair")
    class_counts = dict(sorted(Counter(item[2] for item in classes).items()))
    payload = _payload(invariants, tuple(classes))
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    _verify_deep_identities({graph.signature: graph for graph in graphs})
    return Certificate(
        graphs,
        invariants,
        type_counts,
        dict(sorted(patterns.items())),
        class_counts,
        digest,
    )


def verify_certificate(certificate: Certificate) -> None:
    if certificate.type_counts != EXPECTED_TYPE_COUNTS:
        raise AssertionError("complement census changed")
    if certificate.pattern_counts != EXPECTED_PATTERN_COUNTS:
        raise AssertionError("q3 pattern table changed")
    if certificate.class_counts != EXPECTED_CLASS_COUNTS:
        raise AssertionError("pair classification changed")
    if EXPECTED_SHA256 and certificate.sha256 != EXPECTED_SHA256:
        raise AssertionError("certificate digest changed")
