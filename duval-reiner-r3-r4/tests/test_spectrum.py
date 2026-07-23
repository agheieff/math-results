from duval_reiner_r3_r4.laplacian import gram_matrix, partial_degree_sum, vertex_degrees
from duval_reiner_r3_r4.spectrum import certify_matrix


def _certificate(vertex_count: int, mask: int, index: int) -> object:
    matrix = gram_matrix(vertex_count, mask)
    degrees = vertex_degrees(vertex_count, mask)
    result = certify_matrix(matrix, {index: partial_degree_sum(degrees, index)})
    return result.partial_sums[0]


def test_hardest_screened_cases_have_exact_upper_certificates() -> None:
    r3 = _certificate(6, 3359, 3)
    assert r3.status == "strict"  # type: ignore[attr-defined]
    assert r3.upper_bound < 16  # type: ignore[attr-defined,operator]

    r4 = _certificate(6, 3551, 4)
    assert r4.status == "strict"  # type: ignore[attr-defined]
    assert r4.upper_bound < 22  # type: ignore[attr-defined,operator]


def test_complete_family_has_factor_trace_equality() -> None:
    complete = (1 << 20) - 1
    for index, expected in ((3, 18), (4, 24)):
        certificate = _certificate(6, complete, index)
        assert certificate.status == "equality"  # type: ignore[attr-defined]
        assert certificate.exact_sum == expected  # type: ignore[attr-defined]
