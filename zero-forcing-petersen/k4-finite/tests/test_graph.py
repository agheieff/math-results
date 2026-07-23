import pytest

from zero_forcing_petersen_k4.graph import GeneralizedPetersen


@pytest.mark.parametrize("n", [9, 10, 17, 22, 47])
def test_graph_is_simple_cubic(n: int) -> None:
    graph = GeneralizedPetersen(n)
    assert len(graph.neighbor_masks) == 2 * n
    assert all(neighbors.bit_count() == 3 for neighbors in graph.neighbor_masks)
    for vertex, neighbors in enumerate(graph.neighbor_masks):
        for other in range(graph.order):
            assert bool(neighbors >> other & 1) == bool(graph.neighbor_masks[other] >> vertex & 1)


def test_invalid_simple_graph_parameter() -> None:
    with pytest.raises(ValueError):
        GeneralizedPetersen(8)
