"""Compile and run the exact partitioned balanced-separator DP."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

ORDERS = tuple(range(64, 73))
THREAD_COUNT = 6


@dataclass(frozen=True)
class SeparatorRun:
    orders: tuple[int, ...]
    closure_counts: tuple[int, ...]
    closure_xor: tuple[str, ...]
    closure_sum: tuple[str, ...]
    layer_counts: tuple[int, ...]
    layer_xor: tuple[str, ...]
    layer_sum: tuple[str, ...]

    def closure_records(self) -> list[dict[str, object]]:
        return [
            {
                "n": order,
                "boundary_at_most_seventeen_exists": count > 0,
                "reduced_closure_states": count,
                "closure_xor": xor_value,
                "closure_sum": sum_value,
            }
            for order, count, xor_value, sum_value in zip(
                self.orders,
                self.closure_counts,
                self.closure_xor,
                self.closure_sum,
                strict=True,
            )
        ]


def native_source_path() -> Path:
    return Path(__file__).with_name("native_separator.cpp")


def frozen_transcript_path() -> Path:
    return Path(__file__).resolve().parents[2] / "artifacts" / "native-transcript.txt"


def native_source_digest() -> str:
    return hashlib.sha256(native_source_path().read_bytes()).hexdigest()


def frozen_transcript_file_digest() -> str:
    return hashlib.sha256(frozen_transcript_path().read_bytes()).hexdigest()


def _integers(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split(","))


def _strings(value: str) -> tuple[str, ...]:
    return tuple(value.split(","))


def parse_result(line: str) -> SeparatorRun:
    fields = dict(field.split("=", 1) for field in line.split())
    expected_fields = {
        "orders",
        "closed",
        "closed_xor",
        "closed_sum",
        "counts",
        "xor",
        "sum",
    }
    if fields.keys() != expected_fields:
        raise AssertionError(f"unexpected native output: {line}")
    result = SeparatorRun(
        _integers(fields["orders"]),
        _integers(fields["closed"]),
        _strings(fields["closed_xor"]),
        _strings(fields["closed_sum"]),
        _integers(fields["counts"]),
        _strings(fields["xor"]),
        _strings(fields["sum"]),
    )
    if result.orders != ORDERS:
        raise AssertionError("native verifier returned the wrong orders")
    if not (
        len(result.closure_counts)
        == len(result.closure_xor)
        == len(result.closure_sum)
        == len(ORDERS)
    ):
        raise AssertionError("native closure transcript has the wrong length")
    if not (
        len(result.layer_counts) == len(result.layer_xor) == len(result.layer_sum) == 72 - 8 + 1
    ):
        raise AssertionError("native layer transcript has the wrong length")
    return result


def frozen_separator_run() -> SeparatorRun:
    lines = frozen_transcript_path().read_text().splitlines()
    if len(lines) != 1:
        raise AssertionError("frozen verifier transcript must contain one line")
    return parse_result(lines[0])


def run_separator_dp() -> SeparatorRun:
    compiler = shutil.which("c++")
    if compiler is None:
        raise RuntimeError("a C++20 compiler is required")
    with tempfile.TemporaryDirectory(prefix="petersen-k8-separator-") as temporary:
        executable = Path(temporary) / "separator"
        subprocess.run(
            [
                compiler,
                "-std=c++20",
                "-O3",
                "-DNDEBUG",
                "-Wall",
                "-Wextra",
                "-Wpedantic",
                "-pthread",
                str(native_source_path()),
                "-o",
                str(executable),
            ],
            check=True,
            timeout=120,
        )
        completed = subprocess.run(
            [str(executable), str(THREAD_COUNT)],
            check=True,
            capture_output=True,
            text=True,
            timeout=7200,
        )
    lines = completed.stdout.splitlines()
    if len(lines) != 1:
        raise AssertionError("native verifier returned an unexpected number of lines")
    return parse_result(lines[0])


def transcript_digest(result: SeparatorRun) -> str:
    digest = hashlib.sha256()
    for values in (
        result.orders,
        result.closure_counts,
        result.closure_xor,
        result.closure_sum,
        result.layer_counts,
        result.layer_xor,
        result.layer_sum,
    ):
        digest.update(",".join(str(value) for value in values).encode())
        digest.update(b"|")
    return digest.hexdigest()
