from collections.abc import Iterator, Sequence


def compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for suffix in compositions(total - first, parts - 1):
            yield (first, *suffix)


def has_unique_multiset_sums(family: Sequence[int], modulus: int) -> bool:
    size = len(family)
    target = sum(family) % modulus
    ones = (1,) * size
    return all(
        multiplicities == ones
        or sum(k * value for k, value in zip(multiplicities, family, strict=True)) % modulus
        != target
        for multiplicities in compositions(size, size)
    )


def subset_sums(differences: Sequence[int], modulus: int) -> frozenset[int]:
    values = {0}
    for difference in differences:
        values |= {(value + difference) % modulus for value in tuple(values)}
    return frozenset(values)


def nonzero_doubles(differences: Sequence[int], modulus: int) -> frozenset[int]:
    return frozenset(2 * difference % modulus for difference in differences) - {0}


def doubled_collision_witness(
    family: Sequence[int],
    modulus: int,
) -> tuple[int, ...] | None:
    base = family[0]
    differences = tuple((value - base) % modulus for value in family[1:])
    for chosen, difference in enumerate(differences):
        doubled = 2 * difference % modulus
        if doubled == 0:
            continue
        for mask in range(1, 1 << len(differences)):
            subset = tuple(index for index in range(len(differences)) if mask & (1 << index))
            if sum(differences[index] for index in subset) % modulus != doubled:
                continue
            multiplicities = [1] * len(family)
            multiplicities[0] += len(subset) - 2
            multiplicities[chosen + 1] += 2
            for index in subset:
                multiplicities[index + 1] -= 1
            witness = tuple(multiplicities)
            if min(witness) < 0 or sum(witness) != len(family):
                raise AssertionError("invalid doubled-collision multiplicities")
            target = sum(family) % modulus
            weighted = sum(k * value for k, value in zip(witness, family, strict=True)) % modulus
            if witness == (1,) * len(family) or weighted != target:
                raise AssertionError("doubled-collision witness does not violate uniqueness")
            return witness
    return None


def cyclic_lower_bound(size: int) -> int:
    if size < 2:
        raise ValueError("size must be at least two")
    return (1 << (size - 1)) + 2 * ((size - 1) // 2)


def superincreasing_example(size: int) -> tuple[int, tuple[int, ...]]:
    if size < 2:
        raise ValueError("size must be at least two")
    top_power = 1 << (size.bit_length() - 1)
    modulus = (1 << size) - top_power
    return modulus, tuple((1 << index) - 1 for index in range(size))
