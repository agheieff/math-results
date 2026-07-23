from itertools import combinations

from zero_forcing_petersen_all_orders.graph import (
    boundary_size,
    generic_boundary_size,
    petersen_adjacency,
)


def test_specialized_boundary_matches_definition() -> None:
    for n in (7, 8, 13):
        adjacency = petersen_adjacency(n)
        for weight in range(5):
            for chosen in combinations(range(2 * n), weight):
                selected = sum(1 << vertex for vertex in chosen)
                assert boundary_size(n, selected) == generic_boundary_size(adjacency, selected)


def test_specialized_boundary_exhaustively_at_n7() -> None:
    n = 7
    adjacency = petersen_adjacency(n)
    for selected in range(1 << (2 * n)):
        assert boundary_size(n, selected) == generic_boundary_size(adjacency, selected)
