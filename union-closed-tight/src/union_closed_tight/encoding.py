"""Deterministic SAT encoding of one fixed-cardinality search instance."""

from __future__ import annotations

from dataclasses import dataclass

from pysat.card import CardEnc, EncType  # type: ignore[import-untyped]
from pysat.formula import CNF, IDPool  # type: ignore[import-untyped]


@dataclass(frozen=True)
class Instance:
    """A fixed ground-set order and family cardinality."""

    order: int
    member_count: int

    @property
    def subset_count(self) -> int:
        return 1 << self.order

    def validate(self) -> None:
        if self.order < 1:
            raise ValueError("order must be positive")
        if not 2 <= self.member_count <= self.subset_count:
            raise ValueError("member_count must lie between 2 and 2^order")


def family_variable(mask: int) -> int:
    """Return the DIMACS variable saying that ``mask`` belongs to the family."""

    return mask + 1


def build_cnf(instance: Instance) -> CNF:
    """Encode canonical clean tight union-closed families for ``instance``."""

    instance.validate()
    subset_count = instance.subset_count
    pool = IDPool(start_from=subset_count + 1)
    cnf = CNF()

    # The paper adopts the standing convention that empty is present. Cleanliness
    # implies no idle elements, so the union of all members is the full set.
    cnf.append([family_variable(0)])
    cnf.append([family_variable(subset_count - 1)])

    for left in range(subset_count):
        for right in range(left + 1, subset_count):
            union = left | right
            if union not in (left, right):
                cnf.append(
                    [
                        -family_variable(left),
                        -family_variable(right),
                        family_variable(union),
                    ]
                )

    members = [family_variable(mask) for mask in range(subset_count)]
    cnf.extend(
        CardEnc.equals(
            members,
            bound=instance.member_count,
            vpool=pool,
            encoding=EncType.totalizer,
        ).clauses
    )

    # Tightness: every element occurs in at most floor(|F| / 2) members.
    for element in range(instance.order):
        containing = [
            family_variable(mask) for mask in range(subset_count) if mask & (1 << element)
        ]
        cnf.extend(
            CardEnc.atmost(
                containing,
                bound=instance.member_count // 2,
                vpool=pool,
                encoding=EncType.totalizer,
            ).clauses
        )

    # Element relabeling lets us impose nondecreasing frequencies. If A contains
    # left but not right and B vice versa, freq(left) <= freq(right) is |A| <= |B|.
    for left in range(instance.order - 1):
        right = left + 1
        left_only = [
            family_variable(mask)
            for mask in range(subset_count)
            if mask & (1 << left) and not mask & (1 << right)
        ]
        right_only_negated = [
            -family_variable(mask)
            for mask in range(subset_count)
            if mask & (1 << right) and not mask & (1 << left)
        ]
        cnf.extend(
            CardEnc.atmost(
                left_only + right_only_negated,
                bound=len(right_only_negated),
                vpool=pool,
                encoding=EncType.totalizer,
            ).clauses
        )

    # Clean means that every two incidence columns differ. The full-set unit
    # above also ensures that no element is idle.
    for left in range(instance.order):
        for right in range(left + 1, instance.order):
            cnf.append(
                [
                    family_variable(mask)
                    for mask in range(subset_count)
                    if bool(mask & (1 << left)) != bool(mask & (1 << right))
                ]
            )

    return cnf
