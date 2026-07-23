from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CensusResult:
    n: int
    necklaces: int
    forcing_necklaces: int
    first_witness: int
    replay_digest_sha256: str

    def as_dict(self) -> dict[str, object]:
        return {
            "n": self.n,
            "cyclic_orbits_tested": self.necklaces,
            "forcing_orbits": self.forcing_necklaces,
            "first_forcing_witness_mask": self.first_witness or None,
            "replay_digest_sha256": self.replay_digest_sha256,
        }


def native_source_path() -> Path:
    return Path(__file__).with_name("native_census.cpp")


def native_source_digest() -> str:
    return hashlib.sha256(native_source_path().read_bytes()).hexdigest()


def _parse_result(line: str) -> CensusResult:
    fields = dict(field.split("=", 1) for field in line.split())
    required = {"n", "necklaces", "forcing", "first_witness", "sha256"}
    if fields.keys() != required:
        raise AssertionError(f"unexpected native census output: {line}")
    return CensusResult(
        n=int(fields["n"]),
        necklaces=int(fields["necklaces"]),
        forcing_necklaces=int(fields["forcing"]),
        first_witness=int(fields["first_witness"]),
        replay_digest_sha256=fields["sha256"],
    )


def run_census(orders: Iterable[int]) -> tuple[CensusResult, ...]:
    requested = tuple(orders)
    if not requested or any(not 9 <= n <= 31 for n in requested):
        raise ValueError("orders must be a nonempty iterable contained in [9,31]")
    compiler = shutil.which("c++")
    if compiler is None:
        raise RuntimeError("a C++20 compiler is required for the exact census")

    with tempfile.TemporaryDirectory(prefix="petersen-k4-") as temporary:
        executable = Path(temporary) / "census"
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
                "-lcrypto",
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
        raise AssertionError("native census returned the wrong orders")
    return results
