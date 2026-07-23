from __future__ import annotations

import hashlib
import json

from hadwiger_alpha2_order37.arithmetic import (
    antimatching_lower_bound,
    disjoint_support_lower_bound,
    good_degree_lower_bound,
    minimum_capacity_numerator,
    outside_neighbor_budget,
    possible_two_component_orders,
)


def verification_record() -> dict[str, object]:
    j_empty = {
        str(size): {
            "disjoint": disjoint_support_lower_bound(28, size, 9),
            "F_budget": outside_neighbor_budget(9, size),
        }
        for size in (1, 2)
    }
    matching_one_remainder = {
        str(size): {
            "disjoint": disjoint_support_lower_bound(26, size, 9),
            "F_budget": outside_neighbor_budget(9, size),
        }
        for size in (1, 2)
    }
    endpoint_degrees = {
        str(size): good_degree_lower_bound(28, size, 9, removed_disjoint_vertices=1)
        for size in (1, 2)
    }
    global_good_degrees = {str(size): good_degree_lower_bound(28, size, 9) for size in (1, 2)}
    empty_core = {
        "remainder_order": 27,
        "connectivity": 9,
        "antimatching": antimatching_lower_bound(27, 9),
        "capacity_numerator": minimum_capacity_numerator(27, 9),
    }
    main_remainder = {
        "remainder_order": 24,
        "initial_connectivity": 6,
        "six_cut_components": possible_two_component_orders(24, 6, 9),
        "seven_cut_components": possible_two_component_orders(24, 7, 9),
        "antimatching": antimatching_lower_bound(24, 9),
        "capacity_numerator": minimum_capacity_numerator(24, 9, (9, 0)),
    }

    assert j_empty == {
        "1": {"disjoint": 19, "F_budget": 8},
        "2": {"disjoint": 11, "F_budget": 7},
    }
    assert matching_one_remainder == {
        "1": {"disjoint": 17, "F_budget": 8},
        "2": {"disjoint": 9, "F_budget": 7},
    }
    assert endpoint_degrees == {"1": 10, "2": 3}
    assert global_good_degrees == {"1": 11, "2": 4}
    assert 28 * 3 > 9 * 9
    assert 26 * 3 + 3 == 9 * 9
    assert 5 + 6 > 9
    assert empty_core == {
        "remainder_order": 27,
        "connectivity": 9,
        "antimatching": 9,
        "capacity_numerator": 18,
    }
    assert main_remainder["six_cut_components"] == ((9, 9),)
    assert main_remainder["seven_cut_components"] == ((8, 9),)
    assert main_remainder["antimatching"] == 8
    assert main_remainder["capacity_numerator"] == 16
    assert 11 + 8 == 19

    return {
        "order_frontier": 37,
        "contiguous_conclusion": 38,
        "minimum_counterexample_chromatic_number": 19,
        "sufficient_clique_threshold": 10,
        "J_empty_checks": j_empty,
        "matching_one_remainder_checks": matching_one_remainder,
        "endpoint_good_degree_lower_bounds": endpoint_degrees,
        "global_good_degree_lower_bounds": global_good_degrees,
        "support_incidence_lower_bound": 84,
        "support_incidence_upper_bound": 81,
        "component_union_lower_bounds": [5, 6],
        "support_ground_set_order": 9,
        "empty_support_core": empty_core,
        "main_remainder": {
            **main_remainder,
            "six_cut_components": [list(pair) for pair in main_remainder["six_cut_components"]],
            "seven_cut_components": [list(pair) for pair in main_remainder["seven_cut_components"]],
        },
        "core_branches": 11,
        "seagull_branches": 8,
        "certified_minor_order": 19,
    }


def main() -> None:
    record = verification_record()
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps(record, sort_keys=True, indent=2))
    print("sha256", hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    main()
