from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .certificate import build_certificate


def main() -> None:
    certificate = build_certificate()
    encoded = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
    artifact = Path("artifacts/certificate-summary.json")
    if certificate != json.loads(artifact.read_text()):
        raise SystemExit("generated certificate does not match the frozen artifact")
    print(f"certificate=PASS sha256={hashlib.sha256(encoded).hexdigest()}")


if __name__ == "__main__":
    main()
