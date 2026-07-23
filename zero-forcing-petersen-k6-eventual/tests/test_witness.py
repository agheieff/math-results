from zero_forcing_petersen_k6_eventual.witness import N36_WORD, replay_n36_witness


def test_n36_separator_witness() -> None:
    selected, boundary = replay_n36_witness()
    assert len(N36_WORD) == len(selected) == 36
    assert len(boundary) == 13
