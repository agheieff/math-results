from __future__ import annotations

from dataclasses import dataclass

from ortools.sat.python import cp_model

from hadwiger_alpha2_order39_spanning_k20_search.graph import (
    Branch,
    Edge,
    branches_touch,
    g_edges,
    validate_complete_minor,
)


@dataclass(frozen=True)
class SingletonResult:
    singleton: int
    status: str
    model: tuple[Branch, ...] | None


def solve_for_singleton(
    adjacency_f: tuple[int, ...],
    singleton: int,
    *,
    time_limit_seconds: float = 30.0,
) -> SingletonResult:
    order = len(adjacency_f)
    if not 0 <= singleton < order or time_limit_seconds <= 0:
        raise ValueError("invalid singleton or time limit")

    singleton_branch = (singleton,)
    eligible = tuple(
        edge
        for edge in g_edges(adjacency_f)
        if singleton not in edge and branches_touch(adjacency_f, singleton_branch, edge)
    )
    model = cp_model.CpModel()
    selected = tuple(model.new_bool_var(f"e_{left}_{right}") for left, right in eligible)

    for vertex in range(order):
        if vertex == singleton:
            continue
        incident = [selected[index] for index, edge in enumerate(eligible) if vertex in edge]
        if not incident:
            return SingletonResult(singleton, "INFEASIBLE", None)
        model.add(sum(incident) == 1)

    for left_index, left in enumerate(eligible):
        for right_index in range(left_index + 1, len(eligible)):
            right = eligible[right_index]
            if set(left) & set(right):
                continue
            if not branches_touch(adjacency_f, left, right):
                model.add(selected[left_index] + selected[right_index] <= 1)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_seconds
    solver.parameters.num_search_workers = 2
    solver.parameters.log_search_progress = False
    status = solver.solve(model)
    status_name = solver.status_name(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return SingletonResult(singleton, status_name, None)

    pairs: tuple[Edge, ...] = tuple(
        eligible[index] for index, variable in enumerate(selected) if solver.value(variable)
    )
    branches = (singleton_branch, *pairs)
    validate_spanning_model(adjacency_f, branches)
    return SingletonResult(singleton, status_name, branches)


def find_spanning_model(
    adjacency_f: tuple[int, ...],
    *,
    time_limit_seconds: float = 30.0,
) -> tuple[SingletonResult, ...]:
    results: list[SingletonResult] = []
    for singleton in range(len(adjacency_f)):
        result = solve_for_singleton(
            adjacency_f,
            singleton,
            time_limit_seconds=time_limit_seconds,
        )
        results.append(result)
        if result.model is not None:
            break
    return tuple(results)


def solve_all_singletons(
    adjacency_f: tuple[int, ...],
    *,
    time_limit_seconds: float = 30.0,
) -> tuple[SingletonResult, ...]:
    return tuple(
        solve_for_singleton(
            adjacency_f,
            singleton,
            time_limit_seconds=time_limit_seconds,
        )
        for singleton in range(len(adjacency_f))
    )


def validate_spanning_model(
    adjacency_f: tuple[int, ...],
    branches: tuple[Branch, ...],
) -> None:
    if len(branches) != 20:
        raise ValueError("the model does not have twenty branches")
    if sum(len(branch) == 1 for branch in branches) != 1:
        raise ValueError("the model does not have exactly one singleton")
    if sum(len(branch) == 2 for branch in branches) != 19:
        raise ValueError("the model does not have exactly nineteen pairs")
    if sum(map(len, branches)) != len(adjacency_f):
        raise ValueError("the model is not spanning")
    validate_complete_minor(adjacency_f, branches)
