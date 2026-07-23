from __future__ import annotations

import json

from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    SEED_K20_MODEL,
    SEED_SUPPORTS,
)
from hadwiger_alpha2_order39_spanning_k20_search.component_search import (
    audit_seed_components,
)
from hadwiger_alpha2_order39_spanning_k20_search.graph import (
    complement_adjacency,
    satisfies_explicit_graph_properties,
)
from hadwiger_alpha2_order39_spanning_k20_search.spanning import (
    solve_all_singletons,
    validate_spanning_model,
)
from hadwiger_alpha2_order39_spanning_k20_search.supports import support_system_valid


def verify() -> dict[str, object]:
    assert support_system_valid(SEED_SUPPORTS)
    adjacency_f = complement_adjacency(SEED_SUPPORTS)
    assert satisfies_explicit_graph_properties(adjacency_f)
    validate_spanning_model(adjacency_f, SEED_K20_MODEL)

    singleton_results = solve_all_singletons(adjacency_f, time_limit_seconds=30.0)
    assert all(result.model is not None for result in singleton_results)

    component_audits = audit_seed_components(time_limit_seconds=30.0)
    states = [audit for _, audits in component_audits for audit in audits]
    explicit = [audit for audit in states if audit.explicit_properties]
    assert len(states) == 6
    assert len(explicit) == 6
    assert all(
        audit.spanning_search is not None
        and any(result.model is not None for result in audit.spanning_search)
        for audit in explicit
    )
    return {
        "all_seed_singletons_work": True,
        "components": [len(component.states) for component, _ in component_audits],
        "explicit_states": len(explicit),
        "seed_singletons": len(singleton_results),
        "states_audited": len(states),
        "universal_status": "INCONCLUSIVE",
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
