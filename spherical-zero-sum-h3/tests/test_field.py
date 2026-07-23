from fractions import Fraction

from spherical_zero_sum_h3.field import ONE, PHI, QPhi


def test_golden_ratio_relation() -> None:
    assert PHI * PHI == PHI + ONE
    assert (PHI - ONE) * PHI == ONE
    assert QPhi(Fraction(3, 2), Fraction(-2, 3)).scale(Fraction(6)) == QPhi(
        Fraction(9),
        Fraction(-4),
    )
