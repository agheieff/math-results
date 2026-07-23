"""Generate formulas and independently replay compressed DRAT certificates."""

from __future__ import annotations

import hashlib
import json
import lzma
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from union_closed_tight.encoding import Instance, build_cnf


@dataclass(frozen=True)
class Certificate:
    member_count: int
    cnf_sha256: str
    proof: str
    proof_sha256: str


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> tuple[int, tuple[Certificate, ...]]:
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("order"), int):
        raise ValueError("invalid manifest header")
    minimum = raw.get("minimum_member_count")
    maximum = raw.get("maximum_member_count")
    if not isinstance(minimum, int) or not isinstance(maximum, int):
        raise ValueError("invalid manifest range")
    entries = raw.get("certificates")
    if not isinstance(entries, list):
        raise ValueError("invalid manifest entries")
    certificates = tuple(Certificate(**entry) for entry in entries)
    if [item.member_count for item in certificates] != list(range(minimum, maximum + 1)):
        raise ValueError("manifest does not cover its full inclusive range")
    return raw["order"], certificates


def _run_verified(command: list[str], label: str) -> str:
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    output = result.stdout + result.stderr
    if result.returncode != 0 or "s VERIFIED" not in output:
        raise RuntimeError(f"{label} failed\n{output}")
    return output


def build_certificate(
    instance: Instance,
    solver: str,
    checker: str,
    destination: Path,
) -> Certificate:
    """Generate, trim, replay, and compress one CaDiCaL binary DRAT proof."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="uctight-build-") as temporary:
        root = Path(temporary)
        cnf_path = root / "instance.cnf"
        raw_path = root / "raw.drat"
        trimmed_path = root / "trimmed.drat"
        build_cnf(instance).to_file(cnf_path)
        solve = subprocess.run(
            [solver, "--quiet", str(cnf_path), str(raw_path)],
            check=False,
            capture_output=True,
            text=True,
        )
        if solve.returncode != 20 or "s UNSATISFIABLE" not in solve.stdout + solve.stderr:
            raise RuntimeError(f"solver did not prove UNSAT for m={instance.member_count}")
        _run_verified(
            [
                checker,
                str(cnf_path),
                str(raw_path),
                "-i",
                "-l",
                str(trimmed_path),
                "-C",
            ],
            "raw DRAT replay",
        )
        _run_verified(
            [checker, str(cnf_path), str(trimmed_path), "-i"],
            "trimmed DRAT replay",
        )
        with trimmed_path.open("rb") as source, lzma.open(destination, "wb", preset=6) as target:
            shutil.copyfileobj(source, target, length=1 << 20)
        return Certificate(
            member_count=instance.member_count,
            cnf_sha256=sha256(cnf_path),
            proof=destination.name,
            proof_sha256=sha256(destination),
        )


def build_manifest(
    order: int,
    minimum: int,
    maximum: int,
    solver: str,
    checker: str,
    output: Path,
) -> None:
    certificates = []
    for member_count in range(minimum, maximum + 1):
        proof = output.parent / f"order{order}-members{member_count:02d}.drat.xz"
        certificate = build_certificate(Instance(order, member_count), solver, checker, proof)
        certificates.append(certificate)
        print(f"m={member_count}: built and VERIFIED")
    manifest = {
        "format_version": 1,
        "order": order,
        "minimum_member_count": minimum,
        "maximum_member_count": maximum,
        "certificates": [certificate.__dict__ for certificate in certificates],
    }
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def verify_all(manifest_path: Path, checker: str, lrat_checker: str | None = None) -> None:
    order, certificates = load_manifest(manifest_path)
    proof_root = manifest_path.parent
    for certificate in certificates:
        proof_path = proof_root / certificate.proof
        if sha256(proof_path) != certificate.proof_sha256:
            raise RuntimeError(f"proof checksum mismatch: {proof_path}")
        with tempfile.TemporaryDirectory(prefix="uctight-") as temporary:
            root = Path(temporary)
            cnf_path = root / "instance.cnf"
            drat_path = root / "proof.drat"
            lrat_path = root / "proof.lrat"
            build_cnf(Instance(order, certificate.member_count)).to_file(cnf_path)
            if sha256(cnf_path) != certificate.cnf_sha256:
                raise RuntimeError(f"CNF checksum mismatch for m={certificate.member_count}")
            with lzma.open(proof_path, "rb") as source, drat_path.open("wb") as target:
                for chunk in iter(lambda: source.read(1 << 20), b""):
                    target.write(chunk)
            _run_verified(
                [checker, str(cnf_path), str(drat_path), "-i"],
                f"DRAT replay for m={certificate.member_count}",
            )
            if lrat_checker is not None:
                _run_verified(
                    [checker, str(cnf_path), str(drat_path), "-i", "-L", str(lrat_path)],
                    f"DRAT-to-LRAT conversion for m={certificate.member_count}",
                )
                result = subprocess.run(
                    [lrat_checker, str(cnf_path), str(lrat_path)],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                output = result.stdout + result.stderr
                if result.returncode != 0 or "c VERIFIED" not in output:
                    raise RuntimeError(
                        f"LRAT replay failed for m={certificate.member_count}\n{output}"
                    )
                print(f"m={certificate.member_count}: DRAT+LRAT VERIFIED")
            else:
                print(f"m={certificate.member_count}: DRAT VERIFIED")
