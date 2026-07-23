from decimal import Decimal
from pathlib import Path

from riemann_nonzero_run_refutation.certificate import signs, verify_certificate
from riemann_nonzero_run_refutation.theta import height_with_offset, theta_over_pi

ROOT = Path(__file__).resolve().parents[1]


def test_certificate() -> None:
    result = verify_certificate(ROOT / "artifacts" / "witness.json")
    assert result.sign_pattern == "+-+-"
    assert len(result.gram_indices) == 4
    assert result.left_margin > Decimal("0.38")
    assert result.right_margin > Decimal("0.21")


def test_sign_rule() -> None:
    assert signs((19, 20, 21, 22), Decimal("-46")) == "+-+-"
    assert signs((18, 19, 20, 21), Decimal("-46")) == "-+-+"


def test_theta_is_monotone_across_witness() -> None:
    base = Decimal("1e25")
    left = theta_over_pi(height_with_offset(base, Decimal("24742.820054547281038548")))
    right = theta_over_pi(height_with_offset(base, Decimal("24743.226032454997212501")))
    assert Decimal("3.6") < right - left < Decimal("3.61")
