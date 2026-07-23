from zero_forcing_petersen_k8_eventual.certificate import build_certificate
from zero_forcing_petersen_k8_eventual.separator import frozen_separator_run


def test_fast_certificate_from_frozen_transcript() -> None:
    certificate = build_certificate(frozen_separator_run())
    assert certificate["status"] == "PASS"
    assert certificate["theorem"] == "Z(P(n,8))=18 for every integer n>=65"
