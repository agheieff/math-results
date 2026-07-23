from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from functools import cache
from itertools import combinations

N_COORDS = 10
N_SUPPORTS = 28
ORDER = 39
FULL_COORDS = (1 << N_COORDS) - 1

Branch = tuple[int, ...]


def support_errors(supports: Sequence[int]) -> tuple[str, ...]:
    errors: list[str] = []
    if len(supports) != N_SUPPORTS:
        errors.append("support count is not 28")
    if any(mask <= 0 or mask & ~FULL_COORDS for mask in supports):
        errors.append("a support is outside the ten-coordinate universe")
    if any(mask.bit_count() < 3 for mask in supports):
        errors.append("a support has size below three")
    if sum(mask.bit_count() for mask in supports) > 90:
        errors.append("total incidence exceeds 90")

    coordinate_degrees = tuple(
        sum(mask >> coordinate & 1 for mask in supports) for coordinate in range(N_COORDS)
    )
    if any(degree > 9 for degree in coordinate_degrees):
        errors.append("a coordinate occurs more than nine times")

    counts = Counter(supports)
    active = tuple(counts)
    for mask in active:
        disjoint_count = sum(value for other, value in counts.items() if not mask & other)
        if mask.bit_count() + disjoint_count > 10:
            errors.append(f"degree budget fails at {mask:03x}")
        covered = 0
        for other in active:
            if not mask & other:
                covered |= other
        if (FULL_COORDS ^ mask) & ~covered:
            errors.append(f"diameter-two coverage fails at {mask:03x}")

    if any(
        not (first & second or first & third or second & third)
        for first, second, third in combinations(active, 3)
    ):
        errors.append("three active support types are pairwise disjoint")
    return tuple(errors)


def apply_switch_path(
    supports: Sequence[int],
    path: Sequence[tuple[tuple[int, int], tuple[int, int]]],
) -> tuple[int, ...]:
    current = list(supports)
    for removed, added in path:
        for mask in removed:
            current.remove(mask)
        current.extend(added)
        current.sort()
    return tuple(current)


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


def edge_count(adjacency: Sequence[int]) -> int:
    return sum(mask.bit_count() for mask in adjacency) // 2


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


def non_dominating_complement_edge_count(adjacency_f: Sequence[int]) -> int:
    return sum(
        bool(adjacency_f[left] & adjacency_f[right])
        for left in range(len(adjacency_f))
        for right in range(left + 1, len(adjacency_f))
        if not adjacency_f[left] >> right & 1
    )


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
            raise ValueError("a branch is not connected in G")
        used |= mask

    for index, left in enumerate(branches):
        for right in branches[index + 1 :]:
            if not any(_g_edge(adjacency_f, u, v) for u in left for v in right):
                raise ValueError("two branch sets do not touch")


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
