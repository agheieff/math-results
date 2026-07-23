"""Stable symbolic audit and exact boundary gates."""

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from hashlib import sha256
from math import comb, factorial, isqrt

from laplacian_hook_eleven_deletions.census import (
    augmentation_census,
    burnside_census,
    feasible_census,
    format_graph_key,
)
from laplacian_hook_eleven_deletions.coefficients import (
    normalized_seventh_coefficient,
    normalized_sixth_coefficient,
    normalized_top_five,
)
from laplacian_hook_eleven_deletions.cycle_coefficient import normalized_coefficient
from laplacian_hook_eleven_deletions.immanant import hook_immanantal_polynomial
from laplacian_hook_eleven_deletions.model import (
    EdgeSet,
    GraphKey,
    active_support,
    adjacency_from_deleted,
    compact_edges,
)

REFERENCE_ORDER = 23
TOP_SAMPLES = tuple(range(REFERENCE_ORDER, REFERENCE_ORDER + 13))
Q6_SAMPLES = tuple(range(REFERENCE_ORDER, REFERENCE_ORDER + 15))
Q7_SAMPLES = tuple(range(REFERENCE_ORDER, REFERENCE_ORDER + 18))
Q8_SAMPLES = tuple(range(REFERENCE_ORDER, REFERENCE_ORDER + 40, 2))
CLEARED_DEGREE_BOUNDS = (2, 4, 7, 9, 12, 14, 17, 19)


@dataclass(frozen=True)
class Record:
    key: GraphKey
    name: str
    deleted: EdgeSet
    deletions: int
    support: int


@dataclass(frozen=True)
class StableQ6Pair:
    left: Record
    right: Record
    polynomial: tuple[int, ...]

    def as_json(self) -> dict[str, object]:
        return {
            "left": self.left.name,
            "right": self.right.name,
            "left_edges": [list(edge) for edge in sorted(self.left.deleted)],
            "right_edges": [list(edge) for edge in sorted(self.right.deleted)],
            "scaled_q6_numerator_coefficients": list(self.polynomial),
            "q6_difference": f"({format_polynomial(self.polynomial)})/[8(n-2)(n-4)]",
        }


@dataclass(frozen=True)
class StableQ7Pair:
    left: Record
    right: Record
    polynomial: tuple[int, ...]

    def as_json(self) -> dict[str, object]:
        return {
            "left": self.left.name,
            "right": self.right.name,
            "left_edges": [list(edge) for edge in sorted(self.left.deleted)],
            "right_edges": [list(edge) for edge in sorted(self.right.deleted)],
            "scaled_q7_numerator_coefficients": list(self.polynomial),
            "q7_difference": (f"({format_polynomial(self.polynomial)})/[32(n-6)(n-4)(n-2)]"),
        }


@dataclass(frozen=True)
class StableQ8Pair:
    left: Record
    right: Record
    polynomial: tuple[int, ...]

    def as_json(self) -> dict[str, object]:
        return {
            "left": self.left.name,
            "right": self.right.name,
            "left_edges": [list(edge) for edge in sorted(self.left.deleted)],
            "right_edges": [list(edge) for edge in sorted(self.right.deleted)],
            "sample_variable": "m=(n-23)/2",
            "scaled_q8_numerator_coefficients_in_m": list(self.polynomial),
            "q8_difference": (f"({format_polynomial(self.polynomial, 'm')})/[32(n-6)(n-4)(n-2)]"),
        }


@dataclass(frozen=True)
class StableSpecialization:
    left: Record
    right: Record
    first_index: int
    order: int
    polynomial: tuple[int, ...]
    separating_index: int
    separating_difference: Fraction

    def as_json(self) -> dict[str, object]:
        return {
            "left": self.left.name,
            "right": self.right.name,
            "order": self.order,
            "left_edges": [list(edge) for edge in sorted(self.left.deleted)],
            "right_edges": [list(edge) for edge in sorted(self.right.deleted)],
            "specialized_first_index": self.first_index,
            "scaled_difference_numerator_coefficients": list(self.polynomial),
            "separating_index_at_order": self.separating_index,
            "separating_difference_at_order": str(self.separating_difference),
        }


