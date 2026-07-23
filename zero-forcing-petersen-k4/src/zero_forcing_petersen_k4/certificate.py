from __future__ import annotations

from .census import native_source_digest, run_census
from .graph import GeneralizedPetersen
from .upper import replay_uniform_schedule, uniform_seed

CENSUS_ORDERS = tuple(range(17, 23))


def build_certificate() -> dict[str, object]:
    results = run_census(CENSUS_ORDERS)
    control, *target_results = results
    if control.forcing_necklaces == 0 or control.first_witness == 0:
        raise AssertionError("the n=17 positive control failed")
    if any(result.forcing_necklaces != 0 for result in target_results):
        raise AssertionError("a nine-set forces at a target order")

    replay_orders = tuple(range(9, 201))
    for n in replay_orders:
        replay_uniform_schedule(n)

    graph = GeneralizedPetersen(17)
    control_names = [
        graph.vertex_name(vertex)
        for vertex in range(graph.order)
        if control.first_witness >> vertex & 1
    ]
    control_certificate = control.as_dict()
    control_certificate["first_forcing_witness"] = control_names
    seed_graph = GeneralizedPetersen(18)
    seed_names = [
        seed_graph.vertex_name(vertex)
        for vertex in range(seed_graph.order)
        if uniform_seed(seed_graph.n) >> vertex & 1
    ]
    return {
        "theorem": "Z(P(n,4))=10 for every integer 18<=n<=22",
        "nine_set_census": {
            "symmetry": "cyclic rotations of the column word",
            "native_source_sha256": native_source_digest(),
            "positive_control": control_certificate,
            "target_orders": [result.as_dict() for result in target_results],
        },
        "uniform_upper_bound": {
            "initial_set": seed_names,
            "symbolic_proof": "REPORT.md",
            "replayed_order_range": [replay_orders[0], replay_orders[-1]],
        },
    }
