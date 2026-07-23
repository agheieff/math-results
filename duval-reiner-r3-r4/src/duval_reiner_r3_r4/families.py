from __future__ import annotations

import math
from functools import cache
from itertools import combinations, permutations

Facet = tuple[int, int, int]


@cache
def all_facets(vertex_count: int) -> tuple[Facet, ...]:
    if vertex_count < 0:
        raise ValueError("vertex count must be nonnegative")
    return tuple(combinations(range(vertex_count), 3))


def selected_indices(mask: int, facet_count: int) -> tuple[int, ...]:
    if mask < 0 or mask >= 1 << facet_count:
        raise ValueError("family mask is outside the facet universe")
    return tuple(index for index in range(facet_count) if mask >> index & 1)


def selected_facets(vertex_count: int, mask: int) -> tuple[Facet, ...]:
    facets = all_facets(vertex_count)
    return tuple(facets[index] for index in selected_indices(mask, len(facets)))


def mask_from_facets(vertex_count: int, family: tuple[Facet, ...]) -> int:
    index = {facet: position for position, facet in enumerate(all_facets(vertex_count))}
    mask = 0
    for facet in family:
        normalized = tuple(sorted(facet))
        if len(set(normalized)) != 3 or normalized not in index:
            raise ValueError(f"invalid facet {facet}")
        mask |= 1 << index[normalized]
    if mask.bit_count() != len(family):
        raise ValueError("family contains a repeated facet")
    return mask


@cache
def permutation_actions(vertex_count: int) -> tuple[tuple[int, ...], ...]:
    facets = all_facets(vertex_count)
    index = {facet: position for position, facet in enumerate(facets)}
    actions = []
    for permutation in permutations(range(vertex_count)):
        action = []
        for facet in facets:
            image = tuple(sorted(permutation[vertex] for vertex in facet))
            action.append(index[image])  # type: ignore[index]
        actions.append(tuple(action))
    return tuple(actions)


def transform_mask(mask: int, action: tuple[int, ...]) -> int:
    transformed = 0
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        transformed |= 1 << action[bit.bit_length() - 1]
        remaining -= bit
    return transformed


def orbit_representatives(vertex_count: int) -> tuple[int, ...]:
    facet_count = len(all_facets(vertex_count))
    if facet_count > 20:
        raise ValueError("orbit marking is intentionally limited to at most 20 possible facets")

    actions = permutation_actions(vertex_count)
    seen = bytearray(1 << facet_count)
    representatives = []
    for mask in range(1 << facet_count):
        if seen[mask]:
            continue
        representatives.append(mask)
        for action in actions:
            seen[transform_mask(mask, action)] = 1
    return tuple(representatives)


def induced_cycle_count(action: tuple[int, ...]) -> int:
    unseen = set(range(len(action)))
    cycles = 0
    while unseen:
        cycles += 1
        current = next(iter(unseen))
        while current in unseen:
            unseen.remove(current)
            current = action[current]
    return cycles


def burnside_orbit_count(vertex_count: int) -> int:
    total = sum(1 << induced_cycle_count(action) for action in permutation_actions(vertex_count))
    group_order = math.factorial(vertex_count)
    quotient, remainder = divmod(total, group_order)
    if remainder:
        raise AssertionError("Burnside average is not integral")
    return quotient
