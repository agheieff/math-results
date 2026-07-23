from __future__ import annotations

from dataclasses import dataclass

from .automaton import automaton_digest, build_automaton, transfer_certificate
from .graph import GeneralizedPetersen, internal_boundary

FINITE_START = 17
FINITE_END = 98
RECURRENCE_START = 99
MAX_SEPARATOR = 7

N16_WITNESS_NAMES = (
    "u2",
    "u3",
    "u4",
    "u5",
    "u6",
    "u7",
    "u8",
    "v0",
    "v1",
    "v3",
    "v4",
    "v5",
    "v6",
    "v7",
    "v9",
    "v10",
)


@dataclass(frozen=True)
class SeparatorCertificate:
    column_types: int
    states: int
    transitions: int
    automaton_digest_sha256: str
    accepting_state_digest_sha256: str
    exact_minima_7_through_16: tuple[tuple[int, int], ...]
    excluded_range: tuple[int, int]
    recurrence_start: int
    recurrence_decrement: int
    threshold: int
    n16_witness: tuple[str, ...]
    n16_boundary: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "theorem": (
                "Every n-vertex subset X of P(n,3), for n >= 17, has at least "
                "8 vertices in X adjacent to its complement."
            ),
            "column_types": self.column_types,
            "states": self.states,
            "transitions": self.transitions,
            "automaton_digest_sha256": self.automaton_digest_sha256,
            "accepting_state_digest_sha256": self.accepting_state_digest_sha256,
            "exact_minimum_boundary_7_through_16": {
                str(order): minimum for order, minimum in self.exact_minima_7_through_16
            },
            "finite_excluded_range": list(self.excluded_range),
            "recurrence": {
                "starts_at": self.recurrence_start,
                "decrement": self.recurrence_decrement,
            },
            "exact_threshold": self.threshold,
            "n16_counterexample": {
                "subset": list(self.n16_witness),
                "boundary": list(self.n16_boundary),
            },
            "consequences": {
                "pathwidth_lower_bound": 8,
                "zero_forcing_lower_bound": 8,
                "orders": "n >= 17",
            },
        }


def _mask_from_names(graph: GeneralizedPetersen, names: tuple[str, ...]) -> int:
    mask = 0
    for name in names:
        layer = name[0]
        index = int(name[1:])
        if layer not in {"u", "v"} or not 0 <= index < graph.n:
            raise ValueError(f"invalid vertex name: {name}")
        vertex = index if layer == "u" else graph.n + index
        mask |= 1 << vertex
    return mask


def certify_separator_theorem() -> SeparatorCertificate:
    automaton = build_automaton()
    if len(automaton.states) != 247 or len(automaton.transitions) != 1_233:
        raise AssertionError("unexpected transfer automaton size")

    transfer = transfer_certificate(FINITE_END, MAX_SEPARATOR, automaton)
    expected_minima = (
        (7, 5),
        (8, 5),
        (9, 5),
        (10, 6),
        (11, 6),
        (12, 6),
        (13, 7),
        (14, 7),
        (15, 7),
        (16, 7),
    )
    observed_minima = tuple(
        (order, minimum)
        for order in range(7, FINITE_START)
        if (minimum := transfer.minimum_at(order)) is not None
    )
    if observed_minima != expected_minima:
        raise AssertionError("small-order separator minima changed")
    if any(transfer.minimum_at(order) is not None for order in range(FINITE_START, FINITE_END + 1)):
        raise AssertionError("finite transfer found a boundary-seven counterexample")

    graph = GeneralizedPetersen(16)
    witness = _mask_from_names(graph, N16_WITNESS_NAMES)
    boundary = internal_boundary(graph, witness)
    if witness.bit_count() != graph.n or boundary.bit_count() != 7:
        raise AssertionError("n=16 threshold witness is invalid")
    boundary_names = tuple(
        graph.vertex_name(vertex) for vertex in range(graph.order) if boundary >> vertex & 1
    )

    return SeparatorCertificate(
        7,
        len(automaton.states),
        len(automaton.transitions),
        automaton_digest(automaton),
        transfer.accepting_state_digest_sha256,
        expected_minima,
        (FINITE_START, FINITE_END),
        RECURRENCE_START,
        2,
        FINITE_START,
        N16_WITNESS_NAMES,
        boundary_names,
    )
