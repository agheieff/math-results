from spherical_zero_sum_h3.h3 import certify_h3, zero_sum_edges_exact
from spherical_zero_sum_h3.roots import h3_roots


def test_exact_h3_certificate() -> None:
    certificate = certify_h3()
    assert certificate.vertices == 30
    assert certificate.zero_sum_triples == 20
    assert certificate.independence_number == 20
    assert len(zero_sum_edges_exact(h3_roots())) == 20
