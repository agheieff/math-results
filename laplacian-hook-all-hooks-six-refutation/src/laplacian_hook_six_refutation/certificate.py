"""Build the exact three-class k=1 refutation certificate."""

from dataclasses import dataclass
from hashlib import sha256

from laplacian_hook_six_refutation.canonical import format_graph_key, graph_key
from laplacian_hook_six_refutation.exact import (
    characteristic_polynomial,
    complement_polynomial_from_sparse,
    pad_sparse_polynomial,
    polynomial_product,
)
from laplacian_hook_six_refutation.model import (
    Polynomial,
    Witness,
    dense_complement_laplacian,
    normalize_edges,
    sparse_laplacian,
)

REFERENCE_ORDER = 9


@dataclass(frozen=True)
class WitnessClass:
    label: str
    sparse_factorization: str
    sparse_spectrum: str
    dense_factorization: str
    factors: tuple[Polynomial, ...]
    members: tuple[Witness, ...]

    @property
    def nonzero_factor(self) -> Polynomial:
        return polynomial_product(self.factors)

    @property
    def threshold(self) -> int:
        return max(member.support for member in self.members)


def _witness(key: str, edges: list[tuple[int, int]]) -> Witness:
    return Witness(key, normalize_edges(edges))


CLASSES = (
    WitnessClass(
        label="A",
        sparse_factorization="x^(n-5)(x-4)(x-3)(x-2)^2(x-1)",
        sparse_spectrum="{0^(n-5),1,2,2,3,4}",
        dense_factorization=("x(x-n)^(n-6)(x-n+4)(x-n+3)(x-n+2)^2(x-n+1)"),
        factors=((1, -4), (1, -3), (1, -2), (1, -2), (1, -1)),
        members=(
            _witness(
                "v2e1-v2e1-v4e3c",
                [(0, 1), (0, 2), (0, 3), (1, 2), (4, 5), (6, 7)],
            ),
            _witness(
                "v3e6-v4e33",
                [(0, 1), (0, 2), (1, 3), (2, 3), (4, 5), (4, 6)],
            ),
        ),
    ),
    WitnessClass(
        label="B",
        sparse_factorization="x^(n-5)(x-4)(x-3)^2(x-1)^2",
        sparse_spectrum="{0^(n-5),1,1,3,3,4}",
        dense_factorization=("x(x-n)^(n-6)(x-n+4)(x-n+3)^2(x-n+1)^2"),
        factors=((1, -4), (1, -3), (1, -3), (1, -1), (1, -1)),
        members=(
            _witness(
                "v3e6-v4e3c",
                [(0, 1), (0, 2), (0, 3), (1, 2), (4, 5), (4, 6)],
            ),
            _witness(
                "v3e7-v4e34",
                [(0, 1), (0, 2), (0, 3), (4, 5), (4, 6), (5, 6)],
            ),
            _witness(
                "v6e6443",
                [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5)],
            ),
        ),
    ),
    WitnessClass(
        label="C",
        sparse_factorization="x^(n-5)(x-2)(x^2-5x+3)(x^2-5x+5)",
        sparse_spectrum="{0^(n-5),2,roots(x^2-5x+3),roots(x^2-5x+5)}",
        dense_factorization=("x(x-n)^(n-6)(x-n+2)((x-n)^2+5(x-n)+3)((x-n)^2+5(x-n)+5)"),
        factors=((1, -2), (1, -5, 3), (1, -5, 5)),
        members=(
            _witness(
                "v2e1-v5e3c4",
                [(0, 1), (0, 2), (0, 3), (1, 2), (1, 4), (5, 6)],
            ),
            _witness(
                "v6e6885",
                [(0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (4, 5)],
            ),
        ),
    ),
)


def _assert_complement_identity(
    sparse: tuple[tuple[int, ...], ...],
    dense: tuple[tuple[int, ...], ...],
) -> None:
    order = len(sparse)
    for row in range(order):
        for column in range(order):
            expected = order * int(row == column) - 1 - sparse[row][column]
            if dense[row][column] != expected:
                raise AssertionError("L(complement) != nI-J-L")


def _class_json(witness_class: WitnessClass) -> dict[str, object]:
    nonzero = witness_class.nonzero_factor
    sparse_reference = pad_sparse_polynomial(nonzero, REFERENCE_ORDER)
    dense_reference = complement_polynomial_from_sparse(nonzero, REFERENCE_ORDER)
    return {
        "label": witness_class.label,
        "valid_orders": f"all n>={witness_class.threshold}",
        "sparse_factorization": witness_class.sparse_factorization,
        "sparse_spectrum": witness_class.sparse_spectrum,
        "sparse_nonzero_factor_coefficients": list(nonzero),
        "sparse_polynomial_n9": list(sparse_reference),
        "dense_complement_factorization": witness_class.dense_factorization,
        "dense_complement_polynomial_n9": list(dense_reference),
        "members": [
            {
                "complement_key": member.key,
                "support": member.support,
                "edges": [list(edge) for edge in sorted(member.edges)],
            }
            for member in witness_class.members
        ],
    }


def build_certificate() -> dict[str, object]:
    seen_keys: set[str] = set()
    payload_lines: list[str] = []
    for witness_class in CLASSES:
        expected_sparse = witness_class.nonzero_factor
        for member in witness_class.members:
            if len(member.edges) != 6:
                raise AssertionError("every witness must have exactly six edges")
            computed_key = format_graph_key(graph_key(member.edges))
            if computed_key != member.key or computed_key in seen_keys:
                raise AssertionError("canonical witness key mismatch")
            seen_keys.add(computed_key)

        for order in range(witness_class.threshold, 13):
            sparse_expected = pad_sparse_polynomial(expected_sparse, order)
            dense_expected = complement_polynomial_from_sparse(expected_sparse, order)
            sparse_values: set[Polynomial] = set()
            dense_values: set[Polynomial] = set()
            for member in witness_class.members:
                sparse_matrix = sparse_laplacian(member.edges, order)
                dense_matrix = dense_complement_laplacian(member.edges, order)
                _assert_complement_identity(sparse_matrix, dense_matrix)
                sparse_values.add(characteristic_polynomial(sparse_matrix))
                dense_values.add(characteristic_polynomial(dense_matrix))
            if sparse_values != {sparse_expected} or dense_values != {dense_expected}:
                raise AssertionError(
                    f"spectral identity failed for class {witness_class.label} at n={order}"
                )

        payload_lines.append(
            f"{witness_class.label}|{','.join(map(str, expected_sparse))}|"
            + "|".join(member.key for member in witness_class.members)
        )

    return {
        "refutation": (
            "The universal six-deletion extension over every hook parameter is false: "
            "k=1 already has nonisomorphic cospectral pairs."
        ),
        "hook_parameter": 1,
        "hook_partition": "(1^n)",
        "hook_polynomial": "Phi_1(L(G),x)=det(xI-L(G))",
        "valid_orders": "every n>=8",
        "reason": "L(K_n-H)=nI-J-L(H), so padded Laplacian cospectrality is preserved",
        "reference_order": REFERENCE_ORDER,
        "classes": [_class_json(witness_class) for witness_class in CLASSES],
        "witness_payload_sha256": sha256("\n".join(payload_lines).encode()).hexdigest(),
    }
