from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from itertools import combinations
from math import comb

from .model import MycielskiCycle

Force = tuple[int, int]


def vertex_mask(vertices: Iterable[int]) -> int:
    result = 0
    for vertex in vertices:
        result |= 1 << vertex
    return result


def closure_mask(graph: MycielskiCycle, initial: int) -> int:
    """Return the zero-forcing closure of an initial bitset."""
    black = initial
    changed = True
    while changed:
        changed = False
        for source, neighbors in enumerate(graph.adjacency):
            if not black & (1 << source):
                continue
            white = neighbors & ~black
            if white and white & (white - 1) == 0:
                black |= white
                changed = True
    return black


def forcing_witness(graph: MycielskiCycle) -> tuple[int, ...]:
    return (
        graph.original(0),
        graph.original(1),
        graph.original(2),
        graph.shadow(0),
        graph.shadow(1),
    )


def explicit_forcing_sequence(graph: MycielskiCycle) -> tuple[Force, ...]:
    forces = [
        (graph.original(1), graph.shadow(2)),
        (graph.shadow(1), graph.apex),
        (graph.shadow(0), graph.original(-1)),
        (graph.original(0), graph.shadow(-1)),
    ]
    for index in range(2, graph.order - 2):
        forces.append((graph.shadow(index), graph.original(index + 1)))
        forces.append((graph.original(index), graph.shadow(index + 1)))
    return tuple(forces)


def replay_forces(
    graph: MycielskiCycle,
    initial_vertices: Iterable[int],
    forces: Iterable[Force],
) -> int:
    """Replay a chronological list, rejecting the first invalid force."""
    black = vertex_mask(initial_vertices)
    for source, target in forces:
        if not black & (1 << source):
            raise ValueError(f"white source in force {source}->{target}")
        white = graph.adjacency[source] & ~black
        if white != 1 << target:
            raise ValueError(f"invalid force {source}->{target}")
        black |= 1 << target
    return black


@dataclass(frozen=True)
class ExhaustionResult:
    order: int
    checked: int
    maximum_closure: int
    maximizing_set: tuple[int, ...]


def exhaust_four_sets(graph: MycielskiCycle) -> ExhaustionResult:
    """Exhaust all four-vertex sets and record the largest closure."""
    best_size = -1
    best_set: tuple[int, ...] = ()
    checked = 0
    for initial in combinations(range(graph.vertex_count), 4):
        checked += 1
        size = closure_mask(graph, vertex_mask(initial)).bit_count()
        if size > best_size:
            best_size = size
            best_set = initial

    if checked != comb(graph.vertex_count, 4):
        raise AssertionError("incomplete exhaustion")
    return ExhaustionResult(graph.order, checked, best_size, best_set)
