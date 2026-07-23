from __future__ import annotations

from dataclasses import dataclass
from functools import cache

N_COORDS = 10
N_SUPPORTS = 28
FULL = (1 << N_COORDS) - 1
TYPES = tuple(mask for mask in range(1, FULL + 1) if 3 <= mask.bit_count() <= 10)
INDEX = {mask: index for index, mask in enumerate(TYPES)}


@dataclass(frozen=True)
class Violation:
    types: tuple[int, ...]
    union: int
    weight: int

    @property
    def bound(self) -> int:
        return min(self.union.bit_count(), 9)


def multiplicities(supports: tuple[int, ...]) -> tuple[int, ...]:
    values = [0] * len(TYPES)
    for mask in supports:
        values[INDEX[mask]] += 1
    return tuple(values)


def hall_violations(values: tuple[int, ...]) -> tuple[Violation, ...]:
    if len(values) != len(TYPES) or any(value < 0 for value in values):
        raise ValueError("invalid support multiplicities")
    active = tuple(index for index, value in enumerate(values) if value)
    if not active:
        return ()

    weights = tuple(values[index] for index in active)
    masks = tuple(TYPES[index] for index in active)
    adjacency: list[int] = [0] * len(active)
    for i, first in enumerate(masks):
        for j in range(i + 1, len(active)):
            if first & masks[j]:
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i

    @cache
    def maximum_weight_clique(candidates: int) -> tuple[int, int]:
        if not candidates:
            return (0, 0)
        bit = candidates & -candidates
        vertex = bit.bit_length() - 1
        without = maximum_weight_clique(candidates ^ bit)
        nested_weight, nested_bits = maximum_weight_clique((candidates ^ bit) & adjacency[vertex])
        with_vertex = (nested_weight + weights[vertex], nested_bits | bit)
        return max(without, with_vertex)

    found: dict[tuple[int, ...], Violation] = {}
    for allowed_union in range(1, FULL + 1):
        candidates = 0
        for vertex, mask in enumerate(masks):
            if not mask & ~allowed_union:
                candidates |= 1 << vertex
        weight, chosen_bits = maximum_weight_clique(candidates)
        if not chosen_bits:
            continue
        chosen = tuple(
            active[vertex] for vertex in range(len(active)) if chosen_bits & (1 << vertex)
        )
        actual_union = 0
        for index in chosen:
            actual_union |= TYPES[index]
        violation = Violation(chosen, actual_union, weight)
        if violation.weight > violation.bound:
            found[chosen] = violation
    return tuple(
        sorted(
            found.values(),
            key=lambda violation: (
                violation.weight - violation.bound,
                violation.weight,
                violation.types,
            ),
            reverse=True,
        )
    )
