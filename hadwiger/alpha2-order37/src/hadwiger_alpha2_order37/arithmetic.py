from __future__ import annotations


def disjoint_support_lower_bound(
    outside_order: int,
    support_size: int,
    maximum_degree: int,
    removed_disjoint_vertices: int = 0,
) -> int:
    """Bound disjoint supports after optionally removing known disjoint vertices."""
    if outside_order < 2 or support_size not in {1, 2}:
        raise ValueError("invalid outside order or support size")
    if not 1 <= maximum_degree < outside_order or removed_disjoint_vertices < 0:
        raise ValueError("invalid maximum degree or removal count")
    intersecting_upper = maximum_degree if support_size == 1 else 2 * maximum_degree - 1
    return outside_order - intersecting_upper - removed_disjoint_vertices


def outside_neighbor_budget(maximum_degree: int, support_size: int) -> int:
    """Upper-bound F-neighbours outside the stable core."""
    if maximum_degree < 0 or not 0 <= support_size <= maximum_degree:
        raise ValueError("invalid degree or support size")
    return maximum_degree - support_size


def good_degree_lower_bound(
    outside_order: int,
    support_size: int,
    maximum_degree: int,
    removed_disjoint_vertices: int = 0,
) -> int:
    """Lower-bound good-pair degree after paying the F-neighbour budget."""
    return disjoint_support_lower_bound(
        outside_order,
        support_size,
        maximum_degree,
        removed_disjoint_vertices,
    ) - outside_neighbor_budget(maximum_degree, support_size)


def possible_two_component_orders(
    total_order: int,
    cut_order: int,
    clique_bound: int,
) -> tuple[tuple[int, int], ...]:
    """List unordered component orders when both components are bounded cliques."""
    remaining = total_order - cut_order
    if remaining < 2 or clique_bound < 1:
        raise ValueError("invalid orders")
    return tuple(
        (left, remaining - left)
        for left in range(1, remaining // 2 + 1)
        if left <= remaining - left <= clique_bound
    )


def antimatching_lower_bound(order: int, clique_bound: int) -> int:
    """Bound a matching from the maximum possible number of unmatched vertices."""
    if order < 0 or not 0 <= clique_bound <= order:
        raise ValueError("invalid order or clique bound")
    return (order - clique_bound + 1) // 2


def minimum_capacity_numerator(
    order: int,
    clique_bound: int,
    excluded_case: tuple[int, int] | None = None,
) -> int:
    """Minimise twice the capacity, optionally excluding one separately handled case."""
    if order < 1 or not 1 <= clique_bound <= order:
        raise ValueError("invalid order or clique bound")
    candidates = [
        order - clique_order + mixed_order
        for clique_order in range(1, clique_bound + 1)
        for mixed_order in range(order - clique_order + 1)
        if (clique_order, mixed_order) != excluded_case
    ]
    return min(candidates)
