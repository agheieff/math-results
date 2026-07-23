"""Deterministic CNF encoding, fixed publicly to the order-eight m=16 gate."""

from __future__ import annotations

from dataclasses import dataclass

from pysat.card import CardEnc, EncType  # type: ignore[import-untyped]
from pysat.formula import CNF, IDPool  # type: ignore[import-untyped]


@dataclass(frozen=True)
class Parameters:
    """Encoding dimensions; non-target values support only differential tests."""

    order: int
    member_count: int

    @property
    def subset_count(self) -> int:
        return 1 << self.order

    def validate(self) -> None:
        if self.order < 1:
            raise ValueError("order must be positive")
        if not 2 <= self.member_count <= self.subset_count:
            raise ValueError("member_count must be in [2, 2^order]")


TARGET = Parameters(order=8, member_count=16)


def family_variable(mask: int) -> int:
    """Map a subset bit mask to its one-based DIMACS variable."""

    return mask + 1


def build_cnf(parameters: Parameters = TARGET) -> CNF:
    """Encode canonical clean tight union-closed families."""

    parameters.validate()
    subset_count = parameters.subset_count
    pool = IDPool(start_from=subset_count + 1)
    formula = CNF()

    # The standing empty-set convention and the union of all non-idle columns.
    formula.append([family_variable(0)])
    formula.append([family_variable(subset_count - 1)])

    # Comparable pairs already have one member as their union.
    for left in range(subset_count):
        for right in range(left + 1, subset_count):
            union = left | right
            if union != left and union != right:
                formula.append(
                    [
                        -family_variable(left),
                        -family_variable(right),
                        family_variable(union),
                    ]
                )

    membership_variables = [family_variable(mask) for mask in range(subset_count)]
    formula.extend(
        CardEnc.equals(
            membership_variables,
            bound=parameters.member_count,
            vpool=pool,
            encoding=EncType.totalizer,
        ).clauses
    )

    # Tightness is frequency(x) <= floor(m/2).
    for element in range(parameters.order):
        containing_element = [
            family_variable(mask) for mask in range(subset_count) if mask & (1 << element)
        ]
        formula.extend(
            CardEnc.atmost(
                containing_element,
                bound=parameters.member_count // 2,
                vpool=pool,
                encoding=EncType.totalizer,
            ).clauses
        )

    # Sort element frequencies. For adjacent columns x,y:
    # freq(x) <= freq(y) iff |{A:x in A,y notin A}| <= |{A:y in A,x notin A}|.
    for left_element in range(parameters.order - 1):
        right_element = left_element + 1
        left_only = [
            family_variable(mask)
            for mask in range(subset_count)
            if mask & (1 << left_element) and not mask & (1 << right_element)
        ]
        negated_right_only = [
            -family_variable(mask)
            for mask in range(subset_count)
            if mask & (1 << right_element) and not mask & (1 << left_element)
        ]
        formula.extend(
            CardEnc.atmost(
                left_only + negated_right_only,
                bound=len(negated_right_only),
                vpool=pool,
                encoding=EncType.totalizer,
            ).clauses
        )

    # Cleanliness: every two incidence columns differ. The full-set unit above
    # separately guarantees that no column is idle.
    for left_element in range(parameters.order):
        for right_element in range(left_element + 1, parameters.order):
            formula.append(
                [
                    family_variable(mask)
                    for mask in range(subset_count)
                    if bool(mask & (1 << left_element)) != bool(mask & (1 << right_element))
                ]
            )

    return formula
