from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction

from .families import all_facets, orbit_representatives, selected_facets
from .laplacian import gram_matrix, partial_degree_sum, vertex_degrees
from .spectrum import (
    MatrixCertificate,
    PartialSumCertificate,
    certify_matrix,
    numerical_partial_sums,
)

SCREEN_TOLERANCE = 1e-8


def _fraction_text(value: Fraction | None) -> str | None:
    return None if value is None else str(value)


@dataclass(frozen=True)
class HardestStrictCase:
    index: int
    mask: int
    facets: tuple[tuple[int, int, int], ...]
    degree_sum: int
    numerical_gap: float
    characteristic_polynomial: tuple[int, ...]
    lower_bound: Fraction | None
    upper_bound: Fraction | None

    def as_dict(self) -> dict[str, object]:
        return {
            "index": self.index,
            "mask": self.mask,
            "facets": [list(facet) for facet in self.facets],
            "degree_sum": self.degree_sum,
            "numerical_gap": self.numerical_gap,
            "characteristic_polynomial": list(self.characteristic_polynomial),
            "lower_bound": _fraction_text(self.lower_bound),
            "upper_bound": _fraction_text(self.upper_bound),
        }


def _certificate_by_index(
    certificate: MatrixCertificate,
) -> dict[int, PartialSumCertificate]:
    return {partial.index: partial for partial in certificate.partial_sums}


def run_census(
    vertex_count: int = 6,
    indices: tuple[int, ...] = (3, 4),
) -> dict[str, object]:
    representatives = orbit_representatives(vertex_count)
    facet_count = len(all_facets(vertex_count))
    status_counts = {index: Counter[str]() for index in indices}
    method_counts = {index: Counter[str]() for index in indices}
    screening_candidates = {index: 0 for index in indices}
    screening_max_defect = {index: float("-inf") for index in indices}
    hardest: dict[int, HardestStrictCase] = {}
    exact_violations: dict[int, list[int]] = {index: [] for index in indices}
    digest = hashlib.sha256()
    maximum_denominator = 0

    for mask in representatives:
        matrix = gram_matrix(vertex_count, mask)
        degrees = vertex_degrees(vertex_count, mask)
        degree_sums = {index: partial_degree_sum(degrees, index) for index in indices}
        numerical_sums = numerical_partial_sums(matrix, indices)
        certificate = certify_matrix(matrix, degree_sums)
        partials = _certificate_by_index(certificate)
        maximum_denominator = max(maximum_denominator, certificate.isolation_denominator)

        digest_record = {
            "mask": mask,
            "degrees": degrees,
            "certificate": certificate.as_dict(),
        }
        digest.update(
            json.dumps(digest_record, sort_keys=True, separators=(",", ":")).encode("utf-8")
        )
        digest.update(b"\n")

        for index in indices:
            partial = partials[index]
            status_counts[index][partial.status] += 1
            method_counts[index][partial.method] += 1
            defect = numerical_sums[index] - degree_sums[index]
            screening_max_defect[index] = max(screening_max_defect[index], defect)
            if defect > SCREEN_TOLERANCE:
                screening_candidates[index] += 1
            if partial.status == "violation":
                exact_violations[index].append(mask)
            if partial.status != "strict":
                continue
            gap = -defect
            current = hardest.get(index)
            if current is None or gap < current.numerical_gap:
                hardest[index] = HardestStrictCase(
                    index,
                    mask,
                    selected_facets(vertex_count, mask),
                    degree_sums[index],
                    gap,
                    certificate.characteristic_polynomial,
                    partial.lower_bound,
                    partial.upper_bound,
                )

    index_summaries = {}
    for index in indices:
        maximum = screening_max_defect[index]
        if abs(maximum) < SCREEN_TOLERANCE:
            maximum = 0.0
        index_summaries[str(index)] = {
            "exact_status_counts": dict(sorted(status_counts[index].items())),
            "certificate_methods": dict(sorted(method_counts[index].items())),
            "numerical_screen_candidates": screening_candidates[index],
            "numerical_screen_max_defect": maximum,
            "hardest_numerically_strict_case": hardest[index].as_dict(),
            "exact_violation_masks": exact_violations[index],
        }

    return {
        "vertex_count": vertex_count,
        "possible_facets": facet_count,
        "labeled_families": 1 << facet_count,
        "isomorphism_classes": len(representatives),
        "indices": index_summaries,
        "maximum_root_isolation_denominator": maximum_denominator,
        "certificate_digest_sha256": digest.hexdigest(),
    }
