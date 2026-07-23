from math import comb

import pytest

from zero_forcing_mycielski import (
    MycielskiCycle,
    exhaust_four_sets,
    explicit_forcing_sequence,
    forcing_witness,
    replay_forces,
)


@pytest.mark.parametrize("order", [4, 5, 6, 7, 9, 15])
def test_explicit_five_vertex_witness(order: int) -> None:
    graph = MycielskiCycle.build(order)
    final = replay_forces(
        graph,
        forcing_witness(graph),
        explicit_forcing_sequence(graph),
    )
    assert final.bit_count() == graph.vertex_count
    assert len(explicit_forcing_sequence(graph)) == graph.vertex_count - 5


@pytest.mark.parametrize(
    ("order", "expected_maximum"),
    [(4, 5), (5, 6), (6, 6), (7, 6), (9, 6)],
)
def test_exact_four_set_exhaustion(order: int, expected_maximum: int) -> None:
    graph = MycielskiCycle.build(order)
    result = exhaust_four_sets(graph)
    assert result.checked == comb(graph.vertex_count, 4)
    assert result.maximum_closure == expected_maximum
