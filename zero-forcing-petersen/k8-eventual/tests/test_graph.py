import pytest

from zero_forcing_petersen_k8_eventual.graph import adjacency, edges
from zero_forcing_petersen_k8_eventual.minor import reduced_edges, residue_base


def test_graph_and_minor() -> None:
    for n in range(25, 121):
        assert len(edges(n)) == 3 * n
        assert all(neighbors.bit_count() == 3 for neighbors in adjacency(n))
        assert reduced_edges(n) == edges(n - 8)


def test_residue_bases() -> None:
    for n in range(65, 401):
        base = residue_base(n)
        assert base in range(65, 73)
        assert base <= n
        assert (n - base) % 8 == 0


def test_domains() -> None:
    with pytest.raises(ValueError):
        edges(16)
    with pytest.raises(ValueError):
        reduced_edges(24)
    with pytest.raises(ValueError):
        residue_base(64)
