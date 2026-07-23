from __future__ import annotations

import hashlib
import json
from pathlib import Path

from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    SECOND_SUCCESSOR_CENTERS,
    SECOND_SUCCESSOR_NEW_CLASS_REPRESENTATIVES,
    SECOND_SUCCESSOR_NEW_SUPPORTS,
    SHELL4_HALL_SUPPORTS,
    SHELL6_HALL_SUPPORTS,
    SUCCESSOR_NEW_SUPPORTS,
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
    enumerate_shell_from,
)
from hadwiger_alpha2_order39_spanning_k20_search.spanning import find_spanning_model
from hadwiger_alpha2_order39_spanning_k20_search.supports import SupportState

EXPECTED_CENTER_COUNTS = (
    (7_152, 31, 4),
    (7_157, 29, 3),
    (7_157, 31, 4),
    (23_820, 51, 1),
    (7_190, 15, 2),
    (7_127, 18, 4),
)


def enumerate_second_successors() -> tuple[
    tuple[ShellResult, ...],
    tuple[SupportState, ...],
    tuple[SupportState, ...],
]:
    shells = tuple(enumerate_shell_from(center, 4) for center in SECOND_SUCCESSOR_CENTERS)
    counts = tuple(
        (
            shell.exact_indexed_transitions,
            len(shell.local_states),
            len(shell.hall_states),
        )
        for shell in shells
    )
    if counts != EXPECTED_CENTER_COUNTS:
        raise AssertionError("second-successor shell counts changed")
    hall_union = tuple(sorted({state for shell in shells for state in shell.hall_states}))
    new_states = tuple(state for state in hall_union if state not in _old_states())
    if len(hall_union) != 12 or new_states != SECOND_SUCCESSOR_NEW_SUPPORTS:
        raise AssertionError("second-successor support union changed")
    return shells, hall_union, new_states


def verify_second_successors() -> dict[str, object]:
    shells, hall_union, new_states = enumerate_second_successors()
    old_graphs = [complement_adjacency(state) for state in sorted(_old_states())]
    new_representatives: list[tuple[int, ...]] = []
    models = 0
    for state in new_states:
        adjacency_f = complement_adjacency(state)
        if not satisfies_explicit_graph_properties(adjacency_f):
            raise AssertionError("a second successor fails a frozen graph property")
        is_new_class = not any(
            graphs_are_isomorphic(adjacency_f, old) for old in old_graphs
        ) and not any(
            graphs_are_isomorphic(adjacency_f, representative)
            for representative in new_representatives
        )
        if is_new_class:
            new_representatives.append(adjacency_f)
        results = find_spanning_model(adjacency_f, time_limit_seconds=30.0)
        if not any(result.model is not None for result in results):
            raise AssertionError("a second successor lacks a resolved spanning model")
        models += 1
    if len(new_representatives) != 7:
        raise AssertionError("second-successor class count changed")
    if tuple(new_states[:7]) != SECOND_SUCCESSOR_NEW_CLASS_REPRESENTATIVES:
        raise AssertionError("new-class representatives changed")

    artifact = Path(__file__).resolve().parents[2] / "artifacts" / "successor_wave2.txt"
    return {
        "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        "centers": len(shells),
        "hall_union": len(hall_union),
        "new_graph_isomorphism_classes": len(new_representatives),
        "new_labeled_states": len(new_states),
        "spanning_models": models,
        "universal_status": "INCONCLUSIVE",
    }


def _old_states() -> set[SupportState]:
    return (
        {state for component in enumerate_seed_components() for state in component.states}
        | set(SHELL4_HALL_SUPPORTS)
        | set(SHELL6_HALL_SUPPORTS)
        | set(SUCCESSOR_NEW_SUPPORTS)
    )


def main() -> None:
    print(json.dumps(verify_second_successors(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