@dataclass(frozen=True)
class StableAudit:
    records: tuple[Record, ...]
    histogram: tuple[int, int, int, int, int, int, int, int]
    identity_group_count: int
    q6_pairs: tuple[StableQ6Pair, ...]
    q7_pairs: tuple[StableQ7Pair, ...]
    q8_pairs: tuple[StableQ8Pair, ...]
    specializations: tuple[StableSpecialization, ...]
    signature_sha256: str

    def as_json(self) -> dict[str, object]:
        return {
            "orders": "all odd n>=23",
            "class_count": len(self.records),
            "pair_count": len(self.records) * (len(self.records) - 1) // 2,
            "top_interpolation_orders": list(TOP_SAMPLES),
            "q6_interpolation_orders": list(Q6_SAMPLES),
            "q7_interpolation_orders": list(Q7_SAMPLES),
            "q8_interpolation_orders": list(Q8_SAMPLES),
            "cleared_degree_bounds": list(CLEARED_DEGREE_BOUNDS),
            "symbolic_first_difference_index_histogram": {
                str(index): value for index, value in enumerate(self.histogram, start=1)
            },
            "top_five_identity_group_count": self.identity_group_count,
            "q6_separated_identity_pair_count": len(self.q6_pairs),
            "q6_separated_identity_pairs": [pair.as_json() for pair in self.q6_pairs],
            "q6_identity_pair_count": len(self.q7_pairs),
            "q6_identity_pairs": [pair.as_json() for pair in self.q7_pairs],
            "q7_identity_pair_count": len(self.q8_pairs),
            "q7_identity_pairs": [pair.as_json() for pair in self.q8_pairs],
            "odd_specialization_count": len(self.specializations),
            "odd_specializations": [
                specialization.as_json() for specialization in self.specializations
            ],
            "signature_certificate_sha256": self.signature_sha256,
        }


@dataclass(frozen=True)
class BoundaryDeepPair:
    left: Record
    right: Record
    first_index: int
    difference: Fraction
    left_polynomial: tuple[int, ...] | None = None
    right_polynomial: tuple[int, ...] | None = None

    def as_json(self) -> dict[str, object]:
        result: dict[str, object] = {
            "left": self.left.name,
            "right": self.right.name,
            "left_edges": [list(edge) for edge in sorted(self.left.deleted)],
            "right_edges": [list(edge) for edge in sorted(self.right.deleted)],
            "first_difference_index": self.first_index,
            "normalized_difference": str(self.difference),
        }
        if self.left_polynomial is not None and self.right_polynomial is not None:
            result["left_full_polynomial"] = list(self.left_polynomial)
            result["right_full_polynomial"] = list(self.right_polynomial)
        return result


@dataclass(frozen=True)
class BoundaryAudit:
    order: int
    counts: tuple[int, ...]
    histogram: tuple[int, int, int, int, int, int, int, int]
    deep_pairs: tuple[BoundaryDeepPair, ...]
    signature_sha256: str

    def as_json(self) -> dict[str, object]:
        total = sum(self.counts)
        return {
            "order": self.order,
            "deletion_class_counts": list(self.counts),
            "class_count": total,
            "pair_count": total * (total - 1) // 2,
            "first_difference_index_histogram": {
                str(index): value for index, value in enumerate(self.histogram, start=1)
            },
            "top_five_residual_pair_count": len(self.deep_pairs),
            "top_five_residual_pairs": [pair.as_json() for pair in self.deep_pairs],
            "signature_certificate_sha256": self.signature_sha256,
        }


def records_from_census(
    census: tuple[dict[GraphKey, EdgeSet], ...],
    order: int,
) -> tuple[Record, ...]:
    return tuple(
        Record(
            key=key,
            name=format_graph_key(key),
            deleted=compact_edges(representative),
            deletions=deletions,
            support=active_support(representative),
        )
        for deletions, level in enumerate(census)
        for key, representative in sorted(level.items())
        if sum(component_order for component_order, _ in key) <= order
    )


