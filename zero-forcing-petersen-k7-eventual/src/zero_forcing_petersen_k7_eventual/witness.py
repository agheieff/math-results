"""Balanced separator family on P(7m,7), including the n=49 control."""

from __future__ import annotations

from .graph import internal_boundary, vertex_name

BLOCK = ("BA", "YY", "YY", "YY", "BY", "AA", "AA")


def block_word(multiplier: int) -> tuple[str, ...]:
    if multiplier < 3:
        raise ValueError("require multiplier at least three")
    return BLOCK * multiplier


def replay_block_witness(multiplier: int) -> tuple[tuple[str, ...], tuple[str, ...]]:
    n = 7 * multiplier
    word = block_word(multiplier)
    colors = tuple(column[layer] for layer in range(2) for column in word)
    selected = sum(1 << vertex for vertex, color in enumerate(colors) if color != "Y")
    expected_boundary = sum(1 << vertex for vertex, color in enumerate(colors) if color == "B")
    boundary = internal_boundary(n, selected)
    if (
        selected.bit_count() != n
        or boundary != expected_boundary
        or boundary.bit_count() != 2 * multiplier
    ):
        raise AssertionError("invalid block-family separator witness")
    selected_names = tuple(
        vertex_name(n, vertex) for vertex in range(2 * n) if selected >> vertex & 1
    )
    boundary_names = tuple(
        vertex_name(n, vertex) for vertex in range(2 * n) if boundary >> vertex & 1
    )
    return selected_names, boundary_names
