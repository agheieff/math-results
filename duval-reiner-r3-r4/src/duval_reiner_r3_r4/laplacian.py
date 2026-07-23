from __future__ import annotations

from functools import cache
from itertools import combinations

from .families import all_facets, selected_indices

IntegerMatrix = tuple[tuple[int, ...], ...]
BoundaryColumn = tuple[int, ...]


@cache
def boundary_columns(vertex_count: int) -> tuple[BoundaryColumn, ...]:
    ridges = tuple(combinations(range(vertex_count), 2))
    ridge_index = {ridge: index for index, ridge in enumerate(ridges)}
    columns = []
    for first, second, third in all_facets(vertex_count):
        column = [0] * len(ridges)
        column[ridge_index[(second, third)]] = 1
        column[ridge_index[(first, third)]] = -1
        column[ridge_index[(first, second)]] = 1
        columns.append(tuple(column))
    return tuple(columns)


def gram_matrix(vertex_count: int, mask: int) -> IntegerMatrix:
    columns = boundary_columns(vertex_count)
    selected = selected_indices(mask, len(columns))
    return tuple(
        tuple(
            sum(x * y for x, y in zip(columns[left], columns[right], strict=True))
            for right in selected
        )
        for left in selected
    )


def vertex_degrees(vertex_count: int, mask: int) -> tuple[int, ...]:
    facets = all_facets(vertex_count)
    selected = selected_indices(mask, len(facets))
    return tuple(
        sum(vertex in facets[index] for index in selected) for vertex in range(vertex_count)
    )


def partial_degree_sum(degrees: tuple[int, ...], index: int) -> int:
    if index < 1:
        raise ValueError("partial-sum index must be positive")
    return sum(min(degree, index) for degree in degrees)
