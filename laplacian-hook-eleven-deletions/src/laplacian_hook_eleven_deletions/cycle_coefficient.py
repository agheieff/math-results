"""Generic exact coefficient formula from sparse-complement inclusion-exclusion."""

from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import combinations
from math import comb, factorial

from laplacian_hook_eleven_deletions.character import hook_character
from laplacian_hook_eleven_deletions.coefficients import elementary
from laplacian_hook_eleven_deletions.combinatorics import integer_partitions
from laplacian_hook_eleven_deletions.model import Edge, EdgeSet, adjacency_from_deleted


def _edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


@cache
def _moved_partitions(index: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        parts
        for support in range(2, index + 1)
        for parts in integer_partitions(support)
        if min(parts) >= 2
    )


@cache
def _pattern(parts: tuple[int, ...]) -> tuple[EdgeSet, tuple[int, ...]]:
    edges: set[Edge] = set()
    start = 0
    for length in parts:
        cycle = tuple(range(start, start + length))
        for position, vertex in enumerate(cycle):
            edges.add(_edge(vertex, cycle[(position + 1) % length]))
        start += length
    degrees = tuple(sum(vertex in edge for edge in edges) for vertex in range(sum(parts)))
    return frozenset(edges), degrees


@cache
def _embedding_count(required: EdgeSet, parts: tuple[int, ...]) -> int:
    """Count injective edge-preserving maps from ``required`` into the pattern."""
    if not required:
        return 1
    pattern_edges, pattern_degrees = _pattern(parts)
    vertices = tuple(sorted({vertex for edge in required for vertex in edge}))
    required_neighbors = {
        vertex: frozenset(
            other for edge in required if vertex in edge for other in edge if other != vertex
        )
        for vertex in vertices
    }
    ordered = tuple(sorted(vertices, key=lambda vertex: (-len(required_neighbors[vertex]), vertex)))
    candidates = {
        vertex: tuple(
            target
            for target, degree in enumerate(pattern_degrees)
            if degree >= len(required_neighbors[vertex])
        )
        for vertex in vertices
    }
    assignment: dict[int, int] = {}
    used: set[int] = set()

    def visit(position: int) -> int:
        if position == len(ordered):
            return 1
        vertex = ordered[position]
        total = 0
        for target in candidates[vertex]:
            if target in used or any(
                neighbor in assignment and _edge(target, assignment[neighbor]) not in pattern_edges
                for neighbor in required_neighbors[vertex]
            ):
                continue
            assignment[vertex] = target
            used.add(target)
            total += visit(position + 1)
            used.remove(target)
            del assignment[vertex]
        return total

    return visit(0)


def _orientation_divisor(parts: tuple[int, ...]) -> int:
    divisor = 1
    for length in parts:
        divisor *= 2 if length == 2 else length
    for multiplicity in Counter(parts).values():
        divisor *= factorial(multiplicity)
    return divisor


def _choose(total: int, degree: int) -> int:
    return 0 if degree < 0 or total < degree else comb(total, degree)


@cache
def _degree_sequence(deleted: EdgeSet, order: int) -> tuple[int, ...]:
    return tuple(sum(row) for row in adjacency_from_deleted(deleted, order))


def _outside_elementary(
    global_values: tuple[int, ...],
    degrees: tuple[int, ...],
    vertices: tuple[int, ...],
    degree: int,
) -> int:
    values = list(global_values)
    for vertex in vertices:
        removed = [1] + [0] * degree
        for index in range(1, degree + 1):
            removed[index] = values[index] - degrees[vertex] * removed[index - 1]
        values = removed
    return values[degree]


@cache
def _weighted_cycle_covers(
    deleted: EdgeSet,
    order: int,
    parts: tuple[int, ...],
    outside_degree: int,
) -> int:
    """Sum outside elementary degree weights over oriented covers of ``parts``."""
    support = sum(parts)
    degrees = _degree_sequence(deleted, order)
    global_values = tuple(elementary(degrees, degree) for degree in range(outside_degree + 1))
    missing = tuple(sorted(deleted))
    total = 0
    for size in range(len(missing) + 1):
        sign = -1 if size % 2 else 1
        for chosen in combinations(missing, size):
            required = frozenset(chosen)
            vertices = tuple(sorted({vertex for edge in required for vertex in edge}))
            vertex_count = len(vertices)
            if vertex_count > support:
                continue
            embedding_count = _embedding_count(required, parts)
            if not embedding_count:
                continue
            remaining = support - vertex_count
            total += (
                sign
                * embedding_count
                * factorial(remaining)
                * _choose(order - vertex_count - outside_degree, remaining)
                * _outside_elementary(global_values, degrees, vertices, outside_degree)
            )
    quotient, remainder = divmod(total, _orientation_divisor(parts))
    if remainder:
        raise ArithmeticError("nonintegral oriented cycle-cover weight")
    return quotient


@cache
def normalized_coefficient(deleted: EdgeSet, order: int, index: int) -> Fraction:
    """Return the normalized exceptional-hook coefficient ``q_index``."""
    if index < 1 or index > order:
        raise ValueError("coefficient index outside matrix order")
    degrees = _degree_sequence(deleted, order)
    rank = (order - 1) // 2
    dimension = comb(order - 1, rank)
    result = Fraction((-1) ** index * elementary(degrees, index))
    for parts in _moved_partitions(index):
        support = sum(parts)
        cycles = (*parts, *(1 for _ in range(order - support)))
        ratio = Fraction(hook_character(cycles, rank), dimension)
        if not ratio:
            continue
        weight = _weighted_cycle_covers(deleted, order, parts, index - support)
        result += (-1) ** (index - support) * ratio * weight
    return result
