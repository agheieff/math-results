"""Build and replay the exact C++ exhaustion, then audit both extremizers."""

import json
import subprocess
from pathlib import Path
from typing import Any

from signed_circulant_n26.exact import (
    SEPARATOR_DENOMINATOR,
    SEPARATOR_NUMERATOR,
    characteristic_polynomial,
    expected_extremal_polynomial,
    verify_target_algebra,
)
from signed_circulant_n26.model import (
    CLASS_BITS,
    CLASS_COUNT,
    TARGET_MASKS,
    N,
    matrix_from_mask,
)


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
    verify_target_algebra()


def histogram_total(result: dict[str, Any]) -> int:
    names = ("fast_start_0", "big_start_0", "big_start_1")
    return sum(sum(int(count) for count in result[name].values()) for name in names)


def main() -> None:
    root = project_root()
    executable = build_enumerator(root)
    completed = subprocess.run([executable], check=True, capture_output=True, text=True)
    result: dict[str, Any] = json.loads(completed.stdout)
    saved: dict[str, Any] = json.loads((root / "artifacts" / "n26-certificate.json").read_text())
    saved_summary = {
        key: value for key, value in saved.items() if key != "extremal_characteristic_polynomial"
    }
    if result != saved_summary:
        raise AssertionError("saved certificate disagrees with fresh exhaustion")
    if (
        result["n"] != N
        or result["class_bits"] != CLASS_BITS
        or result["class_count"] != CLASS_COUNT
        or result["separator_square"] != f"{SEPARATOR_NUMERATOR}/{SEPARATOR_DENOMINATOR}"
    ):
        raise AssertionError("enumerator constants disagree with Python model")
    if histogram_total(result) + len(result["unresolved_masks"]) != CLASS_COUNT:
        raise AssertionError("certificate histogram does not cover every class")
    if tuple(result["unresolved_masks"]) != TARGET_MASKS:
        raise AssertionError("enumeration and independent twisted construction disagree")
    verify_extremizers()
    if saved["extremal_characteristic_polynomial"] != list(expected_extremal_polynomial()):
        raise AssertionError("saved characteristic polynomial disagrees")
    print(completed.stdout.strip())
    print("independent_extremal_charpoly=PASS")
