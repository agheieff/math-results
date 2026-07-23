import pytest

from zero_forcing_mycielski import MycielskiCycle


@pytest.mark.parametrize("order", [4, 5, 6, 13])
def test_graph_structure(order: int) -> None:
    graph = MycielskiCycle.build(order)
    assert graph.vertex_count == 2 * order + 1
    assert graph.edge_count == 4 * order
    assert [neighbors.bit_count() for neighbors in graph.adjacency[:order]] == [4] * order
    assert [neighbors.bit_count() for neighbors in graph.adjacency[order : 2 * order]] == [
        3
    ] * order
    assert graph.adjacency[graph.apex].bit_count() == order

    for left in range(graph.vertex_count):
        for right in range(left + 1, graph.vertex_count):
            if not graph.adjacency[left] & (1 << right):
                continue
            assert graph.adjacency[left] & graph.adjacency[right] == 0


@pytest.mark.parametrize("order", [0, 3])
def test_invalid_order_rejected(order: int) -> None:
    with pytest.raises(ValueError):
        MycielskiCycle.build(order)
