from fractions import Fraction
from itertools import permutations
from math import comb

from laplacian_hook_all.characters import hook_character_product
from laplacian_hook_all.graphs import complement_types
from laplacian_hook_all.statistics import normalized_coefficients


def test_all_actual_hooks_at_small_orders_are_injective() -> None:
    graphs = complement_types()
    for order in range(8, 16):
        active = [graph for graph in graphs if graph.vertex_count <= order]
        for hook_parameter in range(1, order + 1):
            values = {normalized_coefficients(graph, order, hook_parameter) for graph in active}
            assert len(values) == len(active)


def _cycle_lengths(permutation: tuple[int, ...]) -> tuple[int, ...]:
    unseen = set(range(len(permutation)))
    lengths = []
    while unseen:
        vertex = min(unseen)
        length = 0
        while vertex in unseen:
            unseen.remove(vertex)
            vertex = permutation[vertex]
            length += 1
        lengths.append(length)
    return tuple(lengths)


def _direct_coefficients(
    deleted: set[tuple[int, int]],
    order: int,
    hook_parameter: int,
) -> tuple[Fraction, ...]:
    degrees = tuple(order - 1 - sum(vertex in edge for edge in deleted) for vertex in range(order))
    coefficients = [0] * (order + 1)
    rank = order - hook_parameter
    for permutation in permutations(range(order)):
        if any(
            index != image and tuple(sorted((index, image))) in deleted
            for index, image in enumerate(permutation)
        ):
            continue
        polynomial = [1]
        for index, image in enumerate(permutation):
            if index != image:
                continue
            updated = [0] * (len(polynomial) + 1)
            for degree, value in enumerate(polynomial):
                updated[degree] -= degrees[index] * value
                updated[degree + 1] += value
            polynomial = updated
        character = hook_character_product(_cycle_lengths(permutation), rank)
        for degree, value in enumerate(polynomial):
            coefficients[degree] += character * value
    dimension = comb(order - 1, rank)
    return tuple(Fraction(coefficients[order - degree], dimension) for degree in range(1, 5))


def test_closed_coefficients_match_direct_immanants() -> None:
    order = 6
    active = [graph for graph in complement_types() if graph.vertex_count <= order]
    for graph in active:
        deleted = set(graph.edges)
        for hook_parameter in range(1, order + 1):
            assert normalized_coefficients(
                graph,
                order,
                hook_parameter,
            ) == _direct_coefficients(deleted, order, hook_parameter)
