from __future__ import annotations

from enum import IntEnum


class Color(IntEnum):
    A = 0
    B = 1
    Y = 2


Column = tuple[Color, Color]
Coloring = tuple[Column, ...]


def compatible(left: Color, right: Color) -> bool:
    return {left, right} != {Color.A, Color.Y}


COLUMNS: tuple[Column, ...] = tuple(
    (outer, inner) for outer in Color for inner in Color if compatible(outer, inner)
)


def parse_coloring(words: tuple[str, ...]) -> Coloring:
    lookup = {"A": Color.A, "B": Color.B, "Y": Color.Y}
    if any(len(word) != 2 or any(symbol not in lookup for symbol in word) for word in words):
        raise ValueError("invalid column word")
    return tuple((lookup[word[0]], lookup[word[1]]) for word in words)


def has_no_a_y_edge(coloring: Coloring, step: int = 4) -> bool:
    n = len(coloring)
    if n < 2 * step + 1:
        raise ValueError("require n >= 2k+1")
    return all(
        compatible(outer, inner)
        and compatible(outer, coloring[(index + 1) % n][0])
        and compatible(inner, coloring[(index + step) % n][1])
        for index, (outer, inner) in enumerate(coloring)
    )


def separator_size(coloring: Coloring) -> int:
    return sum(color == Color.B for column in coloring for color in column)


def is_balanced(coloring: Coloring) -> bool:
    n = len(coloring)
    flattened = tuple(color for column in coloring for color in column)
    b_count = flattened.count(Color.B)
    return (
        has_no_a_y_edge(coloring)
        and flattened.count(Color.Y) == n
        and flattened.count(Color.A) == n - b_count
    )


def clean_runs(coloring: Coloring, color: Color) -> tuple[tuple[int, int], ...]:
    if color == Color.B:
        raise ValueError("clean runs have color A or Y")
    target = (color, color)
    n = len(coloring)
    if all(column == target for column in coloring):
        return ((0, n),)
    runs: list[tuple[int, int]] = []
    for start, column in enumerate(coloring):
        if column != target or coloring[(start - 1) % n] == target:
            continue
        length = 0
        while length < n and coloring[(start + length) % n] == target:
            length += 1
        runs.append((start, length))
    return tuple(runs)


def delete_clean_center(coloring: Coloring, color: Color) -> Coloring:
    run = next((run for run in clean_runs(coloring, color) if run[1] >= 9), None)
    if run is None:
        raise ValueError("no clean run of length at least nine")
    index = (run[0] + 4) % len(coloring)
    reduced = coloring[:index] + coloring[index + 1 :]
    if not has_no_a_y_edge(reduced):
        raise AssertionError("clean deletion introduced an A-Y edge")
    return reduced


def pump_down(coloring: Coloring) -> Coloring:
    if not is_balanced(coloring):
        raise ValueError("coloring is not balanced")
    b_count = separator_size(coloring)
    reduced = delete_clean_center(coloring, Color.A)
    reduced = delete_clean_center(reduced, Color.Y)
    if not is_balanced(reduced) or separator_size(reduced) != b_count:
        raise AssertionError("paired deletion did not preserve the separator constraints")
    return reduced
