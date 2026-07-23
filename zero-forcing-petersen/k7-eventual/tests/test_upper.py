from zero_forcing_petersen_k7_eventual.upper import initial_mask, replay_schedule


def test_uniform_upper_schedule() -> None:
    for n in range(15, 161):
        replay = replay_schedule(n)
        assert initial_mask(n).bit_count() == 16
        assert replay.force_count == 2 * n - 16
