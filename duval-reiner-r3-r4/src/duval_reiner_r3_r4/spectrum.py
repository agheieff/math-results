from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

import numpy as np
from sympy import Matrix, Poly, Rational, Symbol

from .laplacian import IntegerMatrix

Status = Literal["strict", "equality", "violation"]
VARIABLE = Symbol("x")
INITIAL_DENOMINATOR = 100_000
MAX_DENOMINATOR = 10**25


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


@dataclass(frozen=True)
class PartialSumCertificate:
    index: int
    degree_sum: int
    status: Status
    method: str
    lower_bound: Fraction | None = None
    upper_bound: Fraction | None = None
    exact_sum: Fraction | None = None

    def as_dict(self) -> dict[str, int | str]:
        result: dict[str, int | str] = {
            "index": self.index,
            "degree_sum": self.degree_sum,
            "status": self.status,
            "method": self.method,
        }
        if self.lower_bound is not None:
            result["lower_bound"] = _fraction_text(self.lower_bound)
        if self.upper_bound is not None:
            result["upper_bound"] = _fraction_text(self.upper_bound)
        if self.exact_sum is not None:
            result["exact_sum"] = _fraction_text(self.exact_sum)
        return result


@dataclass(frozen=True)
class PolynomialFactor:
    coefficients: tuple[int, ...]
    exponent: int

    def as_dict(self) -> dict[str, int | list[int]]:
        return {"coefficients": list(self.coefficients), "exponent": self.exponent}


@dataclass(frozen=True)
class MatrixCertificate:
    characteristic_polynomial: tuple[int, ...]
    factors: tuple[PolynomialFactor, ...]
    isolation_denominator: int
    partial_sums: tuple[PartialSumCertificate, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "characteristic_polynomial": list(self.characteristic_polynomial),
            "factors": [factor.as_dict() for factor in self.factors],
            "isolation_denominator": self.isolation_denominator,
            "partial_sums": [certificate.as_dict() for certificate in self.partial_sums],
        }


@dataclass(frozen=True)
class _RootBlock:
    factor_index: int
    root_index: int
    lower: Fraction
    upper: Fraction
    multiplicity: int

    @property
    def midpoint(self) -> Fraction:
        return (self.lower + self.upper) / 2


def _to_fraction(value: object) -> Fraction:
    return Fraction(str(value))


def _poly_coefficients(poly: Any) -> tuple[int, ...]:
    return tuple(int(coefficient) for coefficient in poly.all_coeffs())


def _factor_polynomial(poly: Any) -> list[tuple[Any, int]]:
    raw_factors = poly.factor_list()[1]
    return [(factor, int(exponent)) for factor, exponent in raw_factors]


def _isolate_at(
    factors: list[tuple[Any, int]],
    denominator: int,
) -> tuple[_RootBlock, ...] | None:
    blocks = []
    for factor_index, (factor, exponent) in enumerate(factors):
        intervals = factor.intervals(eps=Rational(1, denominator))
        if len(intervals) != factor.degree():
            raise AssertionError("a characteristic-polynomial factor is not totally real")
        for root_index, ((lower, upper), multiplicity) in enumerate(intervals):
            if multiplicity != 1:
                raise AssertionError("an irreducible factor has a repeated root")
            blocks.append(
                _RootBlock(
                    factor_index,
                    root_index,
                    _to_fraction(lower),
                    _to_fraction(upper),
                    exponent,
                )
            )

    blocks.sort(key=lambda block: block.midpoint)
    if any(left.upper >= right.lower for left, right in zip(blocks, blocks[1:], strict=False)):
        return None
    return tuple(blocks)


def _top_occurrences(blocks: tuple[_RootBlock, ...], index: int) -> tuple[int, ...]:
    occurrences = [
        block_index for block_index, block in enumerate(blocks) for _ in range(block.multiplicity)
    ]
    occurrences.sort(key=lambda block_index: blocks[block_index].midpoint, reverse=True)
    return tuple(occurrences[:index])


