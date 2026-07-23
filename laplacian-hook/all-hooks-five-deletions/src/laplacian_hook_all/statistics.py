"""Exact graph statistics and normalized top coefficients."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

from .characters import character_ratios
from .graphs import ComplementType


@dataclass(frozen=True)
class ComplementInvariants:
    signature: tuple[tuple[int, int], ...]
    edge_count: int
    degree_square_sum: int
    degree_cube_sum: int
    triangle_count: int


@dataclass(frozen=True)
class GraphStatistics:
    elementary: tuple[int, int, int, int]
    edge_count: int
    edge_outside_degree_sum: int
    edge_outside_e2_sum: int
    triangle_count: int
    triangle_outside_degree_sum: int
    four_cycle_count: int
    two_matching_count: int


def complement_invariants(graph: ComplementType) -> ComplementInvariants:
    adjacency = [set[int]() for _ in range(graph.vertex_count)]
    edge_set = set(graph.edges)
    for left, right in graph.edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    degrees = tuple(len(neighbors) for neighbors in adjacency)
    triangles = sum(
        {(left, middle), (left, right), (middle, right)} <= edge_set
        for left, middle, right in combinations(range(graph.vertex_count), 3)
    )
    return ComplementInvariants(
        graph.signature,
        graph.edge_count,
        sum(value**2 for value in degrees),
        sum(value**3 for value in degrees),
        triangles,
    )


def _elementary(values: tuple[int, ...], degree: int) -> int:
    coefficients = [1] + [0] * degree
    for value in values:
        for index in range(degree, 0, -1):
            coefficients[index] += value * coefficients[index - 1]
    return coefficients[degree]


def graph_statistics(graph: ComplementType, order: int) -> GraphStatistics:
    if order < graph.vertex_count:
        raise ValueError("complement type does not embed at this order")
    deleted = set(graph.edges)
    missing_degrees = [0] * order
    for left, right in graph.edges:
        missing_degrees[left] += 1
        missing_degrees[right] += 1
    degrees = tuple(order - 1 - value for value in missing_degrees)
    elementary_values = tuple(_elementary(degrees, degree) for degree in range(1, 5))
    elementary = (
        elementary_values[0],
        elementary_values[1],
        elementary_values[2],
        elementary_values[3],
    )
    graph_edge_count = math.comb(order, 2) - graph.edge_count
    degree_sum = sum(degrees)
    degree_square_sum = sum(value**2 for value in degrees)
    edge_outside_degree_sum = graph_edge_count * degree_sum - degree_square_sum

    adjacency = [0] * order
    edge_outside_e2_sum = 0
    for left, right in combinations(range(order), 2):
        if (left, right) in deleted:
            continue
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
        endpoint_sum = degrees[left] + degrees[right]
        edge_outside_e2_sum += (
            elementary[1]
            - endpoint_sum * (degree_sum - endpoint_sum)
            - degrees[left] * degrees[right]
        )

    triangle_count = 0
    triangle_outside_degree_sum = 0
    for left, middle, right in combinations(range(order), 3):
        if (left, middle) in deleted or (left, right) in deleted or (middle, right) in deleted:
            continue
        triangle_count += 1
        triangle_outside_degree_sum += degree_sum - degrees[left] - degrees[middle] - degrees[right]

    four_cycle_count = (
        sum(
            math.comb((adjacency[left] & adjacency[right]).bit_count(), 2)
            for left, right in combinations(range(order), 2)
        )
        // 2
    )
    two_matching_count = math.comb(graph_edge_count, 2) - sum(
        math.comb(value, 2) for value in degrees
    )
    return GraphStatistics(
        elementary,
        graph_edge_count,
        edge_outside_degree_sum,
        edge_outside_e2_sum,
        triangle_count,
        triangle_outside_degree_sum,
        four_cycle_count,
        two_matching_count,
    )


def normalized_coefficients(
    graph: ComplementType,
    order: int,
    hook_parameter: int,
) -> tuple[Fraction, ...]:
    statistics = graph_statistics(graph, order)
    transposition, three_cycle, four_cycle, double_transposition = character_ratios(
        order, hook_parameter
    )
    e1, e2, e3, e4 = statistics.elementary
    return (
        Fraction(-e1),
        Fraction(e2) + transposition * statistics.edge_count,
        Fraction(-e3)
        - transposition * statistics.edge_outside_degree_sum
        + three_cycle * statistics.triangle_count,
        Fraction(e4)
        + transposition * statistics.edge_outside_e2_sum
        - three_cycle * statistics.triangle_outside_degree_sum
        + four_cycle * statistics.four_cycle_count
        + double_transposition * statistics.two_matching_count,
    )
