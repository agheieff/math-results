from fractions import Fraction

from signed_circulant_n24.exact import (
    SEPARATOR_DENOMINATOR,
    SEPARATOR_NUMERATOR,
    characteristic_polynomial,
    expected_extremal_polynomial,
    roots_between,
    verify_target_algebra,
)
from signed_circulant_n24.model import TARGET_MASKS, matrix_from_mask


def test_extremal_characteristic_polynomials() -> None:
    expected = expected_extremal_polynomial()
    assert all(
        characteristic_polynomial(matrix_from_mask(mask)) == expected for mask in TARGET_MASKS
    )


def test_target_algebra_and_sturm_isolation() -> None:
    verify_target_algebra()
    assert (
        roots_between(Fraction(7663, 1000), Fraction(SEPARATOR_NUMERATOR, SEPARATOR_DENOMINATOR))
        == 1
    )
