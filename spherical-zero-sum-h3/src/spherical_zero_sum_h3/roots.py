from __future__ import annotations

from fractions import Fraction
from itertools import product

from .field import INVERSE_PHI, ONE, PHI, ZERO, QPhi

ExactVector = tuple[QPhi, QPhi, QPhi]
FloatVector = tuple[float, float, float]


def vector_scale(vector: ExactVector, factor: Fraction) -> ExactVector:
    return tuple(coordinate.scale(factor) for coordinate in vector)  # type: ignore[return-value]


def vector_add(left: ExactVector, right: ExactVector) -> ExactVector:
    return tuple(x + y for x, y in zip(left, right, strict=True))  # type: ignore[return-value]


def vector_negate(vector: ExactVector) -> ExactVector:
    return tuple(-coordinate for coordinate in vector)  # type: ignore[return-value]


def squared_norm(vector: ExactVector) -> QPhi:
    result = ZERO
    for coordinate in vector:
        result = result + coordinate * coordinate
    return result


def to_float(vector: ExactVector) -> FloatVector:
    return tuple(coordinate.to_float() for coordinate in vector)  # type: ignore[return-value]


def h3_roots() -> tuple[ExactVector, ...]:
    roots: list[ExactVector] = []
    for coordinate in range(3):
        for sign in (-1, 1):
            vector = [ZERO, ZERO, ZERO]
            vector[coordinate] = ONE.scale(Fraction(sign))
            roots.append(tuple(vector))  # type: ignore[arg-type]

    half = Fraction(1, 2)
    base = (ONE.scale(half), PHI.scale(half), INVERSE_PHI.scale(half))
    for permutation in ((0, 1, 2), (2, 0, 1), (1, 2, 0)):
        for signs in product((-1, 1), repeat=3):
            root = tuple(
                base[permutation[index]].scale(Fraction(signs[index])) for index in range(3)
            )
            roots.append((root[0], root[1], root[2]))
    return tuple(roots)


def h3_float_roots() -> tuple[FloatVector, ...]:
    return tuple(to_float(root) for root in h3_roots())
