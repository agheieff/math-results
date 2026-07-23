"""Replay the saved exact certificate."""

import json
from pathlib import Path
from typing import Any

from laplacian_hook_eleven_deletions.certificate import build_certificate


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> None:
    generated = build_certificate()
    saved: dict[str, Any] = json.loads(
        (project_root() / "artifacts" / "eleven-deletion-certificate.json").read_text()
    )
    if generated != saved:
        raise AssertionError("saved certificate disagrees with exact replay")
    stable = generated["stable_symbolic_audit"]
    if not isinstance(stable, dict):
        raise TypeError("malformed stable audit")
    print(
        "certificate=PASS "
        f"classes={generated['stable_class_count']} "
        f"pairs={stable['pair_count']} "
        f"q6_identities={stable['q6_identity_pair_count']} "
        f"q7_identities={stable['q7_identity_pair_count']} "
        f"sha256={stable['signature_certificate_sha256']}"
    )
