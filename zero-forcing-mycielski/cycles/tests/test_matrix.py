from zero_forcing_mycielski.matrix import (
    has_graph_support,
    q4_certificate_matrix,
    q5_certificate_matrix,
    rational_rank,
)
from zero_forcing_mycielski.model import MycielskiCycle


def test_q4_integral_certificate() -> None:
    graph = MycielskiCycle.build(4)
    matrix = q4_certificate_matrix()
    assert has_graph_support(graph, matrix)
    assert rational_rank(matrix) == 4
    assert graph.vertex_count - rational_rank(matrix) == 5


def test_q5_integral_certificate() -> None:
    graph = MycielskiCycle.build(5)
    matrix = q5_certificate_matrix()
    assert has_graph_support(graph, matrix)
    assert rational_rank(matrix) == 6
    assert graph.vertex_count - rational_rank(matrix) == 5
