"""Exact component-multiset census for complements with at most five edges."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from itertools import combinations, permutations

Edge = tuple[int, int]


@dataclass(frozen=True, order=True)
class Component:
    vertex_count: int
    edge_mask: int

    @property
    def edge_count(self) -> int:
        return self.edge_mask.bit_count()


@dataclass(frozen=True)
class ComplementType:
    components: tuple[Component, ...]
    edges: tuple[Edge, ...]
    vertex_count: int

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @property
    def signature(self) -> tuple[tuple[int, int], ...]:
        return tuple((item.vertex_count, item.edge_mask) for item in self.components)


@cache
def complete_edges(vertex_count: int) -> tuple[Edge, ...]:
    return tuple(combinations(range(vertex_count), 2))


@cache
def edge_indices(vertex_count: int) -> dict[Edge, int]:
    return {edge: index for index, edge in enumerate(complete_edges(vertex_count))}


def mask_edges(vertex_count: int, mask: int) -> tuple[Edge, ...]:
    return tuple(
        edge for index, edge in enumerate(complete_edges(vertex_count)) if mask >> index & 1
    )


@cache
def permutation_actions(vertex_count: int) -> tuple[tuple[int, ...], ...]:
    indices = edge_indices(vertex_count)
    actions = []
    for permutation in permutations(range(vertex_count)):
        action = []
        for left, right in complete_edges(vertex_count):
            image_left, image_right = sorted((permutation[left], permutation[right]))
            action.append(indices[(image_left, image_right)])
        actions.append(tuple(action))
    return tuple(actions)


def transform_mask(mask: int, action: tuple[int, ...]) -> int:
    transformed = 0
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        transformed |= 1 << action[bit.bit_length() - 1]
        remaining -= bit
    return transformed


def canonical_mask(vertex_count: int, mask: int) -> int:
    return min(transform_mask(mask, action) for action in permutation_actions(vertex_count))


def is_connected(vertex_count: int, mask: int) -> bool:
    adjacency = [0] * vertex_count
    for index, (left, right) in enumerate(complete_edges(vertex_count)):
        if mask >> index & 1:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    reached = 1
    while True:
        expanded = reached
        for vertex in range(vertex_count):
            if reached >> vertex & 1:
                expanded |= adjacency[vertex]
        if expanded == reached:
            return reached == (1 << vertex_count) - 1
        reached = expanded


@cache
def connected_types(max_edges: int = 5) -> tuple[Component, ...]:
    representatives: set[Component] = set()
    for vertex_count in range(2, max_edges + 2):
        universe_size = len(complete_edges(vertex_count))
        for edge_count in range(vertex_count - 1, min(max_edges, universe_size) + 1):
            for chosen in combinations(range(universe_size), edge_count):
                mask = sum(1 << index for index in chosen)
                if is_connected(vertex_count, mask):
                    representatives.add(Component(vertex_count, canonical_mask(vertex_count, mask)))
    return tuple(
        sorted(
            representatives,
            key=lambda item: (item.edge_count, item.vertex_count, item.edge_mask),
        )
    )


def _embed(components: tuple[Component, ...]) -> ComplementType:
    offset = 0
    edges: list[Edge] = []
    for component in components:
        edges.extend(
            (offset + left, offset + right)
            for left, right in mask_edges(component.vertex_count, component.edge_mask)
        )
        offset += component.vertex_count
    return ComplementType(components, tuple(edges), offset)


@cache
def complement_types(max_edges: int = 5) -> tuple[ComplementType, ...]:
    if max_edges < 0:
        raise ValueError("maximum edge count must be nonnegative")
    types = connected_types(max_edges)
    result: list[ComplementType] = []

    def visit(
        start: int,
        remaining_vertices: int,
        remaining_edges: int,
        chosen: tuple[Component, ...],
    ) -> None:
        result.append(_embed(chosen))
        for index in range(start, len(types)):
            component = types[index]
            if (
                component.vertex_count <= remaining_vertices
                and component.edge_count <= remaining_edges
            ):
                visit(
                    index,
                    remaining_vertices - component.vertex_count,
                    remaining_edges - component.edge_count,
                    chosen + (component,),
                )

    visit(0, 2 * max_edges, max_edges, ())
    return tuple(sorted(result, key=lambda graph: (graph.edge_count, graph.signature)))
