import pytest

from hadwiger_alpha2_order33.local_checks import (
    common_original_neighbors,
    forced_disjoint_neighbors,
    matching_lower_bound,
    minimum_capacity_numerator,
    possible_component_sizes,
)
from hadwiger_alpha2_order33.verify import verification_record


def test_core_has_ten_external_common_neighbors() -> None:
    counts = [
        common_original_neighbors(33, degree_x, degree_y)
        for degree_x in range(1, 9)
        for degree_y in range(1, 9)
    ]

    assert min(counts) == 17
    assert min(counts) - 7 == 10


def test_small_C_incidence_sets_force_excess_degree() -> None:
    forced = [forced_disjoint_neighbors(24, size, 8) for size in range(3)]

    assert forced == [23, 16, 9]
    assert min(forced) > 8
    assert 24 * 3 > 7 * 8


def test_only_five_six_cut_splits() -> None:
    assert possible_component_sizes(21, 5, 8) == ((8, 8),)
    assert possible_component_sizes(21, 6, 8) == ((7, 8),)


def test_capacity_and_antimatching_arithmetic() -> None:
    assert minimum_capacity_numerator(21, 8) == 14
    assert matching_lower_bound(21, 8) == 7


def test_invalid_parameters_fail_fast() -> None:
    with pytest.raises(ValueError):
        common_original_neighbors(1, 1, 1)
    with pytest.raises(ValueError):
        forced_disjoint_neighbors(24, 3, 8)
    with pytest.raises(ValueError):
        possible_component_sizes(5, 5, 2)
    with pytest.raises(ValueError):
        minimum_capacity_numerator(7, 8)
    with pytest.raises(ValueError):
        matching_lower_bound(7, 8)


def test_verification_record_is_stable_in_content() -> None:
    record = verification_record()

    assert record["minimum_common_neighbors_outside_K7"] == 10
    assert record["forced_F_degrees_for_C_incidence_sizes_0_1_2"] == [23, 16, 9]
    assert record["five_six_cut_component_sizes"] == {"5": [[8, 8]], "6": [[7, 8]]}
    assert record["matching_lower_bound_from_independence"] == 7
