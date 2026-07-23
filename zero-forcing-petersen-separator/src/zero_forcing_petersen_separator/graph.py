from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property


@dataclass(frozen=True)
class GeneralizedPetersen:
    n: int
    k: int = 3

    def __post_init__(self) -> None:
        if self.n < 3:
            raise ValueError("n must be at least three")
        if self.k < 1 or 2 * self.k >= self.n:
            raise ValueError("k must satisfy 1 <= k < n/2")

    @property
    def order(self) -> int:
        return 2 * self.n

    @property
    def full_mask(self) -> int:
        return (1 << self.order) - 1

    @cached_property
    def neighbor_masks(self) -> tuple[int, ...]:
        masks = []
        for index in range(self.n):
            masks.append(
                1 << ((index - 1) % self.n) | 1 << ((index + 1) % self.n) | 1 << (self.n + index)
            )
        for index in range(self.n):
            masks.append(
                1 << index
                | 1 << (self.n + (index - self.k) % self.n)
                | 1 << (self.n + (index + self.k) % self.n)
            )
        if any(mask.bit_count() != 3 for mask in masks):
            raise AssertionError("generalized Petersen graph is not simple cubic")
        return tuple(masks)

    def vertex_name(self, vertex: int) -> str:
        if not 0 <= vertex < self.order:
            raise ValueError("vertex is outside the graph")
        layer = "u" if vertex < self.n else "v"
        return f"{layer}{vertex % self.n}"

    def paired_interval(self, start: int, length: int) -> int:
        if not 0 <= length <= self.n:
            raise ValueError("invalid interval length")
        mask = 0
        for offset in range(length):
            index = (start + offset) % self.n
            mask |= 1 << index | 1 << (self.n + index)
        return mask


def internal_boundary(graph: GeneralizedPetersen, subset: int) -> int:
    if subset < 0 or subset & ~graph.full_mask:
        raise ValueError("subset mask is outside the graph")
    boundary = 0
    remaining = subset
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        if graph.neighbor_masks[vertex] & ~subset:
            boundary |= bit
        remaining -= bit
    return boundary
