import pytest

from duval_reiner_r3_r4.families import burnside_orbit_count, orbit_representatives


@pytest.mark.parametrize(
    ("vertex_count", "expected"),
    [(3, 2), (4, 5), (5, 34), (6, 2136)],
)
def test_orbit_representative_counts(vertex_count: int, expected: int) -> None:
    assert len(orbit_representatives(vertex_count)) == expected


def test_seven_vertex_burnside_boundary() -> None:
    assert burnside_orbit_count(7) == 7_013_320
    with pytest.raises(ValueError, match="at most 20"):
        orbit_representatives(7)
