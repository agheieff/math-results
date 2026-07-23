from __future__ import annotations

import hashlib
import json
from pathlib import Path

from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    FIFTH_SUCCESSOR_CENTERS,
    FIFTH_SUCCESSOR_NEW_CLASS_REPRESENTATIVES,
    FIFTH_SUCCESSOR_NEW_SUPPORTS,
    FOURTH_SUCCESSOR_NEW_SUPPORTS,
    SECOND_SUCCESSOR_NEW_SUPPORTS,
    SHELL4_HALL_SUPPORTS,
    SHELL6_HALL_SUPPORTS,
    SUCCESSOR_NEW_SUPPORTS,
    THIRD_SUCCESSOR_NEW_SUPPORTS,
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
    (7_248, 8, 1),
    (7_211, 10, 1),
    (7_096, 19, 5),
    (7_023, 13, 2),
)


def enumerate_fifth_successors() -> tuple[
    tuple[ShellResult, ...],
    tuple[SupportState, ...],
    tuple[SupportState, ...],
]:
    shells = tuple(enumerate_shell_from(center, 4) for center in FIFTH_SUCCESSOR_CENTERS)
    counts = tuple(
        (
            shell.exact_indexed_transitions,
            len(shell.local_states),
            len(shell.hall_states),
        )
        for shell in shells
    )
    if counts != EXPECTED_CENTER_COUNTS:
        raise AssertionError("fifth-successor shell counts changed")
    hall_union = tuple(sorted({state for shell in shells for state in shell.hall_states}))
    new_states = tuple(state for state in hall_union if state not in _old_states())
    if len(hall_union) != 9 or new_states != FIFTH_SUCCESSOR_NEW_SUPPORTS:
        raise AssertionError("fifth-successor support union changed")
    return shells, hall_union, new_states


def verify_fifth_successors() -> dict[str, object]:
    shells, hall_union, new_states = enumerate_fifth_successors()
    old_graphs = [complement_adjacency(state) for state in sorted(_old_states())]
    new_graphs: list[tuple[int, ...]] = []
    for state in new_states:
        adjacency_f = complement_adjacency(state)
        if not satisfies_explicit_graph_properties(adjacency_f):
            raise AssertionError("a fifth successor fails a frozen graph property")
        is_new = not any(
            graphs_are_isomorphic(adjacency_f, graph) for graph in old_graphs
        ) and not any(graphs_are_isomorphic(adjacency_f, graph) for graph in new_graphs)
        if is_new:
            new_graphs.append(adjacency_f)
        results = find_spanning_model(adjacency_f, time_limit_seconds=30.0)
        if not any(result.model is not None for result in results):
            raise AssertionError("a fifth successor lacks a spanning model")
    if len(new_graphs) != 4:
        raise AssertionError("fifth-successor graph-class count changed")
    if new_states[:4] != FIFTH_SUCCESSOR_NEW_CLASS_REPRESENTATIVES:
        raise AssertionError("fifth-successor representatives changed")

    artifact = Path(__file__).resolve().parents[2] / "artifacts" / "successor_wave5.txt"
    return {
        "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        "centers": len(shells),
        "hall_union": len(hall_union),
        "new_graph_isomorphism_classes": len(new_graphs),
        "new_labeled_states": len(new_states),
        "spanning_models": len(new_states),
        "universal_status": "INCONCLUSIVE",
    }


def _old_states() -> set[SupportState]:
    return (
        {state for component in enumerate_seed_components() for state in component.states}
        | set(SHELL4_HALL_SUPPORTS)
        | set(SHELL6_HALL_SUPPORTS)
        | set(SUCCESSOR_NEW_SUPPORTS)
        | set(SECOND_SUCCESSOR_NEW_SUPPORTS)
        | set(THIRD_SUCCESSOR_NEW_SUPPORTS)
        | set(FOURTH_SUCCESSOR_NEW_SUPPORTS)
    )


def main() -> None:
    print(json.dumps(verify_fifth_successors(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
