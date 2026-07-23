"""Replay the exact refutation certificate."""

import json
from pathlib import Path
from typing import Any

from laplacian_hook_six_refutation.certificate import build_certificate


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> None:
    generated = build_certificate()
    saved: dict[str, Any] = json.loads(
        (project_root() / "artifacts" / "refutation-certificate.json").read_text()
    )
    if generated != saved:
        raise AssertionError("saved refutation certificate disagrees with replay")
    classes = generated["classes"]
    if not isinstance(classes, list):
        raise TypeError("malformed class table")
    print(
        "certificate=PASS "
        f"classes={len(classes)} "
        f"witnesses={sum(len(item['members']) for item in classes)} "
        f"sha256={generated['witness_payload_sha256']}"
    )
