from zero_forcing_mycielski_paths.forcing import (
    closure_mask,
    maximum_two_set_closure,
    replay_forces,
    vertex_mask,
)
from zero_forcing_mycielski_paths.model import MycielskiPath


def test_uniform_three_set_forces() -> None:
    for order in range(3, 65):
        graph = MycielskiPath.build(order)
        assert replay_forces(graph) == (1 << graph.vertex_count) - 1


def test_order_two_is_a_five_cycle_with_zero_forcing_number_two() -> None:
    graph = MycielskiPath.build(2)
    assert sorted(row.bit_count() for row in graph.adjacency) == [2] * 5
    assert closure_mask(graph, vertex_mask((0, 1))) == (1 << 5) - 1
    assert all(closure_mask(graph, 1 << vertex) != (1 << 5) - 1 for vertex in range(5))


def test_no_two_set_in_regression_range() -> None:
    for order in range(3, 17):
        graph = MycielskiPath.build(order)
        assert maximum_two_set_closure(graph) < graph.vertex_count
