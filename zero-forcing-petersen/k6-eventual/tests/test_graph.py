from zero_forcing_petersen_k6_eventual.graph import adjacency, edges
from zero_forcing_petersen_k6_eventual.minor import reduced_edges, residue_base


def test_graph_and_minor() -> None:
    for n in range(19, 91):
        assert len(edges(n)) == 3 * n
        assert all(neighbors.bit_count() == 3 for neighbors in adjacency(n))
        assert reduced_edges(n) == edges(n - 6)


def test_residue_bases() -> None:
    for n in range(37, 301):
        base = residue_base(n)
        assert base in (37, 38, 39, 40, 41, 42)
        assert base <= n
        assert (n - base) % 6 == 0
