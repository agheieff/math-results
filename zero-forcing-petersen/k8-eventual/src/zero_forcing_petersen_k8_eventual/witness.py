"""The P(64,8) positive separator control."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .graph import internal_boundary, vertex_name

BLOCK = ("BA", "YY", "YY", "YY", "YY", "BA", "AA", "AA")


@dataclass(frozen=True)
class WitnessReplay:
    word: tuple[str, ...]
    selected: tuple[str, ...]
    boundary: tuple[str, ...]
    word_sha256: str


def replay_n64_witness() -> WitnessReplay:
    n = 64
    word = BLOCK * 8
    colors = tuple(column[layer] for layer in range(2) for column in word)
    selected = sum(1 << vertex for vertex, color in enumerate(colors) if color != "Y")
    expected_boundary = sum(1 << vertex for vertex, color in enumerate(colors) if color == "B")
    boundary = internal_boundary(n, selected)
    if selected.bit_count() != n or boundary != expected_boundary or boundary.bit_count() != 16:
        raise AssertionError("invalid P(64,8) separator control")
    return WitnessReplay(
        word,
        tuple(vertex_name(n, vertex) for vertex in range(2 * n) if selected >> vertex & 1),
        tuple(vertex_name(n, vertex) for vertex in range(2 * n) if boundary >> vertex & 1),
        hashlib.sha256(" ".join(word).encode()).hexdigest(),
    )
