from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction

from .model import MycielskiCycle


def q4_certificate_matrix() -> tuple[tuple[int, ...], ...]:
    """Return the integral q=4 matrix [[C,C,0],[C,0,1],[0,1^T,-2]]."""
    graph = MycielskiCycle.build(4)
    rows = [[0] * graph.vertex_count for _ in range(graph.vertex_count)]

    for index in range(4):
        for neighbor in ((index - 1) % 4, (index + 1) % 4):
            rows[index][neighbor] = 1
            rows[index][4 + neighbor] = 1
            rows[4 + index][neighbor] = 1
        rows[4 + index][8] = 1
        rows[8][4 + index] = 1
    rows[8][8] = -2
    return tuple(tuple(row) for row in rows)


def q5_certificate_matrix() -> tuple[tuple[int, ...], ...]:
    """Return the q=5 certificate, where (a,b,f)=(1,-1,1)."""
    graph = MycielskiCycle.build(5)
    size = graph.vertex_count
    rows = [[0] * size for _ in range(size)]

    for index in range(5):
        rows[index][index] = 1
        rows[5 + index][5 + index] = 1
        rows[index][(index - 1) % 5] = -1
        rows[index][(index + 1) % 5] = -1
        rows[index][5 + (index - 1) % 5] = 1
        rows[index][5 + (index + 1) % 5] = 1
        rows[5 + index][(index - 1) % 5] = 1
        rows[5 + index][(index + 1) % 5] = 1
        rows[5 + index][10] = 1
        rows[10][5 + index] = 1
    rows[10][10] = 1
    return tuple(tuple(row) for row in rows)


def rational_rank(rows: Sequence[Sequence[int]]) -> int:
    """Compute matrix rank by exact Gaussian elimination over Q."""
    if not rows:
        return 0
    width = len(rows[0])
    matrix = [[Fraction(entry) for entry in row] for row in rows]
    rank = 0

    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        for row in range(rank + 1, len(matrix)):
            if not matrix[row][column]:
                continue
            factor = matrix[row][column] / pivot_value
            for inner_column in range(column, width):
                matrix[row][inner_column] -= factor * matrix[rank][inner_column]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def has_graph_support(graph: MycielskiCycle, rows: Sequence[Sequence[int]]) -> bool:
    for left in range(graph.vertex_count):
        for right in range(left + 1, graph.vertex_count):
            is_edge = bool(graph.adjacency[left] & (1 << right))
            if bool(rows[left][right]) != is_edge:
                return False
            if rows[left][right] != rows[right][left]:
                return False
    return True
