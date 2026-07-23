from hadwiger_k7.graph import Graph


def has_complete_minor(graph: Graph, target: int) -> bool:
    """Independently search for pairwise touching, disjoint connected sets."""
    if target < 1:
        raise ValueError("target must be positive")
    if target > graph.order:
        return False

    neighbours = tuple(_neighbour_mask(graph, vertex) for vertex in range(graph.order))
    maximum_size = graph.order - target + 1
    candidates = tuple(
        mask
        for mask in range(1, 1 << graph.order)
        if mask.bit_count() <= maximum_size and _connected(mask, neighbours)
    )
    return _choose_branch_sets(candidates, neighbours, target, 0, 0, ())


def _neighbour_mask(graph: Graph, vertex: int) -> int:
    result = 0
    for left, right in graph.edges:
        if left == vertex:
            result |= 1 << right
        elif right == vertex:
            result |= 1 << left
    return result


def _connected(vertices: int, neighbours: tuple[int, ...]) -> bool:
    first = (vertices & -vertices).bit_length() - 1
    visited = 1 << first
    pending = visited
    while pending:
        current = (pending & -pending).bit_length() - 1
        pending &= ~(1 << current)
        additions = neighbours[current] & vertices & ~visited
        visited |= additions
        pending |= additions
    return visited == vertices


def _choose_branch_sets(
    candidates: tuple[int, ...],
    neighbours: tuple[int, ...],
    target: int,
    start: int,
    used: int,
    chosen: tuple[int, ...],
) -> bool:
    needed = target - len(chosen)
    if needed == 0:
        return True
    if len(candidates) - start < needed:
        return False

    for index in range(start, len(candidates)):
        candidate = candidates[index]
        if candidate & used:
            continue
        if any(not _sets_touch(candidate, previous, neighbours) for previous in chosen):
            continue
        if _choose_branch_sets(
            candidates,
            neighbours,
            target,
            index + 1,
            used | candidate,
            (*chosen, candidate),
        ):
            return True
    return False


def _sets_touch(left: int, right: int, neighbours: tuple[int, ...]) -> bool:
    vertices = left
    touching_vertices = 0
    while vertices:
        current_bit = vertices & -vertices
        vertices ^= current_bit
        touching_vertices |= neighbours[current_bit.bit_length() - 1]
    return bool(touching_vertices & right)
