import json
from pathlib import Path
from typing import Any

from laplacian_hook_eleven_deletions.certificate import build_certificate


def test_saved_certificate_replays() -> None:
    root = Path(__file__).resolve().parents[1]
    saved: dict[str, Any] = json.loads(
        (root / "artifacts" / "eleven-deletion-certificate.json").read_text()
    )
    assert build_certificate() == saved
