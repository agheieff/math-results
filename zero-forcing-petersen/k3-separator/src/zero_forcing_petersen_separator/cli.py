from __future__ import annotations

import json

from .certificate import certify_separator_theorem


def main() -> None:
    print(json.dumps(certify_separator_theorem().as_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
