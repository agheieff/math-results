"""Exact normalized coefficients q1 through q7."""

from fractions import Fraction
from functools import cache
from itertools import permutations
from math import comb

from laplacian_hook_eleven_deletions.model import Edge, EdgeSet, adjacency_from_deleted


def elementary(values: tuple[int, ...], degree: int) -> int:
    coefficients = [1] + [0] * degree
    for value in values:
        for index in range(degree, 0, -1):
            coefficients[index] += value * coefficients[index - 1]
    return coefficients[degree]


def _edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def _fixed_cycles(length: int) -> tuple[tuple[int, ...], ...]:
    return tuple((0, *tail) for tail in permutations(range(1, length)) if tail[0] < tail[-1])


FIVE_CYCLES = tuple(
    frozenset(_edge(cycle[index], cycle[(index + 1) % 5]) for index in range(5))
    for cycle in _fixed_cycles(5)
)
SEVEN_CYCLES = tuple(
    frozenset(_edge(cycle[index], cycle[(index + 1) % 7]) for index in range(7))
    for cycle in _fixed_cycles(7)
)


def _choose(total: int, degree: int) -> int:
    return 0 if degree < 0 or total < degree else comb(total, degree)


@cache
def _five_cycle_statistics(
    deleted: EdgeSet,
    order: int,
    degrees: tuple[int, ...],
) -> tuple[int, int]:
    """Return count and sum of degrees on all C5 vertices by inclusion-exclusion."""
    e1 = sum(degrees)
    cycle_count = 0
    incident_degree = 0
    for weight, vertices in _cycle_requirements(deleted, 5):
        vertex_count = len(vertices)
        choices = _choose(order - vertex_count, 5 - vertex_count)
        active_degree = sum(degrees[vertex] for vertex in vertices)
        cycle_count += weight * choices
        incident_degree += weight * (
            choices * active_degree
            + _choose(order - vertex_count - 1, 4 - vertex_count) * (e1 - active_degree)
        )
    return cycle_count, incident_degree


@cache
def normalized_top_five(deleted: EdgeSet, order: int) -> tuple[Fraction, ...]:
    adjacency = adjacency_from_deleted(deleted, order)
    degrees = tuple(sum(row) for row in adjacency)
    e1 = sum(degrees)
    e2 = elementary(degrees, 2)
    graph_edges = sum(degrees) // 2
    missing_neighbors = [set[int]() for _ in range(order)]
    for left, right in deleted:
        missing_neighbors[left].add(right)
        missing_neighbors[right].add(left)
    missing_triangles = (
        sum(len(missing_neighbors[left] & missing_neighbors[right]) for left, right in deleted) // 3
    )
    triangles = (
        comb(order, 3)
        - len(deleted) * (order - 2)
        + sum(comb(len(neighbors), 2) for neighbors in missing_neighbors)
        - missing_triangles
    )
    vertex_triangle_counts = tuple(
        comb(degrees[vertex], 2)
        - sum(
            vertex not in edge
            and edge[0] not in missing_neighbors[vertex]
            and edge[1] not in missing_neighbors[vertex]
            for edge in deleted
        )
        for vertex in range(order)
    )
    triangle_incident_e1 = sum(
        degree * count for degree, count in zip(degrees, vertex_triangle_counts, strict=True)
    )
    triangle_incident_square_sum = sum(
        degree * degree * count
        for degree, count in zip(degrees, vertex_triangle_counts, strict=True)
    )
    triangle_incident_e2 = sum(
        degrees[left]
        * degrees[right]
        * (
            order
            - 2
            - len(missing_neighbors[left])
            - len(missing_neighbors[right])
            + len(missing_neighbors[left] & missing_neighbors[right])
        )
        for left in range(order)
        for right in range(left + 1, order)
        if adjacency[left][right]
    )
    triangle_outside_e1 = triangles * e1 - triangle_incident_e1
    triangle_outside_e2 = (
        triangles * e2
        - e1 * triangle_incident_e1
        + triangle_incident_square_sum
        + triangle_incident_e2
    )

    matching_twos = comb(graph_edges, 2) - sum(comb(degree, 2) for degree in degrees)
    endpoint_weight = 0
    for vertex, degree in enumerate(degrees):
        matching_count = sum(
            graph_edges - degree - degrees[neighbor] + 1
            for neighbor in range(order)
            if adjacency[vertex][neighbor]
        )
        endpoint_weight += degree * matching_count
    matching_outside_e1 = e1 * matching_twos - endpoint_weight
    five_cycles, _ = _five_cycle_statistics(deleted, order, degrees)

    alpha = Fraction(order - 5, 2 * (order - 2))
    beta = Fraction(
        (order - 7) * (order - 9),
        8 * (order - 2) * (order - 4),
    )
    return (
        Fraction(-e1),
        Fraction(e2),
        -elementary(degrees, 3) + alpha * triangles,
        elementary(degrees, 4) - alpha * triangle_outside_e1 - Fraction(matching_twos, order - 2),
        -elementary(degrees, 5)
        + alpha * triangle_outside_e2
        + Fraction(matching_outside_e1, order - 2)
        + beta * five_cycles,
    )


