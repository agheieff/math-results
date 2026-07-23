from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import cache
from itertools import combinations

N_COORDS = 10
N_SUPPORTS = 28
FULL = (1 << N_COORDS) - 1
TYPES = tuple(mask for mask in range(1, FULL + 1) if 3 <= mask.bit_count() <= 10)
INDEX = {mask: index for index, mask in enumerate(TYPES)}

SupportState = tuple[int, ...]


@dataclass(frozen=True)
class HallViolation:
    types: tuple[int, ...]
    union: int
    weight: int

    @property
    def bound(self) -> int:
        return min(self.union.bit_count(), 9)


def multiplicities(supports: SupportState) -> tuple[int, ...]:
    values = [0] * len(TYPES)
    for mask in supports:
        values[INDEX[mask]] += 1
    return tuple(values)


def locally_valid(supports: SupportState) -> bool:
    if len(supports) != N_SUPPORTS:
        return False
    if any(mask <= 0 or mask & ~FULL or mask.bit_count() < 3 for mask in supports):
        return False
    if sum(mask.bit_count() for mask in supports) > 90:
        return False
    if any(sum(mask >> coordinate & 1 for mask in supports) > 9 for coordinate in range(N_COORDS)):
        return False

    counts = Counter(supports)
    active = tuple(counts)
    for mask in active:
        disjoint_count = sum(value for other, value in counts.items() if not mask & other)
        if mask.bit_count() + disjoint_count > 10:
            return False
        covered = 0
        for other in active:
            if not mask & other:
                covered |= other
        if (FULL ^ mask) & ~covered:
            return False
    disjoint_adjacency = [0] * len(active)
    for left_index, left in enumerate(active):
        for right_index in range(left_index + 1, len(active)):
            if left & active[right_index]:
                continue
            disjoint_adjacency[left_index] |= 1 << right_index
            disjoint_adjacency[right_index] |= 1 << left_index
    for left_index, neighbors in enumerate(disjoint_adjacency):
        later = neighbors & ~((1 << (left_index + 1)) - 1)
        while later:
            right_bit = later & -later
            later ^= right_bit
            right_index = right_bit.bit_length() - 1
            if disjoint_adjacency[right_index] & later:
                return False
    return True


def hall_violations(values: tuple[int, ...]) -> tuple[HallViolation, ...]:
    if len(values) != len(TYPES) or any(value < 0 for value in values):
        raise ValueError("invalid support multiplicities")
    active = tuple(index for index, value in enumerate(values) if value)
    if not active:
        return ()

    weights = tuple(values[index] for index in active)
    masks = tuple(TYPES[index] for index in active)
    adjacency = [0] * len(active)
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

    found: dict[tuple[int, ...], HallViolation] = {}
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
        violation = HallViolation(chosen, actual_union, weight)
        if violation.weight > violation.bound:
            found[chosen] = violation
    return tuple(
        sorted(
            found.values(),
            key=lambda item: (
                item.weight - item.bound,
                item.weight,
                item.types,
            ),
            reverse=True,
        )
    )


def support_system_valid(supports: SupportState) -> bool:
    return locally_valid(supports) and not hall_violations(multiplicities(supports))


def coordinate_switch_neighbors(supports: SupportState) -> tuple[SupportState, ...]:
    found: set[SupportState] = set()
    for left_index, right_index in combinations(range(len(supports)), 2):
        left = supports[left_index]
        right = supports[right_index]
        left_only = left & ~right
        while left_only:
            left_bit = left_only & -left_only
            left_only ^= left_bit
            right_only = right & ~left
            while right_only:
                right_bit = right_only & -right_only
                right_only ^= right_bit
                candidate = list(supports)
                candidate[left_index] = left ^ left_bit ^ right_bit
                candidate[right_index] = right ^ right_bit ^ left_bit
                switched = tuple(sorted(candidate))
                if switched != supports and locally_valid(switched):
                    found.add(switched)
    return tuple(sorted(found))
