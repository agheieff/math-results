from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MycielskiPath:
    """The Mycielskian of P_n, represented by adjacency bitsets."""

    order: int
    adjacency: tuple[int, ...]

    @classmethod
    def build(cls, order: int) -> MycielskiPath:
        if order < 2:
            raise ValueError("order must be at least two")
        adjacency = [0] * (2 * order + 1)

        def add_edge(left: int, right: int) -> None:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left

        for index in range(order - 1):
            add_edge(index, index + 1)
        for index in range(order):
            if index:
                add_edge(order + index, index - 1)
            if index + 1 < order:
                add_edge(order + index, index + 1)
            add_edge(2 * order, order + index)
        return cls(order, tuple(adjacency))

    @property
    def vertex_count(self) -> int:
        return 2 * self.order + 1

    @property
    def apex(self) -> int:
        return 2 * self.order

    def original(self, index: int) -> int:
        if not 0 <= index < self.order:
            raise IndexError(index)
        return index

    def shadow(self, index: int) -> int:
        if not 0 <= index < self.order:
            raise IndexError(index)
        return self.order + index
