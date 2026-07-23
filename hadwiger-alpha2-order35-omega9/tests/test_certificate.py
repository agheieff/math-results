from __future__ import annotations

import pytest

from hadwiger_alpha2_order35_omega9.certificate import (
    ALTERNATE_K18_MODEL,
    GRAPH6,
    K18_MODEL,
    SUPPORTS,
    complement_adjacency,
)
from hadwiger_alpha2_order35_omega9.checks import (
    complement_connectivity,
    contraction_critical_edge_count,
    encode_graph6,
    has_perfect_matching,
    is_factor_critical,
    is_triangle_free,
    maximum_independent_set,
    validate_complete_minor,
)
from hadwiger_alpha2_order35_omega9.verify import verification_record


def test_complement_has_required_ramsey_parameters() -> None:
    adjacency = complement_adjacency()

    assert encode_graph6(adjacency) == GRAPH6
    assert is_triangle_free(adjacency)
    assert len(maximum_independent_set(adjacency)) == 9
    assert sorted(mask.bit_count() for mask in adjacency) == [7] * 2 + [8] * 11 + [9] * 22


def test_minimum_counterexample_local_properties() -> None:
    adjacency = complement_adjacency()

    assert is_factor_critical(adjacency)
    assert complement_connectivity(adjacency) == 25
    assert contraction_critical_edge_count(adjacency) == 445


def test_proposed_core_dominating_edge_does_not_exist() -> None:
    adjacency = complement_adjacency()

    for left, support_left in enumerate(SUPPORTS):
        for right in range(left + 1, len(SUPPORTS)):
            support_right = SUPPORTS[right]
            if not adjacency[left + 9] >> (right + 9) & 1:
                assert support_left & support_right


def test_graph_nevertheless_has_a_k18_minor() -> None:
    adjacency = complement_adjacency()

    validate_complete_minor(adjacency, K18_MODEL)
    validate_complete_minor(adjacency, ALTERNATE_K18_MODEL)
    assert sorted(vertex for branch in K18_MODEL for vertex in branch) == list(range(35))
    assert sorted(vertex for branch in ALTERNATE_K18_MODEL for vertex in branch) == list(range(35))


def test_matching_and_minor_checks_fail_fast() -> None:
    adjacency = complement_adjacency()

    assert not has_perfect_matching(adjacency, (1 << 3) - 1)
    with pytest.raises(ValueError):
        validate_complete_minor(adjacency, ((0, 9),))
    with pytest.raises(ValueError):
        validate_complete_minor(adjacency, ((0,), (0,)))


def test_verification_record_is_stable_in_content() -> None:
    record = verification_record()

    assert record["G_chromatic_number"] == 18
    assert record["G_connectivity"] == 25
    assert record["G_contraction_critical_edges"] == 445
    assert record["C_dominating_edges_in_P"] == []
    assert record["certified_minor_order"] == 18
    assert record["certified_spanning_models"] == 2
