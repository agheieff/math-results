"""Direct mathematical predicates, independent of the SAT construction."""

from __future__ import annotations

from collections.abc import Collection


def element_frequencies(order: int, family: Collection[int]) -> tuple[int, ...]:
    """Count the selected subsets containing each ground-set element."""

    return tuple(sum((mask >> element) & 1 for mask in family) for element in range(order))


def is_canonical_clean_tight(
    order: int,
    member_count: int,
    family: Collection[int],
) -> bool:
    """Recognize the canonical representatives searched by the CNF."""

    if order < 1:
        return False
    subset_count = 1 << order
    selected = set(family)
    if len(selected) != member_count:
        return False
    if any(mask < 0 or mask >= subset_count for mask in selected):
        return False
    if 0 not in selected or subset_count - 1 not in selected:
        return False
    if any((left | right) not in selected for left in selected for right in selected):
        return False

    frequencies = element_frequencies(order, selected)
    if any(2 * frequency > member_count for frequency in frequencies):
        return False
    if any(frequencies[index] > frequencies[index + 1] for index in range(order - 1)):
        return False

    incidence_columns = {
        tuple(bool(mask & (1 << element)) for mask in sorted(selected)) for element in range(order)
    }
    return len(incidence_columns) == order
