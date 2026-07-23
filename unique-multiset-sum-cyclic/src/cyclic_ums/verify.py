from dataclasses import dataclass
from itertools import combinations

from cyclic_ums.model import (
    cyclic_lower_bound,
    has_unique_multiset_sums,
    nonzero_doubles,
    subset_sums,
    superincreasing_example,
)


@dataclass(frozen=True)
class Check:
    size: int
    lower_bound: int
    example_modulus: int
    subset_sums: int
    nonzero_double_holes: int
    example_valid: bool


@dataclass(frozen=True)
class ExhaustiveAudit:
    families: int
    valid_families: int


@dataclass(frozen=True)
class DoublingAudit:
    difference_sets: int
    dissociated_sets: int


def check_size(size: int) -> Check:
    modulus, family = superincreasing_example(size)
    differences = tuple((value - family[0]) % modulus for value in family[1:])
    image = subset_sums(differences, modulus)
    doubles = nonzero_doubles(differences, modulus)
    if not doubles.isdisjoint(image):
        raise AssertionError("nonzero doubled difference lies in the subset-sum image")
    return Check(
        size=size,
        lower_bound=cyclic_lower_bound(size),
        example_modulus=modulus,
        subset_sums=len(image),
        nonzero_double_holes=len(doubles),
        example_valid=has_unique_multiset_sums(family, modulus),
    )


def audit_small(max_size: int = 4, max_modulus: int = 12) -> ExhaustiveAudit:
    families = 0
    valid_families = 0
    for size in range(2, max_size + 1):
        for modulus in range(size, max_modulus + 1):
            for tail in combinations(range(1, modulus), size - 1):
                families += 1
                family = (0, *tail)
                if not has_unique_multiset_sums(family, modulus):
                    continue
                valid_families += 1
                image = subset_sums(tail, modulus)
                doubles = nonzero_doubles(tail, modulus)
                if len(image) != 1 << (size - 1):
                    raise AssertionError("valid family has a subset-sum collision")
                if not doubles.isdisjoint(image):
                    raise AssertionError("valid family violates the doubled-hole lemma")
                if modulus < cyclic_lower_bound(size):
                    raise AssertionError("valid family violates the cyclic lower bound")
    return ExhaustiveAudit(families=families, valid_families=valid_families)


def audit_doubling(max_rank: int = 4, max_modulus: int = 24) -> DoublingAudit:
    difference_sets = 0
    dissociated_sets = 0
    for modulus in range(2, max_modulus + 1):
        for rank in range(1, min(max_rank, modulus - 1) + 1):
            for differences in combinations(range(1, modulus), rank):
                difference_sets += 1
                if len(subset_sums(differences, modulus)) != 1 << rank:
                    continue
                dissociated_sets += 1
                if len(nonzero_doubles(differences, modulus)) < rank - 1:
                    raise AssertionError("dissociated set violates the doubling bound")
    return DoublingAudit(
        difference_sets=difference_sets,
        dissociated_sets=dissociated_sets,
    )


def main() -> None:
    print("n  lower  example_N  subset_sums  double_holes  valid")
    for size in range(2, 8):
        check = check_size(size)
        print(
            check.size,
            check.lower_bound,
            check.example_modulus,
            check.subset_sums,
            check.nonzero_double_holes,
            check.example_valid,
            sep="  ",
        )
    audit = audit_small()
    print(f"small audit: {audit.families} families, {audit.valid_families} valid")
    doubling = audit_doubling()
    print(
        "doubling audit: "
        f"{doubling.difference_sets} difference sets, "
        f"{doubling.dissociated_sets} dissociated"
    )
