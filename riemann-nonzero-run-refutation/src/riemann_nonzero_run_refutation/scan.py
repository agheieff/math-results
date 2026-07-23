import gzip
import hashlib
import math
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from .certificate import Witness
from .theta import distance_to_integer, height_with_offset, theta_over_pi


@dataclass(frozen=True)
class SourceRow:
    row: int
    offset_text: str
    offset: float
    derivative_text: str
    derivative: float


@dataclass(frozen=True)
class ScanResult:
    gaps: int
    histogram: dict[int, int]
    forbidden_gaps: int
    first_forbidden_left_row: int
    ambiguous_endpoints: int


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def rows(zeros_path: Path, derivatives_path: Path) -> Iterator[SourceRow]:
    with (
        gzip.open(zeros_path, "rt", encoding="ascii") as zeros,
        gzip.open(derivatives_path, "rt", encoding="ascii") as derivatives,
    ):
        for row, (zero_line, derivative_line) in enumerate(zip(zeros, derivatives, strict=True), 1):
            zero_parts = zero_line.split()
            derivative_text = derivative_line.strip()
            if zero_parts == ["-1"] or derivative_text == "-1":
                break
            if len(zero_parts) != 2:
                raise ValueError(f"invalid zero row {row}")
            offset_text = f"{zero_parts[0]}{zero_parts[1][1:]}"
            yield SourceRow(
                row,
                offset_text,
                float(zero_parts[0]) + float(zero_parts[1]),
                derivative_text,
                float(derivative_text),
            )


class ThetaFloor:
    def __init__(self, base_height: Decimal) -> None:
        base_q = theta_over_pi(base_height)
        self.base_height = base_height
        self.base_floor = int(base_q // 1)
        self.base_fraction = float(base_q - self.base_floor)
        self.slope = 0.5 * math.log(float(base_height) / (2 * math.pi)) / math.pi

    def classify(self, row: SourceRow) -> tuple[int, bool]:
        relative = self.base_fraction + self.slope * row.offset
        relative_floor = math.floor(relative)
        fraction = relative - relative_floor
        if min(fraction, 1 - fraction) >= 1e-6:
            return self.base_floor + relative_floor, False
        exact = theta_over_pi(height_with_offset(self.base_height, Decimal(row.offset_text)))
        return int(exact // 1), distance_to_integer(exact) < Decimal("1e-9")


def full_scan(zeros_path: Path, derivatives_path: Path, base_height: Decimal) -> ScanResult:
    theta_floor = ThetaFloor(base_height)
    iterator = rows(zeros_path, derivatives_path)
    previous = next(iterator)
    previous_floor, previous_ambiguous = theta_floor.classify(previous)
    histogram: Counter[int] = Counter()
    forbidden = 0
    first_forbidden = 0
    ambiguous_rows: set[int] = set()
    if previous_ambiguous:
        ambiguous_rows.add(previous.row)

    for current in iterator:
        current_floor, current_ambiguous = theta_floor.classify(current)
        if current_ambiguous:
            ambiguous_rows.add(current.row)
        count = current_floor - previous_floor
        histogram[count] += 1
        first_index = previous_floor + 1
        first_positive = previous.derivative * (-1 if first_index % 2 else 1) > 0
        is_forbidden = count >= 5 or (count == 4 and first_positive)
        if is_forbidden:
            forbidden += 1
            if not first_forbidden:
                first_forbidden = previous.row
        previous = current
        previous_floor = current_floor

    return ScanResult(
        sum(histogram.values()),
        dict(sorted(histogram.items())),
        forbidden,
        first_forbidden,
        len(ambiguous_rows),
    )


def verify_sources(zeros_path: Path, derivatives_path: Path, witness: Witness) -> None:
    assert sha256_file(zeros_path) == witness["sources"]["zeros_sha256"]
    assert sha256_file(derivatives_path) == witness["sources"]["derivatives_sha256"]
    wanted = {witness["left"]["row"], witness["right"]["row"]}
    selected = {row.row: row for row in rows(zeros_path, derivatives_path) if row.row in wanted}
    for key in ("left", "right"):
        endpoint = witness[key]
        row = selected[endpoint["row"]]
        expected_offset = f"{endpoint['integer_offset']}{endpoint['fractional_offset'][1:]}"
        assert row.offset_text == expected_offset
        assert row.derivative_text == endpoint["derivative"]
