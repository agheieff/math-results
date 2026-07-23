from zero_forcing_petersen_k7_eventual.graph import adjacency, edges
from zero_forcing_petersen_k7_eventual.minor import reduced_edges, residue_base


def test_graph_and_minor() -> None:
    for n in range(22, 101):
        assert len(edges(n)) == 3 * n
        assert all(neighbors.bit_count() == 3 for neighbors in adjacency(n))
        assert reduced_edges(n) == edges(n - 7)


def test_residue_bases() -> None:
    for n in range(50, 351):
        base = residue_base(n)
        assert base in (50, 51, 52, 53, 54, 55, 56)
        assert base <= n
        assert (n - base) % 7 == 0
