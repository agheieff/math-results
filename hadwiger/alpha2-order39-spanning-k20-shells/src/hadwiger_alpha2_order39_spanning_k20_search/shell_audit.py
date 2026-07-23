from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    SHELL4_HALL_SUPPORTS,
    SHELL6_HALL_SUPPORTS,
)
from hadwiger_alpha2_order39_spanning_k20_search.component_search import (
    enumerate_seed_components,
)
from hadwiger_alpha2_order39_spanning_k20_search.graph import (
    complement_adjacency,
    satisfies_explicit_graph_properties,
)
from hadwiger_alpha2_order39_spanning_k20_search.isomorphism import (
    graphs_are_isomorphic,
)
from hadwiger_alpha2_order39_spanning_k20_search.shell_search import (
    ShellResult,
    enumerate_shell,
)
from hadwiger_alpha2_order39_spanning_k20_search.spanning import find_spanning_model
from hadwiger_alpha2_order39_spanning_k20_search.supports import SupportState

EXPECTED_COUNTS = {
    4: (7_383, 27, 6),
    6: (1_202_709, 114, 3),
}
EXPECTED_HALL = {
    4: SHELL4_HALL_SUPPORTS,
    6: SHELL6_HALL_SUPPORTS,
}


@dataclass(frozen=True)
class AuditedShell:
    result: ShellResult
    explicit_count: int
    spanning_count: int


def audit_shell(distance: int, *, time_limit_seconds: float = 30.0) -> AuditedShell:
    result = enumerate_shell(distance)
    expected_transitions, expected_local, expected_hall = EXPECTED_COUNTS[distance]
    if (
        result.exact_indexed_transitions,
        len(result.local_states),
        len(result.hall_states),
    ) != (expected_transitions, expected_local, expected_hall):
        raise AssertionError("shell counts changed")
    if result.hall_states != EXPECTED_HALL[distance]:
        raise AssertionError("Hall-valid shell endpoints changed")

    explicit_count = 0
    spanning_count = 0
    for supports in result.hall_states:
        adjacency_f = complement_adjacency(supports)
        if not satisfies_explicit_graph_properties(adjacency_f):
            continue
        explicit_count += 1
        results = find_spanning_model(
            adjacency_f,
            time_limit_seconds=time_limit_seconds,
        )
        if any(item.model is not None for item in results):
            spanning_count += 1
    if explicit_count != expected_hall or spanning_count != expected_hall:
        raise AssertionError("a graph-property or spanning certificate changed")
    return AuditedShell(result, explicit_count, spanning_count)


def graph_isomorphism_class_count(shells: tuple[AuditedShell, ...]) -> int:
    states: set[SupportState] = {
        state for component in enumerate_seed_components() for state in component.states
    }
    for shell in shells:
        states.update(shell.result.hall_states)

    representatives: list[tuple[int, ...]] = []
    for state in sorted(states):
        adjacency_f = complement_adjacency(state)
        if any(graphs_are_isomorphic(adjacency_f, other) for other in representatives):
            continue
        representatives.append(adjacency_f)
    return len(representatives)


def verify_shell_checkpoint() -> dict[str, object]:
    shells = tuple(audit_shell(distance) for distance in (4, 6))
    class_count = graph_isomorphism_class_count(shells)
    if class_count != 11:
        raise AssertionError("graph-isomorphism class count changed")
    artifact = Path(__file__).resolve().parents[2] / "artifacts" / "shell_checkpoint.txt"
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    return {
        "artifact_sha256": digest,
        "graph_isomorphism_classes": class_count,
        "shells": [
            {
                "distance": shell.result.distance,
                "exact_indexed_transitions": shell.result.exact_indexed_transitions,
                "explicit": shell.explicit_count,
                "hall_valid": len(shell.result.hall_states),
                "local_unique": len(shell.result.local_states),
                "spanning_models": shell.spanning_count,
            }
            for shell in shells
        ],
        "universal_status": "INCONCLUSIVE",
    }


def main() -> None:
    print(json.dumps(verify_shell_checkpoint(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
