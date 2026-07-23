"""Six-column topological-minor reduction."""

from __future__ import annotations

from .graph import Edge, _edge, edges


def reduced_edges(n: int) -> frozenset[Edge]:
    if n < 19:
        raise ValueError("require n at least nineteen")
    target_n = n - 6
    deleted = {_edge(index, n + index) for index in range(target_n, n)}

    def image(vertex: int) -> int:
        if vertex < n:
            return target_n - 1 if vertex >= target_n else vertex
        index = vertex - n
        if index >= target_n:
            index -= target_n
        return target_n + index

    result = {
        _edge(image(left), image(right))
        for left, right in edges(n) - deleted
        if image(left) != image(right)
    }
    return frozenset(result)


def residue_base(n: int) -> int:
    if n < 37:
        raise ValueError("eventual theorem starts at n=37")
    return 37 + ((n - 37) % 6)
