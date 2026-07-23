from zero_forcing_petersen_k5_eventual.separator import (
    run_separator_dp,
    transcript_digest,
)


def test_native_positive_and_negative_controls() -> None:
    results = run_separator_dp((28, 29))
    assert results[0].counterexample
    assert not results[1].counterexample
    assert results[0].layer_counts[-1] > 0
    assert results[1].layer_counts[-1] == 0
    assert len(transcript_digest(results)) == 64
