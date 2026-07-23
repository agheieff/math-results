from zero_forcing_petersen_infinite.minor import petersen_edges, reduced_minor_edges


def test_three_column_minor_reduction() -> None:
    for order in range(10, 31):
        assert reduced_minor_edges(order) == petersen_edges(order - 3)