def _cleared(value: Fraction, index: int, order: int) -> int:
    if index in (3, 4):
        value *= 2 * (order - 2)
    elif index in (5, 6):
        value *= 8 * (order - 2) * (order - 4)
    elif index in (7, 8):
        value *= 32 * (order - 6) * (order - 4) * (order - 2)
    if value.denominator != 1:
        raise ArithmeticError("cleared coefficient was not integral")
    return value.numerator


def _multiply_ascending(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    output = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            output[left_index + right_index] += left_value * right_value
    return output


def interpolate(values: tuple[int, ...], origin: int) -> tuple[int, ...]:
    differences = list(values)
    newton: list[Fraction] = []
    degree = 0
    while differences:
        newton.append(Fraction(differences[0], factorial(degree)))
        differences = [
            right - left for left, right in zip(differences, differences[1:], strict=False)
        ]
        degree += 1
    polynomial = [Fraction(0)]
    basis = [Fraction(1)]
    for index, coefficient in enumerate(newton):
        if len(polynomial) < len(basis):
            polynomial.extend(Fraction(0) for _ in range(len(basis) - len(polynomial)))
        for power, value in enumerate(basis):
            polynomial[power] += coefficient * value
        basis = _multiply_ascending(basis, [Fraction(-(origin + index)), Fraction(1)])
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial.pop()
    if any(value.denominator != 1 for value in polynomial):
        raise AssertionError("interpolant was not integral")
    return tuple(value.numerator for value in reversed(polynomial))


def evaluate(polynomial: tuple[int, ...], value: int) -> int:
    result = 0
    for coefficient in polynomial:
        result = result * value + coefficient
    return result


def _odd_integer_roots(polynomial: tuple[int, ...], threshold: int) -> tuple[int, ...]:
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial = polynomial[:-1]
    if len(polynomial) == 1:
        if polynomial[0] == 0:
            raise AssertionError("zero difference polynomial")
        return ()
    constant = abs(polynomial[-1])
    candidates: set[int] = set()
    for divisor in range(1, isqrt(constant) + 1):
        if constant % divisor:
            continue
        candidates.add(divisor)
        candidates.add(constant // divisor)
    return tuple(
        candidate
        for candidate in sorted(candidates)
        if candidate >= threshold and candidate % 2 and evaluate(polynomial, candidate) == 0
    )


def _nonnegative_integer_roots(polynomial: tuple[int, ...]) -> tuple[int, ...]:
    has_zero_root = polynomial[-1] == 0
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial = polynomial[:-1]
    if len(polynomial) == 1:
        if polynomial[0] == 0:
            raise AssertionError("zero difference polynomial")
        return ()
    constant = abs(polynomial[-1])
    candidates: set[int] = set()
    for divisor in range(1, isqrt(constant) + 1):
        if not constant % divisor:
            candidates.add(divisor)
            candidates.add(constant // divisor)
    roots = tuple(
        candidate for candidate in sorted(candidates) if evaluate(polynomial, candidate) == 0
    )
    return (0, *roots) if has_zero_root else roots


def format_polynomial(polynomial: tuple[int, ...], variable_name: str = "n") -> str:
    degree = len(polynomial) - 1
    terms: list[str] = []
    for index, coefficient in enumerate(polynomial):
        power = degree - index
        if coefficient == 0:
            continue
        magnitude = abs(coefficient)
        variable = (
            "" if power == 0 else (variable_name if power == 1 else f"{variable_name}^{power}")
        )
        body = variable if magnitude == 1 and variable else f"{magnitude}{variable}"
        if not terms:
            terms.append(body if coefficient > 0 else f"-{body}")
        else:
            terms.append(("+" if coefficient > 0 else "-") + body)
    return "".join(terms)


def _pair_count(size: int) -> int:
    return size * (size - 1) // 2


def _normalized_coefficient(record: Record, index: int, order: int) -> Fraction:
    if index <= 5:
        return normalized_top_five(record.deleted, order)[index - 1]
    if index == 6:
        return normalized_sixth_coefficient(record.deleted, order)
    if index == 7:
        return normalized_seventh_coefficient(record.deleted, order)
    if index == 8:
        return normalized_coefficient(record.deleted, order, 8)
    raise ValueError("unsupported coefficient index")


def _specialization(
    left: Record,
    right: Record,
    first_index: int,
    order: int,
    polynomial: tuple[int, ...],
) -> StableSpecialization:
    for separating_index in range(first_index + 1, 9):
        difference = _normalized_coefficient(
            left, separating_index, order
        ) - _normalized_coefficient(right, separating_index, order)
        if difference:
            return StableSpecialization(
                left,
                right,
                first_index,
                order,
                polynomial,
                separating_index,
                difference,
            )
    raise AssertionError("q1,...,q7 failed at a stable specialization")


@cache
def stable_audit() -> StableAudit:
    records = records_from_census(augmentation_census(), REFERENCE_ORDER)
    top_values = {
        record.name: tuple(normalized_top_five(record.deleted, order) for order in TOP_SAMPLES)
        for record in records
    }
    signatures = {
        record.name: tuple(
            tuple(
                _cleared(values[index - 1], index, order)
                for order, values in zip(TOP_SAMPLES, top_values[record.name], strict=True)
            )
            for index in range(1, 6)
        )
        for record in records
    }
    digest = sha256()
    for record in records:
        digest.update(f"{record.name}|{signatures[record.name]}\n".encode())

    buckets: list[list[Record]] = [list(records)]
    histogram: defaultdict[int, int] = defaultdict(int)
    specializations: list[StableSpecialization] = []
    for index in range(1, 6):
        next_buckets: list[list[Record]] = []
        for bucket in buckets:
            groups: defaultdict[tuple[int, ...], list[Record]] = defaultdict(list)
            for record in bucket:
                groups[signatures[record.name][index - 1]].append(record)
            grouped = list(groups.items())
            histogram[index] += _pair_count(len(bucket)) - sum(
                _pair_count(len(group)) for _, group in grouped
            )
            for left_position, (left_signature, left_group) in enumerate(grouped):
                for right_signature, right_group in grouped[left_position + 1 :]:
                    polynomial = interpolate(
                        tuple(
                            left - right
                            for left, right in zip(
                                left_signature,
                                right_signature,
                                strict=True,
                            )
                        ),
                        TOP_SAMPLES[0],
                    )
                    if len(polynomial) - 1 > CLEARED_DEGREE_BOUNDS[index - 1]:
                        raise AssertionError("top-coefficient degree bound failed")
                    roots = _odd_integer_roots(polynomial, REFERENCE_ORDER)
                    for order in roots:
                        for left in left_group:
                            for right in right_group:
                                specialization = _specialization(
                                    left,
                                    right,
                                    index,
                                    order,
                                    polynomial,
                                )
                                specializations.append(specialization)
                                digest.update(
                                    (
                                        f"root|{index}|{left.name}|{right.name}|"
                                        f"{order}|{polynomial}|"
                                        f"{specialization.separating_index}|"
                                        f"{specialization.separating_difference}\n"
                                    ).encode()
                                )
            next_buckets.extend(group for _, group in grouped if len(group) > 1)
        buckets = next_buckets

    q6_pairs: list[StableQ6Pair] = []
    q6_identities: list[tuple[Record, Record]] = []
    for bucket in buckets:
        for left_position, left in enumerate(bucket):
            for right in bucket[left_position + 1 :]:
                difference = tuple(
                    _cleared(
                        normalized_sixth_coefficient(left.deleted, order)
                        - normalized_sixth_coefficient(right.deleted, order),
                        6,
                        order,
                    )
                    for order in Q6_SAMPLES
                )
                polynomial = interpolate(difference, Q6_SAMPLES[0])
                if len(polynomial) - 1 > CLEARED_DEGREE_BOUNDS[5]:
                    raise AssertionError("q6 degree bound failed")
                if polynomial == (0,):
                    q6_identities.append((left, right))
                    continue
                for order in _odd_integer_roots(polynomial, REFERENCE_ORDER):
                    specialization = _specialization(
                        left,
                        right,
                        6,
                        order,
                        polynomial,
                    )
                    specializations.append(specialization)
                    digest.update(
                        (
                            f"root|6|{left.name}|{right.name}|{order}|"
                            f"{polynomial}|{specialization.separating_index}|"
                            f"{specialization.separating_difference}\n"
                        ).encode()
                    )
                histogram[6] += 1
                q6_pairs.append(StableQ6Pair(left, right, polynomial))
                digest.update(f"q6|{left.name}|{right.name}|{polynomial}\n".encode())

    q7_pairs: list[StableQ7Pair] = []
    q7_identities: list[tuple[Record, Record]] = []
    for left, right in q6_identities:
        difference = tuple(
            _cleared(
                normalized_seventh_coefficient(left.deleted, order)
                - normalized_seventh_coefficient(right.deleted, order),
                7,
                order,
            )
            for order in Q7_SAMPLES
        )
        polynomial = interpolate(difference, Q7_SAMPLES[0])
        if polynomial == (0,):
            q7_identities.append((left, right))
            continue
        if len(polynomial) - 1 > CLEARED_DEGREE_BOUNDS[6]:
            raise AssertionError("q7 degree bound failed")
        for order in _odd_integer_roots(polynomial, REFERENCE_ORDER):
            specialization = _specialization(
                left,
                right,
                7,
                order,
                polynomial,
            )
            specializations.append(specialization)
            digest.update(
                (
                    f"root|7|{left.name}|{right.name}|{order}|"
                    f"{polynomial}|{specialization.separating_index}|"
                    f"{specialization.separating_difference}\n"
                ).encode()
            )
        histogram[7] += 1
        q7_pairs.append(StableQ7Pair(left, right, polynomial))
        digest.update(f"q7|{left.name}|{right.name}|{polynomial}\n".encode())

    q8_pairs: list[StableQ8Pair] = []
    for left, right in q7_identities:
        difference = tuple(
            _cleared(
                normalized_coefficient(left.deleted, order, 8)
                - normalized_coefficient(right.deleted, order, 8),
                8,
                order,
            )
            for order in Q8_SAMPLES
        )
        polynomial = interpolate(difference, 0)
        if polynomial == (0,):
            raise AssertionError("q8 identity in the stable range")
        if len(polynomial) - 1 > CLEARED_DEGREE_BOUNDS[7]:
            raise AssertionError("q8 degree bound failed")
        if _nonnegative_integer_roots(polynomial):
            raise AssertionError("q8 identity-pair specialization")
        histogram[8] += 1
        q8_pairs.append(StableQ8Pair(left, right, polynomial))
        digest.update(f"q8|{left.name}|{right.name}|{polynomial}\n".encode())

    return StableAudit(
        records=records,
        histogram=(
            histogram[1],
            histogram[2],
            histogram[3],
            histogram[4],
            histogram[5],
            histogram[6],
            histogram[7],
            histogram[8],
        ),
        identity_group_count=len(buckets),
        q6_pairs=tuple(q6_pairs),
        q7_pairs=tuple(q7_pairs),
        q8_pairs=tuple(q8_pairs),
        specializations=tuple(specializations),
        signature_sha256=digest.hexdigest(),
    )


def _verify_full(record: Record, order: int) -> tuple[int, ...]:
    dimension = comb(order - 1, (order - 1) // 2)
    polynomial = hook_immanantal_polynomial(
        adjacency_from_deleted(record.deleted, order),
        (order - 1) // 2,
    )
    expected = (
        *normalized_top_five(record.deleted, order),
        normalized_sixth_coefficient(record.deleted, order),
        normalized_seventh_coefficient(record.deleted, order),
        normalized_coefficient(record.deleted, order, 8),
    )
    if polynomial[0] != dimension or any(
        Fraction(polynomial[index], dimension) != value
        for index, value in enumerate(expected, start=1)
    ):
        raise AssertionError("full recurrence disagrees with q1,...,q7")
    return polynomial


@cache
def boundary_audit(order: int) -> BoundaryAudit:
    if order not in (9, 11, 13, 15, 17, 19, 21):
        raise ValueError("invalid boundary order")
    census = feasible_census(order)
    counts = tuple(len(level) for level in census)
    if counts != burnside_census(order):
        raise AssertionError("boundary censuses disagree")
    records = records_from_census(census, order)
    top_values = {record.name: normalized_top_five(record.deleted, order) for record in records}
    digest = sha256()
    for record in records:
        digest.update(f"{record.name}|{top_values[record.name]}\n".encode())

    histogram: defaultdict[int, int] = defaultdict(int)
    buckets: list[list[Record]] = [list(records)]
    for index in range(1, 6):
        next_buckets: list[list[Record]] = []
        for bucket in buckets:
            groups: defaultdict[Fraction, list[Record]] = defaultdict(list)
            for record in bucket:
                groups[top_values[record.name][index - 1]].append(record)
            histogram[index] += _pair_count(len(bucket)) - sum(
                _pair_count(len(group)) for group in groups.values()
            )
            next_buckets.extend(group for group in groups.values() if len(group) > 1)
        buckets = next_buckets

    deep_pairs: list[BoundaryDeepPair] = []
    q6_residuals: list[list[Record]] = []
    for bucket in buckets:
        q6_groups: defaultdict[Fraction, list[Record]] = defaultdict(list)
        for record in bucket:
            q6_groups[normalized_sixth_coefficient(record.deleted, order)].append(record)
        grouped = list(q6_groups.items())
        histogram[6] += _pair_count(len(bucket)) - sum(
            _pair_count(len(group)) for _, group in grouped
        )
        for left_position, (left_value, left_group) in enumerate(grouped):
            for right_value, right_group in grouped[left_position + 1 :]:
                for left in left_group:
                    for right in right_group:
                        difference = left_value - right_value
                        deep_pairs.append(BoundaryDeepPair(left, right, 6, difference))
                        digest.update(f"q6|{left.name}|{right.name}|{difference}\n".encode())
        q6_residuals.extend(group for _, group in grouped if len(group) > 1)

    q7_residuals: list[list[Record]] = []
    for bucket in q6_residuals:
        q7_groups: defaultdict[Fraction, list[Record]] = defaultdict(list)
        for record in bucket:
            q7_groups[normalized_seventh_coefficient(record.deleted, order)].append(record)
        grouped = list(q7_groups.items())
        histogram[7] += _pair_count(len(bucket)) - sum(
            _pair_count(len(group)) for _, group in grouped
        )
        for left_position, (left_value, left_group) in enumerate(grouped):
            for right_value, right_group in grouped[left_position + 1 :]:
                for left in left_group:
                    for right in right_group:
                        difference = left_value - right_value
                        left_polynomial = _verify_full(left, order) if order == 9 else None
                        right_polynomial = _verify_full(right, order) if order == 9 else None
                        deep_pairs.append(
                            BoundaryDeepPair(
                                left,
                                right,
                                7,
                                difference,
                                left_polynomial,
                                right_polynomial,
                            )
                        )
                        digest.update(f"q7|{left.name}|{right.name}|{difference}\n".encode())
        q7_residuals.extend(group for _, group in grouped if len(group) > 1)

    for group in q7_residuals:
        for left_position, left in enumerate(group):
            for right in group[left_position + 1 :]:
                difference = normalized_coefficient(
                    left.deleted, order, 8
                ) - normalized_coefficient(right.deleted, order, 8)
                if not difference:
                    raise AssertionError("q1,...,q8 failed at the boundary")
                histogram[8] += 1
                left_polynomial = _verify_full(left, order) if order == 9 else None
                right_polynomial = _verify_full(right, order) if order == 9 else None
                deep_pairs.append(
                    BoundaryDeepPair(
                        left,
                        right,
                        8,
                        difference,
                        left_polynomial,
                        right_polynomial,
                    )
                )
                digest.update(f"q8|{left.name}|{right.name}|{difference}\n".encode())

    return BoundaryAudit(
        order=order,
        counts=counts,
        histogram=(
            histogram[1],
            histogram[2],
            histogram[3],
            histogram[4],
            histogram[5],
            histogram[6],
            histogram[7],
            histogram[8],
        ),
        deep_pairs=tuple(deep_pairs),
        signature_sha256=digest.hexdigest(),
    )
