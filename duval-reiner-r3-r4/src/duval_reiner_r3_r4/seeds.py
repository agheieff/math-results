from __future__ import annotations

from .families import Facet, mask_from_facets
from .laplacian import gram_matrix, partial_degree_sum, vertex_degrees
from .spectrum import certify_matrix, numerical_partial_sums

F16: tuple[Facet, ...] = (
    (0, 1, 2),
    (0, 1, 3),
    (0, 1, 5),
    (0, 2, 6),
    (1, 2, 3),
    (1, 2, 4),
    (1, 2, 5),
    (1, 2, 6),
    (1, 3, 4),
    (1, 3, 5),
    (1, 3, 6),
    (1, 4, 5),
    (1, 4, 6),
    (1, 5, 6),
    (2, 3, 6),
    (2, 5, 6),
)

F15: tuple[Facet, ...] = (
    (0, 2, 3),
    (0, 2, 5),
    (0, 2, 6),
    (0, 3, 5),
    (0, 3, 6),
    (1, 2, 3),
    (1, 2, 5),
    (1, 2, 6),
    (1, 3, 5),
    (1, 3, 6),
    (2, 3, 4),
    (2, 3, 5),
    (2, 3, 6),
    (2, 5, 6),
    (3, 4, 5),
)


def audit_seed(
    name: str,
    family: tuple[Facet, ...],
    indices: tuple[int, ...],
) -> dict[str, object]:
    vertex_count = 7
    mask = mask_from_facets(vertex_count, family)
    matrix = gram_matrix(vertex_count, mask)
    degrees = vertex_degrees(vertex_count, mask)
    degree_sums = {index: partial_degree_sum(degrees, index) for index in indices}
    numerical = numerical_partial_sums(matrix, indices)
    certificate = certify_matrix(matrix, degree_sums)
    return {
        "name": name,
        "facets": len(family),
        "degrees": list(degrees),
        "numerical_partial_sums": {str(index): numerical[index] for index in indices},
        "certificate": certificate.as_dict(),
    }


def audit_paper_seeds() -> list[dict[str, object]]:
    return [
        audit_seed("F16", F16, (3, 4, 5)),
        audit_seed("F15", F15, (3, 4, 8, 9)),
    ]
