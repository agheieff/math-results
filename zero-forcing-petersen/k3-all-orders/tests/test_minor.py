from zero_forcing_petersen_all_orders.minor import (
    petersen_edges,
    reduced_minor_edges,
    residue_base,
    verify_minor_model,
)


def test_three_column_topological_minor() -> None:
    for n in range(10, 101):
        assert reduced_minor_edges(n) == petersen_edges(n - 3)
        assert verify_minor_model(n)


def test_repeated_reduction_reaches_three_bases() -> None:
    for n in range(14, 501):
        base = residue_base(n)
        assert base in (14, 15, 16)
        assert n >= base
        assert (n - base) % 3 == 0
