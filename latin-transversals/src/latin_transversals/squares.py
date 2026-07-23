"""The two near-cyclic constructions in arXiv:2607.17547v1."""

from collections.abc import Callable
from enum import StrEnum
from typing import NamedTuple


class Family(StrEnum):
    G = "G"
    H = "H"


class Entry(NamedTuple):
    row: int
    column: int
    symbol: int


Square = tuple[tuple[int, ...], ...]


def _g_offset(n: int, row: int, column: int) -> int:
    k = (n - 2) // 4
    if row in {0, 5, 10} and column % 4 == 1 and column > row + 1:
        return 4
    if (row, column) in {(5, 3), (10, 3), (10, 7)}:
        return 4
    if (row, column) in {(1, 2), (6, 6), (11, 10)}:
        return 3
    if (row, column) in {
        (0, 3),
        (0, 4),
        (5, 7),
        (5, 8),
        (10, 11),
        (10, 12),
        (15, 12),
        (15, 13),
        (16, 12),
    }:
        return 1
    if (row, column) in {
        (1, 3),
        (1, 4),
        (1, 5),
        (6, 7),
        (6, 8),
        (6, 9),
        (11, 11),
        (11, 12),
        (11, 13),
        (16, 13),
    }:
        return -1
    if (row, column) in {(4, 2), (4, 5), (9, 6), (9, 9), (14, 10), (14, 13)}:
        return -3
    if row in {4, 9, 14} and column % 4 == 1 and column > row + 1:
        return -4
    if (row, column) in {(9, 3), (14, 3), (14, 7)}:
        return -4
    if row == 15 and column % 2 == 0 and column != 12:
        return 2
    if row == 17 and column % 2 == 0:
        return -2
    if 18 <= row < 3 * k - 9 and row % 3 == 0 and column % 2 == 0:
        return 2
    if 18 <= row < 3 * k - 9 and row % 3 == 2 and column % 2 == 0:
        return -2
    return 0


def _h_offset(n: int, row: int, column: int) -> int:
    if row in {0, 5, 10} and column % 4 == 1 and column - 4 * row // 5 != 1:
        return 4
    if (row, column) in {(1, 1), (6, 5), (11, 9)}:
        return 3
    if row in {0, 5, 10} and 1 <= column - 4 * row // 5 <= 4:
        return 1
    if row in {1, 6, 11} and 2 <= column - 4 * (row - 1) // 5 <= 4:
        return -1
    if row in {4, 9, 14} and column % 4 == 1:
        return -4
    if 15 <= row < n - 21 and row % 4 == 3 and column % 2 == 0:
        return 2
    if 15 <= row < n - 21 and row % 4 == 1 and column % 2 == 0:
        return -2
    return 0


def _validate_order(family: Family, n: int) -> None:
    if family is Family.G and (n < 18 or n % 4 != 2):
        raise ValueError("G_n requires n = 4k + 2 with k >= 4")
    if family is Family.H and (n < 16 or n % 4 != 0):
        raise ValueError("H_n requires n = 4k with k >= 4")


def offset_function(family: Family, n: int) -> Callable[[int, int], int]:
    _validate_order(family, n)
    return lambda row, column: (
        _g_offset(n, row, column) if family is Family.G else _h_offset(n, row, column)
    )


def square(family: Family, n: int) -> Square:
    offset = offset_function(family, n)
    return tuple(
        tuple((row + column + offset(row, column)) % n for column in range(n)) for row in range(n)
    )


def delta(n: int, entry: Entry) -> int:
    """Return the paper's representative in (-n/2, n/2]."""
    residue = (entry.symbol - entry.row - entry.column) % n
    return residue - n if residue > n // 2 else residue


def forced_entries(family: Family) -> tuple[Entry, Entry, Entry]:
    if family is Family.G:
        return (Entry(1, 2, 6), Entry(6, 6, 15), Entry(11, 10, 24))
    return (Entry(1, 1, 5), Entry(6, 5, 14), Entry(11, 9, 23))


def is_latin(table: Square) -> bool:
    n = len(table)
    expected = set(range(n))
    return all(set(row) == expected for row in table) and all(
        {table[row][column] for row in range(n)} == expected for column in range(n)
    )
