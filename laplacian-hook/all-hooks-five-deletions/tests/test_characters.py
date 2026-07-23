from fractions import Fraction
from math import comb

from laplacian_hook_all.characters import character_ratios, hook_character_product


def test_closed_ratios_match_exterior_power_characters() -> None:
    for order in range(8, 18):
        for hook_parameter in range(1, order + 1):
            rank = order - hook_parameter
            dimension = comb(order - 1, rank)
            cycles = (
                (2, *(1 for _ in range(order - 2))),
                (3, *(1 for _ in range(order - 3))),
                (4, *(1 for _ in range(order - 4))),
                (2, 2, *(1 for _ in range(order - 4))),
            )
            multipliers = (1, 2, 2, 1)
            expected = tuple(
                Fraction(multiplier * hook_character_product(cycle, rank), dimension)
                for cycle, multiplier in zip(cycles, multipliers, strict=True)
            )
            assert character_ratios(order, hook_parameter) == expected
