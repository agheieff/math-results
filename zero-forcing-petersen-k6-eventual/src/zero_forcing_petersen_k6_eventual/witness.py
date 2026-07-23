"""Exact n=36 half-set with internal boundary thirteen."""

from __future__ import annotations

from .graph import internal_boundary, vertex_name

N36_WORD = (
    "BA",
    "YY",
    "YY",
    "YY",
    "YB",
    "BA",
    "YB",
    "YY",
    "YY",
    "YY",
    "BA",
    "AA",
    "BA",
    "YY",
    "YY",
    "YY",
    "BA",
    "AA",
    "BA",
    "YY",
    "YY",
    "YY",
    "BA",
    "AA",
    "BA",
    "YY",
    "YY",
    "YY",
    "BA",
    "AA",
    "AA",
    "BY",
    "YY",
    "BY",
    "AA",
    "AA",
)


def replay_n36_witness() -> tuple[tuple[str, ...], tuple[str, ...]]:
    colors = tuple(column[layer] for layer in range(2) for column in N36_WORD)
    selected = sum(1 << vertex for vertex, color in enumerate(colors) if color != "Y")
    expected_boundary = sum(1 << vertex for vertex, color in enumerate(colors) if color == "B")
    boundary = internal_boundary(36, selected)
    if selected.bit_count() != 36 or boundary != expected_boundary or boundary.bit_count() != 13:
        raise AssertionError("invalid n=36 separator witness")
    selected_names = tuple(
        vertex_name(36, vertex) for vertex in range(72) if selected >> vertex & 1
    )
    boundary_names = tuple(
        vertex_name(36, vertex) for vertex in range(72) if boundary >> vertex & 1
    )
    return selected_names, boundary_names
