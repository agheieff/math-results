"""Direct predicates used independently of the SAT encoder."""

from __future__ import annotations

from collections.abc import Collection


def frequencies(order: int, family: Collection[int]) -> tuple[int, ...]:
    return tuple(sum(bool(mask & (1 << element)) for mask in family) for element in range(order))


def is_canonical_clean_tight(
    order: int,
    member_count: int,
    family: Collection[int],
) -> bool:
    """Check exactly the mathematical conditions represented by the CNF."""

    subset_count = 1 << order
    members = set(family)
    if len(members) != member_count or 0 not in members or subset_count - 1 not in members:
        return False
    if any(not 0 <= mask < subset_count for mask in members):
        return False
    if any((left | right) not in members for left in members for right in members):
        return False

    counts = frequencies(order, members)
    if any(2 * count > member_count for count in counts):
        return False
    if any(left > right for left, right in zip(counts, counts[1:], strict=False)):
        return False

    columns = {
        tuple(bool(mask & (1 << element)) for mask in range(subset_count) if mask in members)
        for element in range(order)
    }
    return len(columns) == order
