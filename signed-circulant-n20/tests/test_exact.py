from fractions import Fraction

from signed_circulant.exact import (
    characteristic_polynomial,
    expected_extremal_polynomial,
    roots_between,
    verify_target_isolation,
)
from signed_circulant.model import TARGET_MASKS, matrix_from_mask


def test_extremal_characteristic_polynomials() -> None:
    expected = expected_extremal_polynomial()
    assert all(
        characteristic_polynomial(matrix_from_mask(mask)) == expected for mask in TARGET_MASKS
    )


def test_sturm_isolation() -> None:
    verify_target_isolation()
    assert roots_between(Fraction(7), Fraction(8)) == 1
