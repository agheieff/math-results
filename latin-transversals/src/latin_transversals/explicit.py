"""Explicit transversals in H_{4k} for odd k >= 9.

A donor cycle ``(r_0, ..., r_m)`` means that row ``r_i`` receives the base
column of ``r_{i+1}``, with indices taken cyclically.
"""

from collections.abc import Sequence
from typing import Literal

from latin_transversals.squares import Entry, Family, forced_entries, offset_function

type Omitted = Literal[0, 1, 2]
type Cycle = tuple[int, ...]


def h_base_columns(k: int, *, phase: int = 0) -> tuple[int, ...]:
    """Return c_0, or its column translate c_0 + 4*phase."""
    n = 4 * k
    offsets = (1, 6, -2, 3)
    return tuple((row + offsets[row % 4] + 4 * phase) % n for row in range(n))


def _apply_cycles(base: Sequence[int], cycles: Sequence[Cycle]) -> tuple[int, ...]:
    columns = list(base)
    for cycle in cycles:
        for index, row in enumerate(cycle):
            donor = cycle[(index + 1) % len(cycle)]
            columns[row] = base[donor]
    return tuple(columns)


def _uniform_a_cycles(k: int) -> tuple[Cycle, ...]:
    n = 4 * k
    middle = (
        (2 * k + 5, 2 * k + 8, 2 * k + 6, 2 * k + 9)
        if k % 4 == 1
        else (2 * k + 8, 2 * k + 10, 2 * k + 9, 2 * k + 12)
    )
    return (
        (0, n - 4, n - 15, n - 17, n - 8, n - 19, n - 21, n - 12, 6, 4, n - 7, n - 1, 14, 5),
        (8, 10, 12, 11),
        middle,
    )


def _uniform_b_cycles(k: int) -> tuple[Cycle, ...]:
    n = 4 * k
    if k % 4 == 1:
        return (
            (
                0,
                4,
                3,
                10,
                16,
                11,
                8,
                5,
                12,
                6,
                n - 4,
                n - 15,
                n - 9,
                n - 16,
                n - 19,
                n - 21,
                n - 12,
                1,
            ),
            (2 * k + 2, 2 * k + 8, 2 * k + 12, 2 * k + 13, 2 * k + 9, 2 * k + 16, 2 * k + 11),
        )
    return (
        (0, 4, 7, 14, 5, n - 4, n - 15, n - 9, n - 16, n - 19, n - 21, n - 12, 1),
        (2, 3),
        (8, 10, 12, 11),
        (2 * k - 1, 2 * k + 2, 2 * k + 4, 2 * k + 6, 2 * k + 9, 2 * k + 8),
    )


def _uniform_c_cycles(k: int) -> tuple[Cycle, ...]:
    n = 4 * k
    return (
        (
            0,
            n - 4,
            n - 15,
            n - 17,
            n - 8,
            n - 19,
            n - 21,
            n - 12,
            6,
            4,
            n - 7,
            n - 1,
            5,
            8,
            10,
            12,
            1,
        ),
        (2 * k + 2, 2 * k + 8),
    )


_FINITE_A: dict[int, tuple[Cycle, ...]] = {
    9: ((0, 16, 5), (4, 21, 27, 18, 31, 10, 20, 11, 8, 6), (23, 26, 28)),
    11: ((0, 32, 1, 11, 8, 2, 24, 35, 30, 27, 6, 4, 39, 10, 40, 5),),
    13: ((0, 32, 35, 6, 4, 5), (8, 10, 40, 34, 44, 33, 11), (22, 48, 43)),
    15: ((0, 40, 53, 51, 38, 52, 55, 26, 44, 5), (4, 11, 8, 10, 48, 6)),
}

_FINITE_B: dict[int, tuple[Cycle, ...]] = {
    9: ((0, 20, 31, 12, 9, 19, 2, 4, 5, 28, 1), (8, 11), (10, 24, 30, 16)),
    11: ((0, 36, 23, 4, 9, 27, 24, 1), (5, 20, 33, 11, 8, 10, 40), (32, 38)),
    13: ((0, 28, 5, 36, 43, 16, 45, 31, 42, 40, 1), (4, 11, 8, 10, 48, 50)),
    15: ((0, 4, 47, 10, 56, 3, 26, 52, 5, 40, 1), (2, 11, 8), (32, 43, 58)),
    17: ((0, 36, 43, 59, 42, 55, 20, 66, 48, 1), (4, 11, 8, 13, 63, 10), (5, 52)),
}


def h_phase_zero_transversal(k: int, omitted: Omitted) -> tuple[int, ...]:
    """A transversal omitting one of A, B, C for every odd k >= 9."""
    if k < 9 or k % 2 == 0:
        raise ValueError("the explicit H-family formulas require odd k >= 9")
    if omitted == 0:
        cycles = _FINITE_A.get(k, _uniform_a_cycles(k))
    elif omitted == 1:
        cycles = _FINITE_B.get(k, _uniform_b_cycles(k))
    else:
        cycles = _uniform_c_cycles(k)
    return _apply_cycles(h_base_columns(k), cycles)


def h_phase_one_transversal(k: int) -> tuple[int, ...]:
    """The phase-(+4) transversal omitting A, valid for every odd k >= 9."""
    if k < 9 or k % 2 == 0:
        raise ValueError("the explicit H-family formulas require odd k >= 9")
    n = 4 * k
    first = (
        (0, n - 12, n - 21, n - 14, n - 8, n - 17, n - 10, n - 4, 6)
        if k % 4 == 1
        else (0, n - 12, n - 21, n - 14, n - 16, n - 9, n - 10, n - 4, 6)
    )
    second = (4, 14, 5, 8, n - 3, n - 5, 10, 12, 11)
    return _apply_cycles(h_base_columns(k, phase=1), (first, second))


def h_witnesses(k: int) -> tuple[tuple[int, ...], ...]:
    """Four transversals with empty intersection."""
    return (
        h_phase_zero_transversal(k, 0),
        h_phase_zero_transversal(k, 1),
        h_phase_zero_transversal(k, 2),
        h_phase_one_transversal(k),
    )


def h_target_delta(k: int, omitted: Omitted, row: int) -> int:
    n = 4 * k
    forced_rows = (1, 6, 11)
    if row in {0, 5, 10}:
        return 4
    if row in forced_rows:
        return 0 if row == forced_rows[omitted] else 3
    if 15 <= row < n - 21 and row % 4 == 3:
        return 2
    return 0


def verify_h_transversal(k: int, columns: Sequence[int], omitted: Omitted) -> bool:
    n = 4 * k
    if len(columns) != n or set(columns) != set(range(n)):
        return False
    offset = offset_function(Family.H, n)
    symbols = {(row + column + offset(row, column)) % n for row, column in enumerate(columns)}
    if len(symbols) != n:
        return False
    if any(
        offset(row, column) != h_target_delta(k, omitted, row) for row, column in enumerate(columns)
    ):
        return False
    for index, entry in enumerate(forced_entries(Family.H)):
        if index != omitted and columns[entry.row] != entry.column:
            return False
    return (
        columns[forced_entries(Family.H)[omitted].row] != forced_entries(Family.H)[omitted].column
    )


def common_entries(k: int, transversals: Sequence[Sequence[int]]) -> frozenset[Entry]:
    n = 4 * k
    offset = offset_function(Family.H, n)
    return frozenset(
        Entry(
            row,
            transversals[0][row],
            (row + transversals[0][row] + offset(row, transversals[0][row])) % n,
        )
        for row in range(n)
        if all(columns[row] == transversals[0][row] for columns in transversals[1:])
    )
