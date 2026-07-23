"""Sharp n=28 half-boundary witness."""

from __future__ import annotations

from .graph import internal_boundary, vertex_name

N28_WORD = (
    "YB",
    "YB",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YY",
    "YB",
    "YB",
    "YB",
    "YB",
    "BY",
    "AA",
    "AA",
    "AA",
    "AA",
    "AB",
    "AA",
    "AA",
    "AA",
    "AA",
    "BY",
    "YB",
    "YB",
)


def replay_n28_witness() -> tuple[tuple[str, ...], tuple[str, ...]]:
    colors = tuple(column[layer] for layer in range(2) for column in N28_WORD)
    selected = sum(1 << vertex for vertex, color in enumerate(colors) if color != "Y")
    expected_boundary = sum(1 << vertex for vertex, color in enumerate(colors) if color == "B")
    boundary = internal_boundary(28, selected)
    if selected.bit_count() != 28 or boundary != expected_boundary or boundary.bit_count() != 11:
        raise AssertionError("invalid n=28 threshold witness")
    selected_names = tuple(
        vertex_name(28, vertex) for vertex in range(56) if selected >> vertex & 1
    )
    boundary_names = tuple(
        vertex_name(28, vertex) for vertex in range(56) if boundary >> vertex & 1
    )
    return selected_names, boundary_names
