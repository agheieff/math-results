from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

from .geometry import (
    a3_shared_axis_points,
    a3_standard_points,
    configuration_key,
    critical_orientations,
    deduplicate,
    dodecahedron_points,
    icosahedral_rotation_group,
    icosahedron_points,
    mat_vec,
    rotate_configuration,
    zero_sum_edges_float,
)
from .optimizer import Outcome, independence_number
from .roots import FloatVector, h3_float_roots


def evaluate(points: tuple[FloatVector, ...]) -> Outcome:
    edges = zero_sum_edges_float(points)
    return Outcome(len(points), len(edges), independence_number(len(points), edges))


def union(configurations: list[tuple[FloatVector, ...]]) -> tuple[FloatVector, ...]:
    return deduplicate([point for configuration in configurations for point in configuration])


def component_profile(
    vertex_count: int,
    edges: tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, int], ...]:
    adjacency: list[set[int]] = [set() for _ in range(vertex_count)]
    for edge in edges:
        for vertex in edge:
            adjacency[vertex].update(other for other in edge if other != vertex)

    unseen = set(range(vertex_count))
    components: list[set[int]] = []
    while unseen:
        start = next(iter(unseen))
        component = {start}
        frontier = [start]
        unseen.remove(start)
        while frontier:
            vertex = frontier.pop()
            neighbors = adjacency[vertex] & unseen
            unseen.difference_update(neighbors)
            component.update(neighbors)
            frontier.extend(neighbors)
        components.append(component)

    profile = [
        (len(component), sum(set(edge) <= component for edge in edges)) for component in components
    ]
    return tuple(sorted(profile, reverse=True))


@dataclass(frozen=True)
class FamilySummary:
    name: str
    cases: int
    equality_cases: int
    distinct_outcomes: int
    best: Outcome

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "cases": self.cases,
            "equality_cases": self.equality_cases,
            "distinct_outcomes": self.distinct_outcomes,
            "best": self.best.as_dict(),
        }


def summarize(name: str, outcomes: list[Outcome]) -> FamilySummary:
    best = min(outcomes, key=lambda outcome: outcome.ratio)
    equality_cases = sum(outcome.ratio == Fraction(2, 3) for outcome in outcomes)
    distinct = len({(item.vertices, item.edges, item.independence) for item in outcomes})
    return FamilySummary(name, len(outcomes), equality_cases, distinct, best)


def _subset_outcomes(
    configurations: tuple[tuple[FloatVector, ...], ...],
    fixed: tuple[FloatVector, ...] | None,
) -> list[Outcome]:
    outcomes = []
    minimum_size = 0 if fixed is not None else 1
    for size in range(minimum_size, len(configurations) + 1):
        for chosen in combinations(configurations, size):
            parts = ([] if fixed is None else [fixed]) + list(chosen)
            outcomes.append(evaluate(union(parts)))
    return outcomes


def critical_subset_search() -> tuple[FamilySummary, ...]:
    h3 = h3_float_roots()
    a3 = a3_shared_axis_points()
    aa = tuple(rotate_configuration(a3, angle) for angle in critical_orientations(a3, a3))
    ha = tuple(rotate_configuration(a3, angle) for angle in critical_orientations(h3, a3))
    hh = tuple(rotate_configuration(h3, angle) for angle in critical_orientations(h3, h3))
    return (
        summarize("A3 critical subsets", _subset_outcomes(aa, None)),
        summarize("H3 plus A3 critical subsets", _subset_outcomes(ha, h3)),
        summarize("H3 critical subsets", _subset_outcomes(hh, None)),
    )


def generic_pair_search() -> FamilySummary:
    h3 = h3_float_roots()
    a3 = a3_shared_axis_points()
    angle = math.pi / math.sqrt(2.0)
    outcomes = [
        evaluate(union([a3, rotate_configuration(a3, angle)])),
        evaluate(union([h3, rotate_configuration(a3, angle)])),
        evaluate(union([h3, rotate_configuration(h3, angle)])),
    ]
    return summarize("generic shared-axis pairs", outcomes)


def mixed_critical_search() -> FamilySummary:
    h3 = h3_float_roots()
    a3 = a3_shared_axis_points()
    hh_angles = critical_orientations(h3, h3)
    ha_angles = critical_orientations(h3, a3)
    h3_optional = [
        rotate_configuration(h3, angle)
        for angle in hh_angles
        if configuration_key(rotate_configuration(h3, angle)) != configuration_key(h3)
    ]
    a3_optional = [rotate_configuration(a3, angle) for angle in ha_angles]
    optional = h3_optional + a3_optional
    if len(optional) != 11:
        raise AssertionError("unexpected critical orientation count")

    outcomes = []
    for mask in range(1 << len(optional)):
        chosen = [
            configuration for index, configuration in enumerate(optional) if mask >> index & 1
        ]
        outcomes.append(evaluate(union([h3, *chosen])))
    return summarize("mixed critical subsets", outcomes)


