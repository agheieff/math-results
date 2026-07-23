"""Build and replay the fixed target's retained DRAT and LRAT certificates."""

from __future__ import annotations

import hashlib
import json
import lzma
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from union_closed_tight_m21.encoding import TARGET, build_cnf


@dataclass(frozen=True)
class CompressedArtifact:
    file: str
    compressed_sha256: str
    compressed_bytes: int
    uncompressed_sha256: str
    uncompressed_bytes: int


@dataclass(frozen=True)
class ToolIdentity:
    path: str
    sha256: str


@dataclass(frozen=True)
class Manifest:
    format_version: int
    order: int
    member_count: int
    variables: int
    clauses: int
    cnf_sha256: str
    drat: CompressedArtifact
    lrat: CompressedArtifact
    solver: ToolIdentity
    drat_checker: ToolIdentity
    lrat_checker: ToolIdentity
    timeout_seconds_per_stage: int
    stage_wall_seconds: dict[str, float]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tool_identity(executable: str) -> ToolIdentity:
    resolved = Path(executable).resolve(strict=True)
    return ToolIdentity(path=str(resolved), sha256=sha256(resolved))


def _run(
    command: list[str],
    timeout_seconds: int,
    accepted_return_codes: set[int],
    required_marker: str,
    label: str,
) -> tuple[str, float]:
    started = time.monotonic()
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"{label} exceeded {timeout_seconds}s: {' '.join(command)}") from error
    elapsed = time.monotonic() - started
    output = result.stdout + result.stderr
    if result.returncode not in accepted_return_codes or required_marker not in output:
        raise RuntimeError(
            f"{label} failed with status {result.returncode}: {' '.join(command)}\n{output}"
        )
    return output, elapsed


def _compress(source: Path, destination: Path) -> CompressedArtifact:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as input_stream, lzma.open(destination, "wb", preset=1) as output_stream:
        shutil.copyfileobj(input_stream, output_stream, length=1 << 20)
    return CompressedArtifact(
        file=destination.name,
        compressed_sha256=sha256(destination),
        compressed_bytes=destination.stat().st_size,
        uncompressed_sha256=sha256(source),
        uncompressed_bytes=source.stat().st_size,
    )


def _artifact(raw: Any) -> CompressedArtifact:
    if not isinstance(raw, dict):
        raise ValueError("invalid artifact record")
    return CompressedArtifact(
        file=str(raw["file"]),
        compressed_sha256=str(raw["compressed_sha256"]),
        compressed_bytes=int(raw["compressed_bytes"]),
        uncompressed_sha256=str(raw["uncompressed_sha256"]),
        uncompressed_bytes=int(raw["uncompressed_bytes"]),
    )


def _identity(raw: Any) -> ToolIdentity:
    if not isinstance(raw, dict):
        raise ValueError("invalid tool record")
    return ToolIdentity(path=str(raw["path"]), sha256=str(raw["sha256"]))


def load_manifest(path: Path) -> Manifest:
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("manifest must be an object")
    stages = raw.get("stage_wall_seconds")
    if not isinstance(stages, dict):
        raise ValueError("invalid timing record")
    manifest = Manifest(
        format_version=int(raw["format_version"]),
        order=int(raw["order"]),
        member_count=int(raw["member_count"]),
        variables=int(raw["variables"]),
        clauses=int(raw["clauses"]),
        cnf_sha256=str(raw["cnf_sha256"]),
        drat=_artifact(raw["drat"]),
        lrat=_artifact(raw["lrat"]),
        solver=_identity(raw["solver"]),
        drat_checker=_identity(raw["drat_checker"]),
        lrat_checker=_identity(raw["lrat_checker"]),
        timeout_seconds_per_stage=int(raw["timeout_seconds_per_stage"]),
        stage_wall_seconds={str(key): float(value) for key, value in stages.items()},
    )
    if manifest.format_version != 1:
        raise ValueError("unsupported manifest format")
    if (manifest.order, manifest.member_count) != (TARGET.order, TARGET.member_count):
        raise ValueError("manifest is not for the fixed target")
    return manifest


