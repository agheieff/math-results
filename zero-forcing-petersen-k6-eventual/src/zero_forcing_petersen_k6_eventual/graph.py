"""Bitset model of P(n,6)."""

from __future__ import annotations

Edge = tuple[int, int]


def _edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def edges(n: int) -> frozenset[Edge]:
    if n < 13:
        raise ValueError("P(n,6) requires n at least thirteen")
    result: set[Edge] = set()
    for index in range(n):
        result.add(_edge(index, (index + 1) % n))
        result.add(_edge(index, n + index))
        result.add(_edge(n + index, n + ((index + 6) % n)))
    if len(result) != 3 * n:
        raise AssertionError("P(n,6) is not simple cubic")
    return frozenset(result)


def adjacency(n: int) -> tuple[int, ...]:
    result = [0] * (2 * n)
    for left, right in edges(n):
        result[left] |= 1 << right
        result[right] |= 1 << left
    frozen = tuple(result)
    if any(neighbors.bit_count() != 3 for neighbors in frozen):
        raise AssertionError("P(n,6) is not cubic")
    return frozen


def internal_boundary(n: int, subset: int) -> int:
    graph = adjacency(n)
    full = (1 << (2 * n)) - 1
    if subset < 0 or subset & ~full:
        raise ValueError("subset is outside the graph")
    result = 0
    remaining = subset
    while remaining:
        bit = remaining & -remaining
        remaining -= bit
        vertex = bit.bit_length() - 1
        if graph[vertex] & ~subset:
            result |= bit
    return result


def vertex_name(n: int, vertex: int) -> str:
    return f"{'u' if vertex < n else 'v'}_{vertex % n}"
