import pytest

from zero_forcing_petersen_k4.graph import GeneralizedPetersen
from zero_forcing_petersen_k4.upper import replay_uniform_schedule, uniform_seed


@pytest.mark.parametrize("n", [9, 10, 17, 18, 22, 23, 97, 200])
def test_uniform_ten_set_schedule(n: int) -> None:
    graph = GeneralizedPetersen(n)
    seed = uniform_seed(n)
    forces = replay_uniform_schedule(n)
    assert seed.bit_count() == 10
    assert len(forces) == graph.order - seed.bit_count()
    assert len({force.target for force in forces}) == len(forces)
