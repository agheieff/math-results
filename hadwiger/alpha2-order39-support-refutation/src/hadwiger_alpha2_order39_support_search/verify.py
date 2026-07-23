from __future__ import annotations

import json
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
from hadwiger_alpha2_order39_support_search.supports import hall_violations, multiplicities


def verify() -> dict[str, object]:
    assert not support_errors(SUPPORTS)
    assert apply_switch_path(ONE_DEFECT, SWITCH_PATH) == SUPPORTS
    assert not hall_violations(multiplicities(SUPPORTS))

    near_violations = hall_violations(multiplicities(ONE_DEFECT))
    assert len(near_violations) == 1
    assert (
        near_violations[0].weight,
        near_violations[0].bound,
        near_violations[0].union,
    ) == (10, 9, 0x3FF)

    adjacency_f = complement_adjacency(SUPPORTS)
    assert is_triangle_free(adjacency_f)
    assert diameter_at_most_two(adjacency_f)
    maximum_stable_set = maximum_independent_set(adjacency_f)
    assert len(maximum_stable_set) == 10
    assert is_factor_critical(adjacency_f)

    edges_f = edge_count(adjacency_f)
    edges_g = 39 * 38 // 2 - edges_f
    assert edges_f == 183
    assert edges_g == 558
    assert complement_connectivity(adjacency_f) == 28
    assert contraction_critical_edge_count(adjacency_f) == edges_g
    assert non_dominating_complement_edge_count(adjacency_f) == edges_g
    assert encode_graph6(adjacency_f) == GRAPH6
    validate_complete_minor(adjacency_f, K20_MODEL)

    coordinate_degrees = [
        sum(mask >> coordinate & 1 for mask in SUPPORTS) for coordinate in range(10)
    ]
    return {
        "alpha_F": len(maximum_stable_set),
        "chi_G": 20,
        "contraction_critical_G_edges": edges_g,
        "coordinate_degrees": coordinate_degrees,
        "degree_multiset_F": dict(sorted(Counter(map(int.bit_count, adjacency_f)).items())),
        "diameter_F": 2,
        "edges_F": edges_f,
        "factor_critical_F": True,
        "hall_violations": 0,
        "kappa_G": 28,
        "minor_order_G": len(K20_MODEL),
        "support_incidence": sum(mask.bit_count() for mask in SUPPORTS),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
