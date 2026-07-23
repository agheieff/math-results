import pytest

from zero_forcing_petersen_general_transfer.graph import (
    petersen_adjacency,
    petersen_edges,
)


def test_graph_is_simple_cubic() -> None:
    for k in range(1, 9):
        for n in range(2 * k + 1, 7 * k + 4):
            assert len(petersen_edges(n, k)) == 3 * n
            assert all(neighbors.bit_count() == 3 for neighbors in petersen_adjacency(n, k))


def test_invalid_graph_parameters_fail() -> None:
    with pytest.raises(ValueError):
        petersen_edges(8, 4)
