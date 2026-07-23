"""Build the all-orders theorem certificate."""

from __future__ import annotations

from .finite import certify_seven_sets, eight_outer_vertices_force, replay_symbolic_upper_bound
from .minor import petersen_edges, reduced_minor_edges, residue_base, verify_minor_model
from .pathwidth import certify_no_narrow_layout


def build_certificate() -> dict[str, object]:
    n13 = certify_seven_sets(13)
    if n13.forcing_sets:
        raise AssertionError("a seven-set forces P(13,3)")

    base_certificates = tuple(certify_no_narrow_layout(n) for n in (14, 15, 16))
    if not all(certificate.excludes_layout for certificate in base_certificates):
        raise AssertionError("a width-seven base layout was found")

    minor_orders = tuple(range(10, 81))
    for n in minor_orders:
        if reduced_minor_edges(n) != petersen_edges(n - 3) or not verify_minor_model(n):
            raise AssertionError(f"minor reduction failed at n={n}")

    upper_orders = tuple(range(13, 201))
    if not all(
        eight_outer_vertices_force(n) and replay_symbolic_upper_bound(n) for n in upper_orders
    ):
        raise AssertionError("the uniform eight-set failed in the finite replay range")

    residue_orders = tuple(range(14, 81))
    if any(
        residue_base(n) not in (14, 15, 16) or residue_base(n) > n or (n - residue_base(n)) % 3
        for n in residue_orders
    ):
        raise AssertionError("residue-base reduction failed")
    return {
        "theorem": "Z(P(n,3))=8 for every integer n>=13",
        "n13_lower_bound": n13.as_dict(),
        "pathwidth_base_lower_bounds": [certificate.as_dict() for certificate in base_certificates],
        "minor_reduction": {
            "statement": "P(n-3,3) is a topological minor of P(n,3) for n>=10",
            "replayed_order_range": [minor_orders[0], minor_orders[-1]],
            "residue_base_check_range": [residue_orders[0], residue_orders[-1]],
        },
        "uniform_upper_bound": {
            "initial_set": ["u_0", "u_1", "u_2", "u_3", "u_4", "u_5", "u_6", "u_7"],
            "symbolic_proof": "THEOREM.md",
            "replayed_order_range": [upper_orders[0], upper_orders[-1]],
        },
    }
