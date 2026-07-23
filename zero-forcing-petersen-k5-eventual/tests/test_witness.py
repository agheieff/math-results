from zero_forcing_petersen_k5_eventual.witness import N28_WORD, replay_n28_witness


def test_n28_threshold_witness() -> None:
    selected, boundary = replay_n28_witness()
    assert len(N28_WORD) == len(selected) == 28
    assert len(boundary) == 11
