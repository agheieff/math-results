import json
from pathlib import Path

from zero_forcing_petersen_k4_separator.certificate import build_certificate


def test_frozen_certificate() -> None:
    artifact = json.loads(
        (Path(__file__).parents[1] / "artifacts" / "certificate-summary.json").read_text()
    )
    assert build_certificate() == artifact
