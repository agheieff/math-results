from __future__ import annotations

import hashlib
import json
from pathlib import Path

from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    FIFTH_SUCCESSOR_CENTERS,
    FIFTH_SUCCESSOR_NEW_SUPPORTS,
    FOURTH_SUCCESSOR_CENTERS,
    FOURTH_SUCCESSOR_NEW_SUPPORTS,
    SECOND_SUCCESSOR_CENTERS,
    SECOND_SUCCESSOR_NEW_SUPPORTS,
    SEED_SUPPORTS,
    SEVENTH_SUCCESSOR_CENTERS,
    SEVENTH_SUCCESSOR_NEW_SUPPORTS,
    SHELL4_HALL_SUPPORTS,
    SHELL6_HALL_SUPPORTS,
    SIXTH_SUCCESSOR_CENTERS,
    SIXTH_SUCCESSOR_NEW_SUPPORTS,
    SUCCESSOR_CENTERS,
    SUCCESSOR_NEW_SUPPORTS,
    THIRD_SUCCESSOR_CENTERS,
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
    (7_069, 64, 14),
    (7_123, 49, 6),
    (7_123, 42, 7),
    (7_113, 63, 6),
    (7_123, 46, 6),
    (7_076, 47, 8),
    (7_071, 55, 7),
    (7_064, 73, 10),
    (7_123, 46, 6),
    (7_071, 56, 11),
    (7_136, 17, 3),
    (7_096, 19, 5),
    (7_183, 15, 4),
    (7_071, 51, 7),
    (7_118, 54, 8),
    (7_324, 20, 7),
    (7_324, 21, 6),
    (7_341, 20, 6),
    (7_282, 19, 1),
    (7_341, 28, 6),
    (7_341, 20, 6),
    (7_123, 49, 6),
    (7_127, 18, 4),
)
NEW_STATES_SHA256 = "2528fbc54c7a0091387a1ea79969d5c6c3f163474a1f4258e1ca688e2944b28d"


def enumerate_labeled_catchup() -> tuple[
    tuple[SupportState, ...],
    tuple[ShellResult, ...],
    tuple[SupportState, ...],
    tuple[SupportState, ...],
]:
    discovered = _discovered_states()
    centers = tuple(sorted(discovered - _expanded_centers()))
    if len(discovered) != 58 or len(centers) != 23:
        raise AssertionError("the pre-catch-up labeled frontier changed")
    shells = tuple(enumerate_shell_from(center, 4) for center in centers)
    counts = tuple(
        (
            shell.exact_indexed_transitions,
            len(shell.local_states),
            len(shell.hall_states),
        )
        for shell in shells
    )
    if counts != EXPECTED_CENTER_COUNTS:
        raise AssertionError("labeled catch-up shell counts changed")
    hall_union = tuple(sorted({state for shell in shells for state in shell.hall_states}))
    new_states = tuple(state for state in hall_union if state not in discovered)
    if len(hall_union) != 99 or len(new_states) != 74:
        raise AssertionError("labeled catch-up support union changed")
    if _support_hash(new_states) != NEW_STATES_SHA256:
        raise AssertionError("labeled catch-up support hash changed")
    return centers, shells, hall_union, new_states


def verify_labeled_catchup() -> dict[str, object]:
    centers, _, hall_union, new_states = enumerate_labeled_catchup()
    old_graphs = [complement_adjacency(state) for state in sorted(_discovered_states())]
    new_graphs: list[tuple[int, ...]] = []
    models = 0
    for state in new_states:
        adjacency_f = complement_adjacency(state)
        if not satisfies_explicit_graph_properties(adjacency_f):
            raise AssertionError("a labeled catch-up state fails a frozen graph property")
        results = find_spanning_model(adjacency_f, time_limit_seconds=30.0)
        if not any(result.model is not None for result in results):
            raise AssertionError("a labeled catch-up state lacks a spanning model")
        models += 1
        if any(graphs_are_isomorphic(adjacency_f, graph) for graph in old_graphs):
            continue
        if any(graphs_are_isomorphic(adjacency_f, graph) for graph in new_graphs):
            continue
        new_graphs.append(adjacency_f)
    if len(new_graphs) != 33:
        raise AssertionError("labeled catch-up graph-class count changed")

    artifact = Path(__file__).resolve().parents[2] / "artifacts" / "labeled_catchup.txt"
    return {
        "artifact_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        "centers": len(centers),
        "hall_union": len(hall_union),
        "new_graph_isomorphism_classes": len(new_graphs),
        "new_labeled_states": len(new_states),
        "new_states_sha256": NEW_STATES_SHA256,
        "spanning_models": models,
        "universal_status": "INCONCLUSIVE",
    }


def _discovered_states() -> set[SupportState]:
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
        | set(SEVENTH_SUCCESSOR_NEW_SUPPORTS)
    )


def _expanded_centers() -> set[SupportState]:
    return (
        {SEED_SUPPORTS}
        | set(SUCCESSOR_CENTERS)
        | set(SECOND_SUCCESSOR_CENTERS)
        | set(THIRD_SUCCESSOR_CENTERS)
        | set(FOURTH_SUCCESSOR_CENTERS)
        | set(FIFTH_SUCCESSOR_CENTERS)
        | set(SIXTH_SUCCESSOR_CENTERS)
        | set(SEVENTH_SUCCESSOR_CENTERS)
    )


def _support_hash(states: tuple[SupportState, ...]) -> str:
    payload = "\n".join(
        " ".join(f"{support:03x}" for support in state) for state in states
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    print(json.dumps(verify_labeled_catchup(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
