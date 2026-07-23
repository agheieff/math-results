"""The bi-infinite generalized Petersen strip with inner step three."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Layer = Literal["u", "v"]


@dataclass(frozen=True, order=True)
class Vertex:
    layer: Layer
    index: int

    def shifted(self, offset: int) -> Vertex:
        return Vertex(self.layer, self.index + offset)

    def __str__(self) -> str:
        return f"{self.layer}{self.index}"


def outer(index: int) -> Vertex:
    return Vertex("u", index)


def inner(index: int) -> Vertex:
    return Vertex("v", index)


def neighbors(vertex: Vertex) -> tuple[Vertex, Vertex, Vertex]:
    if vertex.layer == "u":
        return (
            outer(vertex.index - 1),
            outer(vertex.index + 1),
            inner(vertex.index),
        )
    return (
        outer(vertex.index),
        inner(vertex.index - 3),
        inner(vertex.index + 3),
    )


def outer_interval(start: int, length: int) -> frozenset[Vertex]:
    if length < 0:
        raise ValueError("length must be nonnegative")
    return frozenset(outer(start + offset) for offset in range(length))
