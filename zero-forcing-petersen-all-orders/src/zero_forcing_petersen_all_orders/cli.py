"""Command-line certificate replay."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .certificate import build_certificate


def main() -> None:
    certificate = build_certificate()
    encoded = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
    expected_path = Path("artifacts/certificate-summary.json")
    expected = json.loads(expected_path.read_text())
    if certificate != expected:
        raise SystemExit("generated certificate does not match the frozen artifact")
    bases = certificate["pathwidth_base_lower_bounds"]
    if not isinstance(bases, list):
        raise AssertionError("base-certificate field is not a list")
    print(f"certificate=PASS bases={len(bases)} sha256={hashlib.sha256(encoded).hexdigest()}")
