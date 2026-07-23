from zero_forcing_petersen_k5_eventual.graph import adjacency, edges
from zero_forcing_petersen_k5_eventual.minor import reduced_edges, residue_base


def test_graph_and_minor() -> None:
    for n in range(16, 81):
        assert len(edges(n)) == 3 * n
        assert all(neighbors.bit_count() == 3 for neighbors in adjacency(n))
        assert reduced_edges(n) == edges(n - 5)


def test_residue_bases() -> None:
    for n in range(29, 301):
        base = residue_base(n)
        assert base in (29, 30, 31, 32, 33)
        assert base <= n
        assert (n - base) % 5 == 0
