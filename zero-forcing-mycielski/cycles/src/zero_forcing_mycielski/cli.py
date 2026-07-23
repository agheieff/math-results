from __future__ import annotations

import argparse

from .forcing import (
    exhaust_four_sets,
    explicit_forcing_sequence,
    forcing_witness,
    replay_forces,
)
from .forts import q6_fort_certificate
from .matrix import (
    has_graph_support,
    q4_certificate_matrix,
    q5_certificate_matrix,
    rational_rank,
)
from .model import MycielskiCycle


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orders",
        type=int,
        nargs="+",
        default=list(range(4, 14)),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    q4 = MycielskiCycle.build(4)
    matrix4 = q4_certificate_matrix()
    rank4 = rational_rank(matrix4)
    if not has_graph_support(q4, matrix4) or q4.vertex_count - rank4 != 5:
        raise RuntimeError("q=4 matrix certificate failed")
    print("q=4 matrix: PASS (rank=4, nullity=5)")

    q5 = MycielskiCycle.build(5)
    matrix5 = q5_certificate_matrix()
    rank5 = rational_rank(matrix5)
    if not has_graph_support(q5, matrix5) or q5.vertex_count - rank5 != 5:
        raise RuntimeError("q=5 matrix certificate failed")
    print("q=5 matrix: PASS (rank=6, nullity=5)")

    fort_result = q6_fort_certificate()
    if fort_result.final_survivors:
        raise RuntimeError("q=6 fort certificate failed")
    print(
        "q=6 forts: PASS "
        f"(forts={fort_result.fort_count}, candidates={fort_result.candidate_count})"
    )

    for order in args.orders:
        graph = MycielskiCycle.build(order)
        final = replay_forces(
            graph,
            forcing_witness(graph),
            explicit_forcing_sequence(graph),
        )
        if final.bit_count() != graph.vertex_count:
            raise RuntimeError(f"forcing sequence failed at q={order}")
        exhaustion = exhaust_four_sets(graph)
        if exhaustion.maximum_closure == graph.vertex_count:
            raise RuntimeError(f"four-set counterexample at q={order}")
        print(
            f"q={order}: PASS "
            f"(four-sets={exhaustion.checked}, max-closure={exhaustion.maximum_closure})"
        )


if __name__ == "__main__":
    main()
