"""Exact hook characters needed by the first four coefficients."""

from __future__ import annotations

import math
from fractions import Fraction


def _comb(top: int, bottom: int) -> int:
    if bottom < 0 or bottom > top:
        return 0
    return math.comb(top, bottom)


def hook_character_product(cycle_lengths: tuple[int, ...], rank: int) -> int:
    """Extract a hook character from the exterior-power generating product."""

    order = sum(cycle_lengths)
    if any(length <= 0 for length in cycle_lengths):
        raise ValueError("cycle lengths must be positive")
    if rank < 0 or rank >= order:
        raise ValueError("invalid exterior rank")
    numerator = [0] * (rank + 1)
    numerator[0] = 1
    for length in cycle_lengths:
        sign = (-1) ** (length + 1)
        for degree in range(rank, length - 1, -1):
            numerator[degree] += sign * numerator[degree - length]
    quotient = [0] * (rank + 1)
    quotient[0] = numerator[0]
    for degree in range(1, rank + 1):
        quotient[degree] = numerator[degree] - quotient[degree - 1]
    return quotient[rank]


def character_ratios(order: int, hook_parameter: int) -> tuple[Fraction, ...]:
    """Return chi(2), 2chi(3), 2chi(4), chi(2,2), normalized by chi(1)."""

    if order < 5 or not 1 <= hook_parameter <= order:
        raise ValueError("invalid order or hook parameter")
    k = hook_parameter
    dimension = math.comb(order - 1, k - 1)
    numerators = (
        _comb(order - 2, k - 2) - _comb(order - 2, k - 1),
        2 * (_comb(order - 4, k - 4) + _comb(order - 4, k - 1)),
        2 * (_comb(order - 5, k - 5) - _comb(order - 5, k - 1)),
        _comb(order - 5, k - 5) - 2 * _comb(order - 5, k - 3) + _comb(order - 5, k - 1),
    )
    return tuple(Fraction(value, dimension) for value in numerators)


def scaled_character_numerators(order: int, hook_parameter: int) -> tuple[int, int, int]:
    """Return numerators over n-1, (n-1)_2, and (n-1)_3."""

    n, k = order, hook_parameter
    transposition = 2 * k - n - 1
    three_cycle = 2 * (3 * k**2 - 3 * k * n - 3 * k + n**2 + 2)
    four_cycle = 2 * transposition * (2 * k**2 - 2 * k * n - 2 * k + n**2 - 3 * n + 6)
    return transposition, three_cycle, four_cycle
