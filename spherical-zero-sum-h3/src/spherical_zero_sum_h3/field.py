from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True, slots=True)
class QPhi:
    """An exact number a + b*phi, with phi^2 = phi + 1."""

    rational: Fraction
    phi: Fraction

    @classmethod
    def integer(cls, value: int) -> QPhi:
        return cls(Fraction(value), Fraction(0))

    def __add__(self, other: QPhi) -> QPhi:
        return QPhi(self.rational + other.rational, self.phi + other.phi)

    def __sub__(self, other: QPhi) -> QPhi:
        return QPhi(self.rational - other.rational, self.phi - other.phi)

    def __neg__(self) -> QPhi:
        return QPhi(-self.rational, -self.phi)

    def __mul__(self, other: QPhi) -> QPhi:
        return QPhi(
            self.rational * other.rational + self.phi * other.phi,
            self.rational * other.phi + self.phi * other.rational + self.phi * other.phi,
        )

    def scale(self, factor: Fraction) -> QPhi:
        return QPhi(factor * self.rational, factor * self.phi)

    def to_float(self) -> float:
        golden_ratio = (1.0 + math.sqrt(5.0)) / 2.0
        return float(self.rational) + float(self.phi) * golden_ratio


ZERO = QPhi.integer(0)
ONE = QPhi.integer(1)
PHI = QPhi(Fraction(0), Fraction(1))
INVERSE_PHI = PHI - ONE
