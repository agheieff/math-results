"""Parity-dependent exact boundary words on P(km,k)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .model import adjacency, internal_boundary


def block(k: int) -> tuple[str, ...]:
    if k < 3:
        raise ValueError("require k>=3")
    half = k // 2
    if k % 2:
        return ("BA", *("YY",) * half, "BY", *("AA",) * (half - 1))
    return ("BA", *("YY",) * half, "BA", *("AA",) * (half - 2))


def word(k: int, multiplier: int) -> tuple[str, ...]:
    if multiplier < 3:
        raise ValueError("require multiplier>=3")
    return block(k) * multiplier


@dataclass(frozen=True)
class Replay:
    k: int
    multiplier: int
    n: int
    selected_size: int
    boundary_size: int
    y_count: int
    word_sha256: str


def replay(k: int, multiplier: int) -> Replay:
    n = k * multiplier
    columns = word(k, multiplier)
    colors = tuple(column[layer] for layer in range(2) for column in columns)
    selected = sum(1 << vertex for vertex, color in enumerate(colors) if color != "Y")
    expected_boundary = sum(1 << vertex for vertex, color in enumerate(colors) if color == "B")
    boundary = internal_boundary(adjacency(n, k), selected)
    if selected.bit_count() != n or colors.count("Y") != n:
        raise AssertionError("word is not a half-set")
    if boundary != expected_boundary or boundary.bit_count() != 2 * multiplier:
        raise AssertionError("word does not have the claimed exact boundary")
    return Replay(
        k,
        multiplier,
        n,
        selected.bit_count(),
        boundary.bit_count(),
        colors.count("Y"),
        hashlib.sha256(" ".join(columns).encode()).hexdigest(),
    )
