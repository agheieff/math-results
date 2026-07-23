from itertools import combinations

from hadwiger_alpha2_order39_support_search.certificate import ONE_DEFECT, SUPPORTS
from hadwiger_alpha2_order39_support_search.supports import (
    FULL,
    TYPES,
    hall_violations,
    multiplicities,
)


def test_disjoint_triple_enumeration_matches_brute_force() -> None:
    brute = {
        (first, second, third)
        for first, second, third in combinations(range(len(TYPES)), 3)
        if not (
            TYPES[first] & TYPES[second]
            or TYPES[first] & TYPES[third]
            or TYPES[second] & TYPES[third]
        )
    }
    enumerated: set[tuple[int, int, int]] = set()
    disjoint = [
        tuple(other for other, other_mask in enumerate(TYPES) if not mask & other_mask)
        for mask in TYPES
    ]
    for first, first_mask in enumerate(TYPES):
        if first_mask.bit_count() > 4:
            continue
        for second in disjoint[first]:
            if second <= first:
                continue
            second_mask = TYPES[second]
            if first_mask.bit_count() + second_mask.bit_count() > 7:
                continue
            common_free = FULL ^ (first_mask | second_mask)
            for third in range(second + 1, len(TYPES)):
                if TYPES[third] & ~common_free:
                    continue
                enumerated.add((first, second, third))

    assert len(brute) == 4_900
    assert enumerated == brute


def test_one_defect_multiset_has_exactly_one_hall_violation() -> None:
    violations = hall_violations(multiplicities(ONE_DEFECT))

    assert len(violations) == 1
    assert (violations[0].weight, violations[0].bound, violations[0].union) == (10, 9, FULL)
    masks = [TYPES[index] for index in violations[0].types]
    assert all(first & second for first, second in combinations(masks, 2))


def test_certificate_passes_exact_hall_separator() -> None:
    assert not hall_violations(multiplicities(SUPPORTS))
