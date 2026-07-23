"""Build and run the exact C++ exhaustion, then audit the two extremizers."""

import json
import subprocess
from pathlib import Path

from signed_circulant.exact import (
    characteristic_polynomial,
    expected_extremal_polynomial,
    verify_target_isolation,
)
from signed_circulant.model import TARGET_MASKS, matrix_from_mask


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_enumerator(root: Path) -> Path:
    build = root / ".build"
    build.mkdir(exist_ok=True)
    executable = build / "enumerate"
    subprocess.run(
        [
            "c++",
            "-O3",
            "-std=c++20",
            "-Wall",
            "-Wextra",
            "-Werror",
            str(root / "cpp" / "enumerate.cpp"),
            "-o",
            str(executable),
        ],
        check=True,
    )
    return executable


def verify_extremizers() -> None:
    expected = expected_extremal_polynomial()
    for mask in TARGET_MASKS:
        actual = characteristic_polynomial(matrix_from_mask(mask))
        if actual != expected:
            raise AssertionError(f"unexpected characteristic polynomial for mask {mask}")
    verify_target_isolation()


def main() -> None:
    root = project_root()
    executable = build_enumerator(root)
    completed = subprocess.run([executable], check=True, capture_output=True, text=True)
    result = json.loads(completed.stdout)
    saved = json.loads((root / "artifacts" / "n20-certificate.json").read_text())
    for key, value in result.items():
        if saved.get(key) != value:
            raise AssertionError(f"saved certificate disagrees at {key}")
    if tuple(result["unresolved_masks"]) != TARGET_MASKS:
        raise AssertionError("C++ exhaustion and independent twisted construction disagree")
    verify_extremizers()
    if saved["extremal_characteristic_polynomial"] != list(expected_extremal_polynomial()):
        raise AssertionError("saved characteristic polynomial disagrees")
    print(completed.stdout.strip())
    print("independent_extremal_charpoly=PASS")
