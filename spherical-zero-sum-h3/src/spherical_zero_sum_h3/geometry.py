from __future__ import annotations

import math
from itertools import combinations, product

from .roots import FloatVector, h3_float_roots

Matrix = tuple[FloatVector, FloatVector, FloatVector]
TOLERANCE = 1e-7
KEY_DIGITS = 7


def add(left: FloatVector, right: FloatVector) -> FloatVector:
    return tuple(x + y for x, y in zip(left, right, strict=True))  # type: ignore[return-value]


def negate(vector: FloatVector) -> FloatVector:
    return tuple(-coordinate for coordinate in vector)  # type: ignore[return-value]


def dot(left: FloatVector, right: FloatVector) -> float:
    return sum(x * y for x, y in zip(left, right, strict=True))


def norm(vector: FloatVector) -> float:
    return math.sqrt(dot(vector, vector))


def normalize(vector: FloatVector) -> FloatVector:
    length = norm(vector)
    return tuple(coordinate / length for coordinate in vector)  # type: ignore[return-value]


def point_key(vector: FloatVector) -> tuple[float, float, float]:
    return tuple(round(coordinate, KEY_DIGITS) for coordinate in vector)  # type: ignore[return-value]


def deduplicate(points: tuple[FloatVector, ...] | list[FloatVector]) -> tuple[FloatVector, ...]:
    by_key: dict[tuple[float, float, float], FloatVector] = {}
    for point in points:
        by_key.setdefault(point_key(point), point)
    return tuple(by_key.values())


def rotate_x(vector: FloatVector, angle: float) -> FloatVector:
    x, y, z = vector
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return (x, cosine * y - sine * z, sine * y + cosine * z)


def rotate_configuration(
    points: tuple[FloatVector, ...],
    angle: float,
) -> tuple[FloatVector, ...]:
    return tuple(rotate_x(point, angle) for point in points)


def a3_standard_points() -> tuple[FloatVector, ...]:
    points: list[FloatVector] = []
    root_two = math.sqrt(2.0)
    for zero_coordinate in range(3):
        positions = [index for index in range(3) if index != zero_coordinate]
        for signs in product((-1, 1), repeat=2):
            vector = [0.0, 0.0, 0.0]
            vector[positions[0]] = signs[0] / root_two
            vector[positions[1]] = signs[1] / root_two
            points.append(tuple(vector))  # type: ignore[arg-type]
    return tuple(points)


def a3_shared_axis_points() -> tuple[FloatVector, ...]:
    result: list[FloatVector] = []
    root_two = math.sqrt(2.0)
    for x, y, z in a3_standard_points():
        result.append(((x + y) / root_two, (x - y) / root_two, z))
    return tuple(result)


def mat_vec(matrix: Matrix, vector: FloatVector) -> FloatVector:
    return tuple(dot(row, vector) for row in matrix)  # type: ignore[return-value]


def determinant(matrix: Matrix) -> float:
    (a, b, c), (d, e, f), (g, h, i) = matrix
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def matrix_from_columns(
    first: FloatVector,
    second: FloatVector,
    third: FloatVector,
) -> Matrix:
    return (
        (first[0], second[0], third[0]),
        (first[1], second[1], third[1]),
        (first[2], second[2], third[2]),
    )


def configuration_key(points: tuple[FloatVector, ...]) -> tuple[tuple[float, float, float], ...]:
    return tuple(sorted(point_key(point) for point in points))


def zero_sum_edges_float(points: tuple[FloatVector, ...]) -> tuple[tuple[int, int, int], ...]:
    locations = {point_key(point): index for index, point in enumerate(points)}
    edges: set[tuple[int, int, int]] = set()
    for left, right in combinations(range(len(points)), 2):
        target = negate(add(points[left], points[right]))
        final = locations.get(point_key(target))
        if final is None or final <= right:
            continue
        residual = norm(add(add(points[left], points[right]), points[final]))
        if residual < TOLERANCE:
            edges.add((left, right, final))
    return tuple(sorted(edges))


def completions(points: tuple[FloatVector, ...]) -> tuple[FloatVector, ...]:
    result = []
    for left, right in combinations(range(len(points)), 2):
        if abs(dot(points[left], points[right]) + 0.5) < TOLERANCE:
            result.append(negate(add(points[left], points[right])))
    return deduplicate(result)


def _radial_angle(vector: FloatVector) -> float:
    return math.atan2(vector[2], vector[1])


def critical_orientations(
    fixed: tuple[FloatVector, ...],
    moving: tuple[FloatVector, ...],
) -> tuple[float, ...]:
    angles = [0.0]
    for targets, sources in (
        (fixed, moving),
        (completions(fixed), moving),
        (fixed, completions(moving)),
    ):
        for target in targets:
            if math.hypot(target[1], target[2]) < TOLERANCE:
                continue
            for source in sources:
                if abs(target[0] - source[0]) < TOLERANCE:
                    angles.append((_radial_angle(target) - _radial_angle(source)) % (2.0 * math.pi))

    clustered: list[float] = []
    for angle in sorted(angles):
        if not clustered or abs(angle - clustered[-1]) > TOLERANCE:
            clustered.append(angle)

    representatives: dict[tuple[tuple[float, float, float], ...], float] = {}
    for angle in clustered:
        key = configuration_key(rotate_configuration(moving, angle))
        representatives.setdefault(key, angle)
    return tuple(sorted(representatives.values()))


def icosahedral_rotation_group() -> tuple[Matrix, ...]:
    roots = h3_float_roots()
    root_keys = {point_key(root) for root in roots}
    rotations: dict[tuple[float, ...], Matrix] = {}
    for first in roots:
        for second in roots:
            if abs(dot(first, second)) > TOLERANCE:
                continue
            for third in roots:
                if abs(dot(first, third)) > TOLERANCE or abs(dot(second, third)) > TOLERANCE:
                    continue
                matrix = matrix_from_columns(first, second, third)
                if determinant(matrix) < 1.0 - TOLERANCE:
                    continue
                if {point_key(mat_vec(matrix, root)) for root in roots} != root_keys:
                    continue
                key = tuple(round(entry, KEY_DIGITS) for row in matrix for entry in row)
                rotations.setdefault(key, matrix)
    return tuple(rotations.values())


def icosahedron_points() -> tuple[FloatVector, ...]:
    golden_ratio = (1.0 + math.sqrt(5.0)) / 2.0
    result = []
    for permutation in ((0, 1, 2), (2, 0, 1), (1, 2, 0)):
        for first, second in product((-1, 1), repeat=2):
            base = (0.0, float(first), second * golden_ratio)
            result.append(normalize(tuple(base[index] for index in permutation)))  # type: ignore[arg-type]
    return deduplicate(result)


def dodecahedron_points() -> tuple[FloatVector, ...]:
    golden_ratio = (1.0 + math.sqrt(5.0)) / 2.0
    result: list[FloatVector] = [
        normalize(tuple(float(sign) for sign in signs))  # type: ignore[arg-type]
        for signs in product((-1, 1), repeat=3)
    ]
    for permutation in ((0, 1, 2), (2, 0, 1), (1, 2, 0)):
        for first, second in product((-1, 1), repeat=2):
            base = (0.0, first / golden_ratio, second * golden_ratio)
            result.append(normalize(tuple(base[index] for index in permutation)))  # type: ignore[arg-type]
    return deduplicate(result)
