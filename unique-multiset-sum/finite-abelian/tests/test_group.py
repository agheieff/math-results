import pytest

from unique_multiset_sum.group import FiniteAbelianGroup, abelian_group_types


def test_group_arithmetic() -> None:
    group = FiniteAbelianGroup((4, 3))

    assert group.order == 12
    assert group.add((3, 2), (2, 2)) == (1, 1)
    assert group.subtract((0, 1), (3, 2)) == (1, 2)
    assert group.scale(3, (3, 2)) == (1, 0)
    assert len(tuple(group.elements())) == group.order


@pytest.mark.parametrize(
    ("order", "moduli"),
    [
        (1, {()}),
        (4, {(4,), (2, 2)}),
        (8, {(8,), (2, 4), (2, 2, 2)}),
        (12, {(3, 4), (2, 2, 3)}),
    ],
)
def test_abelian_group_classification(
    order: int,
    moduli: set[tuple[int, ...]],
) -> None:
    groups = abelian_group_types(order)

    assert {group.moduli for group in groups} == moduli
    assert all(group.order == order for group in groups)


def test_invalid_factor_modulus() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        FiniteAbelianGroup((2, 1))
