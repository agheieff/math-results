from spherical_zero_sum_h3.geometry import (
    a3_shared_axis_points,
    critical_orientations,
    h3_float_roots,
    zero_sum_edges_float,
)
from spherical_zero_sum_h3.optimizer import independence_number


def test_float_baselines_match_exact_counts() -> None:
    h3 = h3_float_roots()
    a3 = a3_shared_axis_points()
    h3_edges = zero_sum_edges_float(h3)
    a3_edges = zero_sum_edges_float(a3)
    assert len(h3_edges) == 20
    assert len(a3_edges) == 8
    assert independence_number(len(h3), h3_edges, workers=1) == 20
    assert independence_number(len(a3), a3_edges, workers=1) == 8


def test_critical_orientation_counts() -> None:
    h3 = h3_float_roots()
    a3 = a3_shared_axis_points()
    assert len(critical_orientations(a3, a3)) == 3
    assert len(critical_orientations(h3, a3)) == 6
    assert len(critical_orientations(h3, h3)) == 6