def build_certificate(
    solver: str,
    drat_checker: str,
    lrat_checker: str,
    manifest_path: Path,
    work_directory: Path,
    timeout_seconds: int,
) -> Manifest:
    """Run the bounded UNSAT, DRAT, and LRAT pipeline once."""

    if timeout_seconds < 1:
        raise ValueError("timeout must be positive")
    work_directory.mkdir(parents=True, exist_ok=True)
    cnf_path = work_directory / "order8-members21.cnf"
    raw_drat_path = work_directory / "raw.drat"
    trimmed_drat_path = work_directory / "trimmed.drat"
    lrat_path = work_directory / "trimmed.lrat"

    formula = build_cnf()
    formula.to_file(cnf_path)
    timings: dict[str, float] = {}

    _, timings["solver"] = _run(
        [solver, "--quiet", str(cnf_path), str(raw_drat_path)],
        timeout_seconds,
        {20},
        "s UNSATISFIABLE",
        "UNSAT search",
    )
    _, timings["raw_drat_replay_and_trim"] = _run(
        [
            drat_checker,
            str(cnf_path),
            str(raw_drat_path),
            "-i",
            "-l",
            str(trimmed_drat_path),
            "-C",
        ],
        timeout_seconds,
        {0},
        "s VERIFIED",
        "raw DRAT replay and trimming",
    )
    _, timings["trimmed_drat_replay"] = _run(
        [drat_checker, str(cnf_path), str(trimmed_drat_path), "-i"],
        timeout_seconds,
        {0},
        "s VERIFIED",
        "trimmed DRAT replay",
    )
    _, timings["drat_to_lrat"] = _run(
        [
            drat_checker,
            str(cnf_path),
            str(trimmed_drat_path),
            "-i",
            "-L",
            str(lrat_path),
        ],
        timeout_seconds,
        {0},
        "s VERIFIED",
        "DRAT-to-LRAT conversion",
    )
    _, timings["lrat_replay"] = _run(
        [lrat_checker, str(cnf_path), str(lrat_path)],
        timeout_seconds,
        {0},
        "c VERIFIED",
        "LRAT replay",
    )

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    drat_destination = manifest_path.parent / "order8-members21.drat.xz"
    lrat_destination = manifest_path.parent / "order8-members21.lrat.xz"
    drat = _compress(trimmed_drat_path, drat_destination)
    lrat = _compress(lrat_path, lrat_destination)
    manifest = Manifest(
        format_version=1,
        order=TARGET.order,
        member_count=TARGET.member_count,
        variables=formula.nv,
        clauses=len(formula.clauses),
        cnf_sha256=sha256(cnf_path),
        drat=drat,
        lrat=lrat,
        solver=_tool_identity(solver),
        drat_checker=_tool_identity(drat_checker),
        lrat_checker=_tool_identity(lrat_checker),
        timeout_seconds_per_stage=timeout_seconds,
        stage_wall_seconds={key: round(value, 3) for key, value in timings.items()},
    )
    manifest_path.write_text(json.dumps(asdict(manifest), indent=2) + "\n", encoding="utf-8")
    return manifest


def _decompress_and_check(
    artifact: CompressedArtifact,
    compressed_root: Path,
    output_root: Path,
) -> Path:
    compressed = compressed_root / artifact.file
    if compressed.stat().st_size != artifact.compressed_bytes:
        raise RuntimeError(f"compressed size mismatch: {compressed}")
    if sha256(compressed) != artifact.compressed_sha256:
        raise RuntimeError(f"compressed checksum mismatch: {compressed}")
    output = output_root / artifact.file.removesuffix(".xz")
    with lzma.open(compressed, "rb") as input_stream, output.open("wb") as output_stream:
        shutil.copyfileobj(input_stream, output_stream, length=1 << 20)
    if output.stat().st_size != artifact.uncompressed_bytes:
        raise RuntimeError(f"uncompressed size mismatch: {compressed}")
    if sha256(output) != artifact.uncompressed_sha256:
        raise RuntimeError(f"uncompressed checksum mismatch: {compressed}")
    return output


def verify_certificate(
    manifest_path: Path,
    drat_checker: str,
    lrat_checker: str,
    work_directory: Path,
    timeout_seconds: int,
) -> None:
    """Regenerate the CNF and independently replay both retained proofs."""

    manifest = load_manifest(manifest_path)
    work_directory.mkdir(parents=True, exist_ok=True)
    formula = build_cnf()
    if (formula.nv, len(formula.clauses)) != (manifest.variables, manifest.clauses):
        raise RuntimeError("CNF dimensions differ from the manifest")
    cnf_path = work_directory / "verification.cnf"
    formula.to_file(cnf_path)
    if sha256(cnf_path) != manifest.cnf_sha256:
        raise RuntimeError("CNF checksum differs from the manifest")

    drat_path = _decompress_and_check(manifest.drat, manifest_path.parent, work_directory)
    lrat_path = _decompress_and_check(manifest.lrat, manifest_path.parent, work_directory)
    _run(
        [drat_checker, str(cnf_path), str(drat_path), "-i"],
        timeout_seconds,
        {0},
        "s VERIFIED",
        "retained DRAT replay",
    )
    _run(
        [lrat_checker, str(cnf_path), str(lrat_path)],
        timeout_seconds,
        {0},
        "c VERIFIED",
        "retained LRAT replay",
    )
