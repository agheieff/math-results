import pytest

from unique_multiset_sum.checker import (
    difference_subset_collision,
    elementary_two_construction,
    exhaustive_bound_check,
    find_multiset_collision,
    is_forbidden_multiplicity,
    is_unique_multiset_sum,
    witness_from_subset_collision,
)
from unique_multiset_sum.group import FiniteAbelianGroup


@pytest.mark.parametrize("family_size", range(2, 7))
def test_elementary_two_construction(family_size: int) -> None:
    group, family = elementary_two_construction(family_size)

    assert group.order == 1 << (family_size - 1)
    assert is_unique_multiset_sum(group, family)
    assert all(
        difference_subset_collision(group, family, basepoint) is None
        for basepoint in range(family_size)
    )


def test_overlap_and_cardinality_gap_witness() -> None:
    group = FiniteAbelianGroup((7,))
    family = ((0,), (1,), (2,), (3,))
    # From basepoint 0, {1, 2} and {3} both sum to 3. The implementation
    # orients them so the basepoint absorbs the one-unit cardinality gap.
    collision = difference_subset_collision(group, family, 0)

    assert collision is not None
    witness = witness_from_subset_collision(len(family), collision)
    assert is_forbidden_multiplicity(group, family, witness)
    assert all(coefficient >= 0 for coefficient in witness)
    assert sum(witness) == len(family)


def test_modular_collision_need_not_be_integer_equality() -> None:
    group = FiniteAbelianGroup((5,))
    family = ((0,), (1,), (4,))
    collision = difference_subset_collision(group, family, 0)

    assert collision is not None
    witness = witness_from_subset_collision(len(family), collision)
    assert is_forbidden_multiplicity(group, family, witness)


def test_direct_enumerator_finds_non_subset_type_collision() -> None:
    group = FiniteAbelianGroup((4,))
    family = ((0,), (1,), (2,))

    assert find_multiset_collision(group, family) is not None
    assert not is_unique_multiset_sum(group, family)


@pytest.mark.parametrize("family_size", range(2, 6))
def test_exhaustive_lower_bound(family_size: int) -> None:
    result = exhaustive_bound_check(family_size)

    assert result.valid_families == 0
    assert result.equality_construction_valid
