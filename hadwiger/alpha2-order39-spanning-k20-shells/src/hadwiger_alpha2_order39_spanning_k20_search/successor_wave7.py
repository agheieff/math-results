from __future__ import annotations

import hashlib
import json
from pathlib import Path

from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    FIFTH_SUCCESSOR_NEW_SUPPORTS,
    FOURTH_SUCCESSOR_NEW_SUPPORTS,
    SECOND_SUCCESSOR_NEW_SUPPORTS,
    SEVENTH_SUCCESSOR_CENTERS,
    SEVENTH_SUCCESSOR_NEW_CLASS_REPRESENTATIVES,
    SEVENTH_SUCCESSOR_NEW_SUPPORTS,
    SHELL4_HALL_SUPPORTS,
    SHELL6_HALL_SUPPORTS,
    SIXTH_SUCCESSOR_NEW_SUPPORTS,
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
    (7_118, 54, 8),
    (7_071, 51, 7),
)


def enumerate_seventh_successors() -> tuple[
    tuple[ShellResult, ...],
    tuple[SupportState, ...],
    tuple[SupportState, ...],
]:
    shells = tuple(enumerate_shell_from(center, 4) for center in SEVENTH_SUCCESSOR_CENTERS)
    counts = tuple(
        (
            shell.exact_indexed_transitions,
            len(shell.local_states),
            len(shell.hall_states),
        )
        for shell in shells
    )
    if counts != EXPECTED_CENTER_COUNTS:
        raise AssertionError("seventh-successor shell counts changed")
    hall_union = tuple(sorted({state for shell in shells for state in shell.hall_states}))
    new_states = tuple(state for state in hall_union if state not in _old_states())
    if len(hall_union) != 15 or new_states != SEVENTH_SUCCESSOR_NEW_SUPPORTS:
        raise AssertionError("seventh-successor support union changed")
    return shells, hall_union, new_states


def verify_seventh_successors() -> dict[str, object]:
    shells, hall_union, new_states = enumerate_seventh_successors()
    old_graphs = [complement_adjacency(state) for state in sorted(_old_states())]
    new_graphs: list[tuple[int, ...]] = []
    representatives: list[SupportState] = []
    for state in new_states:
        adjacency_f = complement_adjacency(state)
        if not satisfies_explicit_graph_properties(adjacency_f):
            raise AssertionError("a seventh successor fails a frozen graph property")
        is_new = not any(
            graphs_are_isomorphic(adjacency_f, graph) for graph in old_graphs
        ) and not any(graphs_are_isomorphic(adjacency_f, graph) for graph in new_graphs)
        if is_new:
            new_graphs.append(adjacency_f)
            representatives.append(state)
        results = find_spanning_model(adjacency_f, time_limit_seconds=30.0)
        if not any(result.model is not None for result in results):
            raise AssertionError("a seventh successor lacks a spanning model")
    if tuple(representatives) != SEVENTH_SUCCESSOR_NEW_CLASS_REPRESENTATIVES:
        raise AssertionError("seventh-successor representatives changed")

    artifact = Path(__file__).resolve().parents[2] / "artifacts" / "successor_wave7.txt"
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
        | set(FIFTH_SUCCESSOR_NEW_SUPPORTS)
        | set(SIXTH_SUCCESSOR_NEW_SUPPORTS)
    )


def main() -> None:
    print(json.dumps(verify_seventh_successors(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
