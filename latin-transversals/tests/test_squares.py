import pytest

from latin_transversals.squares import Entry, Family, delta, forced_entries, is_latin, square
from latin_transversals.transversals import is_transversal


@pytest.mark.parametrize(
    ("family", "orders"),
    [(Family.G, [18, 22, 30, 38, 102]), (Family.H, [16, 28, 36, 100])],
)
def test_constructions_are_latin(family: Family, orders: list[int]) -> None:
    for n in orders:
        assert is_latin(square(family, n))


@pytest.mark.parametrize("family", [Family.G, Family.H])
def test_forced_entries_have_delta_three(family: Family) -> None:
    entries = forced_entries(family)
    n = 38 if family is Family.G else 36
    table = square(family, n)
    assert all(table[entry.row][entry.column] == entry.symbol for entry in entries)
    assert [delta(n, entry) for entry in entries] == [3, 3, 3]


def test_paper_g30_transversals_are_disjoint() -> None:
    table = square(Family.G, 30)
    first = (
        29,
        12,
        4,
        28,
        11,
        21,
        1,
        2,
        18,
        16,
        7,
        10,
        26,
        9,
        0,
        25,
        19,
        15,
        5,
        8,
        27,
        13,
        20,
        6,
        24,
        3,
        23,
        14,
        22,
        17,
    )
    second = (
        14,
        3,
        21,
        13,
        9,
        1,
        15,
        0,
        23,
        17,
        16,
        24,
        8,
        2,
        7,
        27,
        18,
        4,
        22,
        10,
        12,
        20,
        6,
        25,
        19,
        5,
        28,
        11,
        29,
        26,
    )
    assert is_transversal(table, first)
    assert is_transversal(table, second)
    assert not {Entry(row, first[row], table[row][first[row]]) for row in range(30)} & {
        Entry(row, second[row], table[row][second[row]]) for row in range(30)
    }
