from zero_forcing_petersen_k7_eventual.certificate import (
    EXPECTED_CLOSURES,
    POSITIVE_CONTROLS,
    ZERO_ORDERS,
)
from zero_forcing_petersen_k7_eventual.separator import run_separator_dp, transcript_digest


def test_native_controls_and_exact_orders() -> None:
    result = run_separator_dp()
    assert result.closure_counts == EXPECTED_CLOSURES
    closure_exists = dict(
        zip(result.orders, (count > 0 for count in result.closure_counts), strict=True)
    )
    assert all(closure_exists[n] for n in POSITIVE_CONTROLS)
    assert all(not closure_exists[n] for n in ZERO_ORDERS)
    assert len(transcript_digest(result)) == 64
