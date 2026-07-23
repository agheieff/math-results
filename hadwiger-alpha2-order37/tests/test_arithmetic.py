from __future__ import annotations

import pytest

from hadwiger_alpha2_order37.arithmetic import (
    antimatching_lower_bound,
    disjoint_support_lower_bound,
    good_degree_lower_bound,
    minimum_capacity_numerator,
    outside_neighbor_budget,
    possible_two_component_orders,
)
from hadwiger_alpha2_order37.verify import verification_record


@pytest.mark.parametrize(
    ("outside_order", "support_size", "removed", "disjoint", "budget", "good"),
    [
        (28, 1, 0, 19, 8, 11),
        (28, 2, 0, 11, 7, 4),
        (28, 1, 1, 18, 8, 10),
        (28, 2, 1, 10, 7, 3),
        (26, 1, 0, 17, 8, 9),
        (26, 2, 0, 9, 7, 2),
    ],
)
def test_support_counts(
    outside_order: int,
    support_size: int,
    removed: int,
    disjoint: int,
    budget: int,
    good: int,
) -> None:
    assert (
        disjoint_support_lower_bound(
            outside_order,
            support_size,
            9,
            removed_disjoint_vertices=removed,
        )
        == disjoint
    )
    assert outside_neighbor_budget(9, support_size) == budget
    assert (
        good_degree_lower_bound(
            outside_order,
            support_size,
            9,
            removed_disjoint_vertices=removed,
        )
        == good
    )


def test_incidence_and_component_union_contradictions() -> None:
    assert 28 * 3 == 84 > 81 == 9 * 9
    assert 26 * 3 + 3 == 81
    assert 5 + 6 > 9


def test_empty_support_remainder() -> None:
    assert antimatching_lower_bound(27, 9) == 9
    assert minimum_capacity_numerator(27, 9) == 18


def test_main_remainder() -> None:
    assert possible_two_component_orders(24, 6, 9) == ((9, 9),)
    assert possible_two_component_orders(24, 7, 9) == ((8, 9),)
    assert antimatching_lower_bound(24, 9) == 8
    assert minimum_capacity_numerator(24, 9, (9, 0)) == 16


def test_invalid_inputs_fail_fast() -> None:
    with pytest.raises(ValueError):
        disjoint_support_lower_bound(28, 0, 9)
    with pytest.raises(ValueError):
        possible_two_component_orders(7, 7, 9)


def test_verification_record() -> None:
    record = verification_record()

    assert record["contiguous_conclusion"] == 38
    assert record["certified_minor_order"] == 19
    assert record["endpoint_good_degree_lower_bounds"] == {"1": 10, "2": 3}
