from pathlib import Path

from .certificate import verify_certificate


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    result = verify_certificate(root / "artifacts" / "witness.json")
    print(
        "PASS",
        f"pattern={result.sign_pattern}",
        f"grams={result.gram_indices[0]}..{result.gram_indices[-1]}",
        f"sha256={result.artifact_sha256}",
    )
