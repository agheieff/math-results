from __future__ import annotations

import hashlib
import json

from hadwiger_alpha2_order33.local_checks import (
    common_original_neighbors,
    forced_disjoint_neighbors,
    matching_lower_bound,
    minimum_capacity_numerator,
    possible_component_sizes,
)


def verification_record() -> dict[str, object]:
    common_counts = tuple(
        common_original_neighbors(33, degree_x, degree_y)
        for degree_x in range(1, 9)
        for degree_y in range(1, 9)
    )
    assert min(common_counts) == 17
    assert min(common_counts) - 7 == 10
    assert 10 > 8

    forced_degrees = tuple(forced_disjoint_neighbors(24, size, 8) for size in range(3))
    assert forced_degrees == (23, 16, 9)
    assert all(degree > 8 for degree in forced_degrees)
    minimum_incidence = 24 * 3
    maximum_incidence = 7 * 8
    assert minimum_incidence > maximum_incidence

    cut_splits = {cut_size: possible_component_sizes(21, cut_size, 8) for cut_size in (5, 6)}
    assert cut_splits == {5: ((8, 8),), 6: ((7, 8),)}

    capacity_numerator = minimum_capacity_numerator(21, 8)
    matching_edges = matching_lower_bound(21, 8)
    assert capacity_numerator == 14
    assert matching_edges == 7

    core_branch_sizes = (1,) * 7 + (1, 2, 2)
    final_branch_sizes = core_branch_sizes + (3,) * 7
    assert len(core_branch_sizes) == 10
    assert sum(core_branch_sizes) == 12
    assert len(final_branch_sizes) == 17
    assert sum(final_branch_sizes) == 33

    return {
        "minimum_common_neighbors_of_core_nonedge": min(common_counts),
        "minimum_common_neighbors_outside_K7": min(common_counts) - 7,
        "forced_F_degrees_for_C_incidence_sizes_0_1_2": list(forced_degrees),
        "minimum_total_C_incidence_if_all_sizes_at_least_3": minimum_incidence,
        "maximum_total_C_incidence_from_degree_bound": maximum_incidence,
        "five_six_cut_component_sizes": {
            str(size): [list(pair) for pair in pairs] for size, pairs in cut_splits.items()
        },
        "minimum_twice_capacity": capacity_numerator,
        "required_twice_capacity": 14,
        "matching_lower_bound_from_independence": matching_edges,
        "core_branch_sizes": list(core_branch_sizes),
        "final_minor_branch_sizes": list(final_branch_sizes),
    }


def main() -> None:
    record = verification_record()
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps(record, sort_keys=True, indent=2))
    print("sha256", hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    main()
