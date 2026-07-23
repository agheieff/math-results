import json
from pathlib import Path
from typing import Any

from laplacian_hook_six_refutation.certificate import build_certificate


def test_saved_certificate_replays() -> None:
    root = Path(__file__).resolve().parents[1]
    saved: dict[str, Any] = json.loads(
        (root / "artifacts" / "refutation-certificate.json").read_text()
    )
    assert build_certificate() == saved
