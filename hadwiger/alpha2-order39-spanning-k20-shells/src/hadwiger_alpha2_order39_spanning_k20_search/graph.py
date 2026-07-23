from __future__ import annotations

from collections.abc import Sequence
from functools import cache

from hadwiger_alpha2_order39_spanning_k20_search.supports import N_COORDS, N_SUPPORTS

ORDER = 39
FULL_VERTICES = (1 << ORDER) - 1
Edge = tuple[int, int]
Branch = tuple[int, ...]


def complement_adjacency(supports: Sequence[int]) -> tuple[int, ...]:
    if len(supports) != N_SUPPORTS:
        raise ValueError("exactly 28 supports are required")

    adjacency = [0] * ORDER
    core = range(1, N_COORDS + 1)
    outside = range(N_COORDS + 1, ORDER)
    for point in core:
        adjacency[0] |= 1 << point
        adjacency[point] |= 1

    for vertex, support in zip(outside, supports, strict=True):
        for coordinate, point in enumerate(core):
            if support >> coordinate & 1:
                adjacency[vertex] |= 1 << point
                adjacency[point] |= 1 << vertex

    for left_index, left in enumerate(outside):
        for right_index in range(left_index + 1, N_SUPPORTS):
            right = N_COORDS + 1 + right_index
            if not supports[left_index] & supports[right_index]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
    return tuple(adjacency)


def g_edge(adjacency_f: Sequence[int], left: int, right: int) -> bool:
    return left != right and not adjacency_f[left] >> right & 1


def branches_touch(
    adjacency_f: Sequence[int],
    left: Sequence[int],
    right: Sequence[int],
) -> bool:
    return any(g_edge(adjacency_f, u, v) for u in left for v in right)


def edge_count(adjacency: Sequence[int]) -> int:
    return sum(mask.bit_count() for mask in adjacency) // 2


def g_edges(adjacency_f: Sequence[int]) -> tuple[Edge, ...]:
    return tuple(
        (left, right)
        for left in range(len(adjacency_f))
        for right in range(left + 1, len(adjacency_f))
        if g_edge(adjacency_f, left, right)
    )


def is_triangle_free(adjacency: Sequence[int]) -> bool:
    for left, mask in enumerate(adjacency):
        for right in _vertices(mask):
            if left < right and adjacency[left] & adjacency[right]:
                return False
    return True


def diameter_at_most_two(adjacency: Sequence[int]) -> bool:
    return all(
        left == right or adjacency[left] >> right & 1 or bool(adjacency[left] & adjacency[right])
        for left in range(len(adjacency))
        for right in range(len(adjacency))
    )


def maximum_independent_set(adjacency: Sequence[int]) -> tuple[int, ...]:
    order = len(adjacency)
    full = (1 << order) - 1
    complement = tuple(full & ~(1 << vertex) & ~mask for vertex, mask in enumerate(adjacency))
    best: tuple[int, ...] = ()

    def expand(chosen: tuple[int, ...], candidates: int) -> None:
        nonlocal best
        if len(chosen) + candidates.bit_count() <= len(best):
            return
        if not candidates:
            best = chosen
            return
        while candidates:
            if len(chosen) + candidates.bit_count() <= len(best):
                return
            vertex_bit = candidates & -candidates
            candidates ^= vertex_bit
            vertex = vertex_bit.bit_length() - 1
            expand(chosen + (vertex,), candidates & complement[vertex])

    expand((), full)
    return best


def has_perfect_matching(adjacency: Sequence[int], vertices: int) -> bool:
    if vertices.bit_count() % 2:
        return False

    @cache
    def search(remaining: int) -> bool:
        if not remaining:
            return True
        vertex = min(
            _vertices(remaining),
            key=lambda candidate: (adjacency[candidate] & remaining).bit_count(),
        )
        neighbors = adjacency[vertex] & remaining
        while neighbors:
            neighbor_bit = neighbors & -neighbors
            neighbors ^= neighbor_bit
            if search(remaining & ~(1 << vertex) & ~neighbor_bit):
                return True
        return False

    return search(vertices)


def is_factor_critical(adjacency: Sequence[int]) -> bool:
    full = (1 << len(adjacency)) - 1
    return all(
        has_perfect_matching(adjacency, full & ~(1 << vertex)) for vertex in range(len(adjacency))
    )


def complement_connectivity(adjacency_f: Sequence[int]) -> int:
    order = len(adjacency_f)
    maximum_biclique_order = 0
    full = (1 << order) - 1
    for vertex in range(order):
        neighbors = adjacency_f[vertex]
        subset = neighbors
        while subset:
            common = full
            for right in _vertices(subset):
                common &= adjacency_f[right]
            maximum_biclique_order = max(
                maximum_biclique_order,
                subset.bit_count() + common.bit_count(),
            )
            subset = (subset - 1) & neighbors
    return order - maximum_biclique_order


def contraction_critical_edge_count(adjacency_f: Sequence[int]) -> int:
    order = len(adjacency_f)
    full = (1 << order) - 1
    certified = 0
    for left, right in g_edges(adjacency_f):
        common = adjacency_f[left] & adjacency_f[right]
        while common:
            witness_bit = common & -common
            common ^= witness_bit
            remainder = full & ~(1 << left) & ~(1 << right) & ~witness_bit
            if has_perfect_matching(adjacency_f, remainder):
                certified += 1
                break
    return certified


def non_dominating_g_edge_count(adjacency_f: Sequence[int]) -> int:
    return sum(bool(adjacency_f[left] & adjacency_f[right]) for left, right in g_edges(adjacency_f))


def satisfies_explicit_graph_properties(adjacency_f: Sequence[int]) -> bool:
    edges_g = len(g_edges(adjacency_f))
    return (
        is_triangle_free(adjacency_f)
        and diameter_at_most_two(adjacency_f)
        and len(maximum_independent_set(adjacency_f)) == 10
        and is_factor_critical(adjacency_f)
        and complement_connectivity(adjacency_f) >= 20
        and non_dominating_g_edge_count(adjacency_f) == edges_g
        and contraction_critical_edge_count(adjacency_f) == edges_g
    )


def validate_complete_minor(adjacency_f: Sequence[int], branches: Sequence[Branch]) -> None:
    used = 0
    for branch in branches:
        mask = sum(1 << vertex for vertex in branch)
        if not branch or any(not 0 <= vertex < len(adjacency_f) for vertex in branch):
            raise ValueError("invalid branch")
        if mask.bit_count() != len(branch) or used & mask:
            raise ValueError("branch sets are not disjoint")
        if not _connected_in_g(adjacency_f, mask):
            raise ValueError("a branch is not connected in G")
        used |= mask
    for index, left in enumerate(branches):
        for right in branches[index + 1 :]:
            if not branches_touch(adjacency_f, left, right):
                raise ValueError("two branch sets do not touch")


def _vertices(mask: int) -> tuple[int, ...]:
    return tuple(vertex for vertex in range(mask.bit_length()) if mask >> vertex & 1)


def _connected_in_g(adjacency_f: Sequence[int], branch: int) -> bool:
    reached = branch & -branch
    frontier = reached
    while frontier:
        vertex_bit = frontier & -frontier
        frontier ^= vertex_bit
        vertex = vertex_bit.bit_length() - 1
        neighbors = branch & ~(1 << vertex) & ~adjacency_f[vertex]
        new = neighbors & ~reached
        reached |= new
        frontier |= new
    return reached == branch
