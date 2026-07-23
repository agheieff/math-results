from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MycielskiCycle:
    """The Mycielskian of a cycle, represented by adjacency bitsets."""

    order: int
    adjacency: tuple[int, ...]

    @classmethod
    def build(cls, order: int) -> MycielskiCycle:
        if order < 4:
            raise ValueError("order must be at least four")

        adjacency = [0] * (2 * order + 1)

        def add_edge(left: int, right: int) -> None:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left

        for index in range(order):
            add_edge(index, (index + 1) % order)
            add_edge(order + index, (index - 1) % order)
            add_edge(order + index, (index + 1) % order)
            add_edge(2 * order, order + index)
        return cls(order, tuple(adjacency))

    @property
    def vertex_count(self) -> int:
        return 2 * self.order + 1

    @property
    def apex(self) -> int:
        return 2 * self.order

    @property
    def edge_count(self) -> int:
        return sum(neighbors.bit_count() for neighbors in self.adjacency) // 2

    def original(self, index: int) -> int:
        return index % self.order

    def shadow(self, index: int) -> int:
        return self.order + index % self.order
