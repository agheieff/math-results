from collections import Counter

from laplacian_hook_all.graphs import complement_types, connected_types


def test_complete_census() -> None:
    assert len(connected_types()) == 22
    graphs = complement_types()
    assert len(graphs) == 46
    assert Counter(graph.edge_count for graph in graphs) == {
        0: 1,
        1: 1,
        2: 2,
        3: 5,
        4: 11,
        5: 26,
    }
