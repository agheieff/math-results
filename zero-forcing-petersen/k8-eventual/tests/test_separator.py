from zero_forcing_petersen_k8_eventual.certificate import (
    EXPECTED_CLOSURES,
    EXPECTED_TRANSCRIPT_SHA256,
)
from zero_forcing_petersen_k8_eventual.separator import (
    frozen_separator_run,
    native_source_digest,
    transcript_digest,
)


def test_frozen_exact_transcript() -> None:
    result = frozen_separator_run()
    assert result.closure_counts == EXPECTED_CLOSURES
    assert transcript_digest(result) == EXPECTED_TRANSCRIPT_SHA256
    assert max(result.layer_counts) == 2_638_499_949
    assert native_source_digest() == (
        "b010841c02bd630f87d9500076e2de0b36e79043e58461df20da280d0556a7a0"
    )
