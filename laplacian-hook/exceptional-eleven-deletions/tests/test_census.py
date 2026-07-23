from laplacian_hook_eleven_deletions.census import (
    augmentation_census,
    burnside_census,
    feasible_census,
)


def test_independent_censuses() -> None:
    expected = {
        9: (1, 1, 2, 5, 11, 25, 63, 148, 345, 771, 1637, 3252),
        11: (1, 1, 2, 5, 11, 26, 67, 172, 467, 1305, 3664, 10250),
        13: (1, 1, 2, 5, 11, 26, 68, 176, 492, 1446, 4435, 14140),
        15: (1, 1, 2, 5, 11, 26, 68, 177, 496, 1471, 4583, 15036),
        17: (1, 1, 2, 5, 11, 26, 68, 177, 497, 1475, 4608, 15186),
        19: (1, 1, 2, 5, 11, 26, 68, 177, 497, 1476, 4612, 15211),
        21: (1, 1, 2, 5, 11, 26, 68, 177, 497, 1476, 4613, 15215),
        23: (1, 1, 2, 5, 11, 26, 68, 177, 497, 1476, 4613, 15216),
    }
    assert tuple(len(level) for level in augmentation_census()) == expected[23]
    for order, counts in expected.items():
        assert tuple(len(level) for level in feasible_census(order)) == counts
        assert burnside_census(order) == counts
