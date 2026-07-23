from itertools import combinations

from hadwiger_k7.graph import Graph, degrees, graph_sha256, independent_sets, is_clique
from hadwiger_k7.minor_connected_sets import has_complete_minor as connected_set_check
from hadwiger_k7.minor_partitions import has_complete_minor as partition_check
from hadwiger_k7.obstruction import EXPECTED_ROOK_SHA256, rook_graph
from hadwiger_k7.verify import verify_counterexample


def complete_graph(order: int) -> Graph:
    return Graph(order, frozenset(combinations(range(order), 2)))


def subdivided_k6_with_isolate() -> Graph:
    edges = set(combinations(range(6), 2))
    edges.remove((0, 1))
    edges.update({(0, 6), (1, 6)})
    return Graph(8, frozenset(edges))


def test_minor_checkers_on_controls() -> None:
    for checker in (partition_check, connected_set_check):
        assert checker(complete_graph(6), 6)
        assert checker(subdivided_k6_with_isolate(), 6)
        assert not checker(complete_graph(5), 6)


def test_raw_rook_graph() -> None:
    graph = rook_graph()
    assert graph_sha256(graph) == EXPECTED_ROOK_SHA256
    assert degrees(graph) == (4,) * 9
    assert not any(is_clique(graph, vertices) for vertices in combinations(range(9), 4))
    assert len(independent_sets(graph, 3)) == 6
    assert not independent_sets(graph, 4)


def test_frozen_matching_completion_lemma_is_false() -> None:
    report = verify_counterexample()
    assert report.independent_triples == 6
    assert report.completions_per_triple == (32,) * 6
    assert report.checked_triple_completion_pairs == 192
    assert report.minor_checkers == 2
