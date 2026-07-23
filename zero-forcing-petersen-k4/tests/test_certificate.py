import json
from pathlib import Path

from zero_forcing_petersen_k4.certificate import build_certificate


def test_frozen_certificate() -> None:
    expected = json.loads(Path("artifacts/certificate-summary.json").read_text())
    assert build_certificate() == expected