def generic_offset_search() -> tuple[FamilySummary, ...]:
    h3 = h3_float_roots()
    a3 = a3_shared_axis_points()
    offset = math.pi / math.sqrt(2.0)
    aa = tuple(rotate_configuration(a3, offset + angle) for angle in critical_orientations(a3, a3))
    hh = tuple(rotate_configuration(h3, offset + angle) for angle in critical_orientations(h3, h3))
    return (
        summarize("generic-offset A3 clusters", _subset_outcomes(aa, h3)[1:]),
        summarize("generic-offset H3 clusters", _subset_outcomes(hh, h3)[1:]),
    )


def _orbit_configurations(
    seed: tuple[FloatVector, ...],
) -> tuple[tuple[FloatVector, ...], ...]:
    configurations: dict[
        tuple[tuple[float, float, float], ...],
        tuple[FloatVector, ...],
    ] = {}
    for rotation in icosahedral_rotation_group():
        transformed = tuple(mat_vec(rotation, point) for point in seed)
        configurations.setdefault(configuration_key(transformed), transformed)
    return tuple(configurations.values())


def natural_orbit_search() -> dict[str, object]:
    rotations = icosahedral_rotation_group()
    if len(rotations) != 60:
        raise AssertionError("unexpected icosahedral rotation group order")

    h3 = h3_float_roots()
    standard_a3_orbit = _orbit_configurations(a3_standard_points())
    standard_a3_union = union(list(standard_a3_orbit))
    standard_outcome = evaluate(standard_a3_union)
    h3_plus_standard_points = union([h3, standard_a3_union])
    h3_plus_standard_edges = zero_sum_edges_float(h3_plus_standard_points)
    h3_plus_standard_outcome = Outcome(
        len(h3_plus_standard_points),
        len(h3_plus_standard_edges),
        independence_number(len(h3_plus_standard_points), h3_plus_standard_edges),
    )
    h3_plus_standard_profile = component_profile(
        len(h3_plus_standard_points),
        h3_plus_standard_edges,
    )
    expected_profile = ((30, 20),) + ((12, 8),) * 5
    if h3_plus_standard_profile != expected_profile:
        raise AssertionError("unexpected H3 plus standard A3 orbit decomposition")

    shell_points = {
        "I12": icosahedron_points(),
        "D20": dodecahedron_points(),
        "H30": h3,
        "A60": standard_a3_union,
    }
    shell_outcomes = []
    names = tuple(shell_points)
    for size in range(1, len(names) + 1):
        for selected in combinations(names, size):
            shell_outcomes.append(evaluate(union([shell_points[name] for name in selected])))

    shared_a3 = a3_shared_axis_points()
    a3_orbit_outcomes = []
    for angle in critical_orientations(h3, shared_a3):
        configurations = _orbit_configurations(rotate_configuration(shared_a3, angle))
        a3_orbit_outcomes.append(evaluate(union(list(configurations))))

    h3_orbit_outcomes = []
    for angle in critical_orientations(h3, h3):
        configurations = _orbit_configurations(rotate_configuration(h3, angle))
        h3_orbit_outcomes.append(evaluate(union(list(configurations))))

    all_outcomes = [standard_outcome, *shell_outcomes, *a3_orbit_outcomes, *h3_orbit_outcomes]
    summary = summarize("natural icosahedral orbits", all_outcomes)
    return {
        "group_order": len(rotations),
        "standard_a3_configuration_orbit": len(standard_a3_orbit),
        "standard_a3_union": standard_outcome.as_dict(),
        "h3_plus_standard_a3_union": h3_plus_standard_outcome.as_dict(),
        "h3_plus_standard_a3_components": [
            {"vertices": vertices, "edges": edges} for vertices, edges in h3_plus_standard_profile
        ],
        "shell_unions": len(shell_outcomes),
        "shared_a3_orbits": len(a3_orbit_outcomes),
        "shared_h3_orbits": len(h3_orbit_outcomes),
        "summary": summary.as_dict(),
    }


def run_bounded_search() -> dict[str, object]:
    critical = critical_subset_search()
    generic_offsets = generic_offset_search()
    return {
        "critical_orientation_counts": {
            "A3_A3": len(critical_orientations(a3_shared_axis_points(), a3_shared_axis_points())),
            "H3_A3": len(critical_orientations(h3_float_roots(), a3_shared_axis_points())),
            "H3_H3": len(critical_orientations(h3_float_roots(), h3_float_roots())),
        },
        "generic_pairs": generic_pair_search().as_dict(),
        "critical_subsets": [summary.as_dict() for summary in critical],
        "mixed": mixed_critical_search().as_dict(),
        "generic_offsets": [summary.as_dict() for summary in generic_offsets],
        "natural_orbits": natural_orbit_search(),
    }
