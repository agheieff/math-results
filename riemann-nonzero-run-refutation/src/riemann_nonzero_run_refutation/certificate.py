import hashlib
import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import TypedDict, cast

from .theta import distance_to_integer, height_with_offset, theta_over_pi


class Endpoint(TypedDict):
    row: int
    integer_offset: str
    fractional_offset: str
    derivative: str
    theta_over_pi: str


class Sources(TypedDict):
    zeros_url: str
    zeros_sha256: str
    derivatives_url: str
    derivatives_sha256: str


class FullScan(TypedDict):
    gaps: int
    gram_count_histogram: dict[str, int]
    forbidden_gaps: int
    first_forbidden_left_row: int


class Witness(TypedDict):
    base_height: str
    sources: Sources
    left: Endpoint
    right: Endpoint
    gram_indices: list[str]
    sign_pattern: str
    full_scan: FullScan


@dataclass(frozen=True)
class Verification:
    artifact_sha256: str
    gram_indices: tuple[int, ...]
    sign_pattern: str
    left_margin: Decimal
    right_margin: Decimal


def load_witness(path: Path) -> Witness:
    return cast(Witness, json.loads(path.read_text()))


def endpoint_height(base: Decimal, endpoint: Endpoint) -> Decimal:
    offset = Decimal(endpoint["integer_offset"]) + Decimal(endpoint["fractional_offset"])
    return height_with_offset(base, offset)


def signs(indices: tuple[int, ...], left_derivative: Decimal) -> str:
    z_sign = 1 if left_derivative > 0 else -1
    return "".join("+" if z_sign * (-1 if index % 2 else 1) > 0 else "-" for index in indices)


def verify_certificate(path: Path) -> Verification:
    raw = path.read_bytes()
    witness = load_witness(path)
    base = Decimal(witness["base_height"])
    left_q = theta_over_pi(endpoint_height(base, witness["left"]))
    right_q = theta_over_pi(endpoint_height(base, witness["right"]))
    tolerance = Decimal("1e-60")
    assert abs(left_q - Decimal(witness["left"]["theta_over_pi"])) < tolerance
    assert abs(right_q - Decimal(witness["right"]["theta_over_pi"])) < tolerance
    assert witness["right"]["row"] == witness["left"]["row"] + 1

    first = int(left_q // 1) + 1
    last = int(right_q // 1)
    indices = tuple(range(first, last + 1))
    assert indices == tuple(map(int, witness["gram_indices"]))
    pattern = signs(indices, Decimal(witness["left"]["derivative"]))
    assert pattern == witness["sign_pattern"] == "+-+-"

    left_margin = distance_to_integer(left_q)
    right_margin = distance_to_integer(right_q)
    assert min(left_margin, right_margin) > Decimal("0.2")
    assert abs(Decimal(witness["left"]["derivative"])) > Decimal("40")
    return Verification(
        hashlib.sha256(raw).hexdigest(),
        indices,
        pattern,
        left_margin,
        right_margin,
    )
