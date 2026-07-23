from zero_forcing_petersen_general_transfer.forcing import (
    initial_vertices,
    replay_symbolic_schedule,
    symbolic_schedule,
)


def test_symbolic_schedule_on_grid() -> None:
    for k in range(1, 10):
        for n in range(2 * k + 1, 9 * k + 7):
            replay = replay_symbolic_schedule(n, k)
            assert replay.initial_size == 2 * k + 2
            assert replay.force_count == 2 * n - 2 * k - 2


def test_schedule_endpoints() -> None:
    assert len(initial_vertices(1)) == 4
    assert symbolic_schedule(3, 1) == ((("u", 0), ("u", 2)), (("v", 0), ("v", 2)))
