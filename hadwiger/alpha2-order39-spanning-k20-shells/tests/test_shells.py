from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    FRESH_SHELL4_K20_MODEL,
    FRESH_SHELL4_SUPPORTS,
    SHELL4_HALL_SUPPORTS,
    SHELL6_HALL_SUPPORTS,
)
from hadwiger_alpha2_order39_spanning_k20_search.component_search import (
    enumerate_seed_components,
)
from hadwiger_alpha2_order39_spanning_k20_search.graph import (
    complement_adjacency,
    satisfies_explicit_graph_properties,
)
from hadwiger_alpha2_order39_spanning_k20_search.isomorphism import (
    graphs_are_isomorphic,
)
from hadwiger_alpha2_order39_spanning_k20_search.shell_search import enumerate_shell
from hadwiger_alpha2_order39_spanning_k20_search.spanning import validate_spanning_model
from hadwiger_alpha2_order39_spanning_k20_search.supports import support_system_valid


def test_distance_four_shell_is_complete() -> None:
    result = enumerate_shell(4)

    assert result.exact_indexed_transitions == 7_383
    assert len(result.local_states) == 27
    assert result.hall_states == SHELL4_HALL_SUPPORTS


def test_fresh_shell_certificate() -> None:
    assert support_system_valid(FRESH_SHELL4_SUPPORTS)
    adjacency_f = complement_adjacency(FRESH_SHELL4_SUPPORTS)
    assert satisfies_explicit_graph_properties(adjacency_f)
    validate_spanning_model(adjacency_f, FRESH_SHELL4_K20_MODEL)


def test_fresh_graph_is_not_in_an_old_component() -> None:
    fresh = complement_adjacency(FRESH_SHELL4_SUPPORTS)

    assert all(
        not graphs_are_isomorphic(fresh, complement_adjacency(state))
        for component in enumerate_seed_components()
        for state in component.states
    )


def test_stored_distance_six_endpoints_are_valid() -> None:
    assert len(SHELL6_HALL_SUPPORTS) == 3
    assert all(support_system_valid(state) for state in SHELL6_HALL_SUPPORTS)
