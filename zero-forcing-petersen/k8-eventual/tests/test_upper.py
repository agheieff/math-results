from zero_forcing_petersen_k8_eventual.upper import initial_mask, replay_schedule


def test_uniform_upper_schedule() -> None:
    for n in range(17, 181):
        replay = replay_schedule(n)
        assert initial_mask(n).bit_count() == 18
        assert replay.force_count == 2 * n - 18
