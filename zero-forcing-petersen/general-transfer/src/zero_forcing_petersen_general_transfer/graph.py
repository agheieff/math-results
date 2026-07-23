"""Bitset model of P(n,k)."""

from __future__ import annotations

Vertex = tuple[str, int]
Edge = tuple[Vertex, Vertex]


def validate_parameters(n: int, k: int) -> None:
    if k < 1 or n < 2 * k + 1:
        raise ValueError("require k >= 1 and n >= 2k+1")


def _edge(left: Vertex, right: Vertex) -> Edge:
    return (left, right) if left < right else (right, left)


def petersen_edges(n: int, k: int) -> frozenset[Edge]:
    validate_parameters(n, k)
    edges: set[Edge] = set()
    for index in range(n):
        edges.add(_edge(("u", index), ("u", (index + 1) % n)))
        edges.add(_edge(("u", index), ("v", index)))
        edges.add(_edge(("v", index), ("v", (index + k) % n)))
    if len(edges) != 3 * n:
        raise AssertionError("P(n,k) construction is not simple cubic")
    return frozenset(edges)


def petersen_adjacency(n: int, k: int) -> tuple[int, ...]:
    validate_parameters(n, k)
    adjacency = [0] * (2 * n)

    def add(left: int, right: int) -> None:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left

    for index in range(n):
        add(index, (index + 1) % n)
        add(index, n + index)
        add(n + index, n + ((index + k) % n))
    result = tuple(adjacency)
    if any(neighbors.bit_count() != 3 for neighbors in result):
        raise AssertionError("P(n,k) adjacency is not cubic")
    return result


def vertex_id(n: int, vertex: Vertex) -> int:
    layer, index = vertex
    if layer not in {"u", "v"} or not 0 <= index < n:
        raise ValueError("invalid vertex")
    return index + (n if layer == "v" else 0)


def vertex_name(vertex: Vertex) -> str:
    return f"{vertex[0]}_{vertex[1]}"
