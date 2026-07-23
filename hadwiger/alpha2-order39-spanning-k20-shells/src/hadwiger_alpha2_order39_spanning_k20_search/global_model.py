from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from ortools.sat.python import cp_model

from hadwiger_alpha2_order39_spanning_k20_search.certificate import SEED_SUPPORTS
from hadwiger_alpha2_order39_spanning_k20_search.supports import (
    FULL,
    N_COORDS,
    N_SUPPORTS,
    TYPES,
    HallViolation,
    SupportState,
    multiplicities,
)


@dataclass(frozen=True)
class SupportModel:
    model: cp_model.CpModel
    variables: tuple[cp_model.IntVar, ...]


def build_support_model(
    cuts: Iterable[HallViolation] = (),
    *,
    l1_distance: int | None = None,
    hint: SupportState = SEED_SUPPORTS,
    break_coordinate_symmetry: bool = True,
) -> SupportModel:
    model = cp_model.CpModel()
    variables = tuple(
        model.new_int_var(0, min(mask.bit_count(), 9), f"m_{mask:03x}") for mask in TYPES
    )
    active = tuple(model.new_bool_var(f"a_{mask:03x}") for mask in TYPES)
    hint_values = multiplicities(hint)

    for variable, flag, value in zip(variables, active, hint_values, strict=True):
        model.add(variable >= flag)
        model.add(variable <= N_SUPPORTS * flag)
        model.add_hint(variable, value)
        model.add_hint(flag, int(value > 0))

    model.add(sum(variables) == N_SUPPORTS)
    model.add(sum(mask.bit_count() * variables[index] for index, mask in enumerate(TYPES)) <= 90)
    coordinate_degrees = tuple(
        sum(variables[index] for index, mask in enumerate(TYPES) if mask & (1 << coordinate))
        for coordinate in range(N_COORDS)
    )
    for degree in coordinate_degrees:
        model.add(degree <= 9)
    if break_coordinate_symmetry:
        for left, right in zip(coordinate_degrees[:-1], coordinate_degrees[1:], strict=True):
            model.add(left >= right)

    disjoint_indices: list[tuple[int, ...]] = []
    for index, mask in enumerate(TYPES):
        disjoint = tuple(other_index for other_index, other in enumerate(TYPES) if not mask & other)
        disjoint_indices.append(disjoint)
        disjoint_count = sum(variables[other] for other in disjoint)
        model.add(disjoint_count + mask.bit_count() <= 10).only_enforce_if(active[index])
        for coordinate in range(N_COORDS):
            if mask & (1 << coordinate):
                continue
            cover = sum(variables[other] for other in disjoint if TYPES[other] & (1 << coordinate))
            model.add(cover >= 1).only_enforce_if(active[index])

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
                if TYPES[third_index] & ~common_free:
                    continue
                model.add(active[first_index] + active[second_index] + active[third_index] <= 2)

    for cut in cuts:
        model.add(sum(variables[index] for index in cut.types) <= cut.bound)
    if l1_distance is not None:
        _add_l1_shell(model, variables, l1_distance)
    return SupportModel(model, variables)


def pin_support_state(support_model: SupportModel, supports: SupportState) -> None:
    values = multiplicities(supports)
    for variable, value in zip(support_model.variables, values, strict=True):
        support_model.model.add(variable == value)


def _add_l1_shell(
    model: cp_model.CpModel,
    variables: tuple[cp_model.IntVar, ...],
    distance: int,
) -> None:
    if distance <= 0 or distance % 2:
        raise ValueError("the L1 distance must be a positive even integer")
    seed_values = multiplicities(SEED_SUPPORTS)
    deviations: list[cp_model.LinearExprT] = []
    for index, (variable, seed_value) in enumerate(zip(variables, seed_values, strict=True)):
        if not seed_value:
            deviations.append(variable)
            continue
        deviation = model.new_int_var(0, 9, f"d_{index}")
        model.add_abs_equality(deviation, variable - seed_value)
        deviations.append(deviation)
    model.add(sum(deviations) == distance)
