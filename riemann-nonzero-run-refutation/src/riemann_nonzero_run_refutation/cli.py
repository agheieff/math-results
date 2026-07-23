import argparse
from decimal import Decimal
from pathlib import Path

from .certificate import load_witness, verify_certificate
from .scan import full_scan, verify_sources


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--certificate", type=Path)
    result.add_argument("--zeros", type=Path)
    result.add_argument("--derivatives", type=Path)
    result.add_argument("--full-scan", action="store_true")
    return result


def main() -> None:
    arguments = parser().parse_args()
    root = Path(__file__).resolve().parents[2]
    certificate_path = arguments.certificate or root / "artifacts" / "witness.json"
    verification = verify_certificate(certificate_path)
    witness = load_witness(certificate_path)
    print(
        "PASS certificate",
        f"pattern={verification.sign_pattern}",
        f"grams={verification.gram_indices[0]}..{verification.gram_indices[-1]}",
        f"sha256={verification.artifact_sha256}",
    )

    if (arguments.zeros is None) != (arguments.derivatives is None):
        raise SystemExit("--zeros and --derivatives must be supplied together")
    if arguments.zeros is not None and arguments.derivatives is not None:
        verify_sources(arguments.zeros, arguments.derivatives, witness)
        print("PASS source hashes and witness rows")
        if arguments.full_scan:
            result = full_scan(
                arguments.zeros,
                arguments.derivatives,
                Decimal(witness["base_height"]),
            )
            expected = witness["full_scan"]
            assert result.gaps == expected["gaps"]
            assert result.histogram == {
                int(key): value for key, value in expected["gram_count_histogram"].items()
            }
            assert result.forbidden_gaps == expected["forbidden_gaps"]
            assert result.first_forbidden_left_row == expected["first_forbidden_left_row"]
            assert result.ambiguous_endpoints == 0
            print(
                "PASS full scan",
                f"gaps={result.gaps}",
                f"histogram={result.histogram}",
                f"forbidden={result.forbidden_gaps}",
            )
    elif arguments.full_scan:
        raise SystemExit("--full-scan requires both source files")
