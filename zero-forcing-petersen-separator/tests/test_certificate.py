import json
from pathlib import Path

from zero_forcing_petersen_separator.certificate import certify_separator_theorem


def test_full_certificate() -> None:
    certificate = certify_separator_theorem()
    assert certificate.threshold == 17
    assert certificate.excluded_range == (17, 98)
    assert certificate.recurrence_start == 99
    assert len(certificate.n16_boundary) == 7


def test_frozen_artifact_matches_certificate() -> None:
    artifact_path = Path(__file__).parents[1] / "artifacts" / "certificate-summary.json"
    artifact = json.loads(artifact_path.read_text())
    assert artifact == certify_separator_theorem().as_dict()
