from __future__ import annotations

import json

from .census import run_census
from .families import burnside_orbit_count
from .seeds import audit_paper_seeds


def main() -> None:
    result = {
        "source": "arXiv:2607.20051v1",
        "scope": {
            "unresolved_universal_indices": [3, 4],
            "uniformity_searched": 3,
            "exact_census_through_vertices": 6,
        },
        "census": run_census(),
        "paper_seed_audit": audit_paper_seeds(),
        "next_boundary": {
            "vertex_count": 7,
            "possible_facets": 35,
            "labeled_families": 1 << 35,
            "isomorphism_classes_burnside": burnside_orbit_count(7),
            "enumerated": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
