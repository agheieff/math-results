from latin_transversals.squares import Entry, Family, delta, forced_entries, square
from latin_transversals.transversals import entries, is_transversal

COLUMNS = (
    21,
    29,
    18,
    28,
    19,
    17,
    6,
    15,
    8,
    24,
    33,
    10,
    16,
    14,
    35,
    13,
    27,
    31,
    37,
    32,
    26,
    36,
    23,
    9,
    20,
    34,
    30,
    25,
    22,
    12,
    4,
    11,
    3,
    7,
    5,
    1,
    2,
    0,
)


def test_g38_transversal_refutes_forced_fourth_entry_claim() -> None:
    table = square(Family.G, 38)
    selected = entries(table, COLUMNS)
    first, second, third = forced_entries(Family.G)

    assert is_transversal(table, COLUMNS)
    assert first not in selected
    assert second in selected
    assert third in selected
    assert Entry(16, 12, 29) not in selected
    assert [
        (entry.row, entry.column, delta(38, entry)) for entry in selected if delta(38, entry)
    ] == [
        (0, 21, 4),
        (5, 17, 4),
        (6, 6, 3),
        (10, 33, 4),
        (11, 10, 3),
        (15, 13, 1),
    ]
    assert sum(delta(38, entry) for entry in selected) == 19
