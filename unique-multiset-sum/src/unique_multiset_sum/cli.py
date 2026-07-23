"""Command-line entry point for the exhaustive checker."""

import argparse

from unique_multiset_sum.checker import exhaustive_bound_check


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-n",
        type=int,
        default=5,
        help="largest family size to exhaust (default: 5)",
    )
    return parser


def main() -> None:
    args = _parser().parse_args()
    if args.max_n < 2:
        raise SystemExit("--max-n must be at least 2")

    print("n  bound  group-types  normalized-families  valid-below  equality")
    for family_size in range(2, args.max_n + 1):
        result = exhaustive_bound_check(family_size)
        equality = "valid" if result.equality_construction_valid else "INVALID"
        print(
            f"{result.family_size:<2} {result.lower_bound:<6} "
            f"{result.group_types:<12} {result.normalized_families:<20} "
            f"{result.valid_families:<11} {equality}"
        )


if __name__ == "__main__":
    main()
