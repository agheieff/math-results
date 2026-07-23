from __future__ import annotations

import json

from .certificate import build_certificate, verify_certificate


def main() -> None:
    certificate = build_certificate()
    verify_certificate(certificate)
    print(json.dumps(certificate.summary(), sort_keys=True))
