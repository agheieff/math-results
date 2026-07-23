"""Exact eight-dimensional adjacency-kernel certificate."""

from fractions import Fraction
from functools import cache

from .model import Vertex, neighbors

Vector = tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]

ZERO: Vector = (Fraction(0),) * 8
BASIS: tuple[Vector, ...] = tuple(
    tuple(Fraction(int(row == column)) for column in range(8))  # type: ignore[misc]
    for row in range(8)
)


def _add(*vectors: Vector) -> Vector:
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True))  # type: ignore[return-value]


def _negate(vector: Vector) -> Vector:
    return tuple(-value for value in vector)  # type: ignore[return-value]


@cache
def outer_evaluation(index: int) -> Vector:
    """Return the evaluation row for u_index in initial coordinates u_-4,...,u_3."""
    if -4 <= index <= 3:
        return BASIS[index + 4]
    if index >= 4:
        center = index - 4
        return _add(
            outer_evaluation(center),
            _negate(outer_evaluation(center - 4)),
            _negate(outer_evaluation(center - 2)),
            _negate(outer_evaluation(center + 2)),
        )
    center = index + 4
    return _add(
        outer_evaluation(center),
        _negate(outer_evaluation(center - 2)),
        _negate(outer_evaluation(center + 2)),
        _negate(outer_evaluation(center + 4)),
    )


@cache
def evaluation(vertex: Vertex) -> Vector:
    if vertex.layer == "u":
        return outer_evaluation(vertex.index)
    return _negate(
        _add(
            outer_evaluation(vertex.index - 1),
            outer_evaluation(vertex.index + 1),
        )
    )


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def solution_value(initial: Vector, vertex: Vertex) -> Fraction:
    return dot(evaluation(vertex), initial)


def adjacency_residual(initial: Vector, vertex: Vertex) -> Fraction:
    return sum((solution_value(initial, item) for item in neighbors(vertex)), Fraction(0))


def null_vector_for(vertices: tuple[Vertex, ...]) -> Vector:
    """Return a nonzero exact kernel parameter vanishing on at most seven vertices."""
    if len(vertices) > 7:
        raise ValueError("the dimension argument only guarantees a witness through seven rows")
    matrix = [list(evaluation(vertex)) for vertex in vertices]
    pivot_columns: list[int] = []
    row = 0
    for column in range(8):
        pivot = next((index for index in range(row, len(matrix)) if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        scale = matrix[row][column]
        matrix[row] = [value / scale for value in matrix[row]]
        for other in range(len(matrix)):
            if other == row or not matrix[other][column]:
                continue
            factor = matrix[other][column]
            matrix[other] = [
                value - factor * pivot_value
                for value, pivot_value in zip(matrix[other], matrix[row], strict=True)
            ]
        pivot_columns.append(column)
        row += 1
        if row == len(matrix):
            break

    free_column = next(column for column in range(8) if column not in pivot_columns)
    result = [Fraction(0)] * 8
    result[free_column] = Fraction(1)
    for pivot_row in range(len(pivot_columns) - 1, -1, -1):
        column = pivot_columns[pivot_row]
        result[column] = -sum(
            (matrix[pivot_row][other] * result[other] for other in range(column + 1, 8)),
            Fraction(0),
        )
    witness: Vector = tuple(result)  # type: ignore[assignment]
    if witness == ZERO or any(solution_value(witness, vertex) for vertex in vertices):
        raise AssertionError("exact nullspace construction failed")
    return witness
