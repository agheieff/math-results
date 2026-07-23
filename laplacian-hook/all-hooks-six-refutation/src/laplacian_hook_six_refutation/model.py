"""Sparse witnesses and their dense complements."""

from collections.abc import Sequence
from dataclasses import dataclass

Edge = tuple[int, int]
EdgeSet = frozenset[Edge]
Matrix = tuple[tuple[int, ...], ...]
Polynomial = tuple[int, ...]  # Descending coefficients.


@dataclass(frozen=True)
class Witness:
    key: str
    edges: EdgeSet

    @property
    def support(self) -> int:
        return len({vertex for edge in self.edges for vertex in edge})


def normalize_edges(edges: Sequence[Edge]) -> EdgeSet:
    normalized: set[Edge] = set()
    for left, right in edges:
        if left < 0 or right < 0 or left == right:
            raise ValueError("edges must have distinct nonnegative endpoints")
        normalized.add((left, right) if left < right else (right, left))
    if len(normalized) != len(edges):
        raise ValueError("edges must be distinct")
    return frozenset(normalized)


def sparse_laplacian(edges: EdgeSet, order: int) -> Matrix:
    if any(vertex >= order for edge in edges for vertex in edge):
        raise ValueError("sparse graph does not embed at this order")
    adjacency = [[0] * order for _ in range(order)]
    for left, right in edges:
        adjacency[left][right] = 1
        adjacency[right][left] = 1
    degrees = tuple(sum(row) for row in adjacency)
    return tuple(
        tuple(degrees[row] if row == column else -adjacency[row][column] for column in range(order))
        for row in range(order)
    )


def dense_complement_laplacian(edges: EdgeSet, order: int) -> Matrix:
    sparse = sparse_laplacian(edges, order)
    return tuple(
        tuple(
            order - 1 - sparse[row][row]
            if row == column
            else (-1 if sparse[row][column] == 0 else 0)
            for column in range(order)
        )
        for row in range(order)
    )
