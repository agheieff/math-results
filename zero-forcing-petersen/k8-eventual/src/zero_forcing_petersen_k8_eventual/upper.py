"""Explicit eighteen-vertex forcing schedule."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .graph import adjacency, vertex_name

Force = tuple[int, int]


def initial_mask(n: int) -> int:
    if n < 17:
        raise ValueError("P(n,8) requires n at least seventeen")
    return (1 << 16) - 1 | 1 << n | 1 << (n + 15)


def schedule(n: int) -> tuple[Force, ...]:
    if n < 17:
        raise ValueError("P(n,8) requires n at least seventeen")
    result = [(index, n + index) for index in range(1, 15)]
    for index in range(n - 1, 15, -1):
        result.append(((index + 1) % n, index))
        result.append((n + ((index + 8) % n), n + index))
    return tuple(result)


@dataclass(frozen=True)
class UpperReplay:
    n: int
    force_count: int
    trace_sha256: str


def replay_schedule(n: int) -> UpperReplay:
    graph = adjacency(n)
    black = initial_mask(n)
    digest = hashlib.sha256(f"P({n},8)|".encode())
    for source, target in schedule(n):
        target_bit = 1 << target
        if not black >> source & 1 or graph[source] & ~black != target_bit:
            raise AssertionError("symbolic force is not legal")
        black |= target_bit
        digest.update(f"{vertex_name(n, source)}>{vertex_name(n, target)}|".encode())
    if black != (1 << (2 * n)) - 1:
        raise AssertionError("upper schedule did not force the graph")
    return UpperReplay(n, len(schedule(n)), digest.hexdigest())
