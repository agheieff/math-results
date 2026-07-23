from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    SEED_K20_MODEL,
    SEED_SUPPORTS,
)
from hadwiger_alpha2_order39_spanning_k20_search.graph import (
    complement_adjacency,
    satisfies_explicit_graph_properties,
)
from hadwiger_alpha2_order39_spanning_k20_search.spanning import (
    solve_for_singleton,
    validate_spanning_model,
)


def test_seed_has_all_explicit_graph_properties() -> None:
    adjacency_f = complement_adjacency(SEED_SUPPORTS)

    assert satisfies_explicit_graph_properties(adjacency_f)


def test_stored_spanning_model() -> None:
    adjacency_f = complement_adjacency(SEED_SUPPORTS)

    validate_spanning_model(adjacency_f, SEED_K20_MODEL)


def test_exact_solver_recovers_singleton_zero_model() -> None:
    adjacency_f = complement_adjacency(SEED_SUPPORTS)
    result = solve_for_singleton(adjacency_f, 0)

    assert result.status == "OPTIMAL"
    assert result.model is not None
    validate_spanning_model(adjacency_f, result.model)
