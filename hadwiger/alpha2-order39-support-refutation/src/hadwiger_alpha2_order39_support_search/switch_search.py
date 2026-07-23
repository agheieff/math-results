from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import cache
from itertools import combinations

from hadwiger_alpha2_order39_support_search.certificate import ONE_DEFECT
from hadwiger_alpha2_order39_support_search.supports import (
    FULL,
    N_COORDS,
    N_SUPPORTS,
    hall_violations,
    multiplicities,
)

SupportState = tuple[int, ...]


@dataclass(frozen=True)
class RadiusResult:
    model: SupportState | None
    model_radius: int | None
    frontier_sizes: tuple[int, ...]
    seen: int


@cache
def _locally_valid(state: SupportState) -> bool:
    if len(state) != N_SUPPORTS:
        return False
    if any(mask <= 0 or mask & ~FULL or mask.bit_count() < 3 for mask in state):
        return False
    if sum(mask.bit_count() for mask in state) > 90:
        return False
    if any(sum(mask >> coordinate & 1 for mask in state) > 9 for coordinate in range(N_COORDS)):
        return False

    counts = Counter(state)
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
    return not any(
        not (first & second or first & third or second & third)
        for first, second, third in combinations(active, 3)
    )


def coordinate_switch_neighbors(state: SupportState) -> tuple[SupportState, ...]:
    found: set[SupportState] = set()
    for left_index, right_index in combinations(range(len(state)), 2):
        left = state[left_index]
        right = state[right_index]
        left_only = left & ~right
        while left_only:
            left_bit = left_only & -left_only
            left_only ^= left_bit
            right_only = right & ~left
            while right_only:
                right_bit = right_only & -right_only
                right_only ^= right_bit
                candidate = list(state)
                candidate[left_index] = left ^ left_bit ^ right_bit
                candidate[right_index] = right ^ right_bit ^ left_bit
                switched = tuple(sorted(candidate))
                if switched != state and _locally_valid(switched):
                    found.add(switched)
    return tuple(sorted(found))


def search_switch_radius(max_radius: int = 7) -> RadiusResult:
    if max_radius < 0:
        raise ValueError("radius must be nonnegative")
    start = tuple(sorted(ONE_DEFECT))
    seen = {start}
    frontier: tuple[SupportState, ...] = (start,)
    frontier_sizes = [1]

    if not hall_violations(multiplicities(start)):
        return RadiusResult(start, 0, tuple(frontier_sizes), len(seen))

    for radius in range(1, max_radius + 1):
        next_frontier: list[SupportState] = []
        for state in frontier:
            for candidate in coordinate_switch_neighbors(state):
                if candidate in seen:
                    continue
                seen.add(candidate)
                if not hall_violations(multiplicities(candidate)):
                    frontier_sizes.append(len(next_frontier) + 1)
                    return RadiusResult(
                        candidate,
                        radius,
                        tuple(frontier_sizes),
                        len(seen),
                    )
                next_frontier.append(candidate)
        frontier = tuple(next_frontier)
        frontier_sizes.append(len(frontier))
        if not frontier:
            break
    return RadiusResult(None, None, tuple(frontier_sizes), len(seen))


def main() -> None:
    result = search_switch_radius()
    for radius, size in enumerate(result.frontier_sizes):
        print(f"radius={radius} frontier={size}")
    print(f"seen={result.seen}")
    if result.model is None:
        print("NO MODEL WITHIN SEARCHED RADIUS")
        return
    print(f"MODEL radius={result.model_radius}")
    print(" ".join(f"{mask:03x}" for mask in result.model))


if __name__ == "__main__":
    main()
