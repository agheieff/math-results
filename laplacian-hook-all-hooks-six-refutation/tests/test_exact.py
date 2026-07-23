from laplacian_hook_six_refutation.exact import (
    characteristic_polynomial,
    complement_polynomial_from_sparse,
)
from laplacian_hook_six_refutation.model import (
    dense_complement_laplacian,
    normalize_edges,
    sparse_laplacian,
)


def test_triangle_characteristic_polynomial() -> None:
    edges = normalize_edges([(0, 1), (0, 2), (1, 2)])
    assert characteristic_polynomial(sparse_laplacian(edges, 3)) == (1, -6, 9, 0)


def test_complement_transform_matches_direct_matrix() -> None:
    edges = normalize_edges([(0, 1), (0, 2), (1, 3), (2, 3), (4, 5), (4, 6)])
    sparse_factor = (1, -12, 55, -120, 124, -48)
    assert characteristic_polynomial(dense_complement_laplacian(edges, 9)) == (
        complement_polynomial_from_sparse(sparse_factor, 9)
    )
