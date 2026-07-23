from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from .theta import distance_to_integer, height_with_offset, theta_over_pi


@dataclass(frozen=True)
class Verification:
    artifact_sha256: str
    gram_indices: tuple[int, ...]
    sign_pattern: str
    left_margin: Decimal
    right_margin: Decimal


def _object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _signs(indices: tuple[int, ...], z_value: Decimal) -> str:
    z_sign = 1 if z_value > 0 else -1
    return "".join("+" if z_sign * (-1 if index % 2 else 1) > 0 else "-" for index in indices)


def verify_certificate(path: Path) -> Verification:
    raw = path.read_bytes()
    witness = _object(json.loads(raw), "witness")
    if witness.get("format_version") != 1:
        raise ValueError("unsupported witness format")

    base = Decimal(str(witness["base_height"]))
    zero_table = _object(witness["zero_table"], "zero_table")
    theta_record = _object(witness["theta_over_pi"], "theta_over_pi")
    z_sample = _object(witness["z_sample"], "z_sample")
    sources = _object(witness["sources"], "sources")

    left_offset = Decimal(str(zero_table["left_offset"]))
    right_offset = Decimal(str(zero_table["right_offset"]))
    turing_left = Decimal(str(zero_table["turing_left_offset"]))
    turing_right = Decimal(str(zero_table["turing_right_offset"]))
    if not turing_left < left_offset < right_offset < turing_right:
        raise AssertionError("witness is outside the Turing-checked interval")
    if zero_table["right_line"] != zero_table["left_line"] + 1:
        raise AssertionError("zero-table rows are not adjacent")
    if zero_table["turing_zero_count"] != 220:
        raise AssertionError("unexpected Turing zero count")

    left_q = theta_over_pi(height_with_offset(base, left_offset))
    right_q = theta_over_pi(height_with_offset(base, right_offset))
    tolerance = Decimal("1e-60")
    if abs(left_q - Decimal(str(theta_record["left"]))) >= tolerance:
        raise AssertionError("left theta value changed")
    if abs(right_q - Decimal(str(theta_record["right"]))) >= tolerance:
        raise AssertionError("right theta value changed")

    indices = tuple(range(int(left_q // 1) + 1, int(right_q // 1) + 1))
    expected_indices = tuple(int(value) for value in witness["gram_indices"])
    if indices != expected_indices or len(indices) != 5:
        raise AssertionError("gap does not contain the recorded five Gram indices")

    sample_offset = Decimal(str(z_sample["offset"]))
    sample_value = Decimal(str(z_sample["value"]))
    if not left_offset < sample_offset < right_offset:
        raise AssertionError("Z sample is outside the zero gap")
    if sample_value >= -4000:
        raise AssertionError("Z sample does not robustly establish a negative sign")
    pattern = _signs(indices, sample_value)
    if pattern != witness["sign_pattern"] or pattern != "+-+-+":
        raise AssertionError("sign pattern changed")

    for key in ("zeros_sha256", "maxima_sha256"):
        digest = sources.get(key)
        if not isinstance(digest, str) or len(digest) != 64:
            raise AssertionError(f"invalid source hash: {key}")

    left_margin = distance_to_integer(left_q)
    right_margin = distance_to_integer(right_q)
    if min(left_margin, right_margin) <= Decimal("0.25"):
        raise AssertionError("theta classification lacks the recorded margin")
    return Verification(
        hashlib.sha256(raw).hexdigest(),
        indices,
        pattern,
        left_margin,
        right_margin,
    )
