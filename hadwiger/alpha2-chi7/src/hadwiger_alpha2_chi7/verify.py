from __future__ import annotations

import hashlib
import json

from hadwiger_alpha2_chi7.criterion import (
    find_clique4_seagull_model,
    find_six_pair_cover_model,
    is_clique_model,
)
from hadwiger_alpha2_chi7.graph import Graph


def verification_record() -> dict[str, object]:
    complement = Graph.complete_bipartite(6, 7)
    graph = complement.complement()
    clique = tuple(range(6, 13))
    assert complement.is_triangle_free()
    assert complement.matching_number() == 6
    assert graph.independence_number() == 2
    assert 13 - complement.matching_number() == 7
    assert graph.is_clique(clique)
    assert find_six_pair_cover_model(graph) is None

    cycle_complement = Graph.cycle(13)
    cycle_graph = cycle_complement.complement()
    model = find_clique4_seagull_model(cycle_complement)
    assert model is not None
    assert is_clique_model(cycle_graph, model)

    return {
        "counterexample_complement": "K6,7",
        "counterexample_matching_number": complement.matching_number(),
        "counterexample_chromatic_number": 13 - complement.matching_number(),
        "counterexample_has_K7_subgraph": list(clique),
        "counterexample_has_six_pair_cover_model": False,
        "cycle_complement_model": [list(branch_set) for branch_set in model],
    }


def main() -> None:
    record = verification_record()
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps(record, sort_keys=True, indent=2))
    print("sha256", hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    main()
