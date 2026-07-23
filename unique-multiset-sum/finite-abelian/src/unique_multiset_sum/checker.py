"""Independent direct and subset-collision checks."""

from collections.abc import Iterator
from dataclasses import dataclass
from itertools import combinations

from unique_multiset_sum.group import (
    Element,
    Family,
    FiniteAbelianGroup,
    abelian_group_types,
)

type Multiplicity = tuple[int, ...]


def _validate_family(group: FiniteAbelianGroup, family: Family) -> None:
    if not family:
        raise ValueError("family must be nonempty")
    for element in family:
        group.validate(element)


def multiplicity_vectors(size: int, length: int) -> Iterator[Multiplicity]:
    """Yield every nonnegative vector of the requested length and coordinate sum."""
    if size < 0:
        raise ValueError("size must be nonnegative")
    if length < 1:
        raise ValueError("length must be positive")
    if length == 1:
        yield (size,)
        return
    for first in range(size + 1):
        for rest in multiplicity_vectors(size - first, length - 1):
            yield (first, *rest)


def weighted_sum(
    group: FiniteAbelianGroup,
    family: Family,
    multiplicity: Multiplicity,
) -> Element:
    _validate_family(group, family)
    if len(multiplicity) != len(family):
        raise ValueError("multiplicity vector has the wrong length")
    return group.sum(
        group.scale(coefficient, element)
        for coefficient, element in zip(multiplicity, family, strict=True)
    )


def is_forbidden_multiplicity(
    group: FiniteAbelianGroup,
    family: Family,
    multiplicity: Multiplicity,
) -> bool:
    """Test the original rival-multiset conditions directly."""
    _validate_family(group, family)
    order = len(family)
    return (
        len(multiplicity) == order
        and multiplicity != (1,) * order
        and all(coefficient >= 0 for coefficient in multiplicity)
        and sum(multiplicity) == order
        and weighted_sum(group, family, multiplicity) == group.sum(family)
    )


def find_multiset_collision(
    group: FiniteAbelianGroup,
    family: Family,
) -> Multiplicity | None:
    """Find a rival by exhaustive enumeration of the original multiplicities."""
    _validate_family(group, family)
    order = len(family)
    for multiplicity in multiplicity_vectors(order, order):
        if is_forbidden_multiplicity(group, family, multiplicity):
            return multiplicity
    return None


def is_unique_multiset_sum(group: FiniteAbelianGroup, family: Family) -> bool:
    return find_multiset_collision(group, family) is None


@dataclass(frozen=True)
class SubsetCollision:
    """Two distinct masks with equal sums of differences from one basepoint."""

    basepoint: int
    positions: tuple[int, ...]
    left_mask: int
    right_mask: int
    value: Element


def _masked_sum(
    group: FiniteAbelianGroup,
    elements: tuple[Element, ...],
    mask: int,
) -> Element:
    return group.sum(element for bit, element in enumerate(elements) if mask & (1 << bit))


def difference_subset_collision(
    group: FiniteAbelianGroup,
    family: Family,
    basepoint: int,
) -> SubsetCollision | None:
    """Find a repeated subset sum among the differences from one basepoint."""
    _validate_family(group, family)
    if not 0 <= basepoint < len(family):
        raise ValueError("basepoint is outside the family")

    positions = tuple(index for index in range(len(family)) if index != basepoint)
    differences = tuple(group.subtract(family[index], family[basepoint]) for index in positions)
    seen: dict[Element, int] = {}
    for mask in range(1 << len(differences)):
        value = _masked_sum(group, differences, mask)
        previous = seen.get(value)
        if previous is not None:
            return SubsetCollision(basepoint, positions, previous, mask, value)
        seen[value] = mask
    return None


def witness_from_subset_collision(
    family_size: int,
    collision: SubsetCollision,
) -> Multiplicity:
    """Implement the coefficient construction in the proof."""
    if family_size < 1:
        raise ValueError("family size must be positive")
    if len(collision.positions) != family_size - 1:
        raise ValueError("collision positions do not match the family size")
    if collision.left_mask == collision.right_mask:
        raise ValueError("collision masks must be distinct")

    left_mask = collision.left_mask
    right_mask = collision.right_mask
    if left_mask.bit_count() > right_mask.bit_count():
        left_mask, right_mask = right_mask, left_mask

    coefficients = [0] * family_size
    for bit, position in enumerate(collision.positions):
        coefficients[position] = bool(left_mask & (1 << bit)) - bool(right_mask & (1 << bit))
    coefficients[collision.basepoint] = right_mask.bit_count() - left_mask.bit_count()
    return tuple(1 + coefficient for coefficient in coefficients)


def elementary_two_construction(order: int) -> tuple[FiniteAbelianGroup, Family]:
    if order < 2:
        raise ValueError("family order must be at least 2")
    group = FiniteAbelianGroup((2,) * (order - 1))
    family = (group.zero,) + tuple(
        tuple(int(row == column) for column in range(order - 1)) for row in range(order - 1)
    )
    return group, family


def normalized_families(group: FiniteAbelianGroup, order: int) -> Iterator[Family]:
    """Enumerate translated set representatives containing zero."""
    if order < 1:
        raise ValueError("family order must be positive")
    nonzero = tuple(element for element in group.elements() if element != group.zero)
    for rest in combinations(nonzero, order - 1):
        yield (group.zero, *rest)


@dataclass(frozen=True)
class BoundCheckResult:
    """Summary of an exhaustive below-bound check for one family size."""

    family_size: int
    lower_bound: int
    group_types: int
    normalized_families: int
    valid_families: int
    equality_construction_valid: bool


def exhaustive_bound_check(family_size: int) -> BoundCheckResult:
    """Exhaust all group types and normalized sets below the theorem bound."""
    if family_size < 2:
        raise ValueError("family size must be at least 2")

    lower_bound = 1 << (family_size - 1)
    group_count = 0
    family_count = 0
    valid_count = 0

    for group_order in range(1, lower_bound):
        for group in abelian_group_types(group_order):
            group_count += 1
            for family in normalized_families(group, family_size):
                family_count += 1
                subset_collision = difference_subset_collision(group, family, 0)
                if subset_collision is None:
                    raise AssertionError(
                        f"pigeonhole collision missing in {group.label} for {family}"
                    )
                witness = witness_from_subset_collision(family_size, subset_collision)
                if not is_forbidden_multiplicity(group, family, witness):
                    raise AssertionError(
                        f"constructed witness failed in {group.label} for {family}"
                    )

                direct_collision = find_multiset_collision(group, family)
                if direct_collision is None:
                    valid_count += 1

    equality_group, equality_family = elementary_two_construction(family_size)
    construction_valid = is_unique_multiset_sum(equality_group, equality_family)
    return BoundCheckResult(
        family_size=family_size,
        lower_bound=lower_bound,
        group_types=group_count,
        normalized_families=family_count,
        valid_families=valid_count,
        equality_construction_valid=construction_valid,
    )
