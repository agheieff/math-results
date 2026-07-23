"""Exact symbolic upper-witness replay."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .graph import Vertex, petersen_adjacency, vertex_id, vertex_name

Force = tuple[Vertex, Vertex]


def initial_vertices(k: int) -> tuple[Vertex, ...]:
    if k < 1:
        raise ValueError("require k >= 1")
    return (("v", 0), *(("u", index) for index in range(2 * k)), ("v", 2 * k - 1))


def symbolic_schedule(n: int, k: int) -> tuple[Force, ...]:
    if n < 2 * k + 1:
        raise ValueError("require n >= 2k+1")
    forces: list[Force] = [(("u", index), ("v", index)) for index in range(1, 2 * k - 1)]
    for index in range(n - 1, 2 * k - 1, -1):
        forces.append((("u", (index + 1) % n), ("u", index)))
        forces.append((("v", (index + k) % n), ("v", index)))
    return tuple(forces)


@dataclass(frozen=True)
class ForceReplay:
    n: int
    k: int
    initial_size: int
    force_count: int
    trace_sha256: str


def replay_symbolic_schedule(n: int, k: int) -> ForceReplay:
    adjacency = petersen_adjacency(n, k)
    black = 0
    for vertex in initial_vertices(k):
        black |= 1 << vertex_id(n, vertex)
    if black.bit_count() != 2 * k + 2:
        raise AssertionError("upper witness does not have size 2k+2")

    digest = hashlib.sha256(f"P({n},{k})|".encode())
    for source, target in symbolic_schedule(n, k):
        source_id = vertex_id(n, source)
        target_bit = 1 << vertex_id(n, target)
        if not black & (1 << source_id):
            raise AssertionError(f"white source {vertex_name(source)}")
        white_neighbors = adjacency[source_id] & ~black
        if white_neighbors != target_bit:
            raise AssertionError(
                f"{vertex_name(source)} does not uniquely force {vertex_name(target)}"
            )
        black |= target_bit
        digest.update(f"{vertex_name(source)}>{vertex_name(target)}|".encode())

    if black != (1 << (2 * n)) - 1:
        raise AssertionError("symbolic schedule did not force the whole graph")
    force_count = len(symbolic_schedule(n, k))
    if force_count != 2 * n - (2 * k + 2):
        raise AssertionError("force count does not complement the initial set")
    return ForceReplay(
        n=n,
        k=k,
        initial_size=2 * k + 2,
        force_count=force_count,
        trace_sha256=digest.hexdigest(),
    )
