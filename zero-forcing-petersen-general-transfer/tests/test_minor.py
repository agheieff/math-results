import pytest

from zero_forcing_petersen_general_transfer.graph import petersen_edges
from zero_forcing_petersen_general_transfer.minor import (
    reduced_minor_edges,
    residue_base,
)


def test_general_k_column_minor() -> None:
    for k in range(1, 13):
        for n in range(3 * k + 1, 10 * k + 9):
            assert reduced_minor_edges(n, k) == petersen_edges(n - k, k)


def test_minor_requires_canonical_target() -> None:
    with pytest.raises(ValueError):
        reduced_minor_edges(12, 4)


def test_residue_bases_cover_every_larger_order() -> None:
    for k in range(1, 13):
        start = 2 * k + 1
        for n in range(start, 20 * k + 20):
            base = residue_base(n, k, start)
            assert start <= base < start + k
            assert base <= n
            assert (n - base) % k == 0
