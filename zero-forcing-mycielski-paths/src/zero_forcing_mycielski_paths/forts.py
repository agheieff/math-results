from .model import MycielskiPath


def is_fort(graph: MycielskiPath, vertices: frozenset[int]) -> bool:
    if not vertices:
        return False
    mask = sum(1 << vertex for vertex in vertices)
    return all(
        (graph.adjacency[vertex] & mask).bit_count() != 1
        for vertex in range(graph.vertex_count)
        if vertex not in vertices
    )


def exceptional_forts(graph: MycielskiPath) -> tuple[frozenset[int], ...]:
    n = graph.order
    if n not in (3, 5):
        raise ValueError("the explicit fort certificate is only for n=3 or n=5")
    even = range(0, n, 2)
    odd = range(1, n, 2)
    return (
        frozenset(graph.original(index) for index in even),
        frozenset(graph.shadow(index) for index in even),
        frozenset(
            [
                *(graph.original(index) for index in odd),
                *(graph.shadow(index) for index in odd),
                graph.apex,
            ]
        ),
    )


def verify_exceptional_forts(graph: MycielskiPath) -> None:
    forts = exceptional_forts(graph)
    if not all(is_fort(graph, fort) for fort in forts):
        raise AssertionError("listed set is not a fort")
    if set().union(*forts) != set(range(graph.vertex_count)):
        raise AssertionError("forts do not cover the graph")
    if any(left & right for i, left in enumerate(forts) for right in forts[i + 1 :]):
        raise AssertionError("forts are not pairwise disjoint")
