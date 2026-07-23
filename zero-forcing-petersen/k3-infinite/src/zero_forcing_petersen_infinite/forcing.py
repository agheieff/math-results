"""Finite forcing derivations on the bi-infinite strip."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from .model import Vertex, inner, neighbors, outer, outer_interval


@dataclass(frozen=True)
class Force:
    source: Vertex
    target: Vertex

    def shifted(self, offset: int) -> Force:
        return Force(self.source.shifted(offset), self.target.shifted(offset))


BLOCK_EXPANSION_FORCES = (
    *(Force(outer(index), inner(index)) for index in range(1, 7)),
    Force(inner(3), inner(0)),
    Force(inner(4), inner(7)),
    Force(outer(0), outer(-1)),
    Force(outer(7), outer(8)),
)


def apply_force(black: set[Vertex], force: Force) -> None:
    white = [vertex for vertex in neighbors(force.source) if vertex not in black]
    if white != [force.target]:
        raise AssertionError(
            f"{force.source}->{force.target} is invalid; white neighbors are {white}"
        )
    black.add(force.target)


def replay(initial: frozenset[Vertex], forces: tuple[Force, ...]) -> frozenset[Vertex]:
    black = set(initial)
    for force in forces:
        apply_force(black, force)
    return frozenset(black)


def block_expansion(start: int) -> tuple[Force, ...]:
    return tuple(force.shifted(start) for force in BLOCK_EXPANSION_FORCES)


def verify_block_expansion(start: int = 0) -> frozenset[Vertex]:
    black = replay(outer_interval(start, 8), block_expansion(start))
    required = outer_interval(start - 1, 10)
    if not required <= black:
        raise AssertionError("the eight-vertex block did not expand at both ends")
    return black


def force_until_outer_radius(radius: int) -> tuple[frozenset[Vertex], tuple[Force, ...]]:
    """Run valid forces until u_-radius,...,u_(7+radius) are black."""
    if radius < 0:
        raise ValueError("radius must be nonnegative")
    black = set(outer_interval(0, 8))
    pending = deque(sorted(black))
    forces: list[Force] = []
    target_interval = outer_interval(-radius, 8 + 2 * radius)
    while not target_interval <= black:
        if not pending:
            raise AssertionError("the forcing queue stalled before reaching the target interval")
        source = pending.popleft()
        white = [vertex for vertex in neighbors(source) if vertex not in black]
        if len(white) != 1:
            continue
        target = white[0]
        black.add(target)
        forces.append(Force(source, target))
        pending.append(target)
        pending.extend(vertex for vertex in neighbors(target) if vertex in black)
    return frozenset(black), tuple(forces)
