"""Strict replay of the proved structural lemmas."""

import hashlib
import json

from .forcing import force_until_outer_radius, verify_block_expansion
from .kernel import BASIS, adjacency_residual, evaluation, null_vector_for
from .minor import petersen_edges, reduced_minor_edges
from .model import Vertex, inner, neighbors, outer


def _row_text(vertex: Vertex) -> str:
    row = evaluation(vertex)
    return f"{vertex}|" + ",".join(str(value) for value in row)


def build_certificate() -> dict[str, object]:
    for index in range(-64, 65):
        for vertex in (outer(index), inner(index)):
            if len(set(neighbors(vertex))) != 3:
                raise AssertionError("the strip is not simple cubic")
            for basis in BASIS:
                if adjacency_residual(basis, vertex):
                    raise AssertionError("an evaluation row violates the adjacency equations")

    sample_sets = (
        tuple(outer(index) for index in range(7)),
        (outer(-8), inner(-3), outer(-1), inner(0), outer(4), inner(9), outer(17)),
        (inner(-21), inner(-8), outer(-2), outer(0), inner(5), outer(14), inner(34)),
    )
    witnesses = []
    for vertices in sample_sets:
        witness = null_vector_for(vertices)
        if any(adjacency_residual(witness, outer(index)) for index in range(-64, 65)):
            raise AssertionError("sample lower-bound witness failed on an outer equation")
        if any(adjacency_residual(witness, inner(index)) for index in range(-64, 65)):
            raise AssertionError("sample lower-bound witness failed on an inner equation")
        witnesses.append([str(value) for value in witness])

    for start in range(-16, 17):
        verify_block_expansion(start)
    black, forces = force_until_outer_radius(32)

    minor_orders = list(range(10, 41))
    for order in minor_orders:
        if reduced_minor_edges(order) != petersen_edges(order - 3):
            raise AssertionError(f"three-column minor reduction failed at n={order}")

    rows = [
        _row_text(vertex) for index in range(-64, 65) for vertex in (outer(index), inner(index))
    ]
    payload = {
        "theorem": (
            "The finite-seed, finitary zero forcing number of the bi-infinite "
            "generalized Petersen strip P(Z,3) is eight."
        ),
        "cyclic_conjecture_claimed": False,
        "kernel": {
            "dimension": 8,
            "initial_coordinates": [f"u{index}" for index in range(-4, 4)],
            "recurrence": "u_(i+4)=u_i-u_(i-4)-u_(i-2)-u_(i+2)",
            "sample_null_vectors": witnesses,
            "evaluation_rows_sha256": hashlib.sha256("\n".join(rows).encode()).hexdigest(),
        },
        "upper_bound": {
            "initial_set": [f"u{index}" for index in range(8)],
            "verified_outer_radius": 32,
            "vertices_black_at_stop": len(black),
            "forces_replayed": len(forces),
        },
        "minor_lemma": {
            "statement": "P(n-3,3) is a minor of P(n,3) for every n>=10.",
            "verified_orders": minor_orders,
        },
    }
    return payload


def certificate_sha256(certificate: dict[str, object]) -> str:
    encoded = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()
