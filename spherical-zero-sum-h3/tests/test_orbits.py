from spherical_zero_sum_h3.geometry import (
    a3_standard_points,
    configuration_key,
    icosahedral_rotation_group,
    mat_vec,
)


def test_natural_icosahedral_a3_orbit() -> None:
    group = icosahedral_rotation_group()
    assert len(group) == 60
    configurations = {
        configuration_key(tuple(mat_vec(rotation, point) for point in a3_standard_points()))
        for rotation in group
    }
    assert len(configurations) == 5
