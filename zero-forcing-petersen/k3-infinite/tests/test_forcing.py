from zero_forcing_petersen_infinite.forcing import (
    force_until_outer_radius,
    verify_block_expansion,
)
from zero_forcing_petersen_infinite.model import outer_interval


def test_eight_outer_vertices_expand_both_ways() -> None:
    for start in range(-8, 9):
        assert outer_interval(start - 1, 10) <= verify_block_expansion(start)


def test_finite_prefixes_of_the_infinite_propagation() -> None:
    for radius in (0, 1, 2, 4, 8, 16):
        black, _ = force_until_outer_radius(radius)
        assert outer_interval(-radius, 8 + 2 * radius) <= black
