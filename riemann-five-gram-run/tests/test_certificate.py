from decimal import Decimal
from pathlib import Path

from riemann_five_gram_run.certificate import verify_certificate
from riemann_five_gram_run.theta import height_with_offset, theta_over_pi

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_witness() -> None:
    result = verify_certificate(ROOT / "artifacts" / "witness.json")
    assert result.sign_pattern == "+-+-+"
    assert len(result.gram_indices) == 5
    assert result.left_margin > Decimal("0.25")
    assert result.right_margin > Decimal("0.39")


def test_theta_is_monotone_across_witness() -> None:
    base = Decimal("10121598453421191913984785")
    left = theta_over_pi(height_with_offset(base, Decimal("20.3667281680")))
    right = theta_over_pi(height_with_offset(base, Decimal("20.8915047612")))
    assert Decimal("4.65") < right - left < Decimal("4.66")
