from __future__ import annotations

from collections.abc import Iterable

from ortools.sat.python import cp_model

from hadwiger_alpha2_order39_support_search.certificate import SUPPORTS
from hadwiger_alpha2_order39_support_search.supports import (
    FULL,
    N_COORDS,
    N_SUPPORTS,
    TYPES,
    Violation,
    hall_violations,
)


def build_model(
    cuts: Iterable[Violation],
) -> tuple[cp_model.CpModel, tuple[cp_model.IntVar, ...]]:
    model = cp_model.CpModel()
    multiplicities = tuple(
        model.new_int_var(0, min(mask.bit_count(), 9), f"m_{mask:03x}") for mask in TYPES
    )
    active = tuple(model.new_bool_var(f"a_{mask:03x}") for mask in TYPES)

    for value, flag in zip(multiplicities, active, strict=True):
        model.add(value >= flag)
        model.add(value <= N_SUPPORTS * flag)
    certificate_counts = {mask: SUPPORTS.count(mask) for mask in set(SUPPORTS)}
    for index, mask in enumerate(TYPES):
        model.add_hint(multiplicities[index], certificate_counts.get(mask, 0))
        model.add_hint(active[index], int(mask in certificate_counts))

    model.add(sum(multiplicities) == N_SUPPORTS)
    model.add(
        sum(mask.bit_count() * multiplicities[index] for index, mask in enumerate(TYPES)) <= 90
    )
    coordinate_degrees = []
    for coordinate in range(N_COORDS):
        degree = sum(
            multiplicities[index] for index, mask in enumerate(TYPES) if mask & (1 << coordinate)
        )
        coordinate_degrees.append(degree)
        model.add(degree <= 9)
    # Break coordinate-label symmetry.
    for left_degree, right_degree in zip(
        coordinate_degrees[:-1], coordinate_degrees[1:], strict=True
    ):
        model.add(left_degree >= right_degree)

    disjoint_indices: list[tuple[int, ...]] = []
    for index, mask in enumerate(TYPES):
        disjoint = tuple(other_index for other_index, other in enumerate(TYPES) if not mask & other)
        disjoint_indices.append(disjoint)
        disjoint_count = sum(multiplicities[other] for other in disjoint)
        model.add(disjoint_count + mask.bit_count() <= 10).only_enforce_if(active[index])
        for coordinate in range(N_COORDS):
            if mask & (1 << coordinate):
                continue
            cover = sum(
                multiplicities[other] for other in disjoint if TYPES[other] & (1 << coordinate)
            )
            model.add(cover >= 1).only_enforce_if(active[index])

    # Pairwise-disjoint triples necessarily have sizes (3,3,3) or (3,3,4).
    for first_index, first in enumerate(TYPES):
        if first.bit_count() > 4:
            continue
        for second_index in disjoint_indices[first_index]:
            if second_index <= first_index:
                continue
            second = TYPES[second_index]
            if first.bit_count() + second.bit_count() > 7:
                continue
            common_free = FULL ^ (first | second)
            for third_index in range(second_index + 1, len(TYPES)):
                third = TYPES[third_index]
                if third & ~common_free:
                    continue
                model.add(active[first_index] + active[second_index] + active[third_index] <= 2)

    for cut in cuts:
        model.add(sum(multiplicities[index] for index in cut.types) <= cut.bound)

    return model, multiplicities


def solve() -> None:
    cuts: list[Violation] = []
    for iteration in range(1, 100_000):
        model, variables = build_model(cuts)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 120.0
        solver.parameters.num_search_workers = 2
        solver.parameters.search_branching = cp_model.HINT_SEARCH
        solver.parameters.log_search_progress = False
        status = solver.solve(model)
        print(
            f"iteration={iteration} cuts={len(cuts)} "
            f"status={solver.status_name(status)} conflicts={solver.num_conflicts}"
        )
        if status in (cp_model.INFEASIBLE, cp_model.MODEL_INVALID):
            return
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return
        values = tuple(solver.value(variable) for variable in variables)
        violations = hall_violations(values)
        if not violations:
            supports = [
                f"{TYPES[index]:03x}"
                for index, multiplicity in enumerate(values)
                for _ in range(multiplicity)
            ]
            print("MODEL", " ".join(supports))
            return
        print(f"violations={len(violations)}")
        for violation in violations[:5]:
            print(
                f"  {violation.weight}>{violation.bound} "
                f"union={violation.union:03x} family="
                + ",".join(f"{TYPES[index]:03x}^{values[index]}" for index in violation.types)
            )
        cuts.extend(violations)


if __name__ == "__main__":
    solve()
