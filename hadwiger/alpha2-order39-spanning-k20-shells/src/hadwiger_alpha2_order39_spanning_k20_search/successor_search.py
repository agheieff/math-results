from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    SHELL4_HALL_SUPPORTS,
    SHELL6_HALL_SUPPORTS,
    SUCCESSOR_CENTERS,
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
    (7_176, 22, 6),
    (7_383, 28, 6),
    (7_152, 35, 3),
    (7_564, 8, 0),
    (7_169, 22, 3),
)


@dataclass(frozen=True)
class SuccessorCheckpoint:
    shells: tuple[ShellResult, ...]
    hall_union: tuple[SupportState, ...]
    new_states: tuple[SupportState, ...]


def enumerate_successors() -> SuccessorCheckpoint:
    shells = tuple(enumerate_shell_from(center, 4) for center in SUCCESSOR_CENTERS)
    actual_counts = tuple(
        (
            shell.exact_indexed_transitions,
            len(shell.local_states),
            len(shell.hall_states),
        )
        for shell in shells
    )
    if actual_counts != EXPECTED_CENTER_COUNTS:
        raise AssertionError("successor shell counts changed")

    hall_union = tuple(sorted({state for shell in shells for state in shell.hall_states}))
    old_states = _old_states()
    new_states = tuple(state for state in hall_union if state not in old_states)
    if len(hall_union) != 13 or new_states != SUCCESSOR_NEW_SUPPORTS:
        raise AssertionError("successor support-system union changed")
    return SuccessorCheckpoint(shells, hall_union, new_states)


def verify_successors() -> dict[str, object]:
    checkpoint = enumerate_successors()
    old_graphs = [complement_adjacency(state) for state in sorted(_old_states())]
    new_representatives: list[tuple[int, ...]] = []
    models = 0
    for state in checkpoint.new_states:
        adjacency_f = complement_adjacency(state)
        if not satisfies_explicit_graph_properties(adjacency_f):
            raise AssertionError("a successor fails the frozen graph properties")
        if any(graphs_are_isomorphic(adjacency_f, old) for old in old_graphs):
            raise AssertionError("a recorded successor is isomorphic to an old graph")
        if any(
            graphs_are_isomorphic(adjacency_f, representative)
            for representative in new_representatives
        ):
            raise AssertionError("two recorded successors are isomorphic")
        new_representatives.append(adjacency_f)
        results = find_spanning_model(adjacency_f, time_limit_seconds=30.0)
        if not any(result.model is not None for result in results):
            raise AssertionError("a successor lacks a resolved spanning model")
        models += 1

    artifact = Path(__file__).resolve().parents[2] / "artifacts" / "successor_checkpoint.txt"
    return {
        "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        "centers": len(checkpoint.shells),
        "hall_union": len(checkpoint.hall_union),
        "new_graph_isomorphism_classes": len(new_representatives),
        "new_labeled_states": len(checkpoint.new_states),
        "spanning_models": models,
        "universal_status": "INCONCLUSIVE",
    }


def _old_states() -> set[SupportState]:
    return (
        {state for component in enumerate_seed_components() for state in component.states}
        | set(SHELL4_HALL_SUPPORTS)
        | set(SHELL6_HALL_SUPPORTS)
    )


def main() -> None:
    print(json.dumps(verify_successors(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
