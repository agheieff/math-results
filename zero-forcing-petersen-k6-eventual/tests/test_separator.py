from zero_forcing_petersen_k6_eventual.certificate import EXPECTED_CLOSURES, ISOLATED_ORDER
from zero_forcing_petersen_k6_eventual.separator import run_separator_dp, transcript_digest


def test_native_controls_and_six_negative_bases() -> None:
    result = run_separator_dp()
    assert result.closure_counts == EXPECTED_CLOSURES
    assert result.orders[1] == ISOLATED_ORDER
    assert result.closure_counts[1] == 0
    assert result.closure_counts[2] > 0
    assert result.closure_counts[3:] == (0, 0, 0, 0, 0, 0)
    assert len(transcript_digest(result)) == 64
