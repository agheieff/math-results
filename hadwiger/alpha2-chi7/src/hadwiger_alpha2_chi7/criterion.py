from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from itertools import combinations, permutations

from hadwiger_alpha2_chi7.graph import Edge, Graph


@dataclass(frozen=True)
class Seagull:
    endpoints: Edge
    middle: int

    @property
    def vertices(self) -> tuple[int, int, int]:
        return (self.endpoints[0], self.middle, self.endpoints[1])


def matchings(
    graph: Graph,
    vertices: tuple[int, ...],
    size: int,
) -> Iterator[tuple[Edge, ...]]:
    if size == 0:
        yield ()
        return
    if len(vertices) < 2 * size:
        return
    first = vertices[0]
    rest = vertices[1:]
    yield from matchings(graph, rest, size)
    for index, neighbor in enumerate(rest):
        if not graph.has_edge(first, neighbor):
            continue
        remaining = rest[:index] + rest[index + 1 :]
        for matching in matchings(graph, remaining, size - 1):
            yield ((first, neighbor), *matching)


def perfect_matchings(graph: Graph, vertices: tuple[int, ...]) -> Iterator[tuple[Edge, ...]]:
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, neighbor in enumerate(vertices[1:]):
        if not graph.has_edge(first, neighbor):
            continue
        remaining = vertices[1 : index + 1] + vertices[index + 2 :]
        for matching in perfect_matchings(graph, remaining):
            yield ((first, neighbor), *matching)


def find_seagull_factor(
    complement: Graph,
    singleton_clique: tuple[int, int, int, int],
) -> tuple[Seagull, Seagull, Seagull] | None:
    if not complement.is_independent(singleton_clique):
        raise ValueError("the four singleton branch sets must be a clique in the original graph")
    outside = tuple(vertex for vertex in complement.vertices if vertex not in singleton_clique)
    if len(outside) != 9:
        raise ValueError("the criterion is frozen at 13 vertices")

    for matching in matchings(complement, outside, 3):
        endpoints = {vertex for edge in matching for vertex in edge}
        unmatched = tuple(vertex for vertex in outside if vertex not in endpoints)
        for assigned in permutations(unmatched):
            if all(
                not complement.has_edge(middle, left) and not complement.has_edge(middle, right)
                for (left, right), middle in zip(matching, assigned, strict=True)
            ):
                return tuple(
                    Seagull(edge, middle) for edge, middle in zip(matching, assigned, strict=True)
                )  # type: ignore[return-value]
    return None


def branch_sets(
    singleton_clique: tuple[int, int, int, int],
    seagulls: tuple[Seagull, Seagull, Seagull],
) -> tuple[tuple[int, ...], ...]:
    return tuple((vertex,) for vertex in singleton_clique) + tuple(
        seagull.vertices for seagull in seagulls
    )


def is_clique_model(graph: Graph, model: tuple[tuple[int, ...], ...]) -> bool:
    used: set[int] = set()
    for branch_set in model:
        if not branch_set or used.intersection(branch_set):
            return False
        if not graph.connected_on(branch_set):
            return False
        used.update(branch_set)
    return all(
        graph.adjacent_sets(model[left], model[right])
        for left, right in combinations(range(len(model)), 2)
    )


def find_clique4_seagull_model(
    complement: Graph,
) -> tuple[tuple[int, ...], ...] | None:
    original = complement.complement()
    for singleton_clique in combinations(complement.vertices, 4):
        if not complement.is_independent(singleton_clique):
            continue
        factor = find_seagull_factor(complement, singleton_clique)
        if factor is None:
            continue
        model = branch_sets(singleton_clique, factor)
        if not is_clique_model(original, model):
            raise AssertionError("the complement criterion produced an invalid model")
        return model
    return None


def find_six_pair_cover_model(
    graph: Graph,
) -> tuple[int, tuple[Edge, ...]] | None:
    if graph.order != 13:
        raise ValueError("the six-pair criterion is frozen at 13 vertices")
    for singleton in graph.vertices:
        remaining = tuple(vertex for vertex in graph.vertices if vertex != singleton)
        for matching in perfect_matchings(graph, remaining):
            if not all(
                graph.adjacent_sets(edge, other) for edge, other in combinations(matching, 2)
            ):
                continue
            if not all(graph.adjacent_sets((singleton,), edge) for edge in matching):
                continue
            return singleton, matching
    return None
