"""Finite abelian groups in primary cyclic-factor form."""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from itertools import product
from math import prod

type Element = tuple[int, ...]
type Family = tuple[Element, ...]


@dataclass(frozen=True)
class FiniteAbelianGroup:
    """A direct product of cyclic groups with the given moduli."""

    moduli: tuple[int, ...]

    def __post_init__(self) -> None:
        if any(modulus < 2 for modulus in self.moduli):
            raise ValueError("cyclic factor moduli must be at least 2")

    @property
    def order(self) -> int:
        return prod(self.moduli)

    @property
    def zero(self) -> Element:
        return (0,) * len(self.moduli)

    @property
    def label(self) -> str:
        if not self.moduli:
            return "1"
        return " x ".join(f"C{modulus}" for modulus in self.moduli)

    def validate(self, element: Element) -> None:
        if len(element) != len(self.moduli):
            raise ValueError("element has the wrong number of coordinates")
        if any(
            not 0 <= value < modulus for value, modulus in zip(element, self.moduli, strict=True)
        ):
            raise ValueError("element coordinate is outside its canonical residue range")

    def elements(self) -> Iterator[Element]:
        ranges = tuple(range(modulus) for modulus in self.moduli)
        yield from product(*ranges)

    def add(self, left: Element, right: Element) -> Element:
        self.validate(left)
        self.validate(right)
        return tuple(
            (left_value + right_value) % modulus
            for left_value, right_value, modulus in zip(left, right, self.moduli, strict=True)
        )

    def subtract(self, left: Element, right: Element) -> Element:
        self.validate(left)
        self.validate(right)
        return tuple(
            (left_value - right_value) % modulus
            for left_value, right_value, modulus in zip(left, right, self.moduli, strict=True)
        )

    def scale(self, coefficient: int, element: Element) -> Element:
        self.validate(element)
        return tuple(
            (coefficient * value) % modulus
            for value, modulus in zip(element, self.moduli, strict=True)
        )

    def sum(self, elements: Iterable[Element]) -> Element:
        total = self.zero
        for element in elements:
            total = self.add(total, element)
        return total


def _prime_factorization(value: int) -> tuple[tuple[int, int], ...]:
    factors: list[tuple[int, int]] = []
    candidate = 2
    remaining = value
    while candidate * candidate <= remaining:
        exponent = 0
        while remaining % candidate == 0:
            exponent += 1
            remaining //= candidate
        if exponent:
            factors.append((candidate, exponent))
        candidate += 1
    if remaining > 1:
        factors.append((remaining, 1))
    return tuple(factors)


def _partitions(total: int, maximum: int | None = None) -> Iterator[tuple[int, ...]]:
    if total == 0:
        yield ()
        return
    upper = total if maximum is None else min(total, maximum)
    for first in range(upper, 0, -1):
        for rest in _partitions(total - first, first):
            yield (first, *rest)


def abelian_group_types(order: int) -> tuple[FiniteAbelianGroup, ...]:
    """Return one primary-factor representative of every abelian group of this order."""
    if order < 1:
        raise ValueError("order must be positive")

    choices: list[tuple[tuple[int, ...], ...]] = []
    for prime, exponent in _prime_factorization(order):
        choices.append(
            tuple(tuple(prime**part for part in partition) for partition in _partitions(exponent))
        )

    groups = {
        FiniteAbelianGroup(tuple(sorted(factors)))
        for prime_choices in product(*choices)
        for factors in (tuple(factor for choice in prime_choices for factor in choice),)
    }
    return tuple(sorted(groups, key=lambda group: group.moduli))