def _exact_quotient(value: int, divisor: int) -> int:
    quotient, remainder = divmod(value, divisor)
    if remainder:
        raise ArithmeticError("nonintegral cycle-cover quotient")
    return quotient


@cache
def normalized_sixth_coefficient(deleted: EdgeSet, order: int) -> Fraction:
    """Optimized q6 formula suitable for exact symbolic sampling."""
    from laplacian_hook_eleven_deletions.cycle_coefficient import _weighted_cycle_covers

    adjacency = adjacency_from_deleted(deleted, order)
    degrees = tuple(sum(row) for row in adjacency)
    graph_edges = [
        (left, right)
        for left in range(order)
        for right in range(left + 1, order)
        if adjacency[left][right]
    ]
    edge_count = len(graph_edges)
    e1 = sum(degrees)
    e2 = elementary(degrees, 2)

    triangle_outside_e3 = _exact_quotient(
        _weighted_cycle_covers(deleted, order, (3,), 3),
        2,
    )
    disjoint_triangle_pairs = _exact_quotient(
        _weighted_cycle_covers(deleted, order, (3, 3), 0),
        4,
    )

    matching_count = comb(edge_count, 2) - sum(comb(degree, 2) for degree in degrees)
    matching_vertex_counts = [
        sum(
            edge_count - degrees[vertex] - degrees[neighbor] + 1
            for neighbor in range(order)
            if adjacency[vertex][neighbor]
        )
        for vertex in range(order)
    ]
    matching_incident_e1 = sum(
        degrees[vertex] * matching_vertex_counts[vertex] for vertex in range(order)
    )
    matching_incident_square_sum = sum(
        degrees[vertex] * degrees[vertex] * matching_vertex_counts[vertex]
        for vertex in range(order)
    )
    matching_incident_e2 = 0
    for left in range(order):
        for right in range(left + 1, order):
            adjacent = adjacency[left][right]
            common_neighbors = sum(
                adjacency[left][vertex] * adjacency[right][vertex] for vertex in range(order)
            )
            separate_edges = (degrees[left] - adjacent) * (
                degrees[right] - adjacent
            ) - common_neighbors
            shared_edge_matchings = (
                edge_count - degrees[left] - degrees[right] + 1 if adjacent else 0
            )
            matching_incident_e2 += (
                degrees[left] * degrees[right] * (separate_edges + shared_edge_matchings)
            )
    matching_outside_e2 = (
        matching_count * e2
        - e1 * matching_incident_e1
        + matching_incident_square_sum
        + matching_incident_e2
    )

    five_cycles, five_cycle_incident_degree = _five_cycle_statistics(
        deleted,
        order,
        degrees,
    )
    five_cycle_outside_e1 = e1 * five_cycles - five_cycle_incident_degree

    four_cycle_edge_pairs = _exact_quotient(
        _weighted_cycle_covers(deleted, order, (4, 2), 0),
        2,
    )

    alpha = Fraction(order - 5, 2 * (order - 2))
    beta = Fraction(
        (order - 7) * (order - 9),
        8 * (order - 2) * (order - 4),
    )
    gamma = Fraction(
        order**2 - 12 * order + 59,
        4 * (order - 4) * (order - 2),
    )
    delta = Fraction(-(order - 7), (order - 4) * (order - 2))
    return (
        elementary(degrees, 6)
        - alpha * triangle_outside_e3
        - Fraction(matching_outside_e2, order - 2)
        - beta * five_cycle_outside_e1
        + gamma * disjoint_triangle_pairs
        + delta * four_cycle_edge_pairs
    )


@cache
def _cycle_requirements(
    deleted: EdgeSet,
    length: int,
) -> tuple[tuple[int, tuple[int, ...]], ...]:
    fixed_cycles = FIVE_CYCLES if length == 5 else SEVEN_CYCLES
    missing = tuple(sorted(deleted))
    output: list[tuple[int, tuple[int, ...]]] = []
    for mask in range(1 << len(missing)):
        required = tuple(missing[index] for index in range(len(missing)) if mask & (1 << index))
        vertices = tuple(sorted({vertex for edge in required for vertex in edge}))
        if len(vertices) > length:
            continue
        relabel = {vertex: index for index, vertex in enumerate(vertices)}
        mapped = frozenset(_edge(relabel[left], relabel[right]) for left, right in required)
        fixed_count = sum(mapped <= cycle for cycle in fixed_cycles)
        if fixed_count:
            sign = -1 if mask.bit_count() % 2 else 1
            output.append((sign * fixed_count, vertices))
    return tuple(output)


