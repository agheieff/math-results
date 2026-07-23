"""The three-column minor reduction for finite P(n,3)."""

FiniteVertex = tuple[str, int]
Edge = frozenset[FiniteVertex]


def _edge(left: FiniteVertex, right: FiniteVertex) -> Edge:
    return frozenset((left, right))


def petersen_edges(order: int) -> frozenset[Edge]:
    if order < 7:
        raise ValueError("P(n,3) requires n at least seven")
    edges: set[Edge] = set()
    for index in range(order):
        edges.add(_edge(("u", index), ("u", (index + 1) % order)))
        edges.add(_edge(("u", index), ("v", index)))
        edges.add(_edge(("v", index), ("v", (index + 3) % order)))
    if any(len(edge) != 2 for edge in edges) or len(edges) != 3 * order:
        raise AssertionError("finite generalized Petersen graph was not simple cubic")
    return frozenset(edges)


def reduced_minor_edges(order: int) -> frozenset[Edge]:
    """Delete three spokes and contract the six exposed degree-two vertices."""
    if order < 10:
        raise ValueError("the target P(n-3,3) requires n at least ten")
    removed = range(order - 3, order)
    deleted_spokes = {_edge(("u", index), ("v", index)) for index in removed}

    def image(vertex: FiniteVertex) -> FiniteVertex:
        layer, index = vertex
        if layer == "u" and index >= order - 3:
            return ("u", order - 4)
        if layer == "v" and index >= order - 3:
            return ("v", index - 3)
        return vertex

    result: set[Edge] = set()
    for edge in petersen_edges(order) - deleted_spokes:
        left, right = tuple(edge)
        mapped = _edge(image(left), image(right))
        if len(mapped) == 2:
            result.add(mapped)
    return frozenset(result)
