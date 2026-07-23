from cyclic_ums.model import (
    cyclic_lower_bound,
    doubled_collision_witness,
    has_unique_multiset_sums,
    nonzero_doubles,
    subset_sums,
    superincreasing_example,
)
from cyclic_ums.verify import audit_doubling, audit_small, check_size


def test_lower_bound_values() -> None:
    assert [cyclic_lower_bound(size) for size in range(2, 8)] == [
        2,
        6,
        10,
        20,
        36,
        70,
    ]


def test_examples_and_hole_mechanism() -> None:
    for size in range(2, 8):
        modulus, family = superincreasing_example(size)
        differences = family[1:]
        image = subset_sums(differences, modulus)
        doubles = nonzero_doubles(differences, modulus)
        assert len(image) == 2 ** (size - 1)
        assert doubles.isdisjoint(image)
        assert has_unique_multiset_sums(family, modulus)
        assert check_size(size).example_valid


def test_rejects_known_collision() -> None:
    assert not has_unique_multiset_sums((0, 1, 2), 4)
    assert doubled_collision_witness((0, 1, 2), 4) == (0, 3, 0)


def test_exhaustive_small_audit() -> None:
    audit = audit_small()
    assert audit.families == 781
    assert audit.valid_families == 220


def test_exhaustive_doubling_audit() -> None:
    audit = audit_doubling()
    assert audit.difference_sets == 55_430
    assert audit.dissociated_sets == 13_296
