import pytest

from zero_forcing_mycielski_paths.model import MycielskiPath


def test_order_and_edges() -> None:
    graph = MycielskiPath.build(7)
    assert graph.vertex_count == 15
    assert sum(row.bit_count() for row in graph.adjacency) // 2 == 4 * 7 - 3


def test_small_order_rejected() -> None:
    with pytest.raises(ValueError):
        MycielskiPath.build(1)
