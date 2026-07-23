"""The general k-column topological-minor reduction."""

from __future__ import annotations

from .graph import Edge, Vertex, _edge, petersen_edges, validate_parameters


def reduced_minor_edges(n: int, k: int) -> frozenset[Edge]:
    """Delete the final k spokes and suppress the exposed degree-two vertices."""
    if n < 3 * k + 1:
        raise ValueError("require n >= 3k+1 so the target P(n-k,k) is canonical")
    validate_parameters(n, k)
    target_n = n - k
    deleted_spokes = {_edge(("u", index), ("v", index)) for index in range(target_n, n)}

    def image(vertex: Vertex) -> Vertex:
        layer, index = vertex
        if layer == "u" and index >= target_n:
            return ("u", target_n - 1)
        if layer == "v" and index >= target_n:
            return ("v", index - target_n)
        return vertex

    result: set[Edge] = set()
    for left, right in petersen_edges(n, k) - deleted_spokes:
        mapped_left = image(left)
        mapped_right = image(right)
        if mapped_left != mapped_right:
            result.add(_edge(mapped_left, mapped_right))
    return frozenset(result)


def residue_base(n: int, k: int, base_start: int) -> int:
    if k < 1 or base_start < 2 * k + 1 or n < base_start:
        raise ValueError("invalid transfer parameters")
    return base_start + ((n - base_start) % k)
