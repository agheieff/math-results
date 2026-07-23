from collections.abc import Iterator
from itertools import combinations

from hadwiger_k7.graph import Graph


def has_complete_minor(graph: Graph, target: int) -> bool:
    """Check all selected vertex sets and all canonical branch-set partitions."""
    if target < 1:
        raise ValueError("target must be positive")
    if target > graph.order:
        return False

    adjacency = [0] * graph.order
    for left, right in graph.edges:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left

    for selected_size in range(target, graph.order + 1):
        for selected in combinations(range(graph.order), selected_size):
            for branch_sets in _partitions(selected, target):
                if not all(_is_connected(mask, adjacency) for mask in branch_sets):
                    continue
                if _all_pairs_touch(branch_sets, adjacency):
                    return True
    return False


def _partitions(vertices: tuple[int, ...], parts: int) -> Iterator[tuple[int, ...]]:
    yield from _extend_partition(vertices, parts, 0, ())


def _extend_partition(
    vertices: tuple[int, ...],
    parts: int,
    index: int,
    blocks: tuple[int, ...],
) -> Iterator[tuple[int, ...]]:
    if len(blocks) + len(vertices) - index < parts:
        return
    if index == len(vertices):
        if len(blocks) == parts:
            yield blocks
        return

    vertex_bit = 1 << vertices[index]
    for block_index in range(len(blocks)):
        updated = list(blocks)
        updated[block_index] |= vertex_bit
        yield from _extend_partition(vertices, parts, index + 1, tuple(updated))
    if len(blocks) < parts:
        yield from _extend_partition(vertices, parts, index + 1, (*blocks, vertex_bit))


def _is_connected(vertices: int, adjacency: list[int]) -> bool:
    reached = 0
    frontier = vertices & -vertices
    while frontier:
        vertex_bit = frontier & -frontier
        frontier ^= vertex_bit
        reached |= vertex_bit
        vertex = vertex_bit.bit_length() - 1
        frontier |= adjacency[vertex] & vertices & ~reached
    return reached == vertices


def _all_pairs_touch(branch_sets: tuple[int, ...], adjacency: list[int]) -> bool:
    for left_index, left in enumerate(branch_sets):
        for right in branch_sets[left_index + 1 :]:
            if not _touch(left, right, adjacency):
                return False
    return True


def _touch(left: int, right: int, adjacency: list[int]) -> bool:
    remaining = left
    while remaining:
        vertex_bit = remaining & -remaining
        remaining ^= vertex_bit
        vertex = vertex_bit.bit_length() - 1
        if adjacency[vertex] & right:
            return True
    return False
