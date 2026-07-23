from __future__ import annotations

from itertools import product

MaskPair = tuple[int, int]


def common_original_neighbors(order: int, degree_x: int, degree_y: int) -> int:
    """Count common original-graph neighbours of an edge's ends in a triangle-free complement."""
    if order < 2 or not 1 <= degree_x < order or not 1 <= degree_y < order:
        raise ValueError("invalid order or degrees")
    return order - degree_x - degree_y


def possible_component_sizes(
    remainder_order: int,
    cut_size: int,
    clique_bound: int,
) -> tuple[tuple[int, int], ...]:
    """List two-component size pairs allowed when both components are cliques."""
    outside = remainder_order - cut_size
    if outside < 2 or clique_bound < 1:
        raise ValueError("invalid remainder, cut, or clique bound")
    return tuple(
        (left, outside - left)
        for left in range(1, outside // 2 + 1)
        if left <= clique_bound and left <= outside - left <= clique_bound
    )


def admissible_cut_vertex_patterns(
    left_size: int,
    right_size: int,
    clique_bound: int,
) -> tuple[MaskPair, ...]:
    """Enumerate local adjacency masks for a vertex in the lifted separator.

    The two sides are anticomplete cliques. The vertex must meet both sides,
    cannot complete a side past the clique bound, and cannot have a non-neighbour
    on both sides when the ambient independence number is at most two.
    """
    if min(left_size, right_size, clique_bound) < 1:
        raise ValueError("sizes and clique bound must be positive")
    full_left = (1 << left_size) - 1
    full_right = (1 << right_size) - 1
    patterns: list[MaskPair] = []
    for left_mask, right_mask in product(range(1 << left_size), range(1 << right_size)):
        if left_mask == 0 or right_mask == 0:
            continue
        if left_mask == full_left and left_size + 1 > clique_bound:
            continue
        if right_mask == full_right and right_size + 1 > clique_bound:
            continue
        misses_left = left_mask != full_left
        misses_right = right_mask != full_right
        if misses_left and misses_right:
            continue
        patterns.append((left_mask, right_mask))
    return tuple(patterns)


def minimum_capacity_numerator(order: int, clique_bound: int) -> int:
    """Minimise twice the seagull capacity over the feasible numerical cases.

    For a clique Q and D the vertices mixed on Q, twice its capacity is
    order - |Q| + |D|. The sole numerical deficit at (|Q|, |D|) =
    (clique_bound, 0) is excluded by the proof's alpha-two/max-clique argument.
    """
    if order < 1 or not 1 <= clique_bound <= order:
        raise ValueError("invalid order or clique bound")
    values = []
    for clique_size in range(1, clique_bound + 1):
        for mixed_size in range(order - clique_size + 1):
            if clique_size == clique_bound and mixed_size == 0:
                continue
            values.append(order - clique_size + mixed_size)
    return min(values)


def matching_lower_bound(order: int, independence_bound: int) -> int:
    """Lower-bound matching size because unmatched vertices form an independent set."""
    if order < 0 or not 0 <= independence_bound <= order:
        raise ValueError("invalid order or independence bound")
    return (order - independence_bound + 1) // 2
