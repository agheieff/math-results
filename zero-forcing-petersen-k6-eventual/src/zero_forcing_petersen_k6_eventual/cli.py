"""Command-line frozen-certificate replay."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .certificate import build_certificate


def main() -> None:
    certificate = build_certificate()
    artifact = Path(__file__).resolve().parents[2] / "artifacts" / "certificate-summary.json"
    expected = json.loads(artifact.read_text())
    if certificate != expected:
        raise SystemExit("generated certificate does not match the frozen artifact")
    encoded = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
    print(f"certificate=PASS sha256={hashlib.sha256(encoded).hexdigest()}")
