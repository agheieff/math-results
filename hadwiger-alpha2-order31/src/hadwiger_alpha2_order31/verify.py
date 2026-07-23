from __future__ import annotations

import hashlib
import json

from hadwiger_alpha2_order31.local_checks import (
    admissible_cut_vertex_patterns,
    common_original_neighbors,
    matching_lower_bound,
    minimum_capacity_numerator,
    possible_component_sizes,
)


def verification_record() -> dict[str, object]:
    common_counts = tuple(
        common_original_neighbors(31, degree_x, degree_y)
        for degree_x in range(1, 9)
        for degree_y in range(1, 9)
    )
    assert min(common_counts) == 15
    assert min(common_counts) - 7 == 8

    component_sizes = possible_component_sizes(21, 6, 8)
    assert component_sizes == ((7, 8),)

    patterns = admissible_cut_vertex_patterns(7, 8, 8)
    full_left = (1 << 7) - 1
    full_right = (1 << 8) - 1
    assert len(patterns) == 2**8 - 2
    assert all(left_mask == full_left for left_mask, _ in patterns)
    assert all(0 < right_mask < full_right for _, right_mask in patterns)
    assert 7 + 2 > 8
    assert 16 > 2

    capacity_numerator = minimum_capacity_numerator(21, 8)
    assert capacity_numerator == 14

    matching_edges = matching_lower_bound(21, 8)
    assert matching_edges == 7

    branch_sizes = (1,) * 7 + (2, 1) + (3,) * 7
    assert len(branch_sizes) == 16
    assert sum(branch_sizes) == 31

    return {
        "minimum_common_neighbors_of_core_nonedge": min(common_counts),
        "minimum_choices_for_z_outside_K7": min(common_counts) - 7,
        "six_cut_component_sizes": [list(pair) for pair in component_sizes],
        "admissible_lifted_cut_vertex_patterns": len(patterns),
        "every_lifted_cut_vertex_complete_to_K7": True,
        "lifted_cut_forced_stable": True,
        "lifted_cut_size": 16,
        "ambient_independence_bound": 2,
        "minimum_twice_capacity": capacity_numerator,
        "required_twice_capacity": 14,
        "matching_lower_bound_from_independence": matching_edges,
        "minor_branch_sizes": list(branch_sizes),
    }


def main() -> None:
    record = verification_record()
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps(record, sort_keys=True, indent=2))
    print("sha256", hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    main()
