from __future__ import annotations


def common_original_neighbors(order: int, degree_x: int, degree_y: int) -> int:
    """Count common original-graph neighbours of an edge's ends in a triangle-free complement."""
    if order < 2 or not 1 <= degree_x < order or not 1 <= degree_y < order:
        raise ValueError("invalid order or degrees")
    return order - degree_x - degree_y


def forced_disjoint_neighbors(
    outside_order: int,
    subset_size: int,
    point_degree_bound: int,
) -> int:
    """Lower-bound vertices with disjoint incidence sets.

    For subset sizes one and two, every selected point occurs at most
    ``point_degree_bound`` times. In the size-two case the current vertex
    lies in both point classes, so their union loses at least one.
    """
    if outside_order < 2 or subset_size not in {0, 1, 2} or point_degree_bound < 1:
        raise ValueError("invalid outside order, subset size, or degree bound")
    if subset_size == 0:
        return outside_order - 1
    if subset_size == 1:
        return outside_order - point_degree_bound
    return outside_order - (2 * point_degree_bound - 1)


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


def minimum_capacity_numerator(order: int, clique_bound: int) -> int:
    """Minimise twice the seagull capacity over feasible numerical cases."""
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
