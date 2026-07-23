"""Compile and run the exact native balanced-separator DP."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SeparatorResult:
    n: int
    counterexample: bool
    layer_counts: tuple[int, ...]
    layer_xor: tuple[str, ...]
    layer_sum: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        digest = hashlib.sha256()
        for count, xor_value, sum_value in zip(
            self.layer_counts, self.layer_xor, self.layer_sum, strict=True
        ):
            digest.update(f"{count}:{xor_value}:{sum_value}|".encode())
        return {
            "n": self.n,
            "boundary_at_most_eleven_exists": self.counterexample,
            "layers": len(self.layer_counts),
            "maximum_states": max(self.layer_counts),
            "layer_counts": list(self.layer_counts),
            "state_set_transcript_sha256": digest.hexdigest(),
        }


def native_source_path() -> Path:
    return Path(__file__).with_name("native_separator.cpp")


def native_source_digest() -> str:
    return hashlib.sha256(native_source_path().read_bytes()).hexdigest()


def _parse_values(value: str, converter: type[int] = int) -> tuple[int, ...]:
    return tuple(converter(part) for part in value.split(","))


def _parse_result(line: str) -> SeparatorResult:
    fields = dict(field.split("=", 1) for field in line.split())
    if fields.keys() != {"n", "counterexample", "counts", "xor", "sum"}:
        raise AssertionError(f"unexpected native output: {line}")
    n = int(fields["n"])
    counts = _parse_values(fields["counts"])
    xor_values = tuple(fields["xor"].split(","))
    sum_values = tuple(fields["sum"].split(","))
    if not len(counts) == len(xor_values) == len(sum_values) == n - 4:
        raise AssertionError("native transcript has the wrong number of layers")
    return SeparatorResult(
        n,
        bool(int(fields["counterexample"])),
        counts,
        xor_values,
        sum_values,
    )


def run_separator_dp(orders: Iterable[int]) -> tuple[SeparatorResult, ...]:
    requested = tuple(orders)
    if not requested or any(not 11 <= n <= 33 for n in requested):
        raise ValueError("orders must be a nonempty subset of [11,33]")
    compiler = shutil.which("c++")
    if compiler is None:
        raise RuntimeError("a C++20 compiler is required")

    with tempfile.TemporaryDirectory(prefix="petersen-k5-separator-") as temporary:
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
                str(native_source_path()),
                "-o",
                str(executable),
            ],
            check=True,
            timeout=120,
        )
        completed = subprocess.run(
            [str(executable), *(str(n) for n in requested)],
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
    results = tuple(_parse_result(line) for line in completed.stdout.splitlines())
    if tuple(result.n for result in results) != requested:
        raise AssertionError("native verifier returned the wrong orders")
    return results


def transcript_digest(results: tuple[SeparatorResult, ...]) -> str:
    digest = hashlib.sha256()
    for result in results:
        digest.update(f"{result.n}:{int(result.counterexample)}|".encode())
        for count, xor_value, sum_value in zip(
            result.layer_counts, result.layer_xor, result.layer_sum, strict=True
        ):
            digest.update(f"{count}:{xor_value}:{sum_value}|".encode())
    return digest.hexdigest()
