from zero_forcing_petersen_k8_eventual.witness import BLOCK, replay_n64_witness


def test_n64_positive_separator_control() -> None:
    replay = replay_n64_witness()
    assert len(BLOCK) == 8
    assert len(replay.word) == len(replay.selected) == 64
    assert len(replay.boundary) == 16
    assert replay.word_sha256 == "ef38f30dde297887f7276d3fe9971b3694b0b975697f97cf9456ecc93aa5665b"
