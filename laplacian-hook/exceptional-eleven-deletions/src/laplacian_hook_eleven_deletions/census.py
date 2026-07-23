"""Fast degree-cell augmentation and independent Burnside averaging."""

from collections import Counter
from functools import cache
from math import factorial

import pynauty  # type: ignore[import-untyped]

from laplacian_hook_eleven_deletions.combinatorics import integer_partitions
from laplacian_hook_eleven_deletions.model import (
    MAX_DELETIONS,
    REFERENCE_EDGES,
    REFERENCE_ORDER,
    ComponentKey,
    EdgeSet,
    GraphKey,
)


@cache
def component_key(vertices: frozenset[int], edges: EdgeSet) -> ComponentKey:
    ordered_vertices = tuple(sorted(vertices))
    relabel = {vertex: index for index, vertex in enumerate(ordered_vertices)}
    adjacency: dict[int, list[int]] = {index: [] for index in range(len(vertices))}
    local_edges: set[tuple[int, int]] = set()
    for left, right in edges:
        local_left = relabel[left]
        local_right = relabel[right]
        adjacency[local_left].append(local_right)
        adjacency[local_right].append(local_left)
        local_edges.add((min(local_left, local_right), max(local_left, local_right)))
    graph = pynauty.Graph(
        number_of_vertices=len(vertices),
        directed=False,
        adjacency_dict=adjacency,
    )
    canonical_order = tuple(int(vertex) for vertex in pynauty.canon_label(graph))
    code = 0
    bit = 0
    for left in range(len(canonical_order)):
        for right in range(left + 1, len(canonical_order)):
            edge = (
                min(canonical_order[left], canonical_order[right]),
                max(canonical_order[left], canonical_order[right]),
            )
            if edge in local_edges:
                code |= 1 << bit
            bit += 1
    return len(vertices), code


def graph_key(edges: EdgeSet) -> GraphKey:
    adjacency = [set[int]() for _ in range(REFERENCE_ORDER)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = {vertex for vertex in range(REFERENCE_ORDER) if adjacency[vertex]}
    output: list[ComponentKey] = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        stack = [root]
        vertices: set[int] = set()
        while stack:
            vertex = stack.pop()
            vertices.add(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
        frozen_vertices = frozenset(vertices)
        component_edges = frozenset(
            edge for edge in edges if edge[0] in frozen_vertices and edge[1] in frozen_vertices
        )
        output.append(component_key(frozen_vertices, component_edges))
    return tuple(sorted(output))


def format_graph_key(key: GraphKey) -> str:
    return "empty" if not key else "-".join(f"v{o}e{code:x}" for o, code in key)


@cache
def augmentation_census() -> tuple[dict[GraphKey, EdgeSet], ...]:
    levels: list[dict[GraphKey, EdgeSet]] = [{(): frozenset()}]
    for _ in range(MAX_DELETIONS):
        next_level: dict[GraphKey, EdgeSet] = {}
        for representative in levels[-1].values():
            for edge in REFERENCE_EDGES:
                if edge not in representative:
                    candidate = representative | {edge}
                    next_level.setdefault(graph_key(candidate), candidate)
        levels.append(next_level)
    return tuple(levels)


def feasible_census(order: int) -> tuple[dict[GraphKey, EdgeSet], ...]:
    return tuple(
        {
            key: representative
            for key, representative in level.items()
            if sum(component_order for component_order, _ in key) <= order
        }
        for level in augmentation_census()
    )


def _cycle_representative(parts: tuple[int, ...], order: int) -> tuple[int, ...]:
    permutation = list(range(order))
    start = 0
    for length in parts:
        cycle = tuple(range(start, start + length))
        for index, vertex in enumerate(cycle):
            permutation[vertex] = cycle[(index + 1) % length]
        start += length
    return tuple(permutation)


def _edge_orbits(permutation: tuple[int, ...]) -> tuple[int, ...]:
    edges = tuple(
        (left, right)
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    edge_index = {edge: index for index, edge in enumerate(edges)}
    action = [
        edge_index[
            (
                min(permutation[left], permutation[right]),
                max(permutation[left], permutation[right]),
            )
        ]
        for left, right in edges
    ]
    seen: set[int] = set()
    lengths: list[int] = []
    for root in range(len(edges)):
        if root in seen:
            continue
        value = root
        length = 0
        while value not in seen:
            seen.add(value)
            value = action[value]
            length += 1
        lengths.append(length)
    return tuple(lengths)


def _class_size(parts: tuple[int, ...], order: int) -> int:
    centralizer = 1
    for length, count in Counter(parts).items():
        centralizer *= length**count * factorial(count)
    return factorial(order) // centralizer


@cache
def burnside_census(order: int = REFERENCE_ORDER) -> tuple[int, ...]:
    fixed = [0] * (MAX_DELETIONS + 1)
    for parts in integer_partitions(order):
        coefficients = [1] + [0] * MAX_DELETIONS
        for length in _edge_orbits(_cycle_representative(parts, order)):
            for edge_count in range(MAX_DELETIONS, length - 1, -1):
                coefficients[edge_count] += coefficients[edge_count - length]
        weight = _class_size(parts, order)
        for edge_count, coefficient in enumerate(coefficients):
            fixed[edge_count] += weight * coefficient
    result = []
    for value in fixed:
        quotient, remainder = divmod(value, factorial(order))
        if remainder:
            raise ArithmeticError("nonintegral Burnside average")
        result.append(quotient)
    return tuple(result)
