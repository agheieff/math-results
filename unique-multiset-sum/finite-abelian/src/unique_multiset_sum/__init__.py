"""Tools for auditing unique multiset sums in finite abelian groups."""

from unique_multiset_sum.checker import (
    BoundCheckResult,
    SubsetCollision,
    difference_subset_collision,
    exhaustive_bound_check,
    find_multiset_collision,
    is_forbidden_multiplicity,
    is_unique_multiset_sum,
    witness_from_subset_collision,
)
from unique_multiset_sum.group import (
    Element,
    Family,
    FiniteAbelianGroup,
    abelian_group_types,
)

__all__ = [
    "BoundCheckResult",
    "Element",
    "Family",
    "FiniteAbelianGroup",
    "SubsetCollision",
    "abelian_group_types",
    "difference_subset_collision",
    "exhaustive_bound_check",
    "find_multiset_collision",
    "is_forbidden_multiplicity",
    "is_unique_multiset_sum",
    "witness_from_subset_collision",
]
