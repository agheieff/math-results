from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .field import ONE, ZERO
from .roots import ExactVector, h3_roots, squared_norm, vector_add, vector_negate

Edge = tuple[int, int, int]

H3_MATCHING: tuple[Edge, ...] = (
    (0, 10, 13),
    (1, 7, 8),
    (2, 16, 21),
    (3, 15, 18),
    (4, 23, 29),
    (5, 24, 26),
    (6, 17, 28),
    (9, 14, 27),
    (11, 20, 25),
    (12, 19, 22),
)

H3_INDEPENDENT_SET = (
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    18,
    19,
    20,
    21,
    26,
    27,
    28,
    29,
)


def zero_sum_edges_exact(points: tuple[ExactVector, ...]) -> tuple[Edge, ...]:
    edges: list[Edge] = []
    zero = (ZERO, ZERO, ZERO)
    for edge in combinations(range(len(points)), 3):
        total = vector_add(vector_add(points[edge[0]], points[edge[1]]), points[edge[2]])
        if total == zero:
            edges.append(edge)
    return tuple(edges)


@dataclass(frozen=True)
class H3Certificate:
    vertices: int
    zero_sum_triples: int
    independence_number: int
    matching: tuple[Edge, ...]
    independent_set: tuple[int, ...]


def certify_h3() -> H3Certificate:
    points = h3_roots()
    if len(points) != 30 or len(set(points)) != 30:
        raise AssertionError("H3 root enumeration is not simple")
    if any(squared_norm(point) != ONE for point in points):
        raise AssertionError("an H3 root is not normalized")
    point_set = set(points)
    if any(vector_negate(point) not in point_set for point in points):
        raise AssertionError("H3 roots are not antipodal")

    edges = zero_sum_edges_exact(points)
    edge_set = set(edges)
    if len(edges) != 20:
        raise AssertionError("unexpected H3 zero-sum triple count")
    if {sum(vertex in edge for edge in edges) for vertex in range(30)} != {2}:
        raise AssertionError("unexpected H3 triple degrees")

    if any(edge not in edge_set for edge in H3_MATCHING):
        raise AssertionError("matching contains a nonedge")
    matched_vertices = [vertex for edge in H3_MATCHING for vertex in edge]
    if len(set(matched_vertices)) != 30:
        raise AssertionError("the ten triples are not a perfect matching")

    independent = set(H3_INDEPENDENT_SET)
    if len(independent) != 20 or any(set(edge) <= independent for edge in edges):
        raise AssertionError("the claimed 20-set is not independent")

    return H3Certificate(30, 20, 20, H3_MATCHING, H3_INDEPENDENT_SET)
