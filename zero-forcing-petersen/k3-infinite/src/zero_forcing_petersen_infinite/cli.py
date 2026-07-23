"""Replay the saved exact structural certificate."""

import json
from pathlib import Path
from typing import Any

from .certificate import build_certificate, certificate_sha256


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> None:
    generated = build_certificate()
    path = project_root() / "artifacts" / "certificate-summary.json"
    saved: dict[str, Any] = json.loads(path.read_text())
    if generated != saved:
        raise AssertionError("saved certificate disagrees with exact replay")
    print(
        "certificate=PASS "
        f"kernel_dimension={generated['kernel']['dimension']} "  # type: ignore[index]
        f"minor_orders={len(generated['minor_lemma']['verified_orders'])} "  # type: ignore[index]
        f"sha256={certificate_sha256(generated)}"
    )
