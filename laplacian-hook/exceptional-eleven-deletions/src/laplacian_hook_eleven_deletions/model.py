"""Sparse-complement model."""

REFERENCE_ORDER = 23
MAX_DELETIONS = 11

Edge = tuple[int, int]
EdgeSet = frozenset[Edge]
Matrix = tuple[tuple[int, ...], ...]
Polynomial = tuple[int, ...]
ComponentKey = tuple[int, int]
GraphKey = tuple[ComponentKey, ...]

REFERENCE_EDGES = tuple(
    (left, right) for left in range(REFERENCE_ORDER) for right in range(left + 1, REFERENCE_ORDER)
)


def active_support(deleted: EdgeSet) -> int:
    return len({vertex for edge in deleted for vertex in edge})


def compact_edges(deleted: EdgeSet) -> EdgeSet:
    vertices = sorted({vertex for edge in deleted for vertex in edge})
    relabel = {vertex: index for index, vertex in enumerate(vertices)}
    return frozenset((relabel[left], relabel[right]) for left, right in deleted)


def adjacency_from_deleted(deleted: EdgeSet, order: int) -> Matrix:
    if any(vertex >= order for edge in deleted for vertex in edge):
        raise ValueError("deleted graph does not embed")
    return tuple(
        tuple(
            int(left != right and (min(left, right), max(left, right)) not in deleted)
            for right in range(order)
        )
        for left in range(order)
    )
