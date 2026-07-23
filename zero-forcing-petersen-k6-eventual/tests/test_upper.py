from zero_forcing_petersen_k6_eventual.upper import initial_mask, replay_schedule


def test_uniform_upper_schedule() -> None:
    for n in range(13, 151):
        replay = replay_schedule(n)
        assert initial_mask(n).bit_count() == 14
        assert replay.force_count == 2 * n - 14
