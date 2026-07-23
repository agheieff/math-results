from __future__ import annotations

from enum import IntEnum

from .graph import GeneralizedPetersen, internal_boundary


class Color(IntEnum):
    A = 0
    B = 1
    Y = 2


Column = tuple[Color, Color]
Coloring = tuple[Column, ...]


def compatible(first: Color, second: Color) -> bool:
    return {first, second} != {Color.A, Color.Y}


def has_no_a_y_edge(coloring: Coloring) -> bool:
    n = len(coloring)
    if n < 7:
        raise ValueError("P(n,3) requires n at least seven")
    for index, (outer, inner) in enumerate(coloring):
        if not compatible(outer, inner):
            return False
        if not compatible(outer, coloring[(index + 1) % n][0]):
            return False
        if not compatible(inner, coloring[(index + 3) % n][1]):
            return False
    return True


def is_balanced_separator_coloring(coloring: Coloring) -> bool:
    n = len(coloring)
    flattened = tuple(color for column in coloring for color in column)
    b_count = flattened.count(Color.B)
    return (
        has_no_a_y_edge(coloring)
        and flattened.count(Color.Y) == n
        and flattened.count(Color.A) == n - b_count
    )


def coloring_from_subset(graph: GeneralizedPetersen, subset: int) -> Coloring:
    if subset.bit_count() != graph.n:
        raise ValueError("subset must contain exactly n vertices")
    boundary = internal_boundary(graph, subset)

    def color(vertex: int) -> Color:
        if not subset >> vertex & 1:
            return Color.Y
        return Color.B if boundary >> vertex & 1 else Color.A

    coloring = tuple((color(index), color(graph.n + index)) for index in range(graph.n))
    if not is_balanced_separator_coloring(coloring):
        raise AssertionError("subset did not produce a valid separator coloring")
    return coloring


def subset_from_coloring(coloring: Coloring) -> int:
    if not is_balanced_separator_coloring(coloring):
        raise ValueError("coloring is not balanced and edge-compatible")
    n = len(coloring)
    subset = 0
    for index, column in enumerate(coloring):
        if column[0] != Color.Y:
            subset |= 1 << index
        if column[1] != Color.Y:
            subset |= 1 << (n + index)
    return subset


def separator_size(coloring: Coloring) -> int:
    return sum(color == Color.B for column in coloring for color in column)


def clean_runs(coloring: Coloring, color: Color) -> tuple[tuple[int, int], ...]:
    if color == Color.B:
        raise ValueError("a clean run must have color A or Y")
    target = (color, color)
    n = len(coloring)
    if all(column == target for column in coloring):
        return ((0, n),)
    runs = []
    for start, column in enumerate(coloring):
        if column != target or coloring[(start - 1) % n] == target:
            continue
        length = 0
        while length < n and coloring[(start + length) % n] == target:
            length += 1
        runs.append((start, length))
    return tuple(runs)


def delete_clean_run_center(coloring: Coloring, color: Color) -> Coloring:
    run = next(
        ((start, length) for start, length in clean_runs(coloring, color) if length >= 7),
        None,
    )
    if run is None:
        raise ValueError("no clean run of length at least seven")
    index = (run[0] + 3) % len(coloring)
    reduced = coloring[:index] + coloring[index + 1 :]
    if not has_no_a_y_edge(reduced):
        raise AssertionError("clean-run deletion introduced an A-Y edge")
    return reduced


def pump_down(coloring: Coloring) -> Coloring:
    if not is_balanced_separator_coloring(coloring):
        raise ValueError("coloring is not a balanced separator")
    b_count = separator_size(coloring)
    reduced = delete_clean_run_center(coloring, Color.A)
    reduced = delete_clean_run_center(reduced, Color.Y)
    if not is_balanced_separator_coloring(reduced):
        raise AssertionError("paired clean-run deletion did not preserve balance")
    if separator_size(reduced) != b_count:
        raise AssertionError("paired clean-run deletion changed the separator")
    return reduced
