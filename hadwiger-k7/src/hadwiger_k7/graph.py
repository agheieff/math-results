import json
from collections.abc import Iterator
from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations

type Edge = tuple[int, int]


@dataclass(frozen=True)
class Graph:
    order: int
    edges: frozenset[Edge]

    def __post_init__(self) -> None:
        if self.order < 0:
            raise ValueError("negative graph order")
        if any(not (0 <= left < right < self.order) for left, right in self.edges):
            raise ValueError("edges must be normalized, loopless, and in range")

    def with_added_edges(self, edges: tuple[Edge, ...]) -> "Graph":
        return Graph(self.order, self.edges | frozenset(edges))


def canonical_bytes(graph: Graph) -> bytes:
    payload = {
        "edges": [list(edge) for edge in sorted(graph.edges)],
        "order": graph.order,
    }
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()


def graph_sha256(graph: Graph) -> str:
    return sha256(canonical_bytes(graph)).hexdigest()


def degrees(graph: Graph) -> tuple[int, ...]:
    values = [0] * graph.order
    for left, right in graph.edges:
        values[left] += 1
        values[right] += 1
    return tuple(values)


def is_clique(graph: Graph, vertices: tuple[int, ...]) -> bool:
    return all((left, right) in graph.edges for left, right in combinations(vertices, 2))


def is_independent(graph: Graph, vertices: tuple[int, ...]) -> bool:
    return all((left, right) not in graph.edges for left, right in combinations(vertices, 2))


def independent_sets(graph: Graph, size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        vertices
        for vertices in combinations(range(graph.order), size)
        if is_independent(graph, vertices)
    )


def missing_edge_matchings(
    graph: Graph,
    allowed_vertices: tuple[int, ...],
) -> Iterator[tuple[Edge, ...]]:
    missing = tuple(edge for edge in combinations(allowed_vertices, 2) if edge not in graph.edges)
    yield from _matching_suffix(missing, 0, 0)


def _matching_suffix(
    edges: tuple[Edge, ...],
    start: int,
    used_vertices: int,
) -> Iterator[tuple[Edge, ...]]:
    yield ()
    for index in range(start, len(edges)):
        edge = edges[index]
        endpoints = (1 << edge[0]) | (1 << edge[1])
        if endpoints & used_vertices:
            continue
        for suffix in _matching_suffix(edges, index + 1, used_vertices | endpoints):
            yield (edge, *suffix)
