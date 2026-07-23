"""Bitset model of the generalized Petersen graph P(n,3)."""

from __future__ import annotations


def petersen_adjacency(n: int) -> tuple[int, ...]:
    if n < 7:
        raise ValueError("P(n,3) is simple and cubic only for n at least seven")
    adjacency = [0] * (2 * n)

    def add_edge(left: int, right: int) -> None:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left

    for index in range(n):
        add_edge(index, (index + 1) % n)
        add_edge(index, n + index)
        add_edge(n + index, n + ((index + 3) % n))
    result = tuple(adjacency)
    if any(mask.bit_count() != 3 for mask in result):
        raise AssertionError("P(n,3) construction is not cubic")
    return result


def closure(adjacency: tuple[int, ...], initial: int) -> int:
    full_mask = (1 << len(adjacency)) - 1
    if initial & ~full_mask:
        raise ValueError("initial mask contains a nonexistent vertex")
    black = initial
    while True:
        additions = 0
        sources = black
        while sources:
            source_bit = sources & -sources
            sources -= source_bit
            source = source_bit.bit_length() - 1
            white_neighbors = adjacency[source] & ~black
            if white_neighbors.bit_count() == 1:
                additions |= white_neighbors
        updated = black | additions
        if updated == black:
            return black
        black = updated


def _rotate(bits: int, distance: int, n: int, layer_mask: int) -> int:
    distance %= n
    if distance == 0:
        return bits
    return ((bits << distance) | (bits >> (n - distance))) & layer_mask


def boundary_size(n: int, selected: int) -> int:
    """Count selected vertices adjacent to at least one unselected vertex."""
    layer_mask = (1 << n) - 1
    if selected & ~((1 << (2 * n)) - 1):
        raise ValueError("selected mask contains a nonexistent vertex")
    outer = selected & layer_mask
    inner = (selected >> n) & layer_mask
    interior_outer = (
        outer & _rotate(outer, 1, n, layer_mask) & _rotate(outer, -1, n, layer_mask) & inner
    )
    interior_inner = (
        inner & _rotate(inner, 3, n, layer_mask) & _rotate(inner, -3, n, layer_mask) & outer
    )
    return (outer ^ interior_outer).bit_count() + (inner ^ interior_inner).bit_count()


def generic_boundary_size(adjacency: tuple[int, ...], selected: int) -> int:
    full_mask = (1 << len(adjacency)) - 1
    outside = full_mask ^ selected
    boundary = 0
    remaining = selected
    while remaining:
        vertex_bit = remaining & -remaining
        remaining -= vertex_bit
        vertex = vertex_bit.bit_length() - 1
        if adjacency[vertex] & outside:
            boundary |= vertex_bit
    return boundary.bit_count()
