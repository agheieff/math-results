from __future__ import annotations

from collections import Counter
from collections.abc import Sequence


def graphs_are_isomorphic(left: Sequence[int], right: Sequence[int]) -> bool:
    """Exact color-refinement/individualization graph-isomorphism test."""
    if len(left) != len(right):
        return False
    left_colors = tuple(mask.bit_count() for mask in left)
    right_colors = tuple(mask.bit_count() for mask in right)
    return _individualize(left, right, left_colors, right_colors)


def _individualize(
    left: Sequence[int],
    right: Sequence[int],
    left_colors: tuple[int, ...],
    right_colors: tuple[int, ...],
) -> bool:
    refined = _refine(left, right, left_colors, right_colors)
    if refined is None:
        return False
    left_colors, right_colors = refined
    classes = {
        color: tuple(vertex for vertex, value in enumerate(left_colors) if value == color)
        for color in set(left_colors)
    }
    if all(len(vertices) == 1 for vertices in classes.values()):
        right_by_color = {color: vertex for vertex, color in enumerate(right_colors)}
        permutation = tuple(right_by_color[color] for color in left_colors)
        return all(
            bool(left[u] >> v & 1) == bool(right[permutation[u]] >> permutation[v] & 1)
            for u in range(len(left))
            for v in range(len(left))
        )

    color, vertices = min(
        ((color, vertices) for color, vertices in classes.items() if len(vertices) > 1),
        key=lambda item: len(item[1]),
    )
    left_vertex = vertices[0]
    marker = max((*left_colors, *right_colors)) + 1
    for right_vertex, right_color in enumerate(right_colors):
        if right_color != color:
            continue
        next_left = list(left_colors)
        next_right = list(right_colors)
        next_left[left_vertex] = marker
        next_right[right_vertex] = marker
        if _individualize(left, right, tuple(next_left), tuple(next_right)):
            return True
    return False


def _refine(
    left: Sequence[int],
    right: Sequence[int],
    left_colors: tuple[int, ...],
    right_colors: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    while True:
        left_signatures = _signatures(left, left_colors)
        right_signatures = _signatures(right, right_colors)
        keys = sorted(set((*left_signatures, *right_signatures)))
        color_of = {signature: color for color, signature in enumerate(keys)}
        next_left = tuple(color_of[signature] for signature in left_signatures)
        next_right = tuple(color_of[signature] for signature in right_signatures)
        if Counter(next_left) != Counter(next_right):
            return None
        if next_left == left_colors and next_right == right_colors:
            return next_left, next_right
        left_colors, right_colors = next_left, next_right


def _signatures(
    adjacency: Sequence[int],
    colors: tuple[int, ...],
) -> tuple[tuple[int, tuple[tuple[int, int], ...]], ...]:
    return tuple(
        (
            colors[vertex],
            tuple(
                sorted(
                    Counter(
                        colors[neighbor]
                        for neighbor in range(len(colors))
                        if adjacency[vertex] >> neighbor & 1
                    ).items()
                )
            ),
        )
        for vertex in range(len(adjacency))
    )
