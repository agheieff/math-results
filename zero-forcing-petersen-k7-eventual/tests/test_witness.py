from zero_forcing_petersen_k7_eventual.witness import BLOCK, block_word, replay_block_witness


def test_multiple_of_seven_separator_family() -> None:
    assert len(BLOCK) == 7
    for multiplier in range(3, 11):
        selected, boundary = replay_block_witness(multiplier)
        assert len(block_word(multiplier)) == len(selected) == 7 * multiplier
        assert len(boundary) == 2 * multiplier
