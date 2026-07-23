from __future__ import annotations

from .automaton import automaton_digest, build_automaton, transfer_certificate
from .model import is_balanced, parse_coloring, separator_size

EXACT_MINIMA = (
    (9, 5),
    (10, 5),
    (11, 6),
    (12, 6),
    (13, 7),
    (14, 7),
    (15, 8),
    (16, 7),
    (17, 8),
    (18, 8),
    (19, 9),
    (20, 9),
    (21, 9),
    (22, 9),
)

N22_WORD = (
    "YB",
    "YB",
    "YB",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YB",
    "YB",
    "YB",
    "BY",
    "AA",
    "AA",
    "AA",
    "AB",
    "AA",
    "AA",
    "AA",
    "BY",
)

N23_WORD = (
    "AA",
    "AA",
    "AB",
    "BB",
    "YB",
    "YB",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YB",
    "YB",
    "YB",
    "BB",
    "AA",
    "AA",
    "AA",
    "AA",
)


def build_certificate() -> dict[str, object]:
    automaton = build_automaton()
    if len(automaton.states) != 1_481 or len(automaton.transitions) != 7_383:
        raise AssertionError("unexpected automaton dimensions")
    transfer = transfer_certificate(162, 9, automaton)
    observed = tuple((n, transfer.minimum_at(n)) for n, _ in EXACT_MINIMA)
    if observed != EXACT_MINIMA:
        raise AssertionError("small-order minima changed")
    if any(transfer.minimum_at(n) is not None for n in range(23, 163)):
        raise AssertionError("found a boundary-nine counterexample")

    n22 = parse_coloring(N22_WORD)
    n23 = parse_coloring(N23_WORD)
    if not is_balanced(n22) or separator_size(n22) != 9:
        raise AssertionError("invalid n=22 threshold witness")
    if not is_balanced(n23) or separator_size(n23) != 10:
        raise AssertionError("invalid n=23 equality witness")

    return {
        "theorem": (
            "Every n-vertex subset X of P(n,4), for n>=23, has at least "
            "10 vertices in X adjacent to its complement."
        ),
        "column_types": 7,
        "states": len(automaton.states),
        "transitions": len(automaton.transitions),
        "automaton_digest_sha256": automaton_digest(automaton),
        "accepting_state_digest_sha256": transfer.accepting_state_digest_sha256,
        "exact_minimum_boundary_9_through_22": {
            str(order): minimum for order, minimum in EXACT_MINIMA
        },
        "finite_excluded_range": [23, 162],
        "recurrence": {
            "starts_at": 163,
            "decrement": 2,
            "required_clean_run": 9,
        },
        "exact_threshold": 23,
        "n22_witness": list(N22_WORD),
        "n23_equality_witness": list(N23_WORD),
        "consequences": {
            "pathwidth_lower_bound": 10,
            "zero_forcing_lower_bound": 10,
            "orders": "n>=23",
        },
    }
