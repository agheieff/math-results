from laplacian_hook_eleven_deletions.character import (
    character_ratios,
    expected_character_ratios,
)


def test_character_ratios_through_eight_points() -> None:
    for order in range(9, 64, 2):
        assert character_ratios(order) == expected_character_ratios(order)
