from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from union_closed_tight_m16.certificates import load_manifest, sha256


def test_sha256(tmp_path: Path) -> None:
    path = tmp_path / "bytes"
    path.write_bytes(b"m=16\n")
    assert sha256(path) == hashlib.sha256(b"m=16\n").hexdigest()


def test_manifest_rejects_wrong_target(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text(
        json.dumps(
            {
                "format_version": 1,
                "order": 8,
                "member_count": 15,
                "variables": 1,
                "clauses": 1,
                "cnf_sha256": "0" * 64,
                "drat": {
                    "file": "x",
                    "compressed_sha256": "0" * 64,
                    "compressed_bytes": 0,
                    "uncompressed_sha256": "0" * 64,
                    "uncompressed_bytes": 0,
                },
                "lrat": {
                    "file": "y",
                    "compressed_sha256": "0" * 64,
                    "compressed_bytes": 0,
                    "uncompressed_sha256": "0" * 64,
                    "uncompressed_bytes": 0,
                },
                "solver": {"path": "s", "sha256": "0" * 64},
                "drat_checker": {"path": "d", "sha256": "0" * 64},
                "lrat_checker": {"path": "l", "sha256": "0" * 64},
                "timeout_seconds_per_stage": 1,
                "stage_wall_seconds": {},
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="fixed target"):
        load_manifest(path)
