from laplacian_hook_all.certificate import build_certificate, verify_certificate


def test_symbolic_certificate() -> None:
    certificate = build_certificate()
    verify_certificate(certificate)
    assert certificate.class_counts == {
        "endpoint": 1,
        "q1": 644,
        "q2": 354,
        "q3": 30,
        "q4": 6,
    }