def _cycle_count(deleted: EdgeSet, order: int, length: int) -> int:
    return sum(
        weight * _choose(order - len(vertices), length - len(vertices))
        for weight, vertices in _cycle_requirements(deleted, length)
    )


def _outside_elementary(
    global_values: tuple[int, ...],
    degrees: tuple[int, ...],
    vertices: tuple[int, ...],
    degree: int,
) -> int:
    values = list(global_values[: degree + 1])
    for vertex in vertices:
        removed = [1] + [0] * degree
        for index in range(1, degree + 1):
            removed[index] = values[index] - degrees[vertex] * removed[index - 1]
        values = removed
    return values[degree]


def _five_cycle_outside_e2(
    deleted: EdgeSet,
    order: int,
    degrees: tuple[int, ...],
) -> int:
    global_e1 = sum(degrees)
    global_e2 = elementary(degrees, 2)
    output = 0
    for weight, required in _cycle_requirements(deleted, 5):
        required_set = set(required)
        active = tuple(degrees[vertex] for vertex in required)
        pool = tuple(degrees[vertex] for vertex in range(order) if vertex not in required_set)
        selected = 5 - len(required)
        pool_size = len(pool)
        active_e1 = sum(active)
        active_square_sum = sum(value * value for value in active)
        active_e2 = elementary(active, 2)
        pool_e1 = sum(pool)
        pool_square_sum = sum(value * value for value in pool)
        pool_e2 = elementary(pool, 2)
        choices = _choose(pool_size, selected)
        one_choices = _choose(pool_size - 1, selected - 1)
        two_choices = _choose(pool_size - 2, selected - 2)
        incident_e1 = choices * active_e1 + one_choices * pool_e1
        square_plus_e2 = (
            choices * (active_square_sum + active_e2)
            + one_choices * (pool_square_sum + active_e1 * pool_e1)
            + two_choices * pool_e2
        )
        output += weight * (choices * global_e2 - global_e1 * incident_e1 + square_plus_e2)
    return output


@cache
def normalized_seventh_coefficient(deleted: EdgeSet, order: int) -> Fraction:
    """Optimized exact q7 cycle-type formula."""
    from laplacian_hook_eleven_deletions.cycle_coefficient import _weighted_cycle_covers

    adjacency = adjacency_from_deleted(deleted, order)
    degrees = tuple(sum(row) for row in adjacency)
    global_elementary = tuple(elementary(degrees, degree) for degree in range(8))
    triangle_outside_e4 = _exact_quotient(
        _weighted_cycle_covers(deleted, order, (3,), 4),
        2,
    )
    matching_outside_e3 = _weighted_cycle_covers(deleted, order, (2, 2), 3)
    five_cycle_outside_e2 = _exact_quotient(
        _weighted_cycle_covers(deleted, order, (5,), 2),
        2,
    )
    triangle_pair_outside_e1 = _exact_quotient(
        _weighted_cycle_covers(deleted, order, (3, 3), 1),
        4,
    )
    four_two_outside_e1 = _exact_quotient(
        _weighted_cycle_covers(deleted, order, (4, 2), 1),
        2,
    )
    seven_cycles = _exact_quotient(
        _weighted_cycle_covers(deleted, order, (7,), 0),
        2,
    )
    three_two_two = _exact_quotient(
        _weighted_cycle_covers(deleted, order, (3, 2, 2), 0),
        2,
    )

    alpha = Fraction(order - 5, 2 * (order - 2))
    beta = Fraction(
        (order - 7) * (order - 9),
        8 * (order - 2) * (order - 4),
    )
    gamma = Fraction(
        order**2 - 12 * order + 59,
        4 * (order - 4) * (order - 2),
    )
    delta = Fraction(-(order - 7), (order - 4) * (order - 2))
    epsilon = Fraction(
        (order - 13) * (order - 11) * (order - 9),
        32 * (order - 6) * (order - 4) * (order - 2),
    )
    zeta = Fraction(-(order - 13), 2 * (order - 4) * (order - 2))
    return (
        -global_elementary[7]
        + alpha * triangle_outside_e4
        + Fraction(matching_outside_e3, order - 2)
        + beta * five_cycle_outside_e2
        - gamma * triangle_pair_outside_e1
        - delta * four_two_outside_e1
        + epsilon * seven_cycles
        + zeta * three_two_two
    )
