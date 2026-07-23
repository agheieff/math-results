from itertools import combinations

import pytest

from zero_forcing_petersen_separator.graph import GeneralizedPetersen, internal_boundary
from zero_forcing_petersen_separator.separator import (
    Color,
    coloring_from_subset,
    is_balanced_separator_coloring,
    pump_down,
    separator_size,
    subset_from_coloring,
)


@pytest.mark.parametrize("n", [7, 8, 9])
def test_small_minimum_matches_labeled_brute_force(n: int) -> None:
    graph = GeneralizedPetersen(n)
    minimum = graph.n
    for chosen in combinations(range(graph.order), graph.n):
        subset = sum(1 << vertex for vertex in chosen)
        minimum = min(minimum, internal_boundary(graph, subset).bit_count())
    assert minimum == 5


def test_n16_counterexample_round_trip() -> None:
    graph = GeneralizedPetersen(16)
    outer = (2, 3, 4, 5, 6, 7, 8)
    inner = (0, 1, 3, 4, 5, 6, 7, 9, 10)
    subset = sum(1 << vertex for vertex in outer)
    subset |= sum(1 << (graph.n + vertex) for vertex in inner)
    assert subset.bit_count() == graph.n
    assert internal_boundary(graph, subset).bit_count() == 7
    coloring = coloring_from_subset(graph, subset)
    assert is_balanced_separator_coloring(coloring)
    assert separator_size(coloring) == 7
    assert subset_from_coloring(coloring) == subset


def test_paired_clean_run_deletion_preserves_constraints_and_balance() -> None:
    graph = GeneralizedPetersen(32)
    subset = graph.paired_interval(0, 16)
    coloring = coloring_from_subset(graph, subset)
    assert separator_size(coloring) == 8
    reduced = pump_down(coloring)
    assert len(reduced) == 30
    assert is_balanced_separator_coloring(reduced)
    assert separator_size(reduced) == 8
    assert sum(column.count(Color.A) for column in reduced) == 22
    assert sum(column.count(Color.Y) for column in reduced) == 30
