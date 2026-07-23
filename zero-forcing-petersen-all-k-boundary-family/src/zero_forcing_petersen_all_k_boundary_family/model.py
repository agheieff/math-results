"""Generalized Petersen adjacency and internal boundary."""

from __future__ import annotations


def adjacency(n: int, k: int) -> tuple[int, ...]:
    if k < 1 or n < 2 * k + 1:
        raise ValueError("require k>=1 and n>=2k+1")
    result = [0] * (2 * n)

    def add(left: int, right: int) -> None:
        result[left] |= 1 << right
        result[right] |= 1 << left

    for index in range(n):
        add(index, (index + 1) % n)
        add(index, n + index)
        add(n + index, n + ((index + k) % n))
    frozen = tuple(result)
    if any(neighbors.bit_count() != 3 for neighbors in frozen):
        raise AssertionError("graph is not simple cubic")
    return frozen


def internal_boundary(graph: tuple[int, ...], subset: int) -> int:
    full = (1 << len(graph)) - 1
    if subset < 0 or subset & ~full:
        raise ValueError("subset is outside the graph")
    boundary = 0
    remaining = subset
    while remaining:
        bit = remaining & -remaining
        remaining -= bit
        vertex = bit.bit_length() - 1
        if graph[vertex] & ~subset:
            boundary |= bit
    return boundary
