from __future__ import annotations

import hashlib
import json

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
    edge_count,
    encode_graph6,
    is_factor_critical,
    is_triangle_free,
    maximum_independent_set,
    validate_complete_minor,
)


def verification_record() -> dict[str, object]:
    adjacency = complement_adjacency()
    degrees = tuple(mask.bit_count() for mask in adjacency)
    independent_set = maximum_independent_set(adjacency)
    connectivity = complement_connectivity(adjacency)
    contraction_edges = contraction_critical_edge_count(adjacency)
    validate_complete_minor(adjacency, K18_MODEL)
    validate_complete_minor(adjacency, ALTERNATE_K18_MODEL)

    c_dominating_edges = [
        (left + 9, right + 9)
        for left, support_left in enumerate(SUPPORTS)
        for right, support_right in enumerate(SUPPORTS)
        if left < right
        and support_left & support_right == 0
        and not adjacency[left + 9] >> (right + 9) & 1
    ]
    graph6_hash = hashlib.sha256(f"{GRAPH6}\n".encode()).hexdigest()

    assert len(adjacency) == 35
    assert encode_graph6(adjacency) == GRAPH6
    assert edge_count(adjacency) == 150
    assert is_triangle_free(adjacency)
    assert len(independent_set) == 9
    assert sorted(degrees) == [7] * 2 + [8] * 11 + [9] * 22
    assert is_factor_critical(adjacency)
    assert connectivity == 25
    assert contraction_edges == 445
    assert not c_dominating_edges
    assert len(K18_MODEL) == 18

    return {
        "graph6_sha256": graph6_hash,
        "order": 35,
        "F_edge_count": edge_count(adjacency),
        "F_degree_multiset": sorted(degrees),
        "F_triangle_free": True,
        "F_maximum_independent_set": list(independent_set),
        "F_factor_critical": True,
        "G_chromatic_number": 18,
        "G_clique_number": len(independent_set),
        "G_connectivity": connectivity,
        "G_edge_count": 445,
        "G_contraction_critical_edges": contraction_edges,
        "C_dominating_edges_in_P": c_dominating_edges,
        "certified_minor_order": len(K18_MODEL),
        "certified_spanning_models": 2,
        "minor_branch_sizes": [len(branch) for branch in K18_MODEL],
    }


def main() -> None:
    record = verification_record()
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps(record, sort_keys=True, indent=2))
    print("sha256", hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    main()
