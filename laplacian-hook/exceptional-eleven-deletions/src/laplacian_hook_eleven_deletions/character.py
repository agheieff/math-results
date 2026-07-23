"""Exterior-power character checks through eight moved points."""

from fractions import Fraction
from math import comb


def hook_character(cycles: tuple[int, ...], rank: int) -> int:
    numerator = [1] + [0] * rank
    for length in cycles:
        if length <= rank:
            coefficient = (-1) ** (length + 1)
            for degree in range(rank, length - 1, -1):
                numerator[degree] += coefficient * numerator[degree - length]
    quotient = [0] * (rank + 1)
    quotient[0] = 1
    for degree in range(1, rank + 1):
        quotient[degree] = numerator[degree] - quotient[degree - 1]
    return quotient[rank]


def character_ratios(order: int) -> dict[str, Fraction]:
    rank = (order - 1) // 2
    dimension = comb(order - 1, rank)

    def ratio(parts: tuple[int, ...], orientations: int = 1) -> Fraction:
        cycles = (*parts, *(1 for _ in range(order - sum(parts))))
        return orientations * Fraction(hook_character(cycles, rank), dimension)

    return {
        "33": ratio((3, 3), 4),
        "42": ratio((4, 2), 2),
        "6": ratio((6,)),
        "222": ratio((2, 2, 2)),
        "7": ratio((7,), 2),
        "322": ratio((3, 2, 2), 2),
        "43": ratio((4, 3), 2),
        "52": ratio((5, 2), 2),
        "8": ratio((8,)),
        "62": ratio((6, 2)),
        "53": ratio((5, 3)),
        "44": ratio((4, 4)),
        "422": ratio((4, 2, 2)),
        "332": ratio((3, 3, 2)),
        "2222": ratio((2, 2, 2, 2)),
    }


def expected_character_ratios(order: int) -> dict[str, Fraction]:
    return {
        "33": Fraction(order**2 - 12 * order + 59, 4 * (order - 4) * (order - 2)),
        "42": Fraction(-(order - 7), (order - 4) * (order - 2)),
        "6": Fraction(0),
        "222": Fraction(0),
        "7": Fraction(
            (order - 13) * (order - 11) * (order - 9),
            32 * (order - 6) * (order - 4) * (order - 2),
        ),
        "322": Fraction(-(order - 13), 2 * (order - 4) * (order - 2)),
        "43": Fraction(0),
        "52": Fraction(0),
        "8": Fraction(0),
        "62": Fraction(
            -3 * (order - 9) * (order - 11),
            16 * (order - 6) * (order - 4) * (order - 2),
        ),
        "53": Fraction(
            (order - 9) * (order**2 - 16 * order + 135),
            64 * (order - 6) * (order - 4) * (order - 2),
        ),
        "44": Fraction(
            -(order**2 - 16 * order + 75),
            4 * (order - 6) * (order - 4) * (order - 2),
        ),
        "422": Fraction(0),
        "332": Fraction(0),
        "2222": Fraction(3, (order - 4) * (order - 2)),
    }
