from duval_reiner_r3_r4.families import mask_from_facets
from duval_reiner_r3_r4.laplacian import gram_matrix, partial_degree_sum, vertex_degrees
from duval_reiner_r3_r4.seeds import F15, F16
from duval_reiner_r3_r4.spectrum import certify_matrix


def _seed_statuses(
    family: tuple[tuple[int, int, int], ...], indices: tuple[int, ...]
) -> dict[int, str]:
    mask = mask_from_facets(7, family)
    matrix = gram_matrix(7, mask)
    degrees = vertex_degrees(7, mask)
    degree_sums = {index: partial_degree_sum(degrees, index) for index in indices}
    certificate = certify_matrix(matrix, degree_sums)
    return {partial.index: partial.status for partial in certificate.partial_sums}


def test_paper_seed_characteristic_polynomial_and_statuses() -> None:
    mask = mask_from_facets(7, F16)
    degrees = vertex_degrees(7, mask)
    certificate = certify_matrix(
        gram_matrix(7, mask),
        {index: partial_degree_sum(degrees, index) for index in (3, 4, 5)},
    )
    factors = {(factor.coefficients, factor.exponent) for factor in certificate.factors}
    assert ((1, -19, 133, -413, 527, -175), 1) in factors
    assert _seed_statuses(F16, (3, 4, 5)) == {
        3: "equality",
        4: "strict",
        5: "violation",
    }
    assert _seed_statuses(F15, (3, 4, 8, 9)) == {
        3: "strict",
        4: "strict",
        8: "violation",
        9: "violation",
    }
