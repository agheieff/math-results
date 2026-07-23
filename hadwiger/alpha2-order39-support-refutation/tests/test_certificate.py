from collections import Counter

from hadwiger_alpha2_order39_support_search.certificate import (
    GRAPH6,
    K20_MODEL,
    ONE_DEFECT,
    SUPPORTS,
    SWITCH_PATH,
)
from hadwiger_alpha2_order39_support_search.checks import (
    apply_switch_path,
    complement_adjacency,
    complement_connectivity,
    contraction_critical_edge_count,
    diameter_at_most_two,
    edge_count,
    encode_graph6,
    is_factor_critical,
    is_triangle_free,
    maximum_independent_set,
    non_dominating_complement_edge_count,
    support_errors,
    validate_complete_minor,
)
from hadwiger_alpha2_order39_support_search.switch_search import coordinate_switch_neighbors


def test_supports_and_switch_path() -> None:
    assert apply_switch_path(ONE_DEFECT, SWITCH_PATH) == SUPPORTS
    assert not support_errors(ONE_DEFECT)
    assert not support_errors(SUPPORTS)
    assert Counter(mask.bit_count() for mask in SUPPORTS) == {3: 22, 4: 6}
    assert sum(mask.bit_count() for mask in SUPPORTS) == 90
    assert [sum(mask >> coordinate & 1 for mask in SUPPORTS) for coordinate in range(10)] == [
        9
    ] * 10

    current = list(ONE_DEFECT)
    for removed, added in SWITCH_PATH:
        assert sorted(mask.bit_count() for mask in removed) == sorted(
            mask.bit_count() for mask in added
        )
        assert [sum(mask >> coordinate & 1 for mask in removed) for coordinate in range(10)] == [
            sum(mask >> coordinate & 1 for mask in added) for coordinate in range(10)
        ]
        for mask in removed:
            current.remove(mask)
        current.extend(added)
        current.sort()
        assert not support_errors(current)
    assert tuple(current) == SUPPORTS


def test_first_switch_frontier_is_exact() -> None:
    neighbors = coordinate_switch_neighbors(tuple(sorted(ONE_DEFECT)))

    assert len(neighbors) == 5
    assert SUPPORTS not in neighbors


def test_reconstructed_complement() -> None:
    adjacency_f = complement_adjacency(SUPPORTS)

    assert edge_count(adjacency_f) == 183
    assert Counter(mask.bit_count() for mask in adjacency_f) == {7: 1, 8: 3, 9: 15, 10: 20}
    assert is_triangle_free(adjacency_f)
    assert diameter_at_most_two(adjacency_f)
    assert len(maximum_independent_set(adjacency_f)) == 10
    assert encode_graph6(adjacency_f) == GRAPH6


def test_minimum_counterexample_local_properties() -> None:
    adjacency_f = complement_adjacency(SUPPORTS)
    edges_g = 39 * 38 // 2 - edge_count(adjacency_f)

    assert edges_g == 558
    assert is_factor_critical(adjacency_f)
    assert complement_connectivity(adjacency_f) == 28
    assert contraction_critical_edge_count(adjacency_f) == edges_g
    assert non_dominating_complement_edge_count(adjacency_f) == edges_g


def test_explicit_k20_model() -> None:
    adjacency_f = complement_adjacency(SUPPORTS)

    assert len(K20_MODEL) == 20
    assert sum(map(len, K20_MODEL)) == 39
    validate_complete_minor(adjacency_f, K20_MODEL)
