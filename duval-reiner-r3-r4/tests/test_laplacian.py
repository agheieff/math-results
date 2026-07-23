from duval_reiner_r3_r4.families import mask_from_facets
from duval_reiner_r3_r4.laplacian import (
    gram_matrix,
    partial_degree_sum,
    vertex_degrees,
)


def test_signed_boundary_gram_matrix() -> None:
    mask = mask_from_facets(4, ((0, 1, 2), (0, 1, 3)))
    assert gram_matrix(4, mask) == ((3, 1), (1, 3))
    degrees = vertex_degrees(4, mask)
    assert degrees == (2, 2, 1, 1)
    assert partial_degree_sum(degrees, 3) == 6