def _factor_trace_sum(
    factors: list[tuple[Any, int]],
    blocks: tuple[_RootBlock, ...],
    selected: tuple[int, ...],
) -> Fraction | None:
    counts = Counter(selected)
    result = Fraction()
    for factor_index, (factor, _exponent) in enumerate(factors):
        factor_blocks = [
            block_index
            for block_index, block in enumerate(blocks)
            if block.factor_index == factor_index
        ]
        selected_multiplicities = {counts[block_index] for block_index in factor_blocks}
        if len(selected_multiplicities) != 1:
            return None
        layer_count = selected_multiplicities.pop()
        coefficients = _poly_coefficients(factor)
        result += layer_count * Fraction(-coefficients[1], coefficients[0])
    return result


def _certify_from_blocks(
    factors: list[tuple[Any, int]],
    blocks: tuple[_RootBlock, ...],
    index: int,
    degree_sum: int,
) -> PartialSumCertificate | None:
    selected = _top_occurrences(blocks, index)
    lower = sum((blocks[block_index].lower for block_index in selected), Fraction())
    upper = sum((blocks[block_index].upper for block_index in selected), Fraction())
    exact = _factor_trace_sum(factors, blocks, selected)

    if exact == degree_sum:
        return PartialSumCertificate(
            index,
            degree_sum,
            "equality",
            "factor-trace",
            lower,
            upper,
            exact,
        )
    if lower > degree_sum:
        return PartialSumCertificate(
            index,
            degree_sum,
            "violation",
            "rational-root-lower-bound",
            lower,
            upper,
        )
    if upper < degree_sum:
        return PartialSumCertificate(
            index,
            degree_sum,
            "strict",
            "rational-root-upper-bound",
            lower,
            upper,
        )
    return None


def certify_matrix(
    matrix: IntegerMatrix,
    degree_sums: dict[int, int],
) -> MatrixCertificate:
    dimension = len(matrix)
    if any(len(row) != dimension for row in matrix):
        raise ValueError("matrix must be square")
    if any(index < 1 for index in degree_sums):
        raise ValueError("partial-sum indices must be positive")

    if dimension:
        sympy_matrix = Matrix(matrix)
        poly = sympy_matrix.charpoly(VARIABLE).as_poly()
    else:
        poly = Poly(1, VARIABLE)
    coefficients = _poly_coefficients(poly)
    factors = _factor_polynomial(poly)
    factor_records = tuple(
        PolynomialFactor(_poly_coefficients(factor), exponent) for factor, exponent in factors
    )

    trace = sum(matrix[index][index] for index in range(dimension))
    completed: dict[int, PartialSumCertificate] = {}
    unresolved: dict[int, int] = {}
    for index, degree_sum in degree_sums.items():
        if index < dimension:
            unresolved[index] = degree_sum
            continue
        status: Status
        if trace < degree_sum:
            status = "strict"
        elif trace == degree_sum:
            status = "equality"
        else:
            status = "violation"
        completed[index] = PartialSumCertificate(
            index,
            degree_sum,
            status,
            "trace",
            exact_sum=Fraction(trace),
        )

    denominator = INITIAL_DENOMINATOR
    while unresolved:
        blocks = _isolate_at(factors, denominator)
        if blocks is not None:
            newly_completed = {}
            for index, degree_sum in unresolved.items():
                certificate = _certify_from_blocks(factors, blocks, index, degree_sum)
                if certificate is not None:
                    newly_completed[index] = certificate
            completed.update(newly_completed)
            for index in newly_completed:
                del unresolved[index]
        if unresolved:
            denominator *= 100
            if denominator > MAX_DENOMINATOR:
                raise RuntimeError(
                    f"could not certify partial sums at indices {sorted(unresolved)}"
                )

    ordered = tuple(completed[index] for index in sorted(completed))
    return MatrixCertificate(coefficients, factor_records, denominator, ordered)


def numerical_partial_sums(
    matrix: IntegerMatrix,
    indices: tuple[int, ...],
) -> dict[int, float]:
    if not matrix:
        return {index: 0.0 for index in indices}
    eigenvalues = np.linalg.eigvalsh(np.asarray(matrix, dtype=np.float64))[::-1]
    return {index: float(eigenvalues[:index].sum()) for index in indices}
