from collections.abc import Iterable
from itertools import combinations

from .model import MycielskiPath

Force = tuple[int, int]


def vertex_mask(vertices: Iterable[int]) -> int:
    mask = 0
    for vertex in vertices:
        mask |= 1 << vertex
    return mask


def closure_mask(graph: MycielskiPath, initial: int) -> int:
    black = initial
    changed = True
    while changed:
        changed = False
        for source, neighbors in enumerate(graph.adjacency):
            if not black & (1 << source):
                continue
            white = neighbors & ~black
            if white and not white & (white - 1):
                black |= white
                changed = True
    return black


def forcing_witness(graph: MycielskiPath) -> tuple[int, int, int]:
    return graph.original(0), graph.original(1), graph.shadow(0)


def forcing_sequence(graph: MycielskiPath) -> tuple[Force, ...]:
    forces = [
        (graph.original(0), graph.shadow(1)),
        (graph.shadow(0), graph.apex),
        (graph.shadow(1), graph.original(2)),
        (graph.original(1), graph.shadow(2)),
    ]
    for index in range(2, graph.order - 1):
        forces.append((graph.shadow(index), graph.original(index + 1)))
        forces.append((graph.original(index), graph.shadow(index + 1)))
    return tuple(forces)


def replay_forces(graph: MycielskiPath) -> int:
    black = vertex_mask(forcing_witness(graph))
    for source, target in forcing_sequence(graph):
        white = graph.adjacency[source] & ~black
        if white != 1 << target:
            raise AssertionError(f"invalid force {source}->{target}")
        black |= 1 << target
    return black


def maximum_two_set_closure(graph: MycielskiPath) -> int:
    return max(
        closure_mask(graph, vertex_mask(initial)).bit_count()
        for initial in combinations(range(graph.vertex_count), 2)
    )
