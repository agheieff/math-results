from __future__ import annotations

from collections.abc import Sequence
from functools import cache

Branch = tuple[int, ...]


def edge_count(adjacency: Sequence[int]) -> int:
    return sum(mask.bit_count() for mask in adjacency) // 2


def is_triangle_free(adjacency: Sequence[int]) -> bool:
    for left, mask in enumerate(adjacency):
        for right in _vertices(mask):
            if left < right and adjacency[left] & adjacency[right]:
                return False
    return True


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
    """Decide perfect-matching existence by exact memoized branching."""
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
    return all(has_perfect_matching(adjacency, full & ~(1 << vertex)) for vertex in range(35))


def contraction_critical_edge_count(adjacency_f: Sequence[int]) -> int:
    """Count G-edges whose contraction has chromatic number 17."""
    order = len(adjacency_f)
    full = (1 << order) - 1
    certified = 0
    for left in range(order):
        for right in range(left + 1, order):
            if adjacency_f[left] >> right & 1:
                continue
            common = adjacency_f[left] & adjacency_f[right]
            while common:
                witness_bit = common & -common
                common ^= witness_bit
                remainder = full & ~(1 << left) & ~(1 << right) & ~witness_bit
                if has_perfect_matching(adjacency_f, remainder):
                    certified += 1
                    break
    return certified


def complement_connectivity(adjacency_f: Sequence[int]) -> int:
    """Compute connectivity of the complement via a maximum biclique in F."""
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


def encode_graph6(adjacency: Sequence[int]) -> str:
    order = len(adjacency)
    if not 0 <= order <= 62:
        raise ValueError("only short graph6 order is supported")
    bits = [adjacency[left] >> right & 1 for right in range(1, order) for left in range(right)]
    bits.extend([0] * (-len(bits) % 6))
    payload = "".join(
        chr(63 + sum(bits[start + offset] << (5 - offset) for offset in range(6)))
        for start in range(0, len(bits), 6)
    )
    return chr(63 + order) + payload


def validate_complete_minor(adjacency_f: Sequence[int], branches: Sequence[Branch]) -> None:
    order = len(adjacency_f)
    used = 0
    for branch in branches:
        mask = sum(1 << vertex for vertex in branch)
        if not branch or any(not 0 <= vertex < order for vertex in branch):
            raise ValueError("invalid branch")
        if mask.bit_count() != len(branch) or used & mask:
            raise ValueError("branch sets are not disjoint")
        if not _connected_in_complement(adjacency_f, mask):
            raise ValueError("branch is not connected")
        used |= mask

    for index, left in enumerate(branches):
        for right in branches[index + 1 :]:
            if not any(_g_edge(adjacency_f, u, v) for u in left for v in right):
                raise ValueError("branch sets do not touch")


def _vertices(mask: int) -> tuple[int, ...]:
    return tuple(vertex for vertex in range(mask.bit_length()) if mask >> vertex & 1)


def _g_edge(adjacency_f: Sequence[int], left: int, right: int) -> bool:
    return left != right and not adjacency_f[left] >> right & 1


def _connected_in_complement(adjacency_f: Sequence[int], branch: int) -> bool:
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
