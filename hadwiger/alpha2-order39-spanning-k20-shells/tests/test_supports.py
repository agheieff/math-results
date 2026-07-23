from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    SECOND_SEED,
    SEED_SUPPORTS,
)
from hadwiger_alpha2_order39_spanning_k20_search.component_search import (
    enumerate_seed_components,
)
from hadwiger_alpha2_order39_spanning_k20_search.supports import (
    coordinate_switch_neighbors,
    support_system_valid,
)


def test_seeds_satisfy_exact_support_conditions() -> None:
    assert support_system_valid(SEED_SUPPORTS)
    assert support_system_valid(SECOND_SEED)


def test_two_seed_components_are_exhausted() -> None:
    components = enumerate_seed_components()

    assert [len(component.states) for component in components] == [5, 1]
    assert [component.frontier_sizes for component in components] == [
        (1, 1, 1, 1, 1),
        (1,),
    ]
    assert len(coordinate_switch_neighbors(SEED_SUPPORTS)) == 13
