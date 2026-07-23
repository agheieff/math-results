from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from functools import cache
from itertools import combinations

Edge = tuple[int, int]


@dataclass(frozen=True)
class Graph:
    order: int
    adjacency: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.order < 0 or len(self.adjacency) != self.order:
            raise ValueError("invalid graph order")
        allowed = (1 << self.order) - 1
        for vertex, neighbors in enumerate(self.adjacency):
            if neighbors & ~allowed or neighbors & (1 << vertex):
                raise ValueError("invalid adjacency mask")
            for neighbor in range(self.order):
                if bool(neighbors & (1 << neighbor)) != bool(
                    self.adjacency[neighbor] & (1 << vertex)
                ):
                    raise ValueError("adjacency must be symmetric")

    @classmethod
    def from_edges(cls, order: int, edges: Iterable[Edge]) -> Graph:
        adjacency = [0] * order
        for left, right in edges:
            if not 0 <= left < order or not 0 <= right < order or left == right:
                raise ValueError("invalid edge")
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
        return cls(order, tuple(adjacency))

    @classmethod
    def complete_bipartite(cls, left: int, right: int) -> Graph:
        return cls.from_edges(
            left + right,
            ((u, left + v) for u in range(left) for v in range(right)),
        )

    @classmethod
    def cycle(cls, order: int) -> Graph:
        if order < 3:
            raise ValueError("a simple cycle needs at least three vertices")
        return cls.from_edges(order, ((vertex, (vertex + 1) % order) for vertex in range(order)))

    @property
    def vertices(self) -> tuple[int, ...]:
        return tuple(range(self.order))

    @property
    def edges(self) -> tuple[Edge, ...]:
        return tuple(
            (left, right)
            for left in range(self.order)
            for right in range(left + 1, self.order)
            if self.has_edge(left, right)
        )

    def has_edge(self, left: int, right: int) -> bool:
        return bool(self.adjacency[left] & (1 << right))

    def complement(self) -> Graph:
        allowed = (1 << self.order) - 1
        return Graph(
            self.order,
            tuple(
                allowed ^ neighbors ^ (1 << vertex)
                for vertex, neighbors in enumerate(self.adjacency)
            ),
        )

    def induced(self, vertices: tuple[int, ...]) -> Graph:
        index = {vertex: local for local, vertex in enumerate(vertices)}
        return Graph.from_edges(
            len(vertices),
            (
                (index[left], index[right])
                for left, right in self.edges
                if left in index and right in index
            ),
        )

    def is_clique(self, vertices: Iterable[int]) -> bool:
        items = tuple(vertices)
        return all(self.has_edge(left, right) for left, right in combinations(items, 2))

    def is_independent(self, vertices: Iterable[int]) -> bool:
        items = tuple(vertices)
        return all(not self.has_edge(left, right) for left, right in combinations(items, 2))

    def is_triangle_free(self) -> bool:
        return all(not self.is_clique(vertices) for vertices in combinations(self.vertices, 3))

    def connected_on(self, vertices: Iterable[int]) -> bool:
        items = frozenset(vertices)
        if not items:
            return False
        reached = {next(iter(items))}
        frontier = list(reached)
        while frontier:
            vertex = frontier.pop()
            for neighbor in items - reached:
                if self.has_edge(vertex, neighbor):
                    reached.add(neighbor)
                    frontier.append(neighbor)
        return reached == items

    def adjacent_sets(self, left: Iterable[int], right: Iterable[int]) -> bool:
        return any(self.has_edge(u, v) for u in left for v in right)

    def matching_number(self) -> int:
        @cache
        def solve(mask: int) -> int:
            if not mask:
                return 0
            first_bit = mask & -mask
            vertex = first_bit.bit_length() - 1
            rest = mask ^ first_bit
            best = solve(rest)
            candidates = self.adjacency[vertex] & rest
            while candidates:
                neighbor_bit = candidates & -candidates
                best = max(best, 1 + solve(rest ^ neighbor_bit))
                candidates ^= neighbor_bit
            return best

        return solve((1 << self.order) - 1)

    def independence_number(self) -> int:
        return self.complement().clique_number()

    def clique_number(self) -> int:
        for size in range(self.order, 0, -1):
            if any(self.is_clique(vertices) for vertices in combinations(self.vertices, size)):
                return size
        return 0
