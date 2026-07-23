from itertools import combinations

import pytest

from tau_k_maximal.checker import (
    DirectPackingOracle,
    SparsityOracle,
    encode_edges,
    exhaustive_check,
    tight_construction,
)


@pytest.mark.parametrize(("q", "order"), [(2, 4), (2, 5), (3, 6)])
def test_exhaustive_maximal_sizes(q: int, order: int) -> None:
    result = exhaustive_check(q, order)

    assert result.maximal_graphs > 0
    assert result.maximal_edge_counts == (result.predicted_edge_count,)


def test_isolated_vertex_does_not_hide_packing_subgraph() -> None:
    order = 5
    k4_edges = tuple(combinations(range(4), 2))
    graph_mask = encode_edges(order, k4_edges)

    assert DirectPackingOracle(2, order).contains_q_packing(graph_mask)
    assert not SparsityOracle(2, order).is_sparse(graph_mask)


@pytest.mark.parametrize(("q", "order"), [(2, 4), (2, 8), (3, 6), (3, 9)])
def test_tight_construction(q: int, order: int) -> None:
    graph_mask = encode_edges(order, tight_construction(q, order))

    assert graph_mask.bit_count() == q * order - (q + 1)
    assert SparsityOracle(q, order).is_sparse(graph_mask)
    assert not DirectPackingOracle(q, order).contains_q_packing(graph_mask)


def test_exhaustive_limit_is_explicit() -> None:
    with pytest.raises(ValueError, match="limit"):
        exhaustive_check(2, 7)


def test_theorem_range_is_enforced() -> None:
    with pytest.raises(ValueError, match="order >= 2q"):
        exhaustive_check(3, 5)
