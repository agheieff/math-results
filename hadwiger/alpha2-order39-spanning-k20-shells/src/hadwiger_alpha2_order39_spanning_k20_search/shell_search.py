from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from itertools import combinations

from hadwiger_alpha2_order39_spanning_k20_search.certificate import SEED_SUPPORTS
from hadwiger_alpha2_order39_spanning_k20_search.supports import (
    FULL,
    N_COORDS,
    SupportState,
    hall_violations,
    locally_valid,
    multiplicities,
)


@dataclass(frozen=True)
class ShellResult:
    distance: int
    exact_indexed_transitions: int
    local_states: tuple[SupportState, ...]
    hall_states: tuple[SupportState, ...]


@cache
def _types_within(mask: int) -> tuple[int, ...]:
    return tuple(
        support
        for support in range(1, FULL + 1)
        if not support & ~mask and support.bit_count() >= 3
    )


def enumerate_shell(distance: int) -> ShellResult:
    return enumerate_shell_from(SEED_SUPPORTS, distance)


def enumerate_shell_from(seed: SupportState, distance: int) -> ShellResult:
    if distance == 4:
        return _enumerate_pair_shell(seed)
    if distance == 6:
        return _enumerate_triple_shell(seed)
    raise ValueError("only the complete distance-four and distance-six shells are implemented")


def _coordinate_degrees(seed: SupportState) -> tuple[int, ...]:
    degrees = tuple(
        sum(support >> coordinate & 1 for support in seed) for coordinate in range(N_COORDS)
    )
    if len(seed) != 28 or any(degree > 9 for degree in degrees):
        raise ValueError("the shell center violates the support count or coordinate caps")
    return degrees


def _capacity_masks(
    seed: SupportState,
    removed: tuple[int, ...],
) -> tuple[int, ...]:
    degrees = _coordinate_degrees(seed)
    masks = [0] * len(removed)
    for coordinate, degree in enumerate(degrees):
        removed_use = sum(support >> coordinate & 1 for support in removed)
        capacity = min(len(removed), removed_use + 9 - degree)
        for level in range(capacity):
            masks[level] |= 1 << coordinate
    return tuple(masks)


def _enumerate_pair_shell(seed: SupportState) -> ShellResult:
    _coordinate_degrees(seed)
    exact_transitions = 0
    local: set[SupportState] = set()
    for left_index, right_index in combinations(range(len(seed)), 2):
        removed = (seed[left_index], seed[right_index])
        removed_types = set(removed)
        base = tuple(
            support for index, support in enumerate(seed) if index not in (left_index, right_index)
        )
        capacity_one, capacity_two = _capacity_masks(seed, removed)
        choices = _types_within(capacity_one)
        for first_index, first in enumerate(choices):
            if first in removed_types:
                continue
            for second in choices[first_index:]:
                if second in removed_types or (first & second) & ~capacity_two:
                    continue
                exact_transitions += 1
                state = tuple(sorted((*base, first, second)))
                if locally_valid(state):
                    local.add(state)
    return _finish(seed, 4, exact_transitions, local)


def _enumerate_triple_shell(seed: SupportState) -> ShellResult:
    _coordinate_degrees(seed)
    exact_transitions = 0
    local: set[SupportState] = set()
    for indices in combinations(range(len(seed)), 3):
        removed = tuple(seed[index] for index in indices)
        removed_types = set(removed)
        base = tuple(support for index, support in enumerate(seed) if index not in indices)
        capacity_one, capacity_two, capacity_three = _capacity_masks(seed, removed)
        choices = _types_within(capacity_one)
        for first_index, added_first in enumerate(choices):
            if added_first in removed_types:
                continue
            for added_second in choices[first_index:]:
                if added_second in removed_types:
                    continue
                if (added_first & added_second) & ~capacity_two:
                    continue
                allowed_third = (
                    (capacity_one & ~(added_first | added_second))
                    | (capacity_two & (added_first ^ added_second))
                    | (capacity_three & added_first & added_second)
                )
                for added_third in _types_within(allowed_third):
                    if added_third < added_second or added_third in removed_types:
                        continue
                    exact_transitions += 1
                    state = tuple(sorted((*base, added_first, added_second, added_third)))
                    if state not in local and locally_valid(state):
                        local.add(state)
    return _finish(seed, 6, exact_transitions, local)


def _finish(
    seed: SupportState,
    distance: int,
    transitions: int,
    local: set[SupportState],
) -> ShellResult:
    seed_values = multiplicities(seed)
    ordered_local = tuple(sorted(local))
    if any(
        sum(
            abs(left - right)
            for left, right in zip(seed_values, multiplicities(state), strict=True)
        )
        != distance
        for state in ordered_local
    ):
        raise AssertionError("the replacement generator left the requested L1 shell")
    hall = tuple(state for state in ordered_local if not hall_violations(multiplicities(state)))
    return ShellResult(distance, transitions, ordered_local, hall)
