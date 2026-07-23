import argparse

from .forcing import maximum_two_set_closure, replay_forces
from .forts import verify_exceptional_forts
from .model import MycielskiPath
from .spectral import verify_spectral_parameters


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--maximum-order", type=int, default=16)
    return result


def main() -> None:
    args = parser().parse_args()
    if args.maximum_order < 5:
        raise ValueError("maximum order must be at least five")
    order_two = MycielskiPath.build(2)
    if maximum_two_set_closure(order_two) != order_two.vertex_count:
        raise AssertionError("the n=2 five-cycle did not have a forcing pair")
    print("n=2: PASS")
    for order in range(3, args.maximum_order + 1):
        graph = MycielskiPath.build(order)
        if replay_forces(graph) != (1 << graph.vertex_count) - 1:
            raise AssertionError("forcing sequence did not close")
        if maximum_two_set_closure(graph) == graph.vertex_count:
            raise AssertionError("a two-set unexpectedly forced the graph")
        if order in (3, 5):
            verify_exceptional_forts(graph)
        elif order >= 4:
            verify_spectral_parameters(order)
        print(f"n={order}: PASS")
