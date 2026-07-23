from fractions import Fraction

from laplacian_hook_eleven_deletions.coefficients import (
    normalized_seventh_coefficient,
    normalized_sixth_coefficient,
)
from laplacian_hook_eleven_deletions.cycle_coefficient import normalized_coefficient

PAIR_ONE = (
    frozenset(
        {
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 4),
            (1, 5),
            (2, 6),
            (2, 7),
            (4, 6),
            (5, 8),
            (7, 8),
            (8, 9),
        }
    ),
    frozenset(
        {
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 4),
            (1, 5),
            (2, 6),
            (2, 7),
            (3, 8),
            (4, 8),
            (6, 9),
            (8, 9),
        }
    ),
)


def test_generic_cycle_formula() -> None:
    for deleted in (frozenset(), frozenset({(0, 1)}), *PAIR_ONE):
        assert normalized_coefficient(deleted, 23, 6) == normalized_sixth_coefficient(
            deleted,
            23,
        )
        assert normalized_coefficient(deleted, 23, 7) == normalized_seventh_coefficient(
            deleted,
            23,
        )
    assert normalized_coefficient(PAIR_ONE[0], 23, 8) - normalized_coefficient(
        PAIR_ONE[1], 23, 8
    ) == Fraction(-3251, 13566)
