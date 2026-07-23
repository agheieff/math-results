import pytest

from hadwiger_alpha2_order31.local_checks import (
    admissible_cut_vertex_patterns,
    common_original_neighbors,
    matching_lower_bound,
    minimum_capacity_numerator,
    possible_component_sizes,
)
from hadwiger_alpha2_order31.verify import verification_record


def test_core_common_neighbor_bound() -> None:
    counts = [
        common_original_neighbors(31, degree_x, degree_y)
        for degree_x in range(1, 9)
        for degree_y in range(1, 9)
    ]

    assert min(counts) == 15
    assert min(counts) - 7 == 8


def test_six_cut_has_only_the_seven_eight_split() -> None:
    assert possible_component_sizes(21, 6, 8) == ((7, 8),)


def test_every_lifted_cut_vertex_is_complete_to_the_k7() -> None:
    patterns = admissible_cut_vertex_patterns(7, 8, 8)
    full_left = (1 << 7) - 1
    full_right = (1 << 8) - 1

    assert len(patterns) == 254
    assert all(left_mask == full_left for left_mask, _ in patterns)
    assert all(0 < right_mask < full_right for _, right_mask in patterns)


def test_capacity_and_antimatching_arithmetic() -> None:
    assert minimum_capacity_numerator(21, 8) == 14
    assert matching_lower_bound(21, 8) == 7


def test_invalid_parameters_fail_fast() -> None:
    with pytest.raises(ValueError):
        common_original_neighbors(1, 1, 1)
    with pytest.raises(ValueError):
        possible_component_sizes(5, 5, 2)
    with pytest.raises(ValueError):
        admissible_cut_vertex_patterns(0, 8, 8)
    with pytest.raises(ValueError):
        minimum_capacity_numerator(7, 8)
    with pytest.raises(ValueError):
        matching_lower_bound(7, 8)


def test_verification_record_is_stable_in_content() -> None:
    record = verification_record()

    assert record["minimum_choices_for_z_outside_K7"] == 8
    assert record["six_cut_component_sizes"] == [[7, 8]]
    assert record["every_lifted_cut_vertex_complete_to_K7"] is True
    assert record["matching_lower_bound_from_independence"] == 7
