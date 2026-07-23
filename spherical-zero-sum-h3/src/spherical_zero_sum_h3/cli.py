from __future__ import annotations

import argparse
import json

from .h3 import certify_h3
from .search import run_bounded_search


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-search", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    certificate = certify_h3()
    result: dict[str, object] = {
        "h3": {
            "vertices": certificate.vertices,
            "zero_sum_triples": certificate.zero_sum_triples,
            "independence_number": certificate.independence_number,
            "ratio": "2/3",
        }
    }
    if args.full_search:
        result["bounded_search"] = run_bounded_search()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
