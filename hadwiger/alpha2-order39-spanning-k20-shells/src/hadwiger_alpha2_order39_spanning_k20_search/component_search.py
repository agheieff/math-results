from __future__ import annotations

from dataclasses import dataclass

from hadwiger_alpha2_order39_spanning_k20_search.certificate import (
    SECOND_SEED,
    SEED_SUPPORTS,
)
from hadwiger_alpha2_order39_spanning_k20_search.graph import (
    complement_adjacency,
    satisfies_explicit_graph_properties,
)
from hadwiger_alpha2_order39_spanning_k20_search.spanning import (
    SingletonResult,
    find_spanning_model,
)
from hadwiger_alpha2_order39_spanning_k20_search.supports import (
    SupportState,
    coordinate_switch_neighbors,
    support_system_valid,
)


@dataclass(frozen=True)
class Component:
    seed: SupportState
    states: tuple[SupportState, ...]
    frontier_sizes: tuple[int, ...]


@dataclass(frozen=True)
class StateAudit:
    supports: SupportState
    explicit_properties: bool
    spanning_search: tuple[SingletonResult, ...] | None


def enumerate_switch_component(seed: SupportState) -> Component:
    if not support_system_valid(seed):
        raise ValueError("seed does not satisfy the exact support-system conditions")
    seen = {seed}
    frontier = {seed}
    frontier_sizes = [1]
    while frontier:
        next_frontier = {
            candidate
            for state in frontier
            for candidate in coordinate_switch_neighbors(state)
            if candidate not in seen and support_system_valid(candidate)
        }
        if not next_frontier:
            break
        seen |= next_frontier
        frontier = next_frontier
        frontier_sizes.append(len(frontier))
    return Component(seed, tuple(sorted(seen)), tuple(frontier_sizes))


def enumerate_seed_components() -> tuple[Component, ...]:
    components: list[Component] = []
    globally_seen: set[SupportState] = set()
    for seed in (SEED_SUPPORTS, SECOND_SEED):
        if seed in globally_seen:
            continue
        component = enumerate_switch_component(seed)
        components.append(component)
        globally_seen.update(component.states)
    return tuple(components)


def audit_state(
    supports: SupportState,
    *,
    time_limit_seconds: float = 30.0,
) -> StateAudit:
    adjacency_f = complement_adjacency(supports)
    explicit = satisfies_explicit_graph_properties(adjacency_f)
    if not explicit:
        return StateAudit(supports, False, None)
    spanning = find_spanning_model(
        adjacency_f,
        time_limit_seconds=time_limit_seconds,
    )
    return StateAudit(supports, True, spanning)


def audit_seed_components(
    *,
    time_limit_seconds: float = 30.0,
) -> tuple[tuple[Component, tuple[StateAudit, ...]], ...]:
    return tuple(
        (
            component,
            tuple(
                audit_state(state, time_limit_seconds=time_limit_seconds)
                for state in component.states
            ),
        )
        for component in enumerate_seed_components()
    )


def main() -> None:
    total_states = 0
    total_explicit = 0
    total_models = 0
    unknown = 0
    for index, (component, audits) in enumerate(audit_seed_components(), 1):
        print(
            f"component={index} states={len(component.states)} "
            f"frontiers={','.join(map(str, component.frontier_sizes))}"
        )
        total_states += len(component.states)
        for audit in audits:
            if not audit.explicit_properties:
                continue
            total_explicit += 1
            assert audit.spanning_search is not None
            model_result = next(
                (result for result in audit.spanning_search if result.model is not None),
                None,
            )
            if model_result is not None:
                total_models += 1
                print(
                    "MODEL "
                    f"singleton={model_result.singleton} "
                    + " ".join(f"{mask:03x}" for mask in audit.supports)
                )
            elif any(result.status == "UNKNOWN" for result in audit.spanning_search):
                unknown += 1
                print("UNKNOWN " + " ".join(f"{mask:03x}" for mask in audit.supports))
            else:
                print("COUNTERMODEL " + " ".join(f"{mask:03x}" for mask in audit.supports))
    print(
        f"total_states={total_states} explicit={total_explicit} "
        f"models={total_models} unknown={unknown}"
    )


if __name__ == "__main__":
    main()
