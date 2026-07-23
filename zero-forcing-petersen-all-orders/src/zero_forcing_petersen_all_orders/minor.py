"""The three-column topological-minor reduction."""

from __future__ import annotations

Edge = tuple[int, int]


def _edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def petersen_edges(n: int) -> frozenset[Edge]:
    if n < 7:
        raise ValueError("P(n,3) requires n at least seven")
    edges: set[Edge] = set()
    for index in range(n):
        edges.add(_edge(index, (index + 1) % n))
        edges.add(_edge(index, n + index))
        edges.add(_edge(n + index, n + ((index + 3) % n)))
    if len(edges) != 3 * n:
        raise AssertionError("P(n,3) construction is not simple cubic")
    return frozenset(edges)


def reduced_minor_edges(n: int) -> frozenset[Edge]:
    """Delete three spokes and contract the six exposed degree-two vertices."""
    if n < 10:
        raise ValueError("the target P(n-3,3) requires n at least ten")
    deleted_spokes = {_edge(index, n + index) for index in range(n - 3, n)}

    def image(vertex: int) -> int:
        if vertex < n:
            return n - 4 if vertex >= n - 3 else vertex
        index = vertex - n
        target_n = n - 3
        if index >= n - 3:
            index -= 3
        return target_n + index

    result = {
        _edge(image(left), image(right))
        for left, right in petersen_edges(n) - deleted_spokes
        if image(left) != image(right)
    }
    return frozenset(result)


def minor_branch_sets(n: int) -> tuple[frozenset[int], ...]:
    """Return explicit connected branch sets for the P(n-3,3) minor."""
    if n < 10:
        raise ValueError("the target P(n-3,3) requires n at least ten")
    target_n = n - 3
    branch_sets: list[frozenset[int]] = []
    for index in range(target_n):
        if index == target_n - 1:
            branch_sets.append(frozenset(range(n - 4, n)))
        else:
            branch_sets.append(frozenset((index,)))
    for index in range(target_n):
        vertices = {n + index}
        if index >= n - 6:
            vertices.add(n + index + 3)
        branch_sets.append(frozenset(vertices))
    return tuple(branch_sets)


def verify_minor_model(n: int) -> bool:
    """Check connectivity, disjointness, and the exact quotient edge set."""
    branch_sets = minor_branch_sets(n)
    deleted_spokes = {_edge(index, n + index) for index in range(n - 3, n)}
    remaining_edges = petersen_edges(n) - deleted_spokes
    covered = set().union(*branch_sets)
    if covered != set(range(2 * n)) or sum(map(len, branch_sets)) != 2 * n:
        return False

    owner = {
        vertex: target for target, branch_set in enumerate(branch_sets) for vertex in branch_set
    }
    for branch_set in branch_sets:
        reached = {next(iter(branch_set))}
        while True:
            expanded = reached | {
                endpoint
                for left, right in remaining_edges
                if left in reached or right in reached
                for endpoint in (left, right)
                if endpoint in branch_set
            }
            if expanded == reached:
                break
            reached = expanded
        if reached != set(branch_set):
            return False

    quotient = {
        _edge(owner[left], owner[right])
        for left, right in remaining_edges
        if owner[left] != owner[right]
    }
    return quotient == petersen_edges(n - 3)


def residue_base(n: int) -> int:
    if n < 14:
        raise ValueError("the residue-base reduction is used only for n at least fourteen")
    return 14 + ((n - 14) % 3)
